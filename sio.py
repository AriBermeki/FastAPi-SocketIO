import typing
import json
import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import socketio
import typing as t
from . import JsPyBackground


class SIOMenager:
    def __init__(self) -> None:
        self.active_connections: t.List[str] = []
        self.sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*', json=json)
        self.sio_app = socketio.ASGIApp(socketio_server=self.sio, socketio_path='/hybrid/socket.io')
        self._connected = 0
        self._connection_limit = 0
        self._protocol_table: typing.Dict[str, typing.Callable] = {}
        self._socket_serial = 0
        self.SERIAL_MAX = 0xFFFFFFFF
        self._socket_pool: typing.Dict[int, socketio.AsyncServer] = {}
        self._socket_events: typing.Set[typing.Callable] = set()
        self._socket_id = None  # Instanzattribut für die Socket-ID
        self.init_connection()

    def set_connection_limit(self, limit: int = 0) -> None:
        self._connection_limit = max(0, limit)

    def number_of_connections(self) -> int:
        return self._connected

    def get_socket_ids(self) -> typing.List[int]:
        return list(self._socket_pool.keys())
    
    def close_socket(self, socket_id: int) -> bool:
        sio = self._socket_pool.get(socket_id)
        if sio:
            JsPyBackground.register_function(sio.close, [])
            return True
        return False

    def add_protocol(self, protocol: str, func: typing.Callable) -> None:
        self._protocol_table[protocol] = func

    def add_socket_event(self, func: typing.Callable) -> None:
        self._socket_events.add(func)

    def clear_socket_event(self) -> None:
        self._socket_events.clear()

    def reservecast(self, data, socket: typing.Union[
                    None, int, typing.List[int],
                    typing.Tuple[int], typing.Set[int]]=None) -> None:
        JsPyBackground.register_function(self.multicast, (data, socket))

    def broadcast(self, data) -> typing.Awaitable:
        text_data = json.dumps(data)
        cor_list = []
        for socket_id in self._socket_pool:
            cor_list.append(self._socket_pool[socket_id].emit(text_data))
        return asyncio.gather(*cor_list, return_exceptions=True)

    def multicast(self, data, socket: typing.Union[
                  None, int, typing.List[int],
                  typing.Tuple[int], typing.Set[int]]=None) -> typing.Awaitable:
        cor_list = []
        text_data = json.dumps(data)
        if socket is None:
            return self.broadcast(data)
        elif isinstance(socket, int):
            if socket in self._socket_pool:
                cor_list.append(self._socket_pool[socket].emit(text_data))
        elif isinstance(socket, (tuple, list, set)):
            for i in socket:
                if i in self._socket_pool:
                    cor_list.append(self._socket_pool[i].emit(text_data))
        return asyncio.gather(*cor_list, return_exceptions=True)

    def _append_socket(self, sio: socketio.AsyncServer) -> int:
        self._socket_serial += 1
        if self._socket_serial > self.SERIAL_MAX:
            self._socket_serial = 1
        while self._socket_serial in self._socket_pool:
            self._socket_serial += 1
            if self._socket_serial > self.SERIAL_MAX:
                self._socket_serial = 1
        self._socket_pool[self._socket_serial] = sio
        return self._socket_serial

    def _delete_socket(self, socket_id: int) -> None:
        if socket_id in self._socket_pool:
            del self._socket_pool[socket_id]

    async def on_connect(self, sio: socketio.AsyncServer):
        self._connected += 1
        self._socket_id = self._append_socket(sio)
        if self._connection_limit > 0 and\
           self._connected > self._connection_limit:
            send_dict = {'protocol': 'system', 'key': 'connect', 'id': 0,
                         'data': None, 'exception':
                         'Connection refused due to connection limit @python'}
            await sio.emit(send_dict)
        else:
            send_dict = {'protocol': 'system', 'key': 'connect', 'id': 0,
                         'data': self._socket_id, 'exception': None}
            await sio.emit(send_dict)
        for callback in self._socket_events:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await asyncio.create_task(callback(self._socket_id, 'connect'))
                else:
                    callback(self._socket_id, 'connect')
            except:
                pass

    async def on_receive(self, sio: socketio.AsyncServer, data: str):
        try:
            dict_data = json.loads(data)
            if('protocol' in dict_data and 'key' in dict_data and
               'id' in dict_data and 'data' in dict_data and
               'exception' in dict_data):
                call_func = self._protocol_table[dict_data['protocol']]
                if(asyncio.iscoroutinefunction(call_func)):
                    await asyncio.create_task(call_func(sio, self._socket_id, dict_data))
                else:
                    call_func(sio, self._socket_id, dict_data)
        except:
            pass

    async def on_disconnect(self, sio: socketio.AsyncServer, close_code: int):
        self._delete_socket(self._socket_id)
        self._connected -= 1
        for callback in self._socket_events:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await asyncio.create_task(callback(self._socket_id, 'disconnect'))
                else:
                    callback(self._socket_id, 'disconnect')
            except:
                pass

    def init_connection(self):
        @self.sio.on("connect")
        async def handle_connect(sid, environ):
            print(f"Client connected: {sid}")
            self.add_connection(sid)
            await self.sio.emit('message', {'protocol': 'system_ready', 'exception': None, 'timeout': 0.2}, room=sid)

        @self.sio.on("disconnect")
        def handle_disconnect(sid):
            self.remove_connection(sid)

        @self.sio.on("error")
        def handle_error(sid, error):
            print(f"Socket.IO error from {sid}: {error}")

        @self.sio.on("message")
        async def message(sid, data):
            await self.sio.emit('sendMessage', data, room=sid)

    def add_connection(self, sid: str):
        if sid not in self.active_connections:
            self.active_connections.append(sid)

    def remove_connection(self, sid: str):
        if sid in self.active_connections:
            self.active_connections.remove(sid)

    async def broadcast_message(self, event: str, data: dict):
        for connection in self.active_connections:
            await self.sio.emit(event, data, room=connection)

    def send_message_sync(self, sid: str, event: str, data: dict):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.sio.emit(event, data, room=sid))

    def listen_for_event(self, event: str, handler: t.Callable):
        @self.sio.on(event)
        async def event_handler(sid, data):
            await handler(sid, data)

    async def send_data_periodically(self):
        while True:
            await self.broadcast_message("periodic_data", {"key": "value"})
            await asyncio.sleep(5)

    def initial_sio_app(self, app: FastAPI):
        app.mount('/hybrid/', self.sio_app)
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

nexiom_sio = SIOMenager()

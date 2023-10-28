from fastapi import FastAPI, WebSocket
from socketio import AsyncServer, ASGIApp
from starlette.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
import pathlib
app = FastAPI()
templates = Jinja2Templates(pathlib.Path(__file__).parent / 'templates')
# Hier erstellen wir eine Socket.IO-Instanz und verknüpfen sie mit unserer FastAPI-App.
sio = AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio_app = ASGIApp(socketio_server=sio, socketio_path="socket.io")

app.mount(path='/ws', app=sio_app)
# Erlauben Sie Cross-Origin-Requests, wenn dies erforderlich ist. Passen Sie dies an Ihre Anforderungen an.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hier erstellen wir eine einfache Socket.IO-Manager-Klasse, um die Verbindungen zu verwalten.
class ConnectionManager:
    def __init__(self):
        self.active_connections = set()

    async def connect(self, sid: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, sid: str, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

# Socket.IO-Event-Handler, um Verbindungen zu verwalten
@sio.on("connect")
async def connect(sid, environ):
    return 'ok'

@sio.on("disconnect")
def disconnect(sid):
    pass

# Beispiel: Socket.IO-Event-Handler, um Nachrichten zu senden und empfangen
@sio.on("message")
async def message(sid, data):
    print(data)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)

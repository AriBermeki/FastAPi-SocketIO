import React from 'react';
import { useMachine } from '@xstate/react';
import { createMachine } from 'xstate'; // Änderung hier

const createStateMachine = (config) => {
  return createMachine(config); // Änderung hier
};

const createComponentWithStateMachine = (stateMachine) => {
  return function ComponentWithStateMachine({ initialState, children }) {
    const [state, send] = useMachine(stateMachine, { initialState });

    return children({ state, send });
  };
};

const jsonConfig = {
  'id': 'dynamicStateExample',
  'initial': 'loading',
  'states': {
    'idle': {
      'on': {
        'START': 'loading',
      },
    },
    'loading': {
      'on': {
        'SUCCESS': 'success',
        'ERROR': 'error',
      },
    },
    'success': {},
    'error': {},
  },
};

const stateMachine = createStateMachine(jsonConfig);
const DynamicStateComponent = createComponentWithStateMachine(stateMachine);

const App = () => {
  return (
    <DynamicStateComponent initialState="idle">
      {({ state, send }) => (
        <div>
          <p>Current State: {state.value}</p>
          {state.matches('loading') && <p>Loading...</p>}
          {state.matches('success') && <p>Success!</p>}
          {state.matches('error') && <p>Error!</p>}
          <button onClick={() => send({ 'type': 'SUCCESS' })}>Start</button>        
          </div>
      )}
    </DynamicStateComponent>
  );
};

export default App;

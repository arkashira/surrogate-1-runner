import React from 'react';
import { Provider } from 'react-redux';
import store from './store/store';
import PasscodeInput from './components/PasscodeInput';

const App = () => {
  return (
    <Provider store={store}>
      <div className="App">
        <PasscodeInput />
      </div>
    </Provider>
  );
};

export default App;
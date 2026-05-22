import React from 'react';
import { Provider } from 'react-redux';
import { store } from './store';
import SandboxHeader from './components/SandboxHeader';
import SandboxFooter from './components/SandboxFooter';

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <div className="app">
        <SandboxHeader />
        <div className="sandbox-content">
          {/* Sandbox content goes here */}
        </div>
        <SandboxFooter />
      </div>
    </Provider>
  );
};

export default App;
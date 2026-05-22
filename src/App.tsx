import React from 'react';
import { Provider } from 'react-redux';
import store from './store';
import Dashboard from './components/Dashboard';
import EmailNotification from './components/EmailNotification';

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <div className="app">
        <Dashboard />
        <EmailNotification />
      </div>
    </Provider>
  );
};

export default App;
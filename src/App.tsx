import React from 'react';
import { Provider } from 'react-redux';
import store from './store';
import NotificationSystem from './components/NotificationSystem';

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <div className="App">
        <NotificationSystem />
      </div>
    </Provider>
  );
};

export default App;
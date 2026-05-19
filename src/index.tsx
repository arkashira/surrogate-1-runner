import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { store } from './store';
import './store/persist'; // registers the subscription
import RuleConfig from './components/RuleConfig';
import 'antd/dist/reset.css';

const App = () => (
  <Provider store={store}>
    <div style={{ padding: 24 }}>
      <RuleConfig />
    </div>
  </Provider>
);

ReactDOM.createRoot(document.getElementById('root')!).render(<App />);
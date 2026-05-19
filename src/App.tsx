import React from 'react';
import { Provider } from 'react-redux';
import store from './store';
import InvoiceSummaryDashboard from './components/InvoiceSummaryDashboard';

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <div className="App">
        <InvoiceSummaryDashboard />
      </div>
    </Provider>
  );
};

export default App;
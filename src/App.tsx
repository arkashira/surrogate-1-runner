import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import RootCauseView from './components/RootCauseView';

const App: React.FC = () => {
  return (
    <Router>
      <Switch>
        <Route path="/alerts/:alertId/root-cause" component={RootCauseView} />
        {/* Other routes */}
      </Switch>
    </Router>
  );
};

export default App;
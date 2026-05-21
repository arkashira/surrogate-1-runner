import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Dashboard from './components/Dashboard/Dashboard';
import DetailedFindingView from './components/Dashboard/DetailedFindingView';

const App: React.FC = () => {
  return (
    <Router>
      <Switch>
        <Route path="/dashboard" exact component={Dashboard} />
        <Route path="/dashboard/findings/:id" component={DetailedFindingView} />
      </Switch>
    </Router>
  );
};

export default App;
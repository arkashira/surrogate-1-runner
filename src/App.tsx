import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import { SurrogateProvider } from './contexts/SurrogateContext';

const App: React.FC = () => {
  return (
    <SurrogateProvider>
      <Router>
        <Switch>
          <Route path="/" component={Dashboard} />
        </Switch>
      </Router>
    </SurrogateProvider>
  );
};

export default App;
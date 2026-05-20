import React from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import MarketingFramework from './MarketingFramework';
import Dashboard from './Dashboard';

const App: React.FC = () => {
  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/marketing-framework">Marketing Framework</Link></li>
            <li><Link to="/dashboard">Dashboard</Link></li>
          </ul>
        </nav>
        <Switch>
          <Route path="/marketing-framework">
            <MarketingFramework />
          </Route>
          <Route path="/dashboard">
            <Dashboard />
          </Route>
          <Route path="/">
            <h1>Welcome to the Micro-SaaS Dashboard</h1>
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
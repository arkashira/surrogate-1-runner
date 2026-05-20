import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import PipelineDetail from './pages/PipelineDetail';

const App = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route path="/" exact component={Dashboard} />
        <Route path="/pipelines/:id" component={PipelineDetail} />
      </Switch>
    </BrowserRouter>
  );
};

export default App;
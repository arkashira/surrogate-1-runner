     import React from 'react';
     import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
     import Navigation from './components/Navigation';
     import TroubleshootingGuide from './components/TroubleshootingGuide';

     const App: React.FC = () => {
       return (
         <Router>
           <Navigation />
           <Routes>
             <Route path="/troubleshooting" element={<TroubleshootingGuide />} />
           </Routes>
         </Router>
       );
     };

     export default App;
     import React from 'react';
     import { Link } from 'react-router-dom';

     const TroubleshootingGuide: React.FC = () => {
       return (
         <div className="troubleshooting-guide">
           <h1>CFD Simulation Troubleshooting Guide</h1>
           <h2>Common Errors and Solutions</h2>
           <ul>
             <li>
               <h3>Error: Convergence Failure</h3>
               <p>
                 Symptoms: Simulation iterations not reaching convergence criteria.<br/>
                 Steps: Check mesh quality, reduce relaxation coefficients, verify boundary conditions, increase max iterations.
               </p>
               <Link to="/resources/convergence-failure">Read more</Link>
             </li>
             <li>
               <h3>Error: Mesh Quality Issues</h3>
               <p>
                 Symptoms: High skewness or aspect ratio warnings.<br/>
                 Steps: Run mesh quality check, identify problematic elements, apply local mesh refinement.
               </p>
               <Link to="/resources/mesh-quality-issues">Read more</Link>
             </li>
             <li>
               <h3>Error: Boundary Condition Errors</h3>
               <p>
                 Symptoms: Pressure/velocity oscillations at boundaries.<br/>
                 Steps: Verify boundary type assignments, check for conflicts, apply gradient conditions.
               </p>
               <Link to="/resources/boundary-condition-errors">Read more</Link>
             </li>
             <li>
               <h3>Error: Numerical Instability</h3>
               <p>
                 Symptoms: Solution divergence or NaN values.<br/>
                 Steps: Reduce time step size, enable second-order discretization, check for negative volume cells.
               </p>
               <Link to="/resources/numerical-instability">Read more</Link>
             </li>
           </ul>
         </div>
       );
     };

     export default TroubleshootingGuide;
import React from 'react';
import { Card, CardContent, Typography, List, ListItem, ListItemText } from '@mui/material';

const TroubleshootingGuide = () => {
  const commonIssues = [
    {
      title: 'Mesh Quality Issues',
      steps: [
        'Check the mesh quality metrics (e.g., skewness, aspect ratio).',
        'Refine the mesh in areas with poor quality.',
        'Ensure the mesh is well-aligned with the geometry.'
      ]
    },
    {
      title: 'Boundary Conditions',
      steps: [
        'Verify the boundary conditions are correctly applied.',
        'Ensure the boundary conditions are consistent with the physical problem.',
        'Check for any inconsistencies in the boundary conditions.'
      ]
    },
    {
      title: 'Numerical Instability',
      steps: [
        'Reduce the time step size.',
        'Use a more stable numerical scheme.',
        'Check for any numerical errors in the solver.'
      ]
    },
    {
      title: 'Convergence Issues',
      steps: [
        'Check the residual history to identify where convergence is stalling.',
        'Adjust the solver settings (e.g., relaxation factors, under-relaxation).',
        'Ensure the initial conditions are reasonable.'
      ]
    }
  ];

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="h2">
          CFD Simulation Troubleshooting Guide
        </Typography>
        <Typography variant="body2" color="textSecondary" component="p">
          Follow these steps to diagnose and resolve common CFD simulation divergence issues.
        </Typography>
        {commonIssues.map((issue, index) => (
          <div key={index}>
            <Typography variant="h6" component="h3">
              {issue.title}
            </Typography>
            <List>
              {issue.steps.map((step, stepIndex) => (
                <ListItem key={stepIndex}>
                  <ListItemText primary={step} />
                </ListItem>
              ))}
            </List>
          </div>
        ))}
      </CardContent>
    </Card>
  );
};

export default TroubleshootingGuide;
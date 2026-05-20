const commonCFDErrors = [
  {
    errorName: 'Meshing Error',
    description: 'Issues related to the mesh generation process.',
    stepsToResolve: [
      'Check the quality of the mesh elements.',
      'Adjust mesh parameters such as element size and growth rate.',
      'Consider using a different meshing algorithm.'
    ]
  },
  {
    errorName: 'Convergence Failure',
    description: 'The solver fails to converge within the specified number of iterations.',
    stepsToResolve: [
      'Increase the number of iterations allowed.',
      'Adjust relaxation factors or under-relaxation coefficients.',
      'Check boundary conditions and initial guesses.'
    ]
  },
  {
    errorName: 'Numerical Instability',
    description: 'The simulation results oscillate or blow up.',
    stepsToResolve: [
      'Reduce the time step size.',
      'Change the numerical scheme to a more stable one.',
      'Check for any discontinuities in the input data.'
    ]
  },
  {
    errorName: 'Boundary Condition Error',
    description: 'Incorrect or inconsistent boundary conditions lead to erroneous results.',
    stepsToResolve: [
      'Review and validate all boundary conditions.',
      'Ensure consistency between different boundary conditions.',
      'Consult the documentation or seek expert advice.'
    ]
  },
  {
    errorName: 'Solver Configuration Error',
    description: 'Errors due to incorrect solver settings.',
    stepsToResolve: [
      'Verify solver settings against recommended guidelines.',
      'Check for any deprecated or unsupported options.',
      'Update the solver configuration based on the latest best practices.'
    ]
  },
  {
    errorName: 'Data Input Error',
    description: 'Problems arising from incorrect or incomplete input data.',
    stepsToResolve: [
      'Validate all input data for correctness and completeness.',
      'Use data validation tools or scripts.',
      'Correct any identified issues in the input data.'
    ]
  },
  {
    errorName: 'Resource Limitation',
    description: 'Insufficient computational resources to run the simulation.',
    stepsToResolve: [
      'Optimize the simulation setup to reduce resource requirements.',
      'Allocate more computational resources if possible.',
      'Consider running the simulation on a more powerful system.'
    ]
  },
  {
    errorName: 'Software Bug',
    description: 'Errors caused by bugs in the simulation software.',
    stepsToResolve: [
      'Check for any known issues or bug reports.',
      'Update to the latest version of the software.',
      'Report the issue to the software developers if it is a new bug.'
    ]
  }
];

module.exports = { commonCFDErrors };
/**
 * Troubleshooting Guide Module for CFD Simulation Platform
 * Provides accurate, step-by-step resolution guides for common simulation errors.
 */

const troubleshootingData = {
  'SOLVER_DIVERGENCE': {
    title: 'Solver Divergence Detected',
    description: 'The simulation solution is not converging. This often indicates instability in the flow field or mesh issues.',
    steps: [
      'Check mesh quality: Ensure aspect ratios are within acceptable limits (e.g., < 100).',
      'Verify boundary conditions: Ensure inlet/outlet conditions are physically consistent.',
      'Reduce time step size (if transient) or relaxation factors (if steady).',
      'Check for negative pressure or velocity values in the initial conditions.'
    ],
    resources: [
      'https://docs.axentx.com/cfd/troubleshooting/solver-divergence',
      'https://docs.axentx.com/cfd/troubleshooting/mesh-quality'
    ]
  },
  'MESH_QUALITY_ERROR': {
    title: 'Mesh Quality Critical Failure',
    description: 'The mesh generation process failed or produced invalid elements.',
    steps: [
      'Review the mesh generation log for specific element types (e.g., inverted elements).',
      'Adjust the mesh sizing function to prevent overly skewed elements.',
      'Ensure the domain boundaries are properly defined and non-intersecting.',
      'Regenerate the mesh using a coarser initial seed if the geometry is complex.'
    ],
    resources: [
      'https://docs.axentx.com/cfd/troubleshooting/mesh-generation'
    ]
  },
  'BOUNDARY_CONDITION_MISMATCH': {
    title: 'Boundary Condition Mismatch',
    description: 'Inlet and outlet conditions are incompatible with the flow regime.',
    steps: [
      'Verify the flow direction: Ensure inlet velocity is not opposing the outlet pressure gradient.',
      'Check symmetry conditions: Ensure symmetric boundaries are applied to symmetric geometries.',
      'Review mass balance: The sum of inlet mass flow should match outlet mass flow (within tolerance).',
      'Ensure wall conditions (no-slip, slip) are applied to all solid surfaces.'
    ],
    resources: [
      'https://docs.axentx.com/cfd/troubleshooting/boundary-conditions'
    ]
  },
  'UNKNOWN_ERROR': {
    title: 'Unknown Simulation Error',
    description: 'An unexpected error occurred during the simulation setup or execution.',
    steps: [
      'Check the platform logs for stack traces or specific error codes.',
      'Ensure the solver version is compatible with the mesh and boundary conditions.',
      'Try running a simple test case to isolate whether the issue is geometry-specific.',
      'Contact support with the error code and simulation parameters.'
    ],
    resources: [
      'https://docs.axentx.com/cfd/troubleshooting/general-errors'
    ]
  }
};

/**
 * Retrieves the troubleshooting guide for a specific error code.
 * @param {string} errorCode - The error code or identifier.
 * @returns {object} The guide object containing title, description, steps, and resources.
 */
function getTroubleshootingGuide(errorCode) {
  // Normalize input to uppercase for lookup
  const key = errorCode ? errorCode.toUpperCase() : 'UNKNOWN_ERROR';
  
  // Return the guide or the default unknown error guide
  return troubleshootingData[key] || troubleshootingData['UNKNOWN_ERROR'];
}

/**
 * Checks if the troubleshooting guide contains specific keywords (for accuracy testing).
 * @param {string} errorCode - The error code to check.
 * @param {string[]} keywords - Array of keywords to search for.
 * @returns {boolean} True if all keywords are found in the guide.
 */
function validateGuideAccuracy(errorCode, keywords) {
  const guide = getTroubleshootingGuide(errorCode);
  const content = JSON.stringify(guide).toLowerCase();
  
  return keywords.every(keyword => content.includes(keyword.toLowerCase()));
}

module.exports = {
  getTroubleshootingGuide,
  validateGuideAccuracy
};
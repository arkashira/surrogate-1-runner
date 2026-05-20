import React from 'react';

/**
 * Structured troubleshooting guide for common CFD simulation errors.
 * Each entry contains a title, step-by-step instructions, and optional
 * external resource links for deeper reading.
 */
const guideData = [
  {
    title: 'Mesh Quality Issues',
    steps: [
      'Open the mesh diagnostics panel.',
      'Check for non-manifold edges and inverted normals.',
      'Refine regions with high skewness using the mesh refinement tool.',
      'Re-run the mesh quality check until all metrics are within acceptable ranges.',
    ],
    resources: [
      {
        text: 'Mesh Quality Best Practices',
        url: 'https://www.axentx.com/docs/mesh-quality',
      },
    ],
  },
  {
    title: 'Convergence Failure',
    steps: [
      'Verify that all boundary conditions are correctly defined.',
      'Inspect residual plots for any stagnating variables.',
      'Reduce the Courant number or increase the under-relaxation factors.',
      'If divergence persists, consider using a more robust solver preset.',
    ],
    resources: [
      {
        text: 'Improving Solver Convergence',
        url: 'https://www.axentx.com/docs/solver-convergence',
      },
    ],
  },
  {
    title: 'Numerical Instability (NaNs/Inf)',
    steps: [
      'Check for division-by-zero operations in custom source terms.',
      'Ensure all material properties are positive and finite.',
      'Apply appropriate limiting functions to source terms.',
      'Re-run the simulation with a smaller time step.',
    ],
    resources: [
      {
        text: 'Handling Numerical Instabilities',
        url: 'https://www.axentx.com/docs/numerical-instability',
      },
    ],
  },
];

/**
 * TroubleshootingGuide component renders the guideData in a readable,
 * collapsible format.
 */
export default function TroubleshootingGuide() {
  return (
    <div className="troubleshooting-guide" style={{ padding: '1rem' }}>
      <h2>CFD Simulation Troubleshooting Guide</h2>
      {guideData.map((item, idx) => (
        <section key={idx} style={{ marginBottom: '1.5rem' }}>
          <h3>{item.title}</h3>
          <ol>
            {item.steps.map((step, sIdx) => (
              <li key={sIdx}>{step}</li>
            ))}
          </ol>
          {item.resources && item.resources.length > 0 && (
            <div>
              <strong>Additional Resources:</strong>
              <ul>
                {item.resources.map((res, rIdx) => (
                  <li key={rIdx}>
                    <a href={res.url} target="_blank" rel="noopener noreferrer">
                      {res.text}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      ))}
    </div>
  );
}
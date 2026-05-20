
// Add a new step in the onboarding flow to present the positioning guide
const steps = [
  // existing steps...
  {
    title: 'Understand Your Product',
    content: `
      <p>Welcome to ${productName}! To get started, let's dive into understanding your product.</p>
      <p>Here's a comprehensive guide that will help you position your product effectively:</p>
      <a href="/positioning-guide">Positioning Guide</a>
    `,
  },
  // existing steps...
];

module.exports = {
  steps,
};
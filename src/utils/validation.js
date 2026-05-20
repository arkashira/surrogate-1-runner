
function isValidContributionAmount(amount) {
  const minContribution = 10;
  const maxContribution = 10000;

  if (amount < minContribution || amount > maxContribution) {
    throw new Error('Invalid contribution amount. Please enter a value between $10 and $10,000.');
  }
}

export { isValidContribution };
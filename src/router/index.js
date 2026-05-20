
const ABTester = require('./abTester');
const { getProviders, getRequestType } = require('./providerSelector');
const config = require('../config.json');

const abTester = new ABTester();
let provider = null;

async function setRequestType(request) {
  const providers = await getProviders(request);
  const requestType = getRequestType(request);

  // Select the cheapest provider for the request type
  providers.sort((a, b) => a.costs[requestType] - b.costs[requestType]);
  provider = providers[0];

  if (config.costBasedRouting) {
    // Run A/B test to compare cost-based and random strategies
    const results = await abTester.runABTest(request, 'costBased', 'random', 100);
    console.log(results);
  }
}

async function dispatchRequest(request) {
  if (provider && config.costBasedRouting) {
    // Dispatch the request to the selected provider
    console.log(`Dispatching request to ${provider.id}`);
  } else {
    // Dispatch the request to the default provider
    console.log('Dispatching request to default provider');
  }
}

module.exports = { setRequestType, dispatchRequest };
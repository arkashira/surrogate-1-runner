
const { getCloudCosts, saveToBigQuery } = require('./aggregation');
const { setupTestDB } = require('../test-utils');

jest.mock('aws-sdk');
jest.mock('azure-sdk');
jest.mock('@google-cloud/bigquery');

describe('aggregation', () => {
  beforeAll(async () => {
    await setupTestDB();
  });

  it('should aggregate cloud costs', async () => {
    // Implement test logic here
  });
});
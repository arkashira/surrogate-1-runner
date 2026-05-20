import { generateForecast } from './aws-cost-explorer.js';

// Generate forecast for next month
const forecast = await generateForecast({
  start: '2024-02-01',
  end: '2024-03-01',
  preferences: {
    excludeServices: ['AWSLambda'],
    includeServices: ['AmazonEC2', 'AmazonS3']
  }
});

console.log(JSON.stringify(forecast, null, 2));
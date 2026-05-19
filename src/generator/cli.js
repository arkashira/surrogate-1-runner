const { Command } = require('commander');
const fs = require('fs');
const path = require('path');

const program = new Command();

program
  .name('surrogate-1')
  .description('CLI to generate synthetic metrics')
  .version('1.0.0');

program
  .command('generate-metrics')
  .description('Generate a predefined set of synthetic metrics')
  .option('--profile <profile>', 'Profile to use for generating metrics', 'basic')
  .action((options) => {
    const metrics = generateMetrics(options.profile);
    const output = JSON.stringify(metrics, null, 2);
    console.log(output);
    fs.writeFileSync(path.join(__dirname, 'metrics.json'), output);
  });

function generateMetrics(profile) {
  if (profile === 'basic') {
    return [
      { name: 'metric1', value: 100 },
      { name: 'metric2', value: 200 },
      { name: 'metric3', value: 300 },
      { name: 'metric4', value: 400 },
      { name: 'metric5', value: 500 },
      { name: 'metric6', value: 600 },
      { name: 'metric7', value: 700 },
      { name: 'metric8', value: 800 },
      { name: 'metric9', value: 900 },
      { name: 'metric10', value: 1000 }
    ];
  }
  throw new Error(`Unknown profile: ${profile}`);
}

program.parse(process.argv);
const { generateMetricsCLI } = require('./generator/index');
const yargs = require('yargs');

yargs.command({
  command: 'generate-metrics',
  describe: 'Generate synthetic metrics',
  builder: (yargs) => {
    yargs.option('profile', {
      describe: 'Profile to use',
      type: 'string',
      demandOption: true,
    });
  },
  handler: (argv) => {
    generateMetricsCLI(argv.profile);
  },
});

yargs.parse();
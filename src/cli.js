# src/cli.js
const { Command } = require('commander');
const { run } = require('./runner');

const program = new Command();

program
  .option('-c, --ci', 'Run in CI mode')
  .action((options) => {
    if (options.ci) {
      run({ ...options, ci: true });
    } else {
      run(options);
    }
  });

program.parse(process.argv);
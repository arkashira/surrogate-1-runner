const { Command } = require('commander');
const start = require('./start');
const stop = require('./stop');

const program = new Command();

program
  .command('start')
  .description('Start the sandbox')
  .action(() => {
    start;
  });

program
  .command('stop')
  .description('Stop the sandbox')
  .action(() => {
    stop;
  });

program.parse(process.argv);
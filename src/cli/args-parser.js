// ---------------------------------------------------------------
// Argument parsing – Commander (v10+)
// ---------------------------------------------------------------

const { Command } = require('commander');

const program = new Command();

program
  .name('dep‑validator')
  .description('Validate that a Node.js project contains the required artefacts and that installed package versions match the manifest.')
  .argument('<directory>', 'Path to the project directory to validate')
  .option('-v, --verbose', 'Print detailed information for every check')
  .option('--strict', 'Treat version mismatches as hard failures (default: only missing artefacts fail)')
  .option('--json', 'Emit a machine‑readable JSON report on stdout (in addition to the human‑readable one)')
  .version('1.0.0')
  .parse(process.argv);

const args = program.opts();
args.directory = program.processedArgs[0]; // positional argument

module.exports = {
  /** Absolute (or relative) path supplied by the user */
  getDirectory: () => args.directory,
  /** true → print every path / version / reason */
  isVerbose: () => !!args.verbose,
  /** true → version mismatches cause a non‑zero exit code */
  isStrict: () => !!args.strict,
  /** true → also output a JSON report */
  isJson: () => !!args.json,
  /** raw parsed object – handy for debugging */
  getRaw: () => ({ ...args, directory: args.directory })
};
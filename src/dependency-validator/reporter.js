
const table = require('cli-table3');
const chalk = require('chalk');

function printReport(dependencies, verbose) {
  const headers = ['Package', 'Installed', 'Wanted', 'Mismatch'];
  const tableInstance = new table({
    head: headers,
    colWidths: [30, 15, 15, 15],
  });

  dependencies.forEach(({ packageName, installed, wanted }) => {
    const mismatch = installed !== wanted;
    tableInstance.push([
      packageName,
      chalk.green(installed),
      chalk.yellow(wanted),
      mismatch ? chalk.red('yes') : chalk.green('no'),
    ]);
  });

  if (verbose) {
    tableInstance.printTable();
  } else {
    console.log(tableInstance.toString());
  }
}

module.exports = { printReport };

// src/dependency-validator/formatters.js

const semver = require('semver');

function formatVersion(version) {
  return semver.coerce(version).version;
}

module.exports = { formatVersion };

// src/dependency-validator/index.js

const fs = require('fs');
const path = require('path');
const execSync = require('child_process').execSync;
const reporter = require('./reporter');
const formatters = require('./formatters');

function runDependencyValidation(directory, verbose) {
  const packageJsonPath = path.join(directory, 'package.json');
  const packageJsonContent = fs.readFileSync(packageJsonPath, 'utf8');
  const packageJson = JSON.parse(packageJsonContent);
  const dependencies = Object.keys(packageJson.dependencies || {});

  dependencies.forEach((dependency) => {
    const installedVersion = packageJson.dependencies[dependency];
    const wantedVersion = execSync(`npm info ${dependency} version`, { encoding: 'utf8 }).trim();
    const installed = formatters.formatVersion(installedVersion);
    const wanted = formatters.formatVersion(wantedVersion);
    // ... add logic to compare installed and wanted versions
  });

  reporter.printReport(dependencies, verbose);
}

module.exports = { runDependencyValidation };
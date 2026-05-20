#!/usr/bin/env node

const { program } = require('commander');
const fs = require('fs-extra');
const semver = require('semver');
const chalk = require('chalk');

program
  .argument('<dir>', 'Directory to validate')
  .option('-v, --verbose', 'Enable verbose output')
  .action(async (dir, options) => {
    try {
      const packageJson = await fs.readJson(`${dir}/package.json`);
      const dependencies = Object.keys(packageJson.dependencies || {});
      const devDependencies = Object.keys(packageJson.devDependencies || {});

      const allDependencies = [...dependencies, ...devDependencies];

      const invalidDependencies = allDependencies.filter((dep) => {
        const version = packageJson[dep] || '';
        return !semver.valid(version);
      });

      if (invalidDependencies.length > 0) {
        if (options.verbose) {
          console.log(chalk.yellow('Invalid dependencies found:'));
          invalidDependencies.forEach((dep) => {
            console.log(`- ${dep}: ${packageJson[dep]}`);
          });
        }
        process.exit(1);
      } else {
        console.log(chalk.green('All dependencies are valid'));
      }
    } catch (err) {
      console.error(chalk.red('Error validating dependencies'), err.message);
      process.exit(1);
    }
  });

program.parse(process.argv);
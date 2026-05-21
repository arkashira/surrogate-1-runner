import { expect, test } from '@oclif/test';
import { execSync } from 'child_process';
import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';

describe('install', () => {
  test
    .stdout()
    .command(['install'])
    .it('runs install command and lists suggested npm install commands', ctx => {
      expect(ctx.stdout).to.contain('Suggested npm install commands:');
    });

  test
    .stdout()
    .command(['install', '--apply'])
    .it('runs install command with --apply flag and applies the install commands', ctx => {
      expect(ctx.stdout).to.contain('Successfully executed: npm install some-package');
    });

  test
    .stdout()
    .command(['install', '--apply'])
    .it('runs install command with --apply flag and logs summary', ctx => {
      const summaryPath = join(__dirname, '..', '..', 'logs', 'install-summary.json');
      const summary = JSON.parse(readFileSync(summaryPath, 'utf8'));
      expect(summary.totalCommands).to.be.greaterThan(0);
      expect(summary.applied).to.be.true;
    });
});
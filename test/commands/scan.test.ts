import { expect, test } from '@oclif/test';
import { execSync } from 'child_process';

describe('scan', () => {
  test
    .stdout()
    .command(['scan'])
    .it('runs scan command', (ctx) => {
      expect(ctx.stdout).to.contain('No missing imports found.');
    });

  test
    .stdout()
    .command(['scan', '--apply'])
    .it('runs scan command with apply flag', (ctx) => {
      expect(ctx.stdout).to.contain('Summary of actions taken:');
    });

  test
    .stub(execSync, 'sync', () => {})
    .stdout()
    .command(['scan', '--apply'])
    .it('runs scan command with apply flag and mocks execSync', (ctx) => {
      expect(ctx.stdout).to.contain('Summary of actions taken:');
    });
});
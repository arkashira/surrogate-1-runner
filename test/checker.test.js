const { readFileSync } = require('fs');
const { execSync } = require('child_process');
const path = require('path');

describe('checker.js', () => {
  test('should report missing imports', () => {
    const packageJsonPath = path.join(__dirname, '../package.json');
    const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf-8'));

    // Temporarily remove a dependency to simulate a missing import
    const originalDependencies = { ...packageJson.dependencies };
    delete packageJson.dependencies['some-package'];
    fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));

    try {
      expect(() => {
        execSync('node src/checker.js', { stdio: 'inherit' });
      }).toThrow();

      // Restore the original package.json
      packageJson.dependencies = originalDependencies;
      fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
    } catch (error) {
      throw error;
    }
  });

  test('should exit with zero status when no missing imports', () => {
    const packageJsonPath = path.join(__dirname, '../package.json');
    const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf-8'));

    // Ensure all dependencies are present
    packageJson.dependencies['some-package'] = '1.0.0';
    fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));

    try {
      execSync('node src/checker.js', { stdio: 'inherit' });
    } catch (error) {
      throw error;
    } finally {
      // Restore the original package.json
      packageJson.dependencies = originalDependencies;
      fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
    }
  });
});
const fs = require('fs');
const path = require('path');

class PackageJsonValidator {
  constructor(packageJsonPath) {
    this.packageJsonPath = packageJsonPath;
  }

  validateImports(imports) {
    const packageJson = JSON.parse(fs.readFileSync(this.packageJsonPath, 'utf8'));
    const dependencies = packageJson.dependencies;
    const devDependencies = packageJson.devDependencies;

    imports.forEach((importItem) => {
      const importSource = importItem.importSource;
      if (!dependencies[importSource] && !devDependencies[importSource]) {
        console.log(`Missing package.json entry for ${importSource} in ${importItem.filePath} at line ${importItem.line}, column ${importItem.column}`);
      }
    });
  }
}

module.exports = PackageJsonValidator;
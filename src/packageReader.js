const fs = require('fs');
const path = require('path');

class PackageReader {
  constructor() {
    this.dependencies = new Set();
    this.devDependencies = new Set();
  }

  readPackageJson(filePath = path.join(__dirname, '../../package.json')) {
    try {
      const packageJson = JSON.parse(fs.readFileSync(filePath, 'utf8'));
      this.dependencies = new Set(Object.keys(packageJson.dependencies || {}));
      this.devDependencies = new Set(Object.keys(packageJson.devDependencies || {}));
    } catch (error) {
      console.error('Error reading package.json:', error);
      throw error;
    }
  }

  hasDependency(packageName) {
    return this.dependencies.has(packageName) || this.devDependencies.has(packageName);
  }

  getAllDependencies() {
    return new Set([...this.dependencies, ...this.devDependencies]);
  }
}

module.exports = PackageReader;
const fs = require('fs');
const path = require('path');

class PackageReader {
    constructor(packageJsonPath) {
        this.packageJsonPath = packageJsonPath;
        this.dependencies = {};
        this.devDependencies = {};
        this.loadPackageJson();
    }

    loadPackageJson() {
        const packageJson = JSON.parse(fs.readFileSync(this.packageJsonPath, 'utf-8'));
        this.dependencies = packageJson.dependencies || {};
        this.devDependencies = packageJson.devDependencies || {};
    }

    getAllDependencies() {
        return { ...this.dependencies, ...this.devDependencies };
    }

    isDependencyPresent(dependency) {
        return this.dependencies.hasOwnProperty(dependency) || this.devDependencies.hasOwnProperty(dependency);
    }
}

module.exports = PackageReader;
const fs = require('fs');
const path = require('path');
const PackageReader = require('./packageReader');

describe('PackageReader', () => {
  let packageReader;
  const mockPackageJsonPath = path.join(__dirname, 'mockPackage.json');

  beforeEach(() => {
    packageReader = new PackageReader();
    fs.writeFileSync(mockPackageJsonPath, JSON.stringify({
      dependencies: {
        'react': '^17.0.2',
        'lodash': '^4.17.21'
      },
      devDependencies: {
        'jest': '^27.0.6',
        'webpack': '^5.65.0'
      }
    }));
  });

  afterEach(() => {
    fs.unlinkSync(mockPackageJsonPath);
  });

  test('reads package.json correctly', () => {
    packageReader.readPackageJson(mockPackageJsonPath);
    expect(packageReader.hasDependency('react')).toBe(true);
    expect(packageReader.hasDependency('lodash')).toBe(true);
    expect(packageReader.hasDependency('jest')).toBe(true);
    expect(packageReader.hasDependency('webpack')).toBe(true);
    expect(packageReader.hasDependency('nonexistent')).toBe(false);
  });

  test('gets all dependencies', () => {
    packageReader.readPackageJson(mockPackageJsonPath);
    const allDependencies = packageReader.getAllDependencies();
    expect(allDependencies.has('react')).toBe(true);
    expect(allDependencies.has('lodash')).toBe(true);
    expect(allDependencies.has('jest')).toBe(true);
    expect(allDependencies.has('webpack')).toBe(true);
    expect(allDependencies.size).toBe(4);
  });
});
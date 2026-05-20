const Scanner = require('./scanner');
const PackageJsonValidator = require('./package-json-validator');

const scanner = new Scanner();
const packageJsonValidator = new PackageJsonValidator('/opt/axentx/surrogate-1/package.json');

scanner.scanDirectory('/opt/axentx/surrogate-1/src');
const imports = scanner.getImports();
packageJsonValidator.validateImports(imports);
const fs = require('fs');
const path = require('path');
const PackageReader = require('./package-reader');

class DependencyValidator {
    constructor(packageJsonPath, sourceDir) {
        this.packageReader = new PackageReader(packageJsonPath);
        this.sourceDir = sourceDir;
        this.imports = [];
    }

    scanImports() {
        const files = this.getJavaScriptFiles(this.sourceDir);
        files.forEach(file => {
            const content = fs.readFileSync(file, 'utf-8');
            this.extractImports(content);
        });
    }

    getJavaScriptFiles(dir) {
        return fs.readdirSync(dir).flatMap(file => {
            const fullPath = path.join(dir, file);
            if (fs.statSync(fullPath).isDirectory()) {
                return this.getJavaScriptFiles(fullPath);
            } else if (file.endsWith('.js') || file.endsWith('.ts')) {
                return [fullPath];
            }
            return [];
        });
    }

    extractImports(content) {
        const importRegex = /(?:import\s+(?:\w+|\*\s+as\s+\w+|{[^}]*})\s+from\s+|require\(['"])([^'"]+)(?=['"])/g;
        let match;
        while ((match = importRegex.exec(content)) !== null) {
            this.imports.push(match[1]);
        }
    }

    validateImports() {
        const dependencies = this.packageReader.getAllDependencies();
        const mismatches = this.imports.filter(imported => !dependencies[imported]);
        return mismatches;
    }

    generateReport() {
        const mismatches = this.validateImports();
        if (mismatches.length > 0) {
            console.log('Mismatched Imports:', mismatches);
        } else {
            console.log('All imports are valid.');
        }
    }
}

const packageJsonPath = path.join(__dirname, 'package.json');
const sourceDir = path.join(__dirname, '..'); // Adjust as necessary
const validator = new DependencyValidator(packageJsonPath, sourceDir);
validator.scanImports();
validator.generateReport();
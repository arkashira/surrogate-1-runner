const fs = require('fs');
const path = require('path');
const { parse } = require('@babel/parser');
const traverse = require('@babel/traverse').default;
const { getImportedModules } = require('./ast-utils');

class DependencyParser {
  constructor() {
    this.dependencies = new Set();
  }

  parseFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    const ast = parse(content, {
      sourceType: 'module',
      plugins: ['jsx', 'typescript']
    });

    traverse(ast, {
      ImportDeclaration: (nodePath) => {
        const moduleName = nodePath.node.source.value;
        this.dependencies.add(moduleName);
      },
      CallExpression: (nodePath) => {
        if (nodePath.node.callee.type === 'Import') {
          const moduleName = nodePath.node.arguments[0].value;
          this.dependencies.add(moduleName);
        }
      }
    });
  }

  getDependencies() {
    return Array.from(this.dependencies);
  }
}

module.exports = DependencyParser;
const fs = require('fs');
const path = require('path');
const { parse } = require('@babel/parser');
const { traverse } = require('@babel/traverse');

class AstParser {
  constructor() {
    this.imports = [];
  }

  parseFile(filePath) {
    const fileContent = fs.readFileSync(filePath, 'utf8');
    const ast = parse(fileContent, {
      sourceType: 'module',
      plugins: ['typescript', 'jsx'],
    });

    traverse(ast, {
      ImportDeclaration(path) {
        const importSpecifiers = path.node.specifiers;
        const importSource = path.node.source.value;
        this.imports.push({
          filePath,
          importSource,
          importSpecifiers,
          line: path.node.loc.start.line,
          column: path.node.loc.start.column,
        });
      },
    });
  }

  getImports() {
    return this.imports;
  }
}

module.exports = AstParser;
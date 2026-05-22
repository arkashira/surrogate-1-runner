function getImportedModules(ast) {
  const importedModules = new Set();

  traverse(ast, {
    ImportDeclaration: (nodePath) => {
      const moduleName = nodePath.node.source.value;
      importedModules.add(moduleName);
    },
    CallExpression: (nodePath) => {
      if (nodePath.node.callee.type === 'Import') {
        const moduleName = nodePath.node.arguments[0].value;
        importedModules.add(moduleName);
      }
    }
  });

  return Array.from(importedModules);
}

module.exports = {
  getImportedModules
};
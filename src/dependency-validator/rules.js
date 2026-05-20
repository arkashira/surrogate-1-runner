const rules = {
  'dependency-version': (dependencies, options) => {
    const minVersion = options.minVersion;
    const maxVersion = options.maxVersion;
    const invalidDependencies = dependencies.filter((dependency) => {
      const version = dependency.version;
      return version < minVersion || version > maxVersion;
    });
    if (invalidDependencies.length > 0) {
      throw new Error(`Invalid dependency versions: ${invalidDependencies.map((dependency) => dependency.name).join(', ')}`);
    }
  },
  'dependency-existence': (dependencies, options) => {
    const requiredDependencies = options.dependencies;
    const missingDependencies = requiredDependencies.filter((dependency) => {
      return !dependencies.find((existingDependency) => existingDependency.name === dependency);
    });
    if (missingDependencies.length > 0) {
      throw new Error(`Missing dependencies: ${missingDependencies.join(', ')}`);
    }
  },
};

module.exports = rules;
const validationConfig = {
  rules: [
    {
      name: 'dependency-version',
      description: 'Validate dependency versions',
      enabled: true,
      options: {
        minVersion: '1.0.0',
        maxVersion: '2.0.0',
      },
    },
    {
      name: 'dependency-existence',
      description: 'Validate dependency existence',
      enabled: true,
      options: {
        dependencies: ['dependency1', 'dependency2'],
      },
    },
  ],
};

module.exports = validationConfig;
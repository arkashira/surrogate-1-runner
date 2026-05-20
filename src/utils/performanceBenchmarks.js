const performanceData = {
    'component1': [
        { metric: 'Latency', value: '20ms', unit: 'ms' },
        { metric: 'Throughput', value: '1000 req/s', unit: 'req/s' },
    ],
    'component2': [
        { metric: 'Latency', value: '15ms', unit: 'ms' },
        { metric: 'Throughput', value: '1500 req/s', unit: 'req/s' },
    ],
    // Add more components as needed
};

export const getPerformanceBenchmarks = (componentId) => {
    return performanceData[componentId] || [];
};
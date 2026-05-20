import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BenchmarkPanel = ({ metricDefinition }) => {
  const [benchmarks, setBenchmarks] = useState(null);
  const [selectedIndustry, setSelectedIndustry] = useState('');
  const [selectedStage, setSelectedStage] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/path/to/static/benchmarks.json');
        setBenchmarks(response.data);
      } catch (error) {
        console.error('Error fetching benchmarks:', error);
      }
    };

    fetchData();
  }, []);

  const handleApplyMedianAsTarget = () => {
    // Logic to apply median value as target for the metric
    console.log('Applying median as target');
  };

  const filteredBenchmarks = benchmarks?.filter(
    (benchmark) =>
      benchmark.industry === selectedIndustry && benchmark.stage === selectedStage
  );

  return (
    <div>
      <h2>Benchmarks</h2>
      <select value={selectedIndustry} onChange={(e) => setSelectedIndustry(e.target.value)}>
        <option value="">Select Industry</option>
        {new Set(benchmarks?.map((b) => b.industry)).map((industry) => (
          <option key={industry} value={industry}>
            {industry}
          </option>
        ))}
      </select>
      <select value={selectedStage} onChange={(e) => setSelectedStage(e.target.value)}>
        <option value="">Select Stage</option>
        {new Set(benchmarks?.map((b) => b.stage)).map((stage) => (
          <option key={stage} value={stage}>
            {stage}
          </option>
        ))}
      </select>
      <ul>
        {filteredBenchmarks?.map((benchmark) => (
          <li key={benchmark.id}>
            <p>Median: {benchmark.median}</p>
            <p>25th Percentile: {benchmark.percentile25}</p>
            <p>75th Percentile: {benchmark.percentile75}</p>
            <button onClick={handleApplyMedianAsTarget}>Apply Median as Target</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default BenchmarkPanel;
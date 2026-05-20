import React from 'react';
import { getPerformanceBenchmarks } from '../utils/performanceBenchmarks';

const ComponentDetails = ({ component }) => {
    const benchmarks = getPerformanceBenchmarks(component.id);

    return (
        <div>
            <h1>{component.name} Details</h1>
            <h2>Performance Benchmarks</h2>
            <ul>
                {benchmarks.map((benchmark, index) => (
                    <li key={index}>
                        {benchmark.metric}: {benchmark.value} {benchmark.unit}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ComponentDetails;
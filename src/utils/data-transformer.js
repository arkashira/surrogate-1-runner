import { DataFrame } from 'pandas-js';

export function transformData(data) {
    // Convert data to a pandas DataFrame
    const df = new DataFrame(data);

    // Normalize the data
    df.normalize();

    // Deduplicate the data
    df.dropDuplicates();

    return df;
}

// Example usage
const data = [
    { cost: 100, category: 'A' },
    { cost: 200, category: 'B' },
    { cost: 300, category: 'C' },
    { cost: 400, category: 'D' },
    { cost: 500, category: 'E' }
];

const transformedData = transformData(data);
console.log(transformedData);
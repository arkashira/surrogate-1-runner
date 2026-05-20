const { filterComponents } = require('./filtering');
const components = require('../data/components.json');

describe('filterComponents', () => {
    it('should filter components by CPU', () => {
        const filtered = filterComponents(components, { cpu: 'Intel i7' });
        expect(filtered.length).toBe(1);
        expect(filtered[0].name).toBe('Component A');
    });

    it('should filter components by GPU', () => {
        const filtered = filterComponents(components, { gpu: 'NVIDIA GTX 1080' });
        expect(filtered.length).toBe(1);
        expect(filtered[0].name).toBe('Component A');
    });

    it('should filter components by RAM', () => {
        const filtered = filterComponents(components, { ram: '16GB' });
        expect(filtered.length).toBe(2);
        expect(filtered.map(c => c.name)).toEqual(expect.arrayContaining(['Component A', 'Component C']));
    });

    it('should filter components by multiple specs', () => {
        const filtered = filterComponents(components, { cpu: 'Intel i7', gpu: 'NVIDIA GTX 1080', ram: '16GB' });
        expect(filtered.length).toBe(1);
        expect(filtered[0].name).toBe('Component A');
    });
});
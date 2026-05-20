
import React, { useState, useEffect } from 'react';
import { useDebounce } from 'use-debounce';
import { useFilteredComponents } from '../hooks/useFilteredComponents';
import { PerformanceTracker } from '../utils/performance';

const Filter = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredSpecs, setFilteredSpecs] = useState([]);
  const [filteredPrices, setFilteredPrices] = useState([]);

  const [debouncedSearchTerm] = useDebounce(searchTerm, 500);

  useEffect(() => {
    const fetchFilteredData = async () => {
      const { filteredSpecs, filteredPrices } = await useFilteredComponents(debouncedSearchTerm);
      setFilteredSpecs(filteredSpecs);
      setFilteredPrices(filteredPrices);
    };

    if (debouncedSearchTerm) {
      PerformanceTracker.start('filter-data');
      fetchFilteredData();
      PerformanceTracker.end('filter-data');
    }
  }, [debouncedSearchTerm]);

  return (
    <div>
      {/* search input */}
      {/* filtered specs list */}
      {/* filtered prices list */}
    </div>
  );
};

export default Filter;

// src/utils/performance.js

export class PerformanceTracker {
  constructor() {
    this.trackers = new Map();
  }

  start(name) {
    if (!this.trackers.has(name)) {
      this.trackers.set(name, process.hrtime());
    }
  }

  end(name) {
    const start = this.trackers.get(name);
    if (start) {
      const [seconds, nanoseconds] = process.hrtime(start);
      this.trackers.set(name, null);
      console.log(`${name} took ${seconds} seconds and ${nanoseconds} nanoseconds.`);
    }
  }
}
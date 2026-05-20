import React, { useState } from 'react';
import { useEffect } from 'react';
import axios from 'axios';

const CPUComparison = () => {
  const [cpus, setCpus] = useState([]);
  const [filteredCpus, setFilteredCpus] = useState([]);
  const [brandFilter, setBrandFilter] = useState('');
  const [priceFilter, setPriceFilter] = useState('');
  const [performanceFilter, setPerformanceFilter] = useState('');

  useEffect(() => {
    axios.get('/api/cpus')
      .then(response => {
        setCpus(response.data);
        setFilteredCpus(response.data);
      })
      .catch(error => console.error('Error fetching CPUs:', error));
  }, []);

  const handleBrandChange = (event) => {
    setBrandFilter(event.target.value);
    filterCPUs();
  };

  const handlePriceChange = (event) => {
    setPriceFilter(event.target.value);
    filterCPUs();
  };

  const handlePerformanceChange = (event) => {
    setPerformanceFilter(event.target.value);
    filterCPUs();
  };

  const filterCPUs = () => {
    let filtered = cpus;
    if (brandFilter) {
      filtered = filtered.filter(cpu => cpu.brand.toLowerCase().includes(brandFilter.toLowerCase()));
    }
    if (priceFilter) {
      filtered = filtered.filter(cpu => cpu.price <= parseFloat(priceFilter));
    }
    if (performanceFilter) {
      filtered = filtered.filter(cpu => cpu.performance >= parseFloat(performanceFilter));
    }
    setFilteredCpus(filtered);
  };

  return (
    <div>
      <h1>CPU Comparison</h1>
      <div>
        <label>Brand:</label>
        <input type="text" value={brandFilter} onChange={handleBrandChange} />
      </div>
      <div>
        <label>Max Price:</label>
        <input type="number" value={priceFilter} onChange={handlePriceChange} />
      </div>
      <div>
        <label>Min Performance:</label>
        <input type="number" value={performanceFilter} onChange={handlePerformanceChange} />
      </div>
      <table>
        <thead>
          <tr>
            <th>Brand</th>
            <th>Model</th>
            <th>Price</th>
            <th>Performance</th>
          </tr>
        </thead>
        <tbody>
          {filteredCpus.map((cpu, index) => (
            <tr key={index}>
              <td>{cpu.brand}</td>
              <td>{cpu.model}</td>
              <td>{cpu.price}</td>
              <td>{cpu.performance}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CPUComparison;
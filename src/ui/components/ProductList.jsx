import React, { useEffect, useState } from 'react';
import FilterBar from './FilterBar';
import './ProductList.module.css';

const ProductList = ({ products }) => {
  const [filteredProducts, setFilteredProducts] = useState(products);
  const [sortOption, setSortOption] = useState('priceAsc');

  const categories = [...new Set(products.map((product) => product.category))];
  const brands = [...new Set(products.map((product) => product.brand))];
  const priceRanges = ['0-50', '50-100', '100-200', '200+'];
  const specs = ['VRAM', 'CPU Speed', 'RAM'];

  const applyFilters = (filters) => {
    let filtered = products;

    if (filters.category) {
      filtered = filtered.filter((product) => product.category === filters.category);
    }

    if (filters.priceRange) {
      const [min, max] = filters.priceRange.split('-');
      filtered = filtered.filter(
        (product) => product.price >= parseInt(min) && product.price <= parseInt(max)
      );
    }

    if (filters.brand) {
      filtered = filtered.filter((product) => product.brand === filters.brand);
    }

    if (filters.spec) {
      filtered = filtered.filter((product) => product.specs.includes(filters.spec));
    }

    setFilteredProducts(filtered);
  };

  useEffect(() => {
    // Sort the filtered products based on the selected sort option
    const sortedProducts = [...filteredProducts].sort((a, b) => {
      if (sortOption === 'priceAsc') {
        return a.price - b.price;
      } else if (sortOption === 'priceDesc') {
        return b.price - a.price;
      } else if (sortOption === 'benchmarkScore') {
        return b.benchmarkScore - a.benchmarkScore;
      }
      return 0;
    });

    setFilteredProducts(sortedProducts);
  }, [sortOption, filteredProducts]);

  return (
    <div className="product-list">
      <FilterBar
        categories={categories}
        brands={brands}
        priceRanges={priceRanges}
        specs={specs}
        onFilterChange={applyFilters}
      />
      <select value={sortOption} onChange={(e) => setSortOption(e.target.value)}>
        <option value="priceAsc">Price: Low to High</option>
        <option value="priceDesc">Price: High to Low</option>
        <option value="benchmarkScore">Benchmark Score: High to Low</option>
      </select>
      {filteredProducts.map((product) => (
        <div key={product.id} className="product-item">
          <h3>{product.name}</h3>
          <p>Category: {product.category}</p>
          <p>Brand: {product.brand}</p>
          <p>Price: ${product.price}</p>
          <p>Specs: {product.specs.join(', ')}</p>
        </div>
      ))}
    </div>
  );
};

export default ProductList;
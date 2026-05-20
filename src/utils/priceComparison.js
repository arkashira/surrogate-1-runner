const mockRetailerData = [
  {
    name: "Amazon",
    price: 129.99,
    availability: "In Stock",
    url: "https://amazon.com/product/123"
  },
  {
    name: "Best Buy",
    price: 134.99,
    availability: "In Stock",
    url: "https://bestbuy.com/product/123"
  },
  {
    name: "Newegg",
    price: 124.99,
    availability: "In Stock",
    url: "https://newegg.com/product/123"
  },
  {
    name: "Walmart",
    price: 139.99,
    availability: "Limited Stock",
    url: "https://walmart.com/product/123"
  }
];

export const fetchPriceComparison = async (componentId) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  // In a real implementation, this would make an actual API call
  // const response = await fetch(`/api/price-comparison/${componentId}`);
  // const data = await response.json();
  
  // Mock data for demonstration
  return {
    componentName: "Intel Core i7-12700K",
    retailers: mockRetailerData
  };
};
const getBuildRecommendations = (userBudget, userNeeds) => {
  // Mock build recommendation algorithm
  const builds = [
    {
      id: 'build1',
      name: 'Budget Gaming Build',
      totalCost: 750,
      cpu: 'AMD Ryzen 5 5600',
      gpu: 'NVIDIA GTX 1660 Super',
      motherboard: 'B550M',
      ram: '16GB DDR4',
      psu: '550W',
      ssd: '500GB NVMe',
      relevance: 0.92,
      valueScore: 8.7
    },
    {
      id: 'build2',
      name: 'Productivity Workstation',
      totalCost: 1200,
      cpu: 'Intel i5-12400',
      gpu: 'Integrated Graphics',
      motherboard: 'B660',
      ram: '32GB DDR4',
      psu: '650W',
      ssd: '1TB NVMe',
      relevance: 0.88,
      valueScore: 9.1
    },
    {
      id: 'build3',
      name: 'High-End Gaming',
      totalCost: 1800,
      cpu: 'AMD Ryzen 7 5800X',
      gpu: 'NVIDIA RTX 3080',
      motherboard: 'X570',
      ram: '32GB DDR4',
      psu: '850W',
      ssd: '1TB NVMe',
      relevance: 0.95,
      valueScore: 8.3
    }
  ];

  // Filter builds within budget and sort by relevance
  return builds
    .filter(build => build.totalCost <= userBudget)
    .sort((a, b) => b.relevance - a.relevance)
    .slice(0, 3); // Top 3 recommendations
};

export default getBuildRecommendations;
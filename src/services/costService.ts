import { CostData } from '../models/CostData';

export const getCostData = async (startDate: string, endDate: string, serviceType: string): Promise<CostData[]> => {
  // Mock data for demonstration
  const mockData: CostData[] = [
    { date: '2023-01-01', cost: 100, serviceType: 'compute' },
    { date: '2023-01-02', cost: 150, serviceType: 'storage' },
    { date: '2023-01-03', cost: 200, serviceType: 'networking' },
    // Add more mock data as needed
  ];

  // Filter data based on the provided parameters
  return mockData.filter(item => {
    const itemDate = new Date(item.date);
    const start = new Date(startDate);
    const end = new Date(endDate);
    return (
      itemDate >= start &&
      itemDate <= end &&
      (serviceType === '' || item.serviceType === serviceType)
    );
  });
};
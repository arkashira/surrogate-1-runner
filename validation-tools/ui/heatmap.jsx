import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Heatmap } from 'react-d3-heatmap';

const HeatmapVisualization = ({ problemStatement }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch data from Statista/Google Trends APIs based on the problem statement
        const response = await axios.get(`https://api.example.com/demand-data?problem=${problemStatement}`);
        const fetchedData = response.data;

        // Filter out assumptions with <10k monthly search volume
        const filteredData = fetchedData.filter(item => item.searchVolume >= 10000);

        // Prepare data for heatmap visualization
        const heatmapData = filteredData.map(item => ({
          x: item.location,
          y: item.keyword,
          value: item.searchVolume
        }));

        setData(heatmapData);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching demand data:', error);
        setLoading(false);
      }
    };

    fetchData();
  }, [problemStatement]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Demand Heatmap for "{problemStatement}"</h2>
      <Heatmap
        data={data}
        width={600}
        height={400}
        cellRadius={10}
        colors={['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c']}
      />
    </div>
  );
};

export default HeatmapVisualization;
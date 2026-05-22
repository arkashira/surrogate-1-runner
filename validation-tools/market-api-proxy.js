const express = require('express');
const axios = require('axios');
const app = express();
const PORT = process.env.PORT || 3001;

// Middleware to parse JSON bodies
app.use(express.json());

// Mock API keys - In production, these should be loaded from environment variables
const STATISTA_API_KEY = process.env.STATISTA_API_KEY || 'mock-statista-key';
const GOOGLE_TRENDS_API_KEY = process.env.GOOGLE_TRENDS_API_KEY || 'mock-google-trends-key';

// Route to fetch market data from Statista
app.get('/api/statista/:query', async (req, res) => {
  try {
    const { query } = req.params;
    
    // In a real implementation, this would call the actual Statista API
    // For now, we return mock data
    const mockStatistaData = {
      query: query,
      data: {
        marketSize: Math.floor(Math.random() * 1000000),
        growthRate: (Math.random() * 20).toFixed(2),
        trends: ['increasing', 'stable', 'decreasing']
      }
    };
    
    res.json(mockStatistaData);
  } catch (error) {
    console.error('Error fetching Statista data:', error);
    res.status(500).json({ error: 'Failed to fetch Statista data' });
  }
});

// Route to fetch Google Trends data
app.get('/api/google-trends/:query', async (req, res) => {
  try {
    const { query } = req.params;
    
    // In a real implementation, this would call the actual Google Trends API
    // For now, we return mock data
    const mockTrendsData = {
      query: query,
      data: {
        searchVolume: Math.floor(Math.random() * 50000),
        interestOverTime: Array.from({length: 12}, () => Math.floor(Math.random() * 100)),
        relatedQueries: ['related term 1', 'related term 2', 'related term 3']
      }
    };
    
    res.json(mockTrendsData);
  } catch (error) {
    console.error('Error fetching Google Trends data:', error);
    res.status(500).json({ error: 'Failed to fetch Google Trends data' });
  }
});

// Route to generate demand heatmap
app.post('/api/heatmap', async (req, res) => {
  try {
    const { problemStatements } = req.body;
    
    if (!problemStatements || !Array.isArray(problemStatements)) {
      return res.status(400).json({ error: 'Invalid input: problemStatements must be an array' });
    }
    
    const heatmapData = problemStatements.map(statement => {
      // Simulate generating heatmap data based on statement
      return {
        statement: statement,
        searchVolume: Math.floor(Math.random() * 100000),
        riskLevel: Math.random() > 0.7 ? 'high' : Math.random() > 0.4 ? 'medium' : 'low'
      };
    });
    
    res.json({
      heatmapData: heatmapData,
      flaggedAssumptions: heatmapData.filter(item => item.searchVolume < 10000)
    });
  } catch (error) {
    console.error('Error generating heatmap:', error);
    res.status(500).json({ error: 'Failed to generate heatmap' });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`Market API Proxy server running on port ${PORT}`);
});

module.exports = app;
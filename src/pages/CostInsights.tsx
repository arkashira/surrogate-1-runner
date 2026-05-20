
import React, { useEffect, useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { LineChart, BarChart, Table, Button } from 'react-chartjs-2';
import axios from 'axios';

const CostInsights = () => {
  const { auth } = useAuth();
  const [spendData, setSpendData] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/cost-insights', {
          headers: { Authorization: `Bearer ${auth.token}` },
        });
        setSpendData(response.data.spendData);
        setAlerts(response.data.alerts);
      } catch (error) {
        console.error(error);
      }
    };

    if (auth.isAuthenticated) {
      fetchData();
    }
  }, [auth.isAuthenticated, auth.token]);

  const options = {
    // Line chart options
  };

  const barChartData = {
    // Bar chart data
  };

  const alertTableData = {
    // Table data for alerts
  };

  return (
    <div>
      <h1>Cost Insights</h1>
      <div>
        <LineChart data={spendData} options={options} />
      </div>
      <div>
        <Table data={alertTableData} />
      </div>
      <div>
        <Button onClick={() => window.location.href = '/api/cost-insights/export'}>Export</Button>
      </div>
    </div>
  );
};

export default CostInsights;

// src/hooks/useAuth.ts

import { useState, useEffect } from 'react';

const useAuth = () => {
  const [auth, setAuth] = useState({ isAuthenticated: false, token: null });

  useEffect(() => {
    const token = localStorage.getItem('token');
    setAuth({ isAuthenticated: !!token, token });
  }, []);

  return { auth };
};

export default useAuth;

// src/api/cost-insights.ts

import axios from 'axios';

export const getCostInsights = async () => {
  try {
    const response = await axios.get('/api/cost-insights');
    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
};

// src/api/cost-insights-export.ts

import axios from 'axios';

export const exportCostInsights = async () => {
  try {
    const response = await axios.get('/api/cost-insights/export', {
      responseType: 'blob',
    });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'cost-insights.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error(error);
  }
};

// src/api/cost-insights.ts

import express from 'express';
import cors from 'cors';
import { getCostInsights, exportCostInsights } from './cost-insights';

const app = express();
app.use(cors());

app.get('/api/cost-insights', async (req, res) => {
  const data = await getCostInsights();
  res.json(data);
});

app.get('/api/cost-insights/export', async (req, res) => {
  await exportCostInsights();
  res.sendStatus(204);
});

export default app;
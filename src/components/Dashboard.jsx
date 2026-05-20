import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, Table, Select, Spin } from 'antd';

const { Option } = Select;

const Dashboard = () => {
  const [costData, setCostData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/cloud-costs');
        setCostData(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };

    fetchData();

    const interval = setInterval(fetchData, 15 * 60 * 1000); // Refresh every 15 minutes

    return () => clearInterval(interval);
  }, []);

  const filteredData = costData.filter(item => {
    if (filter === 'all') return true;
    return item.team === filter || item.project === filter;
  });

  const columns = [
    {
      title: 'Provider',
      dataIndex: 'provider',
      key: 'provider',
    },
    {
      title: 'Resource Type',
      dataIndex: 'resourceType',
      key: 'resourceType',
    },
    {
      title: 'Cost',
      dataIndex: 'cost',
      key: 'cost',
    },
    {
      title: 'Team',
      dataIndex: 'team',
      key: 'team',
    },
    {
      title: 'Project',
      dataIndex: 'project',
      key: 'project',
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Card title="Cloud Cost Dashboard">
        <div style={{ marginBottom: '16px' }}>
          <Select
            defaultValue="all"
            style={{ width: 200 }}
            onChange={value => setFilter(value)}
          >
            <Option value="all">All</Option>
            <Option value="team1">Team 1</Option>
            <Option value="team2">Team 2</Option>
            <Option value="project1">Project 1</Option>
            <Option value="project2">Project 2</Option>
          </Select>
        </div>
        <Spin spinning={loading}>
          <Table
            columns={columns}
            dataSource={filteredData}
            rowKey="id"
            pagination={{ pageSize: 10 }}
          />
        </Spin>
      </Card>
    </div>
  );
};

export default Dashboard;
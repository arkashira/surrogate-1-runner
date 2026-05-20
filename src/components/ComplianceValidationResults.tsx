import React, { useState, useEffect } from 'react';
import { Table, Input, Button, Select, Space } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import { getComplianceValidationResults, filterAndSortResults } from '../services/complianceService';

const { Option } = Select;

const ComplianceValidationResults = () => {
  const [results, setResults] = useState([]);
  const [filteredResults, setFilteredResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchText, setSearchText] = useState('');
  const [sortField, setSortField] = useState('timestamp');
  const [sortOrder, setSortOrder] = useState('descend');

  useEffect(() => {
    const fetchResults = async () => {
      setLoading(true);
      const data = await getComplianceValidationResults();
      setResults(data);
      setFilteredResults(data);
      setLoading(false);
    };

    fetchResults();
  }, []);

  const handleSearch = (value) => {
    setSearchText(value);
    const filteredData = filterAndSortResults(results, value, sortField, sortOrder);
    setFilteredResults(filteredData);
  };

  const handleSort = (field, order) => {
    setSortField(field);
    setSortOrder(order);
    const filteredData = filterAndSortResults(results, searchText, field, order);
    setFilteredResults(filteredData);
  };

  const columns = [
    {
      title: 'Validation ID',
      dataIndex: 'validationId',
      key: 'validationId',
      sorter: true,
    },
    {
      title: 'Timestamp',
      dataIndex: 'timestamp',
      key: 'timestamp',
      sorter: true,
      sortOrder: sortField === 'timestamp' ? sortOrder : null,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      filters: [
        { text: 'Pass', value: 'Pass' },
        { text: 'Fail', value: 'Fail' },
      ],
      onFilter: (value, record) => record.status.indexOf(value) === 0,
    },
    {
      title: 'Violations',
      dataIndex: 'violations',
      key: 'violations',
      render: (violations) => violations.join(', '),
    },
  ];

  return (
    <div>
      <Space style={{ marginBottom: 16 }}>
        <Input
          placeholder="Search"
          prefix={<SearchOutlined />}
          onChange={(e) => handleSearch(e.target.value)}
          style={{ width: 200 }}
        />
        <Select
          defaultValue="timestamp"
          style={{ width: 120 }}
          onChange={(value) => handleSort(value, sortOrder)}
        >
          <Option value="validationId">Validation ID</Option>
          <Option value="timestamp">Timestamp</Option>
          <Option value="status">Status</Option>
        </Select>
        <Select
          defaultValue="descend"
          style={{ width: 120 }}
          onChange={(value) => handleSort(sortField, value)}
        >
          <Option value="ascend">Ascending</Option>
          <Option value="descend">Descending</Option>
        </Select>
      </Space>
      <Table
        columns={columns}
        dataSource={filteredResults}
        loading={loading}
        onChange={(pagination, filters, sorter) => {
          handleSort(sorter.field, sorter.order);
        }}
      />
    </div>
  );
};

export default ComplianceValidationResults;
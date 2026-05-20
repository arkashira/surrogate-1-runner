import React from 'react';
import { Table, Input, DatePicker, Space } from 'antd';
import moment from 'moment';
import LogViewer from './LogViewer';

const { RangePicker } = DatePicker;

const ShellSessionsTable = ({ sessions }) => {
  const [filteredSessions, setFilteredSessions] = React.useState(sessions);
  const [dateRange, setDateRange] = React.useState([]);
  const [searchUser, setSearchUser] = React.useState('');
  const [searchNode, setSearchNode] = React.useState('');

  const handleDateChange = (dates) => {
    setDateRange(dates);
    filterSessions();
  };

  const handleUserSearch = (value) => {
    setSearchUser(value);
    filterSessions();
  };

  const handleNodeSearch = (value) => {
    setSearchNode(value);
    filterSessions();
  };

  const filterSessions = () => {
    let filtered = sessions;
    if (dateRange.length > 0) {
      const startDate = dateRange[0].startOf('day');
      const endDate = dateRange[1].endOf('day');
      filtered = filtered.filter(
        (session) =>
          moment(session.start).isSameOrAfter(startDate) &&
          moment(session.start).isSameOrBefore(endDate)
      );
    }
    if (searchUser) {
      filtered = filtered.filter((session) => session.user.includes(searchUser));
    }
    if (searchNode) {
      filtered = filtered.filter((session) => session.node.includes(searchNode));
    }
    setFilteredSessions(filtered);
  };

  const columns = [
    {
      title: 'User',
      dataIndex: 'user',
      key: 'user',
      render: (text) => <Input value={text} onChange={(e) => handleUserSearch(e.target.value)} />,
    },
    {
      title: 'Node',
      dataIndex: 'node',
      key: 'node',
      render: (text) => <Input value={text} onChange={(e) => handleNodeSearch(e.target.value)} />,
    },
    {
      title: 'Start',
      dataIndex: 'start',
      key: 'start',
      render: (text) => moment(text).format('YYYY-MM-DD HH:mm:ss'),
    },
    {
      title: 'Duration',
      dataIndex: 'duration',
      key: 'duration',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
    },
  ];

  return (
    <>
      <Space direction="vertical">
        <RangePicker onChange={handleDateChange} />
        <LogViewer logs={filteredSessions} />
      </Space>
      <Table dataSource={filteredSessions} columns={columns} />
    </>
  );
};

export default ShellSessionsTable;
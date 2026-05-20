import React, { useEffect, useState } from 'react';
import { Table, Button, message } from 'antd';
import { getWorkflows, executeWorkflow } from '../services/workflowService';

const WorkflowExecutionList: React.FC = () => {
  const [workflows, setWorkflows] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchWorkflows = async () => {
      setLoading(true);
      try {
        const data = await getWorkflows();
        setWorkflows(data);
      } catch (error) {
        message.error('Failed to fetch workflows');
      } finally {
        setLoading(false);
      }
    };

    fetchWorkflows();
  }, []);

  const handleExecute = async (id: string) => {
    setLoading(true);
    try {
      await executeWorkflow(id);
      message.success('Workflow executed successfully');
    } catch (error) {
      message.error('Failed to execute workflow');
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Trigger',
      dataIndex: 'trigger',
      key: 'trigger',
    },
    {
      title: 'Source',
      dataIndex: 'source',
      key: 'source',
    },
    {
      title: 'Destination',
      dataIndex: 'destination',
      key: 'destination',
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (text: any, record: any) => (
        <Button type="primary" onClick={() => handleExecute(record.id)} loading={loading}>
          Execute
        </Button>
      ),
    },
  ];

  return (
    <Table
      dataSource={workflows}
      columns={columns}
      rowKey="id"
      loading={loading}
    />
  );
};

export default WorkflowExecutionList;
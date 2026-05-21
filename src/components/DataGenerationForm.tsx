import React, { useState } from 'react';
import { Form, Input, Button, Select, message } from 'antd';
import { generateSyntheticData } from '../services/dataService';

const { Option } = Select;

const DataGenerationForm: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const onFinish = async (values: any) => {
    setLoading(true);
    try {
      await generateSyntheticData(values);
      message.success('Data generation started successfully!');
    } catch (error) {
      message.error('Failed to start data generation.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Form form={form} onFinish={onFinish} layout="vertical">
      <Form.Item name="datasetType" label="Dataset Type" rules={[{ required: true }]}>
        <Select placeholder="Select dataset type">
          <Option value="users">Users</Option>
          <Option value="products">Products</Option>
          <Option value="transactions">Transactions</Option>
        </Select>
      </Form.Item>
      <Form.Item name="recordCount" label="Number of Records" rules={[{ required: true }]}>
        <Input type="number" placeholder="Enter number of records" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>
          Generate Data
        </Button>
      </Form.Item>
    </Form>
  );
};

export default DataGenerationForm;
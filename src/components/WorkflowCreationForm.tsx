import React, { useState } from 'react';
import { Button, Form, Input, Select, message } from 'antd';
import { createWorkflow } from '../services/workflowService';

const { Option } = Select;

const WorkflowCreationForm: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const onFinish = async (values: any) => {
    setLoading(true);
    try {
      await createWorkflow(values);
      message.success('Workflow created successfully');
      form.resetFields();
    } catch (error) {
      message.error('Failed to create workflow');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Form form={form} onFinish={onFinish} layout="vertical">
      <Form.Item
        name="name"
        label="Workflow Name"
        rules={[{ required: true, message: 'Please input the workflow name!' }]}
      >
        <Input />
      </Form.Item>
      <Form.Item
        name="trigger"
        label="Trigger"
        rules={[{ required: true, message: 'Please select a trigger!' }]}
      >
        <Select>
          <Option value="manual">Manual</Option>
          <Option value="schedule">Schedule</Option>
          <Option value="event">Event</Option>
        </Select>
      </Form.Item>
      <Form.Item
        name="source"
        label="Source"
        rules={[{ required: true, message: 'Please select a source!' }]}
      >
        <Select>
          <Option value="github">GitHub</Option>
          <Option value="surrogate">Surrogate-1</Option>
        </Select>
      </Form.Item>
      <Form.Item
        name="destination"
        label="Destination"
        rules={[{ required: true, message: 'Please select a destination!' }]}
      >
        <Select>
          <Option value="github">GitHub</Option>
          <Option value="surrogate">Surrogate-1</Option>
        </Select>
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>
          Create Workflow
        </Button>
      </Form.Item>
    </Form>
  );
};

export default WorkflowCreationForm;
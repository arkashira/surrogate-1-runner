import React, { useState } from 'react';
import { Form, Input, Select, notification } from 'antd';
import axios from 'axios';

const { Option } = Select;

const AlertSettingsForm = ({ user, onSubmit }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const onFinish = async (values) => {
    setLoading(true);
    try {
      await axios.post('/api/alert-settings', { ...values, userId: user.id });
      notification.success({ message: 'Alert settings saved!' });
      onSubmit();
    } catch (error) {
      notification.error({ message: 'Error saving alert settings.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Form form={form} onFinish={onFinish}>
      <Form.Item label="Threshold Type" name="thresholdType" rules={[{ required: true }]}>
        <Select>
          <Option value="percentage">Percentage</Option>
          <Option value="absolute">Absolute Value</Option>
        </Select>
      </Form.Item>
      <Form.Item label="Threshold Value" name="thresholdValue" rules={[{ required: true }]}>
        <Input type="number" step="0.01" />
      </Form.Item>
      <Form.Item label="Notification Channels" name="notificationChannels" rules={[{ required: true }]}>
        <Select mode="multiple">
          <Option value="email">Email</Option>
          <Option value="sms">SMS</Option>
          <Option value="webhook">Webhook</Option>
        </Select>
      </Form.Item>
      <Form.Item>
        <button type="primary" htmlType="submit" loading={loading}>
          Save Alert Settings
        </button>
      </Form.Item>
    </Form>
  );
};

export default AlertSettingsForm;
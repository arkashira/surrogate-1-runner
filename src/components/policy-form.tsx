import React from 'react';
import { Form, Input, Button } from 'antd';

interface PolicyFormProps {
  onSubmit: (policy: any) => void;
}

const PolicyForm: React.FC<PolicyFormProps> = ({ onSubmit }) => {
  const [policy, setPolicy] = React.useState({
    name: '',
    maxInstanceSize: '',
    idleTimeout: '',
  });

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    onSubmit(policy);
  };

  return (
    <Form
      onFinish={handleSubmit}
      initialValues={policy}
      layout="vertical"
    >
      <Form.Item label="Policy Name" name="name">
        <Input />
      </Form.Item>
      <Form.Item label="Max Instance Size" name="maxInstanceSize">
        <Input />
      </Form.Item>
      <Form.Item label="Idle Timeout" name="idleTimeout">
        <Input />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit">
          Create Policy
        </Button>
      </Form.Item>
    </Form>
  );
};

export default PolicyForm;
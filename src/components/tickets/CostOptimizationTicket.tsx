
import React, { useState } from 'react';
import { Button, Form, Input, Space } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

const CostOptimizationTicket = () => {
  const [tickets, setTickets] = useState([]);

  const handleAddTicket = () => {
    // Add new ticket to the state
  };

  return (
    <div>
      <h1>Cost Optimization Tickets</h1>
      <Form.List name="tickets">
        {tickets.map((ticket, index) => (
          <Form.Item
            key={index}
            name={[index, 'title']}
            label={`Ticket ${index + 1}`}
            rules={[{ required: true, message: 'Please input ticket title' }]}
          >
            <Input placeholder="Title" />
          </Form.Item>
        ))}
      </Form.List>
      <Form.Item>
        <Button type="dashed" onClick={handleAddTicket} block icon={<PlusOutlined />}>
          Add Ticket
        </Button>
      </Form.Item>
    </div>
  );
};

export default CostOptimizationTicket;
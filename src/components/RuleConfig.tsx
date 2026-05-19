import React from 'react';
import { Form, InputNumber, Select, Switch, Button } from 'antd';
import { useDispatch, useSelector } from 'react-redux';
import { updateRules } from '../store/rulesSlice';
import { RootState } from '../store';

const { Option } = Select;

const RuleConfig: React.FC = () => {
  const dispatch = useDispatch();
  const rules = useSelector((state: RootState) => state.rules);

  const onValuesChange = (_: any, allValues: any) => {
    dispatch(updateRules(allValues));
  };

  return (
    <Form
      layout="vertical"
      initialValues={rules}
      onValuesChange={onValuesChange}
      style={{ maxWidth: 400 }}
    >
      <Form.Item label="Indent Size" name="indentSize">
        <InputNumber min={1} max={8} />
      </Form.Item>

      <Form.Item label="Tab Size" name="tabSize">
        <InputNumber min={1} max={8} />
      </Form.Item>

      <Form.Item label="End of Line" name="endOfLine">
        <Select>
          <Option value="lf">LF</Option>
          <Option value="crlf">CRLF</Option>
          <Option value="cr">CR</Option>
        </Select>
      </Form.Item>

      <Form.Item label="Insert Spaces" name="insertSpaces" valuePropName="checked">
        <Switch />
      </Form.Item>

      <Form.Item>
        <Button type="primary" onClick={() => console.log('Rules saved', rules)}>
          Save Rules
        </Button>
      </Form.Item>
    </Form>
  );
};

export default RuleConfig;
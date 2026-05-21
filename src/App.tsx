import React from 'react';
import { Layout, Menu } from 'antd';
import DataGenerationForm from './components/DataGenerationForm';
import DataGenerationStatus from './components/DataGenerationStatus';

const { Header, Content } = Layout;

const App: React.FC = () => {
  return (
    <Layout>
      <Header>
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
          <Menu.Item key="1">Data Generation</Menu.Item>
        </Menu>
      </Header>
      <Content style={{ padding: '50px' }}>
        <DataGenerationForm />
        <DataGenerationStatus />
      </Content>
    </Layout>
  );
};

export default App;
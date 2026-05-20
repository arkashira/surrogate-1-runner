import React from 'react';
import { Table, Modal, Button } from 'antd';
import moment from 'moment';

const LogViewer = ({ logs }) => {
  const [selectedLog, setSelectedLog] = React.useState(null);
  const [isModalVisible, setIsModalVisible] = React.useState(false);

  const columns = [
    {
      title: 'User',
      dataIndex: 'user',
      key: 'user',
    },
    {
      title: 'Node',
      dataIndex: 'node',
      key: 'node',
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

  const handleRowClick = (record) => {
    setSelectedLog(record);
    setIsModalVisible(true);
  };

  const handleModalClose = () => {
    setIsModalVisible(false);
  };

  return (
    <>
      <Table
        dataSource={logs}
        columns={columns}
        onRow={(record) => ({
          onClick: () => handleRowClick(record),
        })}
      />
      <Modal
        title="Command Log"
        visible={isModalVisible}
        onCancel={handleModalClose}
        footer={[
          <Button key="back" onClick={handleModalClose}>
            Close
          </Button>,
        ]}
      >
        {selectedLog && (
          <div>
            {selectedLog.commands.map((command, index) => (
              <p key={index}>
                {moment(command.timestamp).format('YYYY-MM-DD HH:mm:ss')} - {command.command}
              </p>
            ))}
          </div>
        )}
      </Modal>
    </>
  );
};

export default LogViewer;
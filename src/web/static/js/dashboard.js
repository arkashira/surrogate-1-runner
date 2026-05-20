import React, { useEffect, useState } from 'react';
import { Table, Button } from 'react-bootstrap';
import { connect } from 'react-redux';
import { fetchPipelines, updatePipelineStatus } from './actions/pipelineActions';

const Dashboard = ({ pipelines, fetchPipelines, updatePipelineStatus }) => {
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    fetchPipelines();
    const newSocket = new WebSocket('wss://your-websocket-url');
    setSocket(newSocket);
    newSocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      updatePipelineStatus(data.pipelineId, data.status);
    };
    return () => newSocket.close();
  }, [fetchPipelines, updatePipelineStatus]);

  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          <th>Name</th>
          <th>Status</th>
          <th>Last Run</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {pipelines.map((pipeline) => (
          <tr key={pipeline.id}>
            <td>{pipeline.name}</td>
            <td>{pipeline.status}</td>
            <td>{new Date(pipeline.lastRun).toLocaleString()}</td>
            <td>
              <Button onClick={() => openDetailView(pipeline.id)}>View Logs</Button>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

const mapStateToProps = (state) => ({
  pipelines: state.pipelines,
});

export default connect(mapStateToProps, { fetchPipelines, updatePipelineStatus })(Dashboard);
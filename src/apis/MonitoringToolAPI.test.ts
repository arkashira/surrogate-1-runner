import axios from 'axios';
import { MonitoringToolAPI } from './MonitoringToolAPI';

jest.mock('axios');

describe('MonitoringToolAPI', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should connect to a monitoring tool', async () => {
    const response = { data: {} };
    axios.post.mockResolvedValue(response);
    const monitoringToolAPI = new MonitoringToolAPI();
    await monitoringToolAPI.connectMonitoringTool('test-id', {
      username: 'test-username',
      password: 'test-password',
    });
    expect(axios.post).toHaveBeenCalledWith(
      '/monitoring-tools/test-id/connect',
      { username: 'test-username', password: 'test-password' }
    );
    expect(response.data).toEqual(await monitoringToolAPI.connectMonitoringTool('test-id', { username: 'test-username', password: 'test-password' }));
  });

  it('should get monitoring tool connections', async () => {
    const response = { data: [] };
    axios.get.mockResolvedValue(response);
    const monitoringToolAPI = new MonitoringToolAPI();
    await monitoringToolAPI.getMonitoringToolConnections();
    expect(axios.get).toHaveBeenCalledWith('/monitoring-tools/connections');
    expect(response.data).toEqual(await monitoringToolAPI.getMonitoringToolConnections());
  });

  it('should get monitoring tool artifacts', async () => {
    const response = { data: [] };
    axios.get.mockResolvedValue(response);
    const monitoringToolAPI = new MonitoringToolAPI();
    await monitoringToolAPI.getMonitoringToolArtifacts('test-id');
    expect(axios.get).toHaveBeenCalledWith('/monitoring-tools/test-id/artifacts');
    expect(response.data).toEqual(await monitoringToolAPI.getMonitoringToolArtifacts('test-id'));
  });
});
import axios, { AxiosInstance } from 'axios';

interface MonitoringTool {
  id: string;
  name: string;
  url: string;
}

interface MonitoringToolConnection {
  id: string;
  monitoringTool: MonitoringTool;
  credentials: {
    username: string;
    password: string;
  };
}

class MonitoringToolAPI {
  private axios: AxiosInstance;

  constructor(axios: AxiosInstance = axios) {
    this.axios = axios;
  }

  async connectMonitoringTool(
    monitoringToolId: string,
    credentials: {
      username: string;
      password: string;
    }
  ): Promise<MonitoringToolConnection> {
    const response = await this.axios.post(
      `/monitoring-tools/${monitoringToolId}/connect`,
      credentials
    );
    return response.data;
  }

  async getMonitoringToolConnections(): Promise<MonitoringToolConnection[]> {
    const response = await this.axios.get('/monitoring-tools/connections');
    return response.data;
  }

  async getMonitoringToolArtifacts(
    monitoringToolId: string
  ): Promise<any[]> {
    const response = await this.axios.get(
      `/monitoring-tools/${monitoringToolId}/artifacts`
    );
    return response.data;
  }
}

export { MonitoringToolAPI };
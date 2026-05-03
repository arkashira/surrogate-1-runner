export class ConnectorError extends Error {
  constructor(
    public code: string,
    message: string,
    public details?: unknown
  ) {
    super(message);
    this.name = 'ConnectorError';
  }
}

export type HealthStatus = 'healthy' | 'unhealthy' | 'degraded';

export interface HealthResult {
  status: HealthStatus;
  latency_ms?: number;
  details?: Record<string, unknown>;
  timestamp: string;
}

export interface Connector {
  connect(): Promise<void>;
  call<T = unknown>(method: string, params?: Record<string, unknown>): Promise<T>;
  health(): Promise<HealthResult>;
}
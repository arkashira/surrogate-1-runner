import * as fs from 'fs';
import * as path from 'path';
import { LogEntry } from './types';

export class LocalLogStore {
  private logPath: string;
  private readonly MAX_LOG_ENTRIES: number = 10000;

  constructor(logDir: string) {
    this.logPath = path.join(logDir, 'execution-logs.json');
    this.ensureLogDir(logDir);
  }

  private ensureLogDir(logDir: string): void {
    try {
      if (!fs.existsSync(logDir)) {
        fs.mkdirSync(logDir, { recursive: true });
      }
    } catch (error) {
      console.error(`Failed to create log directory: ${logDir}`, error);
    }
  }

  private getLogs(): LogEntry[] {
    try {
      if (!fs.existsSync(this.logPath)) {
        return [];
      }
      const content = fs.readFileSync(this.logPath, 'utf-8');
      return JSON.parse(content);
    } catch (error) {
      console.error('Failed to read logs:', error);
      return [];
    }
  }

  private saveLogs(logs: LogEntry[]): void {
    try {
      fs.writeFileSync(this.logPath, JSON.stringify(logs, null, 2), 'utf-8');
    } catch (error) {
      console.error('Failed to save logs:', error);
    }
  }

  append(log: LogEntry): LogEntry {
    const logs = this.getLogs();
    logs.push(log);
    
    // Trim to max entries
    if (logs.length > this.MAX_LOG_ENTRIES) {
      logs.splice(0, logs.length - this.MAX_LOG_ENTRIES);
    }
    
    this.saveLogs(logs);
    return log;
  }

  getLogs(): LogEntry[] {
    return this.getLogs();
  }

  getLogsByWorkflowId(workflowId: string): LogEntry[] {
    const logs = this.getLogs();
    return logs.filter(log => log.workflowId === workflowId);
  }

  getLogsByStepId(stepId: string): LogEntry[] {
    const logs = this.getLogs();
    return logs.filter(log => log.stepId === stepId);
  }

  getLogsByTimestampRange(startTime: Date, endTime: Date): LogEntry[] {
    const logs = this.getLogs();
    return logs.filter(log => {
      const logTime = new Date(log.timestamp);
      return logTime >= startTime && logTime <= endTime;
    });
  }

  clear(): void {
    try {
      fs.writeFileSync(this.logPath, '[]', 'utf-8');
    } catch (error) {
      console.error('Failed to clear logs:', error);
    }
  }

  getLogCount(): number {
    return this.getLogs().length;
  }

  getLatestLog(): LogEntry | null {
    const logs = this.getLogs();
    return logs.length > 0 ? logs[logs.length - 1] : null;
  }

  getLogSummary(): { total: number; byStatus: Record<string, number> } {
    const logs = this.getLogs();
    const byStatus: Record<string, number> = {};
    
    logs.forEach(log => {
      byStatus[log.status] = (byStatus[log.status] || 0) + 1;
    });
    
    return {
      total: logs.length,
      byStatus
    };
  }
}
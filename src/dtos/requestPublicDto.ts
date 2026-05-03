export class RequestPublicDto {
  title: string;
  status: string;
  timeline: string;
  sla: string;
  lastUpdated: Date;
  statusLabel: string;

  constructor(title: string, status: string, timeline: string, sla: string, lastUpdated: Date, statusLabel: string) {
    this.title = title;
    this.status = status;
    this.timeline = timeline;
    this.sla = sla;
    this.lastUpdated = lastUpdated;
    this.statusLabel = statusLabel;
  }
}
import { BaseModel } from '../base/baseModel';
import { PrismaClient } from '@prisma/client';

export interface IssueEvent {
  id: string;
  repoId: string;
  issueNumber: number;
  eventType: 'created' | 'closed' | 'labeled';
  payload: any;
  createdAt: Date;
  updatedAt: Date;
}

export class IssueEventModel extends BaseModel {
  constructor(private prisma: PrismaClient) {
    super();
  }

  async create(event: Omit<IssueEvent, 'id' | 'createdAt' | 'updatedAt'>): Promise<IssueEvent> {
    const result = await this.prisma.githubIssueEvents.create({
      data: {
        repo_id: event.repoId,
        issue_number: event.issueNumber,
        event_type: event.eventType,
        payload: event.payload,
        created_at: new Date(),
        updated_at: new Date(),
      },
      select: {
        id: true,
        repoId: true,
        issueNumber: true,
        eventType: true,
        payload: true,
        createdAt: true,
        updatedAt: true,
      },
    });
    return result;
  }

  async findUniqueByRepoAndIssueAndType(
    repoId: string,
    issueNumber: number,
    eventType: 'created' | 'closed' | 'labeled'
  ): Promise<IssueEvent | null> {
    return this.prisma.githubIssueEvents.findUnique({
      where: {
        repo_id_issue_number_event_type: {
          repo_id: repoId,
          issue_number: issueNumber,
          event_type: eventType,
        },
      },
      select: {
        id: true,
        repoId: true,
        issueNumber: true,
        eventType: true,
        payload: true,
        createdAt: true,
        updatedAt: true,
      },
    });
  }
}
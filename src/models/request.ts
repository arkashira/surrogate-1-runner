// /opt/axentx/surrogate-1/src/models/request.ts

import { Follower } from './follower';

export interface RequestProps {
  id?: string;
  title: string;
  status: string;
  publicUrl: string;
  followers?: Follower[];
  statusChangedAt?: Date | null;
  createdAt?: Date;
  updatedAt?: Date;
}

export class Request {
  id?: string;
  title: string;
  status: string;
  publicUrl: string;
  followers: Follower[];
  statusChangedAt: Date | null;
  createdAt: Date;
  updatedAt: Date;

  constructor(props: RequestProps) {
    this.id = props.id;
    this.title = props.title;
    this.status = props.status;
    this.publicUrl = props.publicUrl;
    this.followers = props.followers ?? [];
    this.statusChangedAt = props.statusChangedAt ?? null;
    this.createdAt = props.createdAt ?? new Date();
    this.updatedAt = props.updatedAt ?? new Date();
  }

  addFollower(userId: string): Follower {
    const existing = this.followers.find((f) => f.userId === userId);
    if (existing) return existing;

    const follower = new Follower({
      userId,
      requestId: this.id ?? '',
      optedOut: false,
    });
    this.followers.push(follower);
    this.updatedAt = new Date();
    return follower;
  }

  removeFollower(userId: string): boolean {
    const before = this.followers.length;
    this.followers = this.followers.filter((f) => f.userId !== userId);
    if (this.followers.length !== before) {
      this.updatedAt = new Date();
      return true;
    }
    return false;
  }

  getNotifiableFollowers(): Follower[] {
    return this.followers.filter((f) => !f.optedOut);
  }

  setFollowerOptOut(userId: string, optedOut: boolean): Follower | null {
    const follower = this.followers.find((f) => f.userId === userId);
    if (!follower) return null;

    if (optedOut) follower.optOut();
    else follower.optIn();

    this.updatedAt = new Date();
    return follower;
  }

  updateStatus(newStatus: string): { previous: string; current: string }

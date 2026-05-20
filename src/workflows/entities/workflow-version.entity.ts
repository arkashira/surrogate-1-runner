import {
  Entity,
  PrimaryKey,
  Property,
  Index,
  Unique,
} from '@mikro-orm/core';

@Entity({ tableName: 'workflow_versions' })
@Unique({ properties: ['workflowId', 'version'] })
export class WorkflowVersion {
  @PrimaryKey()
  id!: string; // UUID

  @Property()
  workflowId!: string; // FK → workflows.id

  @Property()
  @Index()
  version!: number;

  @Property()
  name!: string;

  @Property({ nullable: true })
  description?: string | null;

  @Property({ type: 'json' })
  inputs: unknown = {};

  @Property({ type: 'json' })
  steps: unknown = [];

  @Property({ type: 'json' })
  outputs: unknown = {};

  @Property({ onCreate: () => new Date() })
  createdAt = new Date();
}
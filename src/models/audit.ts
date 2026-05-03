import { Column, Model, Table, DataType, ForeignKey, BelongsTo } from 'sequelize-typescript';
import { Request } from './request';

@Table({ tableName: 'audits', timestamps: true })
export class Audit extends Model {
  @Column({ type: DataType.STRING, allowNull: false })
  action!: string; // e.g., 'status_change'

  @Column({ type: DataType.JSONB, allowNull: true })
  details!: Record<string, any> | null;

  @ForeignKey(() => Request)
  @Column({ type: DataType.UUID, allowNull: false })
  requestId!: string;

  @BelongsTo(() => Request)
  request!: Request;

  @Column({ type: DataType.UUID, allowNull: false })
  actorId!: string;

  @Column({ type: DataType.STRING, allowNull: false })
  actorType!: string; // e.g., 'platform_engineer'
}
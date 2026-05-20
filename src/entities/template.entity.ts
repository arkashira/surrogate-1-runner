import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  Index,
} from "typeorm";
import { TemplateCategory } from "../types/template.types";

@Entity({ name: "templates" })
export class Template {
  @PrimaryGeneratedColumn("uuid")
  id!: string;

  @Column({ unique: true })
  @Index()
  name!: string;

  @Column({ nullable: true })
  description?: string;

  @Column({ type: "enum", enum: [
    "data-ingest",
    "data-processing",
    "model-training",
    "evaluation",
    "deployment",
    "monitoring",
    "custom",
  ] })
  category!: TemplateCategory;

  // Simple array of tags (comma‑separated in DB)
  @Column("simple-array", { nullable: true })
  tags?: string[];

  // Numeric version for ordering (auto‑increment on import)
  @Column({ default: 1 })
  version!: number;

  // Human‑readable semver (e.g. "1.0.0")
  @Column({ default: "1.0.0" })
  semver!: string;

  // Full workflow definition (JSONB in Postgres, JSON in SQLite)
  @Column("json")
  workflowDefinition!: Record<string, unknown>;

  // Optional catalogue of parameters (JSON array)
  @Column("json", { nullable: true })
  parameters?: Record<string, unknown>[];

  @CreateDateColumn()
  createdAt!: Date;

  @UpdateDateColumn()
  updatedAt!: Date;
}
export enum TemplateCategory {
  GENERAL = 'general',
  DATA_INTEGRATION = 'data_integration',
  MACHINE_LEARNING = 'machine_learning',
}

export enum TemplateTag {
  BASIC = 'basic',
  ADVANCED = 'advanced',
  ENTERPRISE = 'enterprise',
}

export interface TemplateMetadata {
  id: string;
  name: string;
  description: string;
  category: TemplateCategory;
  tags: TemplateTag[];
  version: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Template {
  metadata: TemplateMetadata;
  parameters: { [key: string]: any };
}
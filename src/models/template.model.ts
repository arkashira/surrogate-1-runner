import { TemplateMetadata, Template } from './template';

export class TemplateModel {
  private templateRepository: TemplateRepository;

  constructor(templateRepository: TemplateRepository) {
    this.templateRepository = templateRepository;
  }

  async getTemplateById(templateId: string): Promise<Template> {
    const templateMetadata = await this.templateRepository.getTemplateMetadataById(templateId);
    return {
      metadata: templateMetadata,
      parameters: {}, // TODO: fetch parameters from database
    };
  }

  async createTemplate(template: Template): Promise<Template> {
    const templateMetadata = await this.templateRepository.createTemplateMetadata(template.metadata);
    return {
      metadata: templateMetadata,
      parameters: template.parameters,
    };
  }
}

interface TemplateRepository {
  getTemplateMetadataById(templateId: string): Promise<TemplateMetadata>;
  createTemplateMetadata(templateMetadata: TemplateMetadata): Promise<TemplateMetadata>;
}
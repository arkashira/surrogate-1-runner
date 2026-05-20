import { Request, Response } from 'express';
import * as fs from 'fs';
import * as path from 'path';

/**
 * DocsController – generates Markdown documentation from workflow metadata.
 *
 * Expected metadata file location: <project_root>/workflow.metadata.json
 * Example structure:
 * {
 *   "description": "Overall workflow description",
 *   "steps": [
 *     {
 *       "name": "fetch-data",
 *       "description": "Retrieve raw data from source",
 *       "parameters": [
 *         { "name": "url", "type": "string", "description": "Source endpoint" },
 *         { "name": "timeout", "type": "number", "description": "Request timeout in ms" }
 *       ]
 *     },
 *     ...
 *   ]
 * }
 */
class DocsController {
  /**
   * GET /docs/workflow – returns generated Markdown documentation.
   */
  static getWorkflowDocs(req: Request, res: Response): void {
    const metadataPath = path.resolve(__dirname, '../../workflow.metadata.json');

    try {
      const raw = fs.readFileSync(metadataPath, 'utf-8');
      const metadata = JSON.parse(raw);
      const markdown = DocsController.generateMarkdown(metadata);
      res.type('text/markdown').send(markdown);
    } catch (err) {
      console.error('Failed to generate workflow documentation:', err);
      res.status(500).json({ error: 'Unable to generate documentation' });
    }
  }

  /**
   * Convert the workflow metadata JSON into a Markdown string.
   */
  private static generateMarkdown(metadata: any): string {
    let md = '# Workflow Documentation\n\n';

    if (metadata.description) {
      md += `${metadata.description}\n\n`;
    }

    if (Array.isArray(metadata.steps) && metadata.steps.length) {
      md += '## Steps\n\n';
      metadata.steps.forEach((step: any, index: number) => {
        md += `### ${index + 1}. ${step.name}\n`;
        if (step.description) {
          md += `${step.description}\n`;
        }

        if (Array.isArray(step.parameters) && step.parameters.length) {
          md += '\n**Parameters:**\n\n';
          step.parameters.forEach((param: any) => {
            const type = param.type ? `(${param.type})` : '';
            const desc = param.description ? `: ${param.description}` : '';
            md += `- \`${param.name}\` ${type}${desc}\n`;
          });
        }
        md += '\n';
      });
    } else {
      md += '_No steps defined in workflow metadata._\n';
    }

    return md;
  }
}

export default DocsController;
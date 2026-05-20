
import { createClient } from '@elastic/elasticsearch';
import { Workflow } from './workflow';

export class Observability {
  private esClient: any;

  constructor() {
    this.esClient = createClient({ node: 'http://localhost:9200' });
  }

  async start() {
    const workflow = new Workflow();
    setInterval(async () => {
      const runningWorkflows = await this.esClient.search({
        index: 'workflows',
        body: {
          query: {
            bool: {
              must: [
                {
                  match: {
                    status: 'running',
                  },
                },
              ],
            },
          },
        },
      });

      console.log(`Currently running workflows: ${runningWorkflows.body.hits.total}`);

      const completedWorkflows = await this.esClient.search({
        index: 'workflows',
        body: {
          query: {
            bool: {
              must: [
                {
                  match: {
                    status: 'completed',
                  },
                },
              ],
            },
          },
        },
      });

      console.log(`Completed workflows: ${completedWorkflows.body.hits.total}`);

      workflow.execute();
    }, 1000);
  }
}
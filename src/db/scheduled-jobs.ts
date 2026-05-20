import { createConnection } from 'typeorm';
import { Job } from './Job';

export async function getQueuedJobs() {
  const connection = await createConnection();
  const jobs = await connection.query('SELECT * FROM scheduled_jobs');
  connection.close();
  return jobs.map((job) => new Job(job.id, job.timestamp, job.workflow_id));
}

export async function saveJob(job: Job) {
  const connection = await createConnection();
  await connection.query('INSERT INTO scheduled_jobs (id, timestamp, workflow_id) VALUES (?, ?, ?)', [job.id, job.timestamp, job.workflowId]);
  connection.close();
}
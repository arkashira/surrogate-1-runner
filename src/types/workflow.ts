export interface Workflow {
  id: string;
  name: string;
  steps: Step[];
  createdAt: Date;
  updatedAt: Date;
}

export interface Step {
  id: string;
  name: string;
  action: string;
  params: any;
  createdAt: Date;
  updatedAt: Date;
}
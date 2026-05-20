export interface Template {
  id: string;
  name: string;
  description: string;
  model: string;
  prompt: string;
}

export type Templates = Template[];
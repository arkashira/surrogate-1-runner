import { z } from 'zod';

export const LlmInvokeRequestSchema = z.object({
  model: z.string().describe('The identifier of the LLM provider to use'),
  prompt: z.string().describe('The text prompt to send to the LLM'),
  temperature: z.number()
    .min(0)
    .max(1)
    .optional()
    .describe('Sampling temperature (0-1, optional)'),
  maxTokens: z.number()
    .positive()
    .optional()
    .describe('Maximum tokens in the generated text (optional)'),
});

export type LlmInvokeRequest = z.infer<typeof LlmInvokeRequestSchema>;
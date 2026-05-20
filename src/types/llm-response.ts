import { z } from 'zod';

export const LlmInvokeResponseSchema = z.object({
  model: z.string().describe('The identifier of the LLM provider that generated the response'),
  content: z.string().describe('The generated text response'),
  error: z.union([
    z.object({
      message: z.string().describe('Error message from the provider'),
      code: z.string().optional().describe('Error code from the provider'),
    }),
    z.literal(null).describe('No error occurred'),
  ]).default(null).describe('Error details if the request failed'),
  metadata: z.object({
    tokensUsed: z.number().optional().describe('Number of tokens used'),
    modelVersion: z.string().optional().describe('Specific model version used'),
  }).optional().describe('Additional metadata about the response')
}).refine(
  (data) => data.error === null || data.content === '',
  {
    message: "Content must be empty when there's an error",
    path: ["content"]
  }
);

export type LlmInvokeResponse = z.infer<typeof LlmInvokeResponseSchema>;
export interface Variant {
  id: string;
  name: string;
  openaiCompatibility: 'full' | 'partial' | 'none';
  modelContextProtocolVersion: string;
  containerizationRequirements: string[];
  harnessPatternType: 'serverless' | 'streaming' | 'batch';
}
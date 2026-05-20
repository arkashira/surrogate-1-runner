export interface TypeSafetyIssue {
  filePath: string;
  line: number;
  column: number;
  message: string;
  severity: 'error' | 'warning' | 'info';
  code?: number;
}

export interface OptimizationRecommendation {
  filePath: string;
  line: number;
  message: string;
  impact: 'low' | 'medium' | 'high';
}

export interface TypeAnalysisReport {
  issues: TypeSafetyIssue[];
  recommendations: OptimizationRecommendation[];
  compilationTime: number;
  filesAnalyzed: number;
}

export interface AnalyzerConfig {
  rootDir: string;
  tsConfigPath: string;
  includePatterns?: string[];
  excludePatterns?: string[];
}
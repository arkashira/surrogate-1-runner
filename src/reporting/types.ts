/**
 * Core type definitions for the reporting system drill-down functionality
 */

export interface TypeIssue {
  id: string;
  severity: 'error' | 'warning' | 'info';
  message: string;
  filePath: string;
  line: number;
  column: number;
  code: string;
  suggestion?: string;
  relatedNodes?: string[];
}

export interface TypeAnalysisReport {
  id: string;
  timestamp: Date;
  summary: ReportSummary;
  issues: TypeIssue[];
  recommendations: OptimizationRecommendation[];
}

export interface ReportSummary {
  totalIssues: number;
  errorCount: number;
  warningCount: number;
  infoCount: number;
  filesAnalyzed: number;
  avgCompilationTimeMs: number;
}

export interface OptimizationRecommendation {
  id: string;
  category: 
    | 'type-simplification' 
    | 'generics' 
    | 'imports' 
    | 'any-usage' 
    | 'inference';
  title: string;
  description: string;
  impact: 'high' | 'medium' | 'low';
  affectedFiles: string[];
  potentialSavingsMs?: number;
}

export interface DrillDownContext {
  reportId: string;
  selectedIssueId?: string;
  selectedFile?: string;
  selectedCategory?: string;
  filters: DrillDownFilters;
}

export interface DrillDownFilters {
  severity?: ('error' | 'warning' | 'info')[];
  filePath?: string;
  category?: string[];
  dateRange?: {
    start: Date;
    end: Date;
  };
}

export interface DrillDownResult {
  issues: TypeIssue[];
  groupedBy: 'file' | 'severity' | 'category' | 'none';
  totalCount: number;
  page: number;
  pageSize: number;
}
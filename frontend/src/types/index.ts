export interface Session {
  id: string;
  status: 'running' | 'stopped' | 'completed' | 'error';
  created_at: string;
  updated_at: string;
  grant_topic: string;
  funding_agency?: string;
  grant_amount?: number;
  keywords?: string[];
  model?: string;
  message?: string;
  current_agent?: string;
  progress: number;
}

export interface ProposalDraft {
  version: number;
  content: Record<string, string>;
  sections: Record<string, string>;
  metadata: Record<string, any>;
  scores: Record<string, number>;
  feedback: string[];
  created_at: string;
  agent_notes: Record<string, string>;
}

export interface ComplianceIssue {
  rule_id: string;
  category: string;
  section: string;
  issue: string;
  severity: 'pass' | 'warning' | 'fail' | 'skip';
  suggestion: string;
}

export interface ComplianceReport {
  agency: string;
  proposal_type: string;
  total_rules: number;
  passed: number;
  warnings: number;
  failed: number;
  skipped: number;
  issues: ComplianceIssue[];
  overall_status: 'pass' | 'warning' | 'fail';
  score: number;
}

export interface QualityScore {
  criterion: string;
  score: number;
  weight: number;
  strengths: string[];
  weaknesses: string[];
  suggestions: string[];
}

export interface QualityAssessment {
  overall_score: number;
  criterion_scores: QualityScore[];
  summary: string;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  estimated_success_rate: number;
}

export interface Citation {
  id: string;
  title: string;
  authors: string[];
  journal: string;
  year: number;
  doi?: string;
  pmid?: string;
  abstract?: string;
  relevance_score: number;
}

export interface Template {
  template_id: string;
  name: string;
  agency: string;
  proposal_type: string;
  description: string;
  sections: {
    name: string;
    title: string;
    description: string;
    required: boolean;
    max_words?: number;
    guidance: string;
  }[];
  page_limit: number;
  format_requirements: Record<string, string>;
}

export interface BudgetItem {
  category: string;
  description: string;
  amount: number;
  justification: string;
}

export interface Metrics {
  total_sessions: number;
  active_sessions: number;
  completed_sessions: number;
  failed_sessions: number;
  average_completion_time?: number;
  total_cost: number;
  total_api_calls: number;
  budget: {
    limit?: number;
    spent: number;
    remaining?: number;
    utilization?: number;
  };
}

export interface StartProposalRequest {
  grant_topic: string;
  funding_agency?: string;
  grant_amount?: number;
  keywords?: string[];
  model?: string;
}

export interface StartProposalResponse {
  session_id: string;
  status: string;
  created_at: string;
  updated_at: string;
  grant_topic: string;
  message: string;
  current_agent?: string;
  progress: number;
}
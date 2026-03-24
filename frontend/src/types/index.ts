export type InputType = "text" | "file" | "sql" | "log" | "chat"
export type RiskLevel = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
export type ActionTaken = "allowed" | "masked" | "blocked"

export interface Finding {
  type: string;
  risk: RiskLevel;
  line?: number;
  masked_value?: string;
  original_line?: string;
  detection_method?: string;
  recommendation?: string;
  value?: string;
}

export interface AnalyzeResponse {
  summary: string;
  content_type: string;
  findings: Finding[];
  risk_score: number;
  risk_level: RiskLevel;
  action: ActionTaken;
  insights: string[];
  anomalies: string[];
  ai_used: boolean;
  request_id: string;
  duration_ms: number;
  total_lines?: number;
  detection_breakdown?: {
    regex_findings: number;
    statistical_findings: number;
    ml_findings: number;
    ai_findings: number;
  };
}

export interface AnalyzeOptions {
  mask_output: boolean;
  use_ai: boolean;
  block_on_critical: boolean;
}


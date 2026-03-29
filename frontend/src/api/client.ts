import axios from 'axios';
import type {
  Session,
  StartProposalRequest,
  StartProposalResponse,
  Metrics,
} from '../types';

const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';

class ApiClient {
  private client = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
    timeout: 120000, // 2 minute timeout
  });

  // Session management
  async startProposal(request: StartProposalRequest): Promise<StartProposalResponse> {
    const response = await this.client.post<StartProposalResponse>('/api/proposal/start', request);
    return response.data;
  }

  async stopProposal(sessionId: string): Promise<Session> {
    const response = await this.client.post<Session>(`/api/proposal/stop?session_id=${sessionId}`);
    return response.data;
  }

  async getSessionStatus(sessionId: string): Promise<Session> {
    const response = await this.client.get<Session>(`/api/proposal/status?session_id=${sessionId}`);
    return response.data;
  }

  async getSessionHistory(limit: number = 50, offset: number = 0): Promise<{
    total: number;
    sessions: Session[];
  }> {
    const response = await this.client.get(`/api/proposal/history?limit=${limit}&offset=${offset}`);
    return response.data;
  }

  // Compliance & Quality
  async checkCompliance(proposalText: string, agency: string, grantType?: string): Promise<any> {
    const response = await this.client.post('/api/compliance/check', {
      proposal_text: proposalText,
      agency,
      grant_type: grantType,
    });
    return response.data;
  }

  async assessQuality(proposalText: string, agency: string, sections?: Record<string, string>): Promise<any> {
    const response = await this.client.post('/api/quality/assess', {
      proposal_text: proposalText,
      agency,
      sections,
    });
    return response.data;
  }

  // Templates
  async getTemplates(agency?: string): Promise<any> {
    const response = await this.client.get(`/api/templates${agency ? `?agency=${agency}` : ''}`);
    return response.data;
  }

  async getTemplate(templateId: string): Promise<any> {
    const response = await this.client.get(`/api/templates/${templateId}`);
    return response.data;
  }

  // Export
  async exportProposal(sessionId: string, format: 'pdf' | 'docx' | 'latex' | 'markdown' = 'pdf', templateId?: string): Promise<any> {
    const response = await this.client.post(`/api/proposal/${sessionId}/export`, {
      format,
      template_id: templateId,
    });
    return response.data;
  }

  // Metrics
  async getMetrics(): Promise<Metrics> {
    const response = await this.client.get<Metrics>('/api/metrics');
    return response.data;
  }

  async getCostSummary(): Promise<Record<string, any>> {
    const response = await this.client.get('/api/cost/summary');
    return response.data;
  }

  // Health check
  async healthCheck(): Promise<{ status: string; uptime_seconds: number }> {
    const response = await this.client.get('/health');
    return response.data;
  }
}

export const apiClient = new ApiClient();
export default apiClient;
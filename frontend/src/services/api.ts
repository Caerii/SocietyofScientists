import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// API endpoints
export const proposalApi = {
  start: (task: string) => api.post('/api/proposal/start', { task }),
  stop: () => api.post('/api/proposal/stop'),
  status: () => api.get('/api/proposal/status'),
  getHistory: () => api.get('/api/proposal/history'),
  getProposal: (id: string) => api.get(`/api/proposal/${id}`),
}

export const costApi = {
  getSummary: () => api.get('/api/cost/summary'),
  getDetails: () => api.get('/api/cost/details'),
}

export const statsApi = {
  getStats: () => api.get('/api/stats'),
}

import axios from 'axios';
import type { AskRequest, AskResponse } from '../types/chat';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds timeout for responses
});

export const chatService = {
  async askQuestion(question: string): Promise<AskResponse> {
    const request: AskRequest = { question };
    const response = await api.post<AskResponse>('/api/rag/ask', request);
    return response.data;
  },

  async checkHealth(): Promise<boolean> {
    try {
      await api.get('/');
      return true;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
};

export default chatService;

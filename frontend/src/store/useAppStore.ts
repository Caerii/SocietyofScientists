import { create } from 'zustand';
import { Session } from '../types';

interface AppState {
  currentSession: Session | null;
  sessions: Session[];
  isGenerating: boolean;
  // Actions
  setCurrentSession: (session: Session | null) => void;
  setSessions: (sessions: Session[]) => void;
  addSession: (session: Session) => void;
  updateSession: (sessionId: string, updates: Partial<Session>) => void;
  setGenerating: (isGenerating: boolean) => void;
}

export const useAppStore = create<AppState>((set) => ({
  currentSession: null,
  sessions: [],
  isGenerating: false,

  setCurrentSession: (session) => set({ currentSession: session }),

  setSessions: (sessions) => set({ sessions }),

  addSession: (session) => set((state) => ({ 
    sessions: [session, ...state.sessions],
    currentSession: session,
  })),

  updateSession: (sessionId, updates) => set((state) => ({
    currentSession: state.currentSession?.id === sessionId
      ? { ...state.currentSession, ...updates }
      : state.currentSession,
    sessions: state.sessions.map(s =>
      s.id === sessionId ? { ...s, ...updates } : s
    ),
  })),

  setGenerating: (isGenerating) => set({ isGenerating }),
}));
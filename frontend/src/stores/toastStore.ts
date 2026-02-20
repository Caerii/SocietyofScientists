import { create } from 'zustand'
import { ToastMessage } from '../components/ui/ToastContainer'

interface ToastStore {
  toasts: ToastMessage[]
  addToast: (message: string, type?: ToastMessage['type'], duration?: number) => void
  removeToast: (id: string) => void
  success: (message: string, duration?: number) => void
  error: (message: string, duration?: number) => void
  info: (message: string, duration?: number) => void
  warning: (message: string, duration?: number) => void
}

export const useToastStore = create<ToastStore>((set) => ({
  toasts: [],
  addToast: (message, type = 'info', duration = 5000) => {
    const id = Math.random().toString(36).substring(7)
    set((state) => ({
      toasts: [...state.toasts, { id, message, type, duration }],
    }))
    return id
  },
  removeToast: (id) =>
    set((state) => ({
      toasts: state.toasts.filter((toast) => toast.id !== id),
    })),
  success: (message, duration) => {
    useToastStore.getState().addToast(message, 'success', duration)
  },
  error: (message, duration) => {
    useToastStore.getState().addToast(message, 'error', duration)
  },
  info: (message, duration) => {
    useToastStore.getState().addToast(message, 'info', duration)
  },
  warning: (message, duration) => {
    useToastStore.getState().addToast(message, 'warning', duration)
  },
}))

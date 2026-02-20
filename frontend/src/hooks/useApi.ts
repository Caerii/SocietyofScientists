import { useState, useEffect, useCallback } from 'react'
import { api } from '../services/api'
import { useToastStore } from '../stores/toastStore'

interface UseApiOptions<T> {
  initialData?: T
  onSuccess?: (data: T) => void
  onError?: (error: any) => void
  showErrorToast?: boolean
  enabled?: boolean
}

export function useApi<T = any>(
  url: string,
  options: UseApiOptions<T> = {}
) {
  const {
    initialData,
    onSuccess,
    onError,
    showErrorToast = true,
    enabled = true,
  } = options

  const [data, setData] = useState<T | undefined>(initialData)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<any>(null)
  const { error: showError } = useToastStore()

  const fetchData = useCallback(async () => {
    if (!enabled) return

    setLoading(true)
    setError(null)

    try {
      const response = await api.get(url)
      setData(response.data)
      onSuccess?.(response.data)
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'An error occurred'
      setError(err)
      if (showErrorToast) {
        showError(errorMessage)
      }
      onError?.(err)
    } finally {
      setLoading(false)
    }
  }, [url, enabled, onSuccess, onError, showErrorToast, showError])

  useEffect(() => {
    fetchData()
  }, [fetchData])

  const refetch = useCallback(() => {
    fetchData()
  }, [fetchData])

  return { data, loading, error, refetch }
}

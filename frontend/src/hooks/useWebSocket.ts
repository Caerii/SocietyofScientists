import { useEffect, useRef, useState, useCallback } from 'react'

type MessageHandler = (data: any) => void

export function useWebSocket() {
  const [socket, setSocket] = useState<WebSocket | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const reconnectTimeoutRef = useRef<number>()
  const messageHandlersRef = useRef<Map<string, MessageHandler[]>>(new Map())
  const reconnectAttemptsRef = useRef(0)
  const maxReconnectAttempts = 5

  const connect = useCallback(() => {
    if (socket?.readyState === WebSocket.OPEN) return

    const wsUrl = (import.meta as any).env?.VITE_WS_URL || 'ws://localhost:8000/ws'
    const newSocket = new WebSocket(wsUrl)

    newSocket.onopen = () => {
      console.log('WebSocket connected')
      setIsConnected(true)
      reconnectAttemptsRef.current = 0
    }

    newSocket.onclose = () => {
      console.log('WebSocket disconnected')
      setIsConnected(false)
      
      // Attempt to reconnect
      if (reconnectAttemptsRef.current < maxReconnectAttempts) {
        reconnectAttemptsRef.current++
        reconnectTimeoutRef.current = setTimeout(() => {
          connect()
        }, 1000 * reconnectAttemptsRef.current)
      }
    }

    newSocket.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    newSocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        const { type, ...payload } = data
        
        // Call registered handlers for this message type
        const handlers = messageHandlersRef.current.get(type) || []
        handlers.forEach(handler => handler(payload))
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error)
      }
    }

    setSocket(newSocket)
  }, [socket])

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
    }
    if (socket) {
      socket.close()
      setSocket(null)
      setIsConnected(false)
    }
  }, [socket])

  const sendMessage = useCallback((type: string, data: any) => {
    if (socket?.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ type, ...data }))
    }
  }, [socket])

  const onMessage = useCallback((type: string, handler: MessageHandler) => {
    if (!messageHandlersRef.current.has(type)) {
      messageHandlersRef.current.set(type, [])
    }
    messageHandlersRef.current.get(type)!.push(handler)

    // Return cleanup function
    return () => {
      const handlers = messageHandlersRef.current.get(type)
      if (handlers) {
        const index = handlers.indexOf(handler)
        if (index > -1) {
          handlers.splice(index, 1)
        }
      }
    }
  }, [])

  useEffect(() => {
    return () => {
      disconnect()
    }
  }, [disconnect])

  return {
    connect,
    disconnect,
    sendMessage,
    onMessage,
    isConnected,
    socket,
  }
}

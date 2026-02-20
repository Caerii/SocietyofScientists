import { useEffect, useRef } from 'react'
import { MessageSquare } from 'lucide-react'
import Card from './ui/Card'
import Message, { MessageProps } from './ui/Message'
import EmptyState from './ui/EmptyState'

interface ConversationViewProps {
  conversation: MessageProps[]
  isRunning: boolean
}

export default function ConversationView({ conversation, isRunning }: ConversationViewProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Only auto-scroll if user is near bottom
    if (messagesEndRef.current && containerRef.current) {
      const container = containerRef.current
      const isNearBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 100
      if (isNearBottom) {
        messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
      }
    }
  }, [conversation])

  return (
    <Card
      title="Conversation"
      icon={MessageSquare}
      className="relative"
    >
      {isRunning && (
        <span className="absolute top-6 right-6 px-2 py-1 text-xs bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400 rounded animate-pulse">
          Active
        </span>
      )}
      <div 
        ref={containerRef}
        className="space-y-4 max-h-96 overflow-y-auto scroll-smooth"
      >
        {conversation.length === 0 ? (
          <EmptyState
            icon={MessageSquare}
            title="No messages yet"
            description="Start a proposal to see agent conversations"
          />
        ) : (
          <>
            {conversation.map((msg, idx) => (
              <Message
                key={idx}
                role={msg.role}
                content={msg.content}
                agent={msg.agent}
                timestamp={msg.timestamp}
              />
            ))}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>
    </Card>
  )
}

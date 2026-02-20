import { User, Bot } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { cn } from '../../utils/cn'

export interface MessageProps {
  role: 'user' | 'agent' | 'system'
  content: string
  agent?: string
  timestamp?: string
}

export default function Message({ role, content, agent, timestamp }: MessageProps) {
  const isUser = role === 'user'
  const isSystem = role === 'system'

  return (
    <div
      className={cn(
        'flex space-x-3',
        isUser ? 'justify-end' : 'justify-start'
      )}
    >
      {!isUser && (
        <div className="flex-shrink-0">
          <div className="h-8 w-8 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center">
            <Bot className="h-5 w-5 text-primary-600 dark:text-primary-400" />
          </div>
        </div>
      )}
      <div
        className={cn(
          'max-w-3xl rounded-lg p-4 transition-all',
          isUser
            ? 'bg-primary-600 text-white'
            : isSystem
            ? 'bg-gray-200 dark:bg-gray-800 text-gray-800 dark:text-gray-200'
            : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
        )}
      >
        <div className="flex items-center justify-between mb-1">
          <div className="text-sm font-medium">
            {isUser ? 'You' : agent || 'Agent'}
          </div>
          {timestamp && (
            <div className="text-xs opacity-70">
              {new Date(timestamp).toLocaleTimeString()}
            </div>
          )}
        </div>
        <div className="prose prose-sm dark:prose-invert max-w-none">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </div>
      {isUser && (
        <div className="flex-shrink-0">
          <div className="h-8 w-8 rounded-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center">
            <User className="h-5 w-5 text-gray-600 dark:text-gray-300" />
          </div>
        </div>
      )}
    </div>
  )
}

import { useState, useEffect } from 'react'
import { Clock, FileText, Search, Eye } from 'lucide-react'
import { proposalApi } from '../services/api'
import Input from '../components/ui/Input'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import EmptyState from '../components/ui/EmptyState'
import { useToastStore } from '../stores/toastStore'

interface Conversation {
  id: string
  task: string
  created_at: string
  status: string
  cost: number
}

export default function ConversationHistory() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const { error } = useToastStore()

  useEffect(() => {
    setLoading(true)
proposalApi
      .getHistory()
      .then((res) => setConversations(res.data))
      .catch(() => {
        error('Failed to load conversation history')
        setConversations([])
      })
      .finally(() => setLoading(false))
  }, [error])

  const filtered = conversations.filter((conv) =>
    conv.task.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
        Conversation History
      </h2>

      {/* Search */}
      <Card>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          <Input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search conversations..."
            className="pl-10"
          />
        </div>
      </Card>

      {/* Conversations List */}
      {loading ? (
        <Card>
          <LoadingSpinner size="lg" text="Loading conversations..." />
        </Card>
      ) : filtered.length === 0 ? (
        <Card>
          <EmptyState
            icon={FileText}
            title={search ? 'No conversations found' : 'No conversations yet'}
            description={
              search
                ? 'Try adjusting your search terms'
                : 'Start creating proposals to see them here'
            }
          />
        </Card>
      ) : (
        <div className="space-y-4">
          {filtered.map((conv) => (
            <Card
              key={conv.id}
              className="hover:shadow-md transition-all duration-200"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    {conv.task}
                  </h3>
                  <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
                    <div className="flex items-center space-x-1">
                      <Clock className="h-4 w-4" />
                      <span>{new Date(conv.created_at).toLocaleString()}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <FileText className="h-4 w-4" />
                      <span className="capitalize">{conv.status}</span>
                    </div>
                    <span>Cost: ${conv.cost.toFixed(4)}</span>
                  </div>
                </div>
                <Button variant="ghost" size="sm">
                  <Eye className="h-4 w-4 mr-2" />
                  View
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

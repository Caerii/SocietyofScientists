import { useState, useEffect } from 'react'
import { Send, Loader2, Download } from 'lucide-react'
import { api } from '../services/api'
import { useWebSocket } from '../hooks/useWebSocket'
import AgentStatus from '../components/AgentStatus'
import ConversationView from '../components/ConversationView'
import ProposalPreview from '../components/ProposalPreview'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'
import Card from '../components/ui/Card'
import { useToastStore } from '../stores/toastStore'

export default function ProposalBuilder() {
  const [task, setTask] = useState('')
  const [isRunning, setIsRunning] = useState(false)
  const [conversation, setConversation] = useState<any[]>([])
  const [activeAgent, setActiveAgent] = useState<string | null>(null)
  const [proposal, setProposal] = useState<string>('')
  const { connect, disconnect, isConnected, onMessage } = useWebSocket()
  const { success, error } = useToastStore()

  useEffect(() => {
    connect()
    return () => disconnect()
  }, [connect, disconnect])

  // Set up WebSocket message handlers
  useEffect(() => {
    const cleanupAgentMessage = onMessage('agent_message', (data) => {
      setActiveAgent(data.agent)
      setConversation((prev) => [...prev, {
        role: 'agent',
        agent: data.agent,
        content: data.content,
        timestamp: new Date().toISOString(),
      }])
    })

    const cleanupProposalUpdate = onMessage('proposal_update', (data) => {
      setProposal(data.proposal || '')
    })

    const cleanupCostUpdate = onMessage('cost_update', (data) => {
      // Handle cost updates if needed
      console.log('Cost update:', data)
    })

    return () => {
      cleanupAgentMessage()
      cleanupProposalUpdate()
      cleanupCostUpdate()
    }
  }, [onMessage])

  // Prevent auto-scroll on mount
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [])

  const handleStart = async () => {
    if (!task.trim()) {
      error('Please enter a research task')
      return
    }

    setIsRunning(true)
    setConversation([])
    setProposal('')

    try {
      const response = await api.post('/api/proposal/start', { task })
      success('Proposal generation started')
      console.log('Started proposal generation:', response.data)
    } catch (err: any) {
      error(err.response?.data?.detail || 'Failed to start proposal generation')
      setIsRunning(false)
    }
  }

  const handleStop = () => {
    setIsRunning(false)
    api
      .post('/api/proposal/stop')
      .then(() => success('Proposal generation stopped'))
      .catch(() => error('Failed to stop proposal generation'))
  }

  const handleExport = () => {
    // Export proposal as markdown
    const blob = new Blob([proposal], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `proposal-${Date.now()}.md`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
          Proposal Builder
        </h2>
        <Button
          variant="secondary"
          onClick={handleExport}
          disabled={!proposal}
        >
          <Download className="h-5 w-5 mr-2" />
          Export
        </Button>
      </div>

      {/* Task Input */}
      <Card>
        <Input
          label="Research Task / Proposal Topic"
          value={task}
          onChange={(e) => setTask(e.target.value)}
          placeholder="e.g., Propose a novel neural network architecture..."
          disabled={isRunning}
          className="mb-4"
        />
        <div className="flex items-center justify-between">
          <Button
            variant="primary"
            onClick={isRunning ? handleStop : handleStart}
            disabled={!task.trim() || !isConnected}
          >
            {isRunning ? (
              <>
                <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                Stop
              </>
            ) : (
              <>
                <Send className="h-5 w-5 mr-2" />
                Start
              </>
            )}
          </Button>
          {!isConnected && (
            <p className="text-sm text-red-600 dark:text-red-400">
              Not connected to server. Please check backend.
            </p>
          )}
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Agent Status */}
        <div className="lg:col-span-1">
          <AgentStatus activeAgent={activeAgent} />
        </div>

        {/* Conversation & Proposal */}
        <div className="lg:col-span-2 space-y-6">
          <ConversationView
            conversation={conversation}
            isRunning={isRunning}
          />
          <ProposalPreview proposal={proposal} />
        </div>
      </div>
    </div>
  )
}

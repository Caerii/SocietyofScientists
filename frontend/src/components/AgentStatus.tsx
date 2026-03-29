import { Brain, CheckCircle2, Loader2 } from 'lucide-react'
import Card from './ui/Card'
import { cn } from '../utils/cn'

interface AgentStatusProps {
  activeAgent: string | null
}

const AGENTS = [
  'planner',
  'scientist_computer_vision_engineer',
  'scientist_ai_language_models',
  'scientist_ai_hardware_engineer',
  'scientist',
  'hypothesis_agent',
  'objective_agent',
  'methodology_agent',
  'ethics_agent',
  'comparison_agent',
  'novelty_agent',
  'budget_agent',
  'critic_agent',
] as const

function formatAgentName(agent: string): string {
  return agent
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (l) => l.toUpperCase())
    .replace(/\bai\b/gi, 'AI')
}

export default function AgentStatus({ activeAgent }: AgentStatusProps) {
  return (
    <Card title="Agent Status" icon={Brain}>
      <div className="space-y-2 max-h-96 overflow-y-auto scroll-smooth">
        {AGENTS.map((agent) => {
          const isActive = activeAgent === agent
          return (
            <div
              key={agent}
              className={cn(
                'flex items-center space-x-3 p-3 rounded-lg transition-all duration-200',
                isActive
                  ? 'bg-primary-50 dark:bg-primary-900/20 border border-primary-200 dark:border-primary-800 shadow-sm'
                  : 'bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700'
              )}
            >
              {isActive ? (
                <Loader2 className="h-4 w-4 text-primary-600 dark:text-primary-400 animate-spin flex-shrink-0" />
              ) : (
                <CheckCircle2 className="h-4 w-4 text-gray-400 dark:text-gray-500 flex-shrink-0" />
              )}
              <span
                className={cn(
                  'text-sm font-medium transition-colors',
                  isActive
                    ? 'text-primary-900 dark:text-primary-200'
                    : 'text-gray-700 dark:text-gray-300'
                )}
              >
                {formatAgentName(agent)}
              </span>
            </div>
          )
        })}
      </div>
    </Card>
  )
}

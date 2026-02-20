import { Link } from 'react-router-dom'
import { Plus, TrendingUp, DollarSign, Users, FileText } from 'lucide-react'
import { useCostStore } from '../stores/costStore'
import StatCard from '../components/ui/StatCard'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import { useApi } from '../hooks/useApi'

interface DashboardStats {
  totalProposals: number
  activeConversations: number
  totalCost: number
  agentsActive: number
}

export default function Dashboard() {
  const { totalCost } = useCostStore()
  const { data: stats = {
    totalProposals: 0,
    activeConversations: 0,
    totalCost: totalCost,
    agentsActive: 12,
  }, loading } = useApi<DashboardStats>('/api/stats', {
    showErrorToast: true,
    initialData: {
      totalProposals: 0,
      activeConversations: 0,
      totalCost: totalCost,
      agentsActive: 12,
    },
  })

  const statCards = [
    {
      title: 'Total Proposals',
      value: stats.totalProposals,
      icon: FileText,
      color: 'text-blue-600 dark:text-blue-400',
      bgColor: 'bg-blue-50 dark:bg-blue-900/20',
    },
    {
      title: 'Active Conversations',
      value: stats.activeConversations,
      icon: Users,
      color: 'text-green-600 dark:text-green-400',
      bgColor: 'bg-green-50 dark:bg-green-900/20',
    },
    {
      title: 'Total Cost',
      value: `$${stats.totalCost.toFixed(4)}`,
      icon: DollarSign,
      color: 'text-purple-600 dark:text-purple-400',
      bgColor: 'bg-purple-50 dark:bg-purple-900/20',
    },
    {
      title: 'Active Agents',
      value: stats.agentsActive,
      icon: TrendingUp,
      color: 'text-orange-600 dark:text-orange-400',
      bgColor: 'bg-orange-50 dark:bg-orange-900/20',
    },
  ]

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
          Dashboard
        </h2>
        <Link to="/proposal">
          <Button>
            <Plus className="h-5 w-5 mr-2" />
            New Proposal
          </Button>
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat) => (
          <StatCard
            key={stat.title}
            title={stat.title}
            value={stat.value}
            icon={stat.icon}
            color={stat.color}
            bgColor={stat.bgColor}
            loading={loading}
          />
        ))}
      </div>

      {/* Quick Actions */}
      <Card title="Quick Actions">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            to="/proposal"
            className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-all duration-200"
          >
            <h4 className="font-medium text-gray-900 dark:text-white">
              Create New Proposal
            </h4>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              Start a new grant proposal with multi-agent collaboration
            </p>
          </Link>
          <Link
            to="/history"
            className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-all duration-200"
          >
            <h4 className="font-medium text-gray-900 dark:text-white">
              View History
            </h4>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              Browse past proposals and conversations
            </p>
          </Link>
          <Link
            to="/analytics"
            className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-all duration-200"
          >
            <h4 className="font-medium text-gray-900 dark:text-white">
              View Analytics
            </h4>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              Monitor costs and agent performance
            </p>
          </Link>
        </div>
      </Card>
    </div>
  )
}

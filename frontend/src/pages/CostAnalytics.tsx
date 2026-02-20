import { DollarSign, TrendingUp, Activity } from 'lucide-react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import StatCard from '../components/ui/StatCard'
import Card from '../components/ui/Card'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import EmptyState from '../components/ui/EmptyState'
import { useApi } from '../hooks/useApi'

interface CostSummary {
  total_cost: number
  total_tokens: number
  total_calls: number
  by_model: Record<string, { cost: number; calls: number }>
}

export default function CostAnalytics() {
  const { data: summary = {
    total_cost: 0,
    total_tokens: 0,
    total_calls: 0,
    by_model: {},
  }, loading } = useApi<CostSummary>('/api/cost/summary', {
    showErrorToast: true,
    initialData: {
      total_cost: 0,
      total_tokens: 0,
      total_calls: 0,
      by_model: {},
    },
  })

  const chartData = Object.entries(summary.by_model).map(
    ([model, data]: [string, any]) => ({
      model,
      cost: data.cost || 0,
      calls: data.calls || 0,
    })
  )

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
        Cost Analytics
      </h2>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Total Cost"
          value={`$${summary.total_cost.toFixed(6)}`}
          icon={DollarSign}
          color="text-green-600 dark:text-green-400"
          bgColor="bg-green-50 dark:bg-green-900/20"
          loading={loading}
        />
        <StatCard
          title="Total Tokens"
          value={summary.total_tokens.toLocaleString()}
          icon={Activity}
          color="text-blue-600 dark:text-blue-400"
          bgColor="bg-blue-50 dark:bg-blue-900/20"
          loading={loading}
        />
        <StatCard
          title="Total Calls"
          value={summary.total_calls}
          icon={TrendingUp}
          color="text-purple-600 dark:text-purple-400"
          bgColor="bg-purple-50 dark:bg-purple-900/20"
          loading={loading}
        />
      </div>

      {/* Cost by Model Chart */}
      <Card title="Cost by Model">
        {loading ? (
          <LoadingSpinner size="lg" text="Loading chart data..." />
        ) : chartData.length === 0 ? (
          <EmptyState
            icon={Activity}
            title="No cost data available"
            description="Cost data will appear here as you use the system"
          />
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-gray-300 dark:stroke-gray-700" />
              <XAxis
                dataKey="model"
                className="text-gray-600 dark:text-gray-400"
              />
              <YAxis className="text-gray-600 dark:text-gray-400" />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'var(--tw-color-gray-800)',
                  border: '1px solid var(--tw-color-gray-700)',
                  borderRadius: '0.5rem',
                }}
              />
              <Bar dataKey="cost" fill="#0ea5e9" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
      </Card>
    </div>
  )
}

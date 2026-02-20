import { ReactNode } from 'react'
import { LucideIcon } from 'lucide-react'
import { cn } from '../../utils/cn'

interface StatCardProps {
  title: string
  value: string | number
  icon: LucideIcon
  color?: string
  bgColor?: string
  trend?: {
    value: number
    label: string
    isPositive: boolean
  }
  loading?: boolean
}

export default function StatCard({
  title,
  value,
  icon: Icon,
  color = 'text-primary-600',
  bgColor = 'bg-primary-50',
  trend,
  loading = false,
}: StatCardProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm text-gray-600 dark:text-gray-400">{title}</p>
          {loading ? (
            <div className="h-8 w-24 bg-gray-200 dark:bg-gray-700 rounded animate-pulse mt-2" />
          ) : (
            <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2">
              {value}
            </p>
          )}
          {trend && !loading && (
            <p
              className={cn(
                'text-xs mt-1',
                trend.isPositive
                  ? 'text-green-600 dark:text-green-400'
                  : 'text-red-600 dark:text-red-400'
              )}
            >
              {trend.isPositive ? '↑' : '↓'} {trend.value} {trend.label}
            </p>
          )}
        </div>
        <div className={cn(bgColor, color, 'p-3 rounded-lg')}>
          <Icon className="h-6 w-6" />
        </div>
      </div>
    </div>
  )
}

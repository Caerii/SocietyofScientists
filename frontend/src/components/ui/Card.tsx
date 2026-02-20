import { ReactNode } from 'react'
import { cn } from '../../utils/cn'

interface CardProps {
  children: ReactNode
  className?: string
  title?: string
  icon?: React.ComponentType<{ className?: string }>
}

export default function Card({ children, className, title, icon: Icon }: CardProps) {
  return (
    <div className={cn('bg-white dark:bg-gray-800 rounded-lg shadow p-6', className)}>
      {(title || Icon) && (
        <div className="flex items-center space-x-2 mb-4">
          {Icon && <Icon className="h-5 w-5 text-gray-600 dark:text-gray-400" />}
          {title && (
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              {title}
            </h3>
          )}
        </div>
      )}
      {children}
    </div>
  )
}

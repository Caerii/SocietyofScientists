import { ReactNode, CSSProperties } from 'react'
import { cn } from '../../utils/cn'

interface CardProps {
  children: ReactNode
  className?: string
  title?: string
  subtitle?: string
  icon?: React.ComponentType<{ className?: string }>
  action?: ReactNode
  variant?: 'default' | 'gradient' | 'bordered'
  style?: CSSProperties
}

export default function Card({
  children,
  className,
  title,
  subtitle,
  icon: Icon,
  action,
  variant = 'default',
  style,
}: CardProps) {
  return (
    <div
      className={cn(
        'card',
        'animation',
        {
          'bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-900':
            variant === 'gradient',
          'border-2 border-blue-200 dark:border-blue-800': variant === 'bordered',
        },
        className
      )}
      style={style}
    >
      {(title || Icon || action || subtitle) && (
        <div className="card-header">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              {Icon && (
                <div className="flex-shrink-0">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-100 dark:bg-blue-900/30">
                    <Icon className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                  </div>
                </div>
              )}
              <div>
                {title && (
                  <h3 className="text-base font-semibold text-neutral-900 dark:text-white">
                    {title}
                  </h3>
                )}
                {subtitle && (
                  <p className="text-sm text-neutral-500 dark:text-neutral-400 mt-0.5">
                    {subtitle}
                  </p>
                )}
              </div>
            </div>
            {action && <div className="flex-shrink-0 ml-4">{action}</div>}
          </div>
        </div>
      )}
      <div className="card-body">{children}</div>
    </div>
  )
}
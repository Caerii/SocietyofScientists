import { CheckCircle2, AlertTriangle, XCircle, TrendingUp } from 'lucide-react'
import { cn } from '../../utils/cn'

interface ScoreDisplayProps {
  score: number
  maxScore: number
  label: string
  size?: 'sm' | 'md' | 'lg'
}

export function ScoreDisplay({ score, maxScore, label, size = 'md' }: ScoreDisplayProps) {
  const percentage = (score / maxScore) * 100
  const isGood = percentage >= 80
  const isWarning = percentage >= 60 && percentage < 80
  const isPoor = percentage < 60

  const sizeClasses = {
    sm: 'text-2xl',
    md: 'text-4xl',
    lg: 'text-5xl',
  }

  const circleSize = {
    sm: 80,
    md: 120,
    lg: 160,
  }

  const radius = circleSize[size] / 2 - 8
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - (percentage / 100) * circumference

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: circleSize[size], height: circleSize[size] }}>
        <svg className="transform -rotate-90">
          <circle
            cx={circleSize[size] / 2}
            cy={circleSize[size] / 2}
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-neutral-200 dark:text-neutral-700"
          />
          <circle
            cx={circleSize[size] / 2}
            cy={circleSize[size] / 2}
            r={radius}
            fill="none"
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            className={cn(
              'transition-all duration-1000 ease-out',
              {
                'text-green-500': isGood,
                'text-yellow-500': isWarning,
                'text-red-500': isPoor,
              }
            )}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={cn('font-bold text-neutral-900 dark:text-white', sizeClasses[size])}>
            {score.toFixed(1)}
          </span>
          <span className="text-xs text-neutral-500 dark:text-neutral-400">/{maxScore}</span>
        </div>
      </div>
      <span className="text-xs font-semibold text-neutral-600 dark:text-neutral-400 uppercase tracking-wide">
        {label}
      </span>
    </div>
  )
}

interface ComplianceStatusProps {
  compliant: boolean
  score: number
  issues: number
  warnings: number
}

export function ComplianceStatus({ compliant, score, issues, warnings }: ComplianceStatusProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        {compliant ? (
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30">
            <CheckCircle2 className="h-6 w-6 text-green-600 dark:text-green-400" />
          </div>
        ) : (
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/30">
            <XCircle className="h-6 w-6 text-red-600 dark:text-red-400" />
          </div>
        )}
        <div>
          <h3 className="text-base font-semibold text-neutral-900 dark:text-white">
            {compliant ? 'Compliant' : 'Not Compliant'}
          </h3>
          <p className="text-sm text-neutral-500 dark:text-neutral-400">
            {compliant ? 'All requirements met' : 'Issues need attention'}
          </p>
        </div>
      </div>

      <div
        className={cn(
          'flex items-center justify-between px-4 py-3 rounded-lg border-2',
          compliant
            ? 'bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-800'
            : 'bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800'
        )}
      >
        <div className="flex items-center gap-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-neutral-900 dark:text-white">
              {score.toFixed(1)}
            </div>
            <div className="text-xs text-neutral-500 dark:text-neutral-400">Score</div>
          </div>
          <div className="h-8 w-px bg-neutral-200 dark:bg-neutral-700" />
          <div className="text-center">
            <div className="text-2xl font-bold text-red-600 dark:text-red-400">
              {issues}
            </div>
            <div className="text-xs text-neutral-500 dark:text-neutral-400">Errors</div>
          </div>
          <div className="h-8 w-px bg-neutral-200 dark:bg-neutral-700" />
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-600 dark:text-yellow-400">
              {warnings}
            </div>
            <div className="text-xs text-neutral-500 dark:text-neutral-400">Warnings</div>
          </div>
        </div>
      </div>
    </div>
  )
}

interface CriteriaScoreProps {
  criterion: string
  score: number
  strengths: string[]
  weaknesses: string[]
}

export function CriteriaScore({
  criterion,
  score,
  strengths,
  weaknesses,
}: CriteriaScoreProps) {
  const isGood = score >= 8
  const isWarning = score >= 6 && score < 8
  const isPoor = score < 6

  return (
    <div className="space-y-3 rounded-lg bg-neutral-50 dark:bg-neutral-900 p-4 border border-neutral-200 dark:border-neutral-700">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-neutral-900 dark:text-white capitalize">
          {criterion.replace(/_/g, ' ')}
        </h4>
        <div
          className={cn(
            'flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold',
            {
              'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300':
                isGood,
              'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300':
                isWarning,
              'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300': isPoor,
            }
          )}
        >
          <TrendingUp className="h-3 w-3" />
          {score.toFixed(1)}/10
        </div>
      </div>

      <div className="h-1.5 w-full rounded-full bg-neutral-200 dark:bg-neutral-700">
        <div
          className={cn(
            'h-full rounded-full transition-all duration-500',
            {
              'bg-green-500': isGood,
              'bg-yellow-500': isWarning,
              'bg-red-500': isPoor,
            }
          )}
          style={{ width: `${score * 10}%` }}
        />
      </div>

      {(strengths.length > 0 || weaknesses.length > 0) && (
        <div className="space-y-2">
          {strengths.length > 0 && (
            <div className="flex items-start gap-2">
              <CheckCircle2 className="h-4 w-4 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
              <ul className="text-xs text-neutral-600 dark:text-neutral-400 space-y-0.5">
                {strengths.slice(0, 2).map((strength, idx) => (
                  <li key={idx}>{strength}</li>
                ))}
                {strengths.length > 2 && (
                  <li className="text-neutral-400">+{strengths.length - 2} more</li>
                )}
              </ul>
            </div>
          )}

          {weaknesses.length > 0 && (
            <div className="flex items-start gap-2">
              <AlertTriangle className="h-4 w-4 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
              <ul className="text-xs text-neutral-600 dark:text-neutral-400 space-y-0.5">
                {weaknesses.slice(0, 2).map((weakness, idx) => (
                  <li key={idx}>{weakness}</li>
                ))}
                {weaknesses.length > 2 && (
                  <li className="text-neutral-400">+{weaknesses.length - 2} more</li>
                )}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
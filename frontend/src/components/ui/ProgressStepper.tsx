import { Check } from 'lucide-react'
import { cn } from '../../utils/cn'

interface Step {
  id: string
  label: string
  description?: string
  status: 'pending' | 'active' | 'completed' | 'error'
}

interface ProgressStepperProps {
  steps: Step[]
  currentStep: number
}

export default function ProgressStepper({ steps, currentStep }: ProgressStepperProps) {
  return (
    <div className="w-full">
      <div className="relative flex items-center justify-between">
        <div
          className="absolute left-0 top-1/2 h-0.5 w-full -translate-y-1/2 bg-neutral-200 dark:bg-neutral-700"
          aria-hidden="true"
        />
        <div
          className="absolute left-0 top-1/2 h-0.5 -translate-y-1/2 bg-primary-600 transition-all duration-500"
          style={{ width: `${(currentStep / (steps.length - 1)) * 100}%` }}
          aria-hidden="true"
        />

        {steps.map((step, index) => {
          const isActive = index === currentStep
          const isCompleted = step.status === 'completed'
          const isError = step.status === 'error'

          return (
            <div
              key={step.id}
              className="relative flex flex-col items-center"
              style={{ flex: 1 }}
            >
              <div
                className={cn(
                  'relative flex h-10 w-10 items-center justify-center rounded-full border-2 transition-all duration-300',
                  {
                    'border-primary-600 bg-primary-600 text-white':
                      isActive || isCompleted,
                    'border-red-500 bg-red-500 text-white': isError,
                    'border-neutral-300 bg-white dark:border-neutral-600 dark:bg-neutral-800 dark:text-neutral-400':
                      step.status === 'pending',
                    'transform scale-110 shadow-lg': isActive,
                  }
                )}
              >
                {isCompleted ? (
                  <Check className="h-5 w-5" />
                ) : isError ? (
                  <span className="font-bold">!</span>
                ) : (
                  <span className="text-sm font-semibold">{index + 1}</span>
                )}
              </div>

              <div className="absolute top-14 flex w-32 flex-col items-center">
                <span
                  className={cn(
                    'text-xs font-semibold text-center',
                    {
                      'text-primary-600 dark:text-primary-400': isActive || isCompleted,
                      'text-red-600 dark:text-red-400': isError,
                      'text-neutral-500 dark:text-neutral-500': step.status === 'pending',
                    }
                  )}
                >
                  {step.label}
                </span>
                {step.description && (
                  <span className="text-[10px] text-neutral-500 dark:text-neutral-400 mt-0.5 text-center">
                    {step.description}
                  </span>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
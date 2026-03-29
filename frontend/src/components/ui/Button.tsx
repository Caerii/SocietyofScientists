import { forwardRef, ButtonHTMLAttributes, ReactNode } from 'react'
import { cn } from '../../utils/cn'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
  leftIcon?: ReactNode
  rightIcon?: ReactNode
  fullWidth?: boolean
  children: ReactNode
}

const variantStyles = {
  primary: 'btn-primary',
  secondary: 'btn-secondary',
  outline: 'btn-secondary',
  ghost: 'btn-ghost',
  danger: 'bg-red-600 hover:bg-red-700 text-white',
}

const sizeStyles = {
  sm: 'px-3 py-1.5 text-xs font-medium',
  md: 'px-4 py-2 text-sm font-medium',
  lg: 'px-6 py-3 text-base font-medium',
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      isLoading = false,
      leftIcon,
      rightIcon,
      fullWidth = false,
      className,
      disabled,
      children,
      ...props
    },
    ref
  ) => {
    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(
          'btn',
          'group',
          'relative',
          'overflow-hidden',
          {
            [variantStyles[variant]]: variant,
            [sizeStyles[size]]: size,
            'w-full': fullWidth,
          },
          disabled && 'cursor-not-allowed opacity-50',
          className
        )}
        {...props}
      >
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-white/20">
            <svg
              className="animate-spin h-4 w-4"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
          </div>
        )}
        <span className={cn('flex items-center gap-2', isLoading && 'opacity-0')}>
          {leftIcon && <span className="flex-shrink-0">{leftIcon}</span>}
          <span className="truncate">{children}</span>
          {rightIcon && <span className="flex-shrink-0">{rightIcon}</span>}
        </span>
      </button>
    )
  }
)

Button.displayName = 'Button'

export default Button

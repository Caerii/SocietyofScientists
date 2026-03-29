import { Brain, Flame, Award } from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'
import { cn } from '../utils/cn'

export default function Header() {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard', icon: Brain },
    { path: '/proposal', label: 'Create Proposal', icon: Flame },
    { path: '/history', label: 'History', icon: Award },
  ]

  return (
    <header className="glass sticky top-0 z-50 border-b border-neutral-200 dark:border-neutral-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-3 group">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 shadow-lg group-hover:shadow-xl transition-all duration-300">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-neutral-900 dark:text-white tracking-tight">
                Society of Scientists
              </h1>
              <p className="text-xs text-neutral-500 dark:text-neutral-400">
                AI-Powered Grant Proposal System
              </p>
            </div>
          </Link>

          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={cn(
                    'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200',
                    isActive
                      ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'
                      : 'text-neutral-600 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-700 hover:text-neutral-900 dark:hover:text-white'
                  )}
                >
                  <Icon className="h-4 w-4" />
                  {item.label}
                </Link>
              )
            })}
          </nav>

          <div className="flex items-center gap-4">
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-100 dark:bg-green-900/30 border border-green-200 dark:border-green-800">
              <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-xs font-medium text-green-700 dark:text-green-300">
                System Online
              </span>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}
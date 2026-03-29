import { Link } from 'react-router-dom'
import {
  Flame,
  FileText,
  TrendingUp,
  DollarSign,
  Zap,
  BarChart3,
  Clock,
  CheckCircle2,
  ArrowRight,
} from 'lucide-react'
import { useCostStore } from '../stores/costStore'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'

interface QuickAction {
  title: string
  description: string
  icon: React.ComponentType<{ className?: string }>
  to: string
  gradient: string
}

export default function Dashboard() {
  const { totalCost } = useCostStore()

  const stats = [
    {
      title: 'Total Proposals',
      value: '0',
      change: '+0 this month',
      icon: FileText,
      color: 'from-blue-500 to-blue-600',
      bgColor: 'bg-blue-100 dark:bg-blue-900/30',
    },
    {
      title: 'Active Sessions',
      value: '0',
      change: 'Real-time',
      icon: Zap,
      color: 'from-green-500 to-green-600',
      bgColor: 'bg-green-100 dark:bg-green-900/30',
    },
    {
      title: 'Total Cost',
      value: `$${totalCost.toFixed(4)}`,
      change: 'All time',
      icon: DollarSign,
      color: 'from-purple-500 to-purple-600',
      bgColor: 'bg-purple-100 dark:bg-purple-900/30',
    },
    {
      title: 'Success Rate',
      value: '100%',
      change: 'Compliance',
      icon: CheckCircle2,
      color: 'from-emerald-500 to-emerald-600',
      bgColor: 'bg-emerald-100 dark:bg-emerald-900/30',
    },
  ]

  const quickActions: QuickAction[] = [
    {
      title: 'Create New Proposal',
      description: 'Start a new grant proposal with AI-powered multi-agent collaboration',
      icon: Flame,
      to: '/proposal',
      gradient: 'from-blue-500 to-indigo-600',
    },
    {
      title: 'View History',
      description: 'Browse past proposals and review generated content',
      icon: Clock,
      to: '/history',
      gradient: 'from-green-500 to-emerald-600',
    },
    {
      title: 'View Analytics',
      description: 'Monitor costs, agent performance, and system metrics',
      icon: BarChart3,
      to: '/analytics',
      gradient: 'from-purple-500 to-pink-600',
    },
  ]

  const features = [
    {
      icon: CheckCircle2,
      title: 'Compliance Guaranteed',
      description:
        'All proposals validated against NIH, NSF, and DOE requirements',
    },
    {
      icon: Zap,
      title: 'Lightning Fast',
      description: 'Generate complete proposals in minutes, not days',
    },
    {
      icon: TrendingUp,
      title: 'Quality Assured',
      description: 'Built-in quality assessment based on agency review criteria',
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-neutral-50 via-white to-neutral-50 dark:from-neutral-900 dark:via-neutral-800 dark:to-neutral-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="mb-10 animate-fadeIn">
          <div className="flex items-start justify-between gap-8">
            <div className="flex-1 max-w-2xl">
              <h1 className="text-4xl font-bold text-neutral-900 dark:text-white mb-3 tracking-tight">
                Welcome back, Scientist
              </h1>
              <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-6 leading-relaxed">
                Your AI-powered research assistant is ready. Create grant proposals
                validated by compliance and quality assessments in minutes.
              </p>
              <Link to="/proposal">
                <Button size="lg" className="shadow-lg shadow-blue-500/25">
                  <Flame className="h-5 w-5 mr-2" />
                  Create Your First Proposal
                  <ArrowRight className="h-5 w-5 ml-2" />
                </Button>
              </Link>
            </div>

            {/* Stats */}
            <div className="flex-shrink-0 hidden lg:block">
              <div className="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl p-6 text-white shadow-xl">
                <div className="flex items-center gap-3 mb-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-white/20 backdrop-blur-sm">
                    <FileText className="h-6 w-6" />
                  </div>
                  <div>
                    <p className="text-sm text-white/80">AI-Proposals</p>
                    <p className="text-2xl font-bold">Ready</p>
                  </div>
                </div>
                <p className="text-sm text-white/80">
                  Create professional grant proposals with our multi-agent system
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          {stats.map((stat, idx) => {
            const Icon = stat.icon
            return (
              <div
                key={idx}
                className="group animate-fadeIn"
                style={{ animationDelay: `${idx * 100}ms` }}
              >
                <div className="relative overflow-hidden rounded-xl bg-white dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700 shadow-sm hover:shadow-md transition-all duration-300">
                  <div className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div
                        className={cn(
                          'flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br',
                          stat.color,
                          'text-white shadow-lg'
                        )}
                      >
                        <Icon className="h-6 w-6" />
                      </div>
                      <span className="text-xs font-medium text-neutral-500 dark:text-neutral-400">
                        {stat.change}
                      </span>
                    </div>
                    <p className="text-sm font-medium text-neutral-600 dark:text-neutral-400 mb-1">
                      {stat.title}
                    </p>
                    <p className="text-3xl font-bold text-neutral-900 dark:text-white">
                      {stat.value}
                    </p>
                  </div>
                  <div
                    className={cn('absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r', stat.color)}
                  />
                </div>
              </div>
            )
          })}
        </div>

        {/* Quick Actions */}
        <div className="mb-10">
          <h2 className="text-xl font-bold text-neutral-900 dark:text-white mb-4">
            Quick Actions
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {quickActions.map((action, idx) => {
              const Icon = action.icon
              return (
                <Link
                  key={idx}
                  to={action.to}
                  className="group animate-slideIn"
                  style={{ animationDelay: `${idx * 100 + 200}ms` }}
                >
                  <div className="relative overflow-hidden rounded-xl bg-white dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700 shadow-sm hover:shadow-lg transition-all duration-300 group-hover:-translate-y-1">
                    <div className="absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-5 transition-opacity duration-300 from-blue-500 to-indigo-600" />
                    <div className="relative p-6">
                      <div
                        className={cn(
                          'flex h-14 w-14 items-center justify-center rounded-xl bg-gradient-to-br',
                          action.gradient,
                          'text-white shadow-lg mb-4 group-hover:scale-110 transition-transform duration-300'
                        )}
                      >
                        <Icon className="h-7 w-7" />
                      </div>
                      <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-2">
                        {action.title}
                      </h3>
                      <p className="text-sm text-neutral-600 dark:text-neutral-400 leading-relaxed">
                        {action.description}
                      </p>
                      <div className="mt-4 flex items-center text-sm font-medium text-blue-600 dark:text-blue-400 group-hover:text-blue-700 dark:group-hover:text-blue-300 transition-colors">
                        Get started
                        <ArrowRight className="h-4 w-4 ml-2 group-hover:translate-x-1 transition-transform" />
                      </div>
                    </div>
                  </div>
                </Link>
              )
            })}
          </div>
        </div>

        {/* Features */}
        <Card
          title="Why Choose Society of Scientists?"
          subtitle="AI-powered multi-agent proposal generation"
          variant="gradient"
          className="animate-scaleIn"
          style={{ animationDelay: '400ms' }}
        >
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, idx) => {
              const Icon = feature.icon
              return (
                <div
                  key={idx}
                  className="flex items-start gap-4 p-4 rounded-xl bg-white/50 dark:bg-neutral-800/50"
                >
                  <div className="flex-shrink-0">
                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100 dark:bg-blue-900/30">
                      <Icon className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                    </div>
                  </div>
                  <div>
                    <h3 className="text-base font-semibold text-neutral-900 dark:text-white mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-sm text-neutral-600 dark:text-neutral-400 leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                </div>
              )
            })}
          </div>
        </Card>
      </div>
    </div>
  )
}

function cn(...classes: (string | boolean | undefined | null)[]) {
  return classes.filter(Boolean).join(' ')
}
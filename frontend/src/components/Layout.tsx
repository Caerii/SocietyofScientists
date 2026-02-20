import { ReactNode } from 'react'
import Header from './Header'
import Sidebar from './Sidebar'
import { useUIStore } from '../stores/uiStore'
import { cn } from '../utils/cn'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const { sidebarCollapsed } = useUIStore()

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header />
      <div className="flex">
        <Sidebar />
        <main 
          className={cn(
            'flex-1 p-6 transition-all duration-300 ease-in-out',
            sidebarCollapsed ? 'ml-0' : ''
          )}
        >
          {children}
        </main>
      </div>
    </div>
  )
}

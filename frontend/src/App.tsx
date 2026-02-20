import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import ErrorBoundary from './components/ErrorBoundary'
import ToastContainer from './components/ui/ToastContainer'
import { useToastStore } from './stores/toastStore'
import Dashboard from './pages/Dashboard'
import ProposalBuilder from './pages/ProposalBuilder'
import ConversationHistory from './pages/ConversationHistory'
import CostAnalytics from './pages/CostAnalytics'
import Settings from './pages/Settings'

function App() {
  const { toasts, removeToast } = useToastStore()

  return (
    <ErrorBoundary>
      <Router
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/proposal" element={<ProposalBuilder />} />
            <Route path="/history" element={<ConversationHistory />} />
            <Route path="/analytics" element={<CostAnalytics />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Layout>
        <ToastContainer toasts={toasts} onRemove={removeToast} />
      </Router>
    </ErrorBoundary>
  )
}

export default App

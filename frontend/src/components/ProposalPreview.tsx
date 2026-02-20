import { FileText } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import Card from './ui/Card'

interface ProposalPreviewProps {
  proposal: string
}

export default function ProposalPreview({ proposal }: ProposalPreviewProps) {
  return (
    <Card title="Proposal Preview" icon={FileText}>
      <div className="prose prose-sm dark:prose-invert max-w-none max-h-96 overflow-y-auto">
        {proposal ? (
          <ReactMarkdown>{proposal}</ReactMarkdown>
        ) : (
          <p className="text-gray-500 dark:text-gray-400">
            Proposal will appear here as agents generate it...
          </p>
        )}
      </div>
    </Card>
  )
}

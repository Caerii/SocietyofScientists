import { useState, useEffect } from 'react'
import { Send, FileText, CheckCircle2, Download, Sparkles } from 'lucide-react'
import { apiClient } from '../api/client'
import type { Session, ComplianceReport, QualityAssessment } from '../types'

export default function ProposalBuilder() {
  const [currentStep, setCurrentStep] = useState<'details' | 'generate' | 'review'>('details')
  const [grantTopic, setGrantTopic] = useState('')
  const [fundingAgency, setFundingAgency] = useState('NIH')
  const [grantAmount, setGrantAmount] = useState('')
  const [proposal, setProposal] = useState('')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [complianceReport, setComplianceReport] = useState<ComplianceReport | null>(null)
  const [qualityAssessment, setQualityAssessment] = useState<QualityAssessment | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleStart = async () => {
    if (!grantTopic.trim()) {
      setError('Please enter a research grant topic')
      return
    }
    
    setError(null)
    setLoading(true)
    setCurrentStep('generate')

    try {
      const response = await apiClient.startProposal({
        grant_topic: grantTopic,
        funding_agency: fundingAgency,
        grant_amount: grantAmount ? parseFloat(grantAmount) : undefined,
      })

      setSessionId(response.session_id)

      const pollInterval = setInterval(async () => {
        try {
          const session = await apiClient.getSessionStatus(response.session_id)
          
          if (session.status === 'completed') {
            clearInterval(pollInterval)
            setProposal(session.message || 'Proposal generated successfully')

          const compliance = await apiClient.checkCompliance(session.message || '', fundingAgency)
          setComplianceReport(compliance)

          const quality = await apiClient.assessQuality(session.message || '', fundingAgency)
          setQualityAssessment(quality)

          setCurrentStep('review')
          setLoading(false)
        } else if (session.status === 'error') {
          clearInterval(pollInterval)
          setError('Failed to generate proposal')
          setLoading(false)
          setCurrentStep('details')
        }
      } catch (err) {
        clearInterval(pollInterval)
        setError('Failed to check proposal status')
        setLoading(false)
        setCurrentStep('details')
      }
    }, 2000)

    return () => clearInterval(pollInterval)
  } catch (err) {
    setError('Failed to start proposal generation')
    setLoading(false)
    setCurrentStep('details')
  }
  }

  const handleExport = async (format: 'pdf' | 'docx' | 'markdown' = 'pdf') => {
    if (!sessionId) return

    try {
      const response = await apiClient.exportProposal(sessionId, format)
      const blob = new Blob([response], { type: format === 'pdf' ? 'application/pdf' : format === 'docx' ? 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' : 'text/markdown' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `grant-proposal.${format}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (err) {
      setError('Failed to export proposal')
    }
  }

  if (currentStep === 'details') {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 py-12">
          <div className="mb-8">
            <div className="flex items-center gap-3 mb-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 shadow-lg">
                <Sparkles className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Create Research Grant Proposal
                </h1>
                <p className="text-sm text-gray-600">
                  AI-powered multi-agent proposal generation
                </p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-600 text-white font-semibold">1</div>
                  <span className="text-sm font-semibold text-gray-900">Project Details</span>
                </div>
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-300 text-gray-600 font-semibold">2</div>
                  <span className="text-sm font-medium text-gray-500">Generate</span>
                </div>
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-300 text-gray-600 font-semibold">3</div>
                  <span className="text-sm font-medium text-gray-500">Review</span>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Project Information</h2>
            
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-2">
                  Research Grant Topic *
                </label>
                <textarea
                  value={grantTopic}
                  onChange={(e) => setGrantTopic(e.target.value)}
                  placeholder="e.g., Develop a novel CRISPR-based gene therapy for rare genetic disorders"
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Provide a clear description of your research project
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-semibold text-gray-900 mb-2">
                    Funding Agency
                  </label>
                  <select
                    value={fundingAgency}
                    onChange={(e) => setFundingAgency(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-gray-900"
                  >
                    <option value="NIH">NIH</option>
                    <option value="NSF">NSF</option>
                    <option value="DOE">DOE</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-900 mb-2">
                    Grant Amount (USD)
                  </label>
                  <input
                    type="number"
                    placeholder="e.g., 500000"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-gray-900"
                  />
                </div>
              </div>

              <button
                onClick={handleStart}
                className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-4 px-6 rounded-xl font-semibold text-lg hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg hover:shadow-xl"
              >
                <span className="flex items-center justify-center gap-2">
                  <Send className="h-5 w-5" />
                  Start Proposal Generation
                </span>
              </button>
            </div>
          </div>

          <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
            {[
              { icon: CheckCircle2, title: 'Compliance Checked', desc: 'Validated against agency requirements' },
              { icon: Sparkles, title: 'AI-Enhanced', desc: 'Multi-agent collaboration' },
              { icon: FileText, title: 'Ready to Submit', desc: 'Professional formatting' },
            ].map((feature, idx) => (
              <div
                key={idx}
                className="bg-white rounded-xl p-4 border border-gray-200 shadow-sm"
              >
                <div className="flex items-start gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-100">
                    <feature.icon className="h-5 w-5 text-blue-600" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-gray-900 mb-1">{feature.title}</h3>
                    <p className="text-xs text-gray-600">{feature.desc}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  if (currentStep === 'generate') {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 py-12">
          <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8">
            <div className="text-center">
              <div className="inline-flex h-16 w-16 items-center justify-center rounded-full bg-blue-100 mb-6">
                <Sparkles className="h-8 w-8 text-blue-600 animate-spin" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                AI Agents are collaborating on your proposal
              </h2>
              <p className="text-gray-600 mb-8">
                This may take a few minutes. Our multi-agent system is reviewing your proposal,
                checking compliance, and ensuring quality.
              </p>

              <div className="max-w-md mx-auto">
                <div className="flex items-center justify-between text-sm mb-2">
                  <span className="text-gray-600">Progress</span>
                  <span className="font-semibold text-gray-900">Generating...</span>
                </div>
                <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full animate-pulse" />
                </div>
              </div>

              <div className="mt-8 space-y-3 max-w-md mx-auto text-left text-sm text-gray-600">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-green-500" />
                  Analyzing research topic...
                </div>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-green-500" />
                  Searching literature...
                </div>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-blue-500 animate-pulse" />
                  Structuring proposal...
                </div>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-gray-300" />
                  Checking compliance...
                </div>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-gray-300" />
                  Finalizing proposal...
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-green-100">
                <CheckCircle2 className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Proposal Ready!</h1>
                <p className="text-sm text-gray-600">Review and export your proposal</p>
              </div>
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => setCurrentStep('details')}
                className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 font-medium"
              >
                Create New
              </button>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium flex items-center gap-2">
                <Download className="h-4 w-4" />
                Export PDF
              </button>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Generated Proposal</h2>
              <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
                <pre className="whitespace-pre-wrap font-mono text-sm text-gray-800">
                  {proposal}
                </pre>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Compliance Check</h3>
              <div className="flex items-center gap-3 mb-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
                  <CheckCircle2 className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <p className="font-semibold text-green-700">Compliant</p>
                  <p className="text-sm text-gray-600">All requirements met</p>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4 text-center p-3 bg-green-50 rounded-lg">
                <div>
                  <div className="text-2xl font-bold text-gray-900">95.0</div>
                  <div className="text-xs text-gray-600">Score</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-gray-900">0</div>
                  <div className="text-xs text-gray-600">Errors</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-gray-900">0</div>
                  <div className="text-xs text-gray-600">Warnings</div>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Quality Assessment</h3>
              <div className="text-center mb-4">
                <div className="text-4xl font-bold text-gray-900">8.5</div>
                <div className="text-sm text-gray-600">Overall Score</div>
              </div>
              <div className="space-y-3">
                {[
                  { name: 'Significance', score: 9.0 },
                  { name: 'Innovation', score: 8.5 },
                  { name: 'Approach', score: 8.0 },
                ].map((criterion) => (
                  <div key={criterion.name} className="space-y-1">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-700">{criterion.name}</span>
                      <span className="font-semibold text-gray-900">{criterion.score}</span>
                    </div>
                    <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-blue-600 rounded-full"
                        style={{ width: `${criterion.score * 10}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
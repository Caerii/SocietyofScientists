import { Link } from 'react-router-dom';
import { Sparkles, Brain, FileText, Zap, ArrowRight } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="animate-in">
      {/* Hero Section */}
      <div className="text-center py-16">
        <div className="inline-flex items-center gap-2 bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-medium mb-6">
          <Sparkles className="w-4 h-4" />
          AI-Powered Grant Writing
        </div>
        
        <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
          Generate Winning Grants<br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
            In Minutes, Not Days
          </span>
        </h1>
        
        <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
          Society of Scientists uses advanced AI to help researchers create
          competitive grant proposals for NIH, NSF, DOE, and more.
        </p>

        <div className="flex gap-4 justify-center">
          <Link
            to="/proposal/new"
            className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl"
          >
            Start Free Proposal
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link
            to="/dashboard"
            className="inline-flex items-center gap-2 bg-white text-gray-900 px-8 py-4 rounded-lg font-medium border border-gray-200 hover:bg-gray-50 transition-all"
          >
            View Dashboard
          </Link>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid md:grid-cols-3 gap-8 mt-20">
        <FeatureCard
          icon={<Brain className="w-8 h-8 text-blue-600" />}
          title="AI Agent System"
          description="Multiple specialized AI agents collaborate to write, review, and refine your proposal."
        />
        <FeatureCard
          icon={<FileText className="w-8 h-8 text-purple-600" />}
          title="Agency Templates"
          description="Pre-built templates for NIH R01, NSF CAREER, DOE, and other major funding agencies."
        />
        <FeatureCard
          icon={<Zap className="w-8 h-8 text-yellow-600" />}
          title="Lightning Fast"
          description="Generate complete proposals in 15 minutes instead of 2-4 weeks of manual work."
        />
      </div>

      {/* Stats */}
      <div className="mt-20 bg-white rounded-2xl p-12 shadow-lg">
        <div className="grid md:grid-cols-4 gap-8 text-center">
          <div>
            <div className="text-4xl font-bold text-gray-900 mb-2">15 min</div>
            <div className="text-gray-600">Average Generation Time</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-gray-900 mb-2">$1.00</div>
            <div className="text-gray-600">AI Cost per Proposal</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-gray-900 mb-2">10+</div>
            <div className="text-gray-600">Agency Templates</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-gray-900 mb-2">92%</div>
            <div className="text-gray-600">User Satisfaction</div>
          </div>
        </div>
      </div>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}
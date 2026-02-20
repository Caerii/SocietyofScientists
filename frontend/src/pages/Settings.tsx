import { useState } from 'react'
import { Settings as SettingsIcon, Key, Save, Info } from 'lucide-react'
import Card from '../components/ui/Card'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'
import { useToastStore } from '../stores/toastStore'

export default function Settings() {
  const [apiKeys, setApiKeys] = useState({
    ai21: '',
    exa: '',
  })
  const { success, info } = useToastStore()

  const handleSave = () => {
    // API keys should be configured server-side via .env file
    info('API keys are configured server-side via .env file for security')
    success('Settings saved (note: API keys managed server-side)')
  }

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <h2 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center space-x-2">
        <SettingsIcon className="h-8 w-8" />
        <span>Settings</span>
      </h2>

      <Card
        title="API Configuration"
        icon={Key}
      >
        <div className="space-y-4">
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 flex items-start space-x-3">
            <Info className="h-5 w-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm font-medium text-blue-900 dark:text-blue-200">
                API Keys Configuration
              </p>
              <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">
                API keys are configured server-side via the <code className="bg-blue-100 dark:bg-blue-900/50 px-1 rounded">.env</code> file for security.
                Edit the <code className="bg-blue-100 dark:bg-blue-900/50 px-1 rounded">.env</code> file in the project root to update keys.
              </p>
            </div>
          </div>

          <div>
            <Input
              label="AI21 API Key"
              type="password"
              value={apiKeys.ai21}
              onChange={(e) => setApiKeys({ ...apiKeys, ai21: e.target.value })}
              placeholder="Configured in .env file"
              disabled
            />
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
              Set via <code className="bg-gray-100 dark:bg-gray-700 px-1 rounded">AI21_API_KEY</code> in .env
            </p>
          </div>
          <div>
            <Input
              label="Exa API Key"
              type="password"
              value={apiKeys.exa}
              onChange={(e) => setApiKeys({ ...apiKeys, exa: e.target.value })}
              placeholder="Configured in .env file"
              disabled
            />
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
              Set via <code className="bg-gray-100 dark:bg-gray-700 px-1 rounded">EXA_API_KEY</code> in .env
            </p>
          </div>
          <Button onClick={handleSave}>
            <Save className="h-5 w-5 mr-2" />
            Save Settings
          </Button>
        </div>
      </Card>
    </div>
  )
}

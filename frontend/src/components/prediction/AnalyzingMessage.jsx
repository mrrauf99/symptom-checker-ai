import Spinner from '../ui/Spinner.jsx'
import { Activity } from '../layout/icons.jsx'

export default function AnalyzingMessage() {
  return (
    <div className="flex items-end gap-3 animate-fade-in">
      <div className="w-8 h-8 rounded-full bg-mint-100 flex items-center justify-center flex-shrink-0">
        <Activity size={14} className="text-mint-600" />
      </div>
      
      <div className="bg-white border border-slate-100 rounded-2xl rounded-bl-sm px-4 py-3 shadow-card">
        <div className="flex items-center gap-2">
          <Spinner size={16} />
          <span className="text-sm font-body text-slate-600">Analyzing symptoms...</span>
        </div>
      </div>
    </div>
  )
}

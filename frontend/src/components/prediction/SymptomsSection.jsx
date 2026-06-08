import { Activity } from '../layout/icons.jsx'

export default function SymptomsSection({ symptoms }) {
  if (!symptoms || symptoms.length === 0) {
    return null
  }

  return (
    <div className="prediction-card animate-fade-in-scale" style={{ animationDelay: '50ms' }}>
      <div className="flex items-center gap-2 mb-4">
        <div className="w-10 h-10 rounded-xl bg-blue-100 flex items-center justify-center flex-shrink-0">
          <Activity size={18} className="text-blue-600" />
        </div>
        <h4 className="text-sm font-display font-semibold text-slate-800">Detected Symptoms</h4>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        {symptoms.map((symptom, idx) => (
          <div
            key={idx}
            className="flex items-center gap-2 p-2.5 rounded-lg bg-blue-50 hover:bg-blue-100 transition-colors"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-blue-500" />
            <span className="text-sm font-body text-slate-700 capitalize">{symptom}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

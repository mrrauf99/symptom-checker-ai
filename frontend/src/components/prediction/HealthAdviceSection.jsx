import { CheckCircle } from '../layout/icons.jsx'

export default function HealthAdviceSection({ advice }) {
  if (!advice || advice.length === 0) {
    return null
  }

  return (
    <div className="prediction-card animate-fade-in-scale" style={{ animationDelay: '150ms' }}>
      <div className="flex items-center gap-2 mb-4">
        <div className="w-10 h-10 rounded-xl bg-green-100 flex items-center justify-center flex-shrink-0">
          <span className="text-lg">💡</span>
        </div>
        <h4 className="text-sm font-display font-semibold text-slate-800">Health Advice</h4>
      </div>
      
      <div className="space-y-2.5">
        {advice.map((item, idx) => (
          <div key={idx} className="flex items-start gap-3">
            <CheckCircle size={18} className="text-green-600 mt-0.5 flex-shrink-0" />
            <span className="text-sm font-body text-slate-700">{item}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

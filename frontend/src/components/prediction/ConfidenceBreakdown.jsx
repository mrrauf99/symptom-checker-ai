import { TrendingUp } from '../layout/icons.jsx'

export default function ConfidenceBreakdown({ topPredictions }) {
  if (!topPredictions || topPredictions.length === 0) {
    return null
  }

  // Sort by confidence descending and take top 5
  const sorted = [...topPredictions].sort((a, b) => b.confidence - a.confidence).slice(0, 5)

  return (
    <div className="prediction-card animate-fade-in-scale" style={{ animationDelay: '200ms' }}>
      <div className="flex items-center gap-2 mb-4">
        <div className="w-10 h-10 rounded-xl bg-purple-100 flex items-center justify-center flex-shrink-0">
          <TrendingUp size={18} className="text-purple-600" />
        </div>
        <h4 className="text-sm font-display font-semibold text-slate-800">Confidence Breakdown</h4>
      </div>
      
      <div className="space-y-4">
        {sorted.map((pred, idx) => (
          <div key={idx}>
            <div className="flex items-baseline justify-between mb-1.5">
              <span className="text-sm font-body font-medium text-slate-700">{pred.disease}</span>
              <span className="text-xs font-mono font-bold text-purple-600">{pred.confidence?.toFixed(1)}%</span>
            </div>
            
            <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-purple-400 to-purple-600 rounded-full transition-all duration-700 ease-out"
                style={{
                  width: `${pred.confidence}%`,
                  animation: `slideIn 0.8s ease-out ${idx * 80}ms`
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

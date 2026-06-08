export default function ConditionDescription({ description }) {
  if (!description) {
    return null
  }

  return (
    <div className="prediction-card animate-fade-in-scale" style={{ animationDelay: '100ms' }}>
      <div className="flex items-center gap-2 mb-4">
        <div className="w-10 h-10 rounded-xl bg-amber-100 flex items-center justify-center flex-shrink-0">
          <span className="text-lg">📖</span>
        </div>
        <h4 className="text-sm font-display font-semibold text-slate-800">About This Condition</h4>
      </div>
      
      <p className="text-sm font-body text-slate-700 leading-relaxed">
        {description}
      </p>
    </div>
  )
}

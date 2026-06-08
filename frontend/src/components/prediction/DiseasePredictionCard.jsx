import { Stethoscope } from '../layout/icons.jsx'

export default function DiseasePredictionCard({ disease, specialist, confidence }) {
  return (
    <div className="prediction-card animate-fade-in-scale">
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-mint-400 to-mint-600 flex items-center justify-center flex-shrink-0 shadow-sm">
          <Stethoscope size={24} className="text-white" />
        </div>
        
        <div className="flex-1 min-w-0">
          <p className="text-xs font-display font-semibold text-slate-500 uppercase tracking-wide mb-1">
            Primary Prediction
          </p>
          <h3 className="text-3xl font-display font-bold text-slate-800 mb-3 break-words">
            {disease}
          </h3>
          
          <div className="flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-6">
            <div className="flex-1">
              <p className="text-xs font-body text-slate-500 mb-1">Confidence Score</p>
              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-display font-bold text-mint-600">
                  {confidence?.toFixed(1) || '0'}%
                </span>
              </div>
            </div>
            
            {specialist && (
              <div className="flex-1">
                <p className="text-xs font-body text-slate-500 mb-1">Recommended Specialist</p>
                <div className="inline-block">
                  <span className="px-3 py-1.5 rounded-full bg-mint-100 text-mint-700 text-sm font-display font-semibold">
                    {specialist}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

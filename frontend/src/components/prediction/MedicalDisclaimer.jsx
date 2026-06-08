import { AlertCircle } from '../layout/icons.jsx'

export default function MedicalDisclaimer() {
  return (
    <div className="prediction-card bg-gradient-to-br from-rose-50 to-rose-50 border-rose-200 animate-fade-in-scale" style={{ animationDelay: '250ms' }}>
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 mt-0.5">
          <AlertCircle size={20} className="text-rose-600" />
        </div>
        
        <div>
          <h4 className="text-sm font-display font-semibold text-rose-800 mb-1">⚠️ Medical Disclaimer</h4>
          <p className="text-xs font-body text-rose-700 leading-relaxed">
            This AI prediction is for informational purposes only and is <strong>not a medical diagnosis</strong>. 
            Symptoms can overlap between conditions and require professional medical evaluation. 
            Please consult a qualified healthcare professional for proper assessment, diagnosis, and treatment. 
            In case of emergency, seek immediate medical attention.
          </p>
        </div>
      </div>
    </div>
  )
}

import DiseasePredictionCard from './DiseasePredictionCard.jsx'
import SymptomsSection from './SymptomsSection.jsx'
import ConditionDescription from './ConditionDescription.jsx'
import HealthAdviceSection from './HealthAdviceSection.jsx'
import ConfidenceBreakdown from './ConfidenceBreakdown.jsx'
import MedicalDisclaimer from './MedicalDisclaimer.jsx'

export default function PredictionResponse({ data }) {
  if (!data) {
    return null
  }

  const primaryConfidence = data.top_predictions?.[0]?.confidence || 0

  return (
    <div className="space-y-3 animate-slide-up">
      <DiseasePredictionCard
        disease={data.prediction}
        specialist={data.specialist}
        confidence={primaryConfidence}
      />
      
      <SymptomsSection symptoms={data.symptoms} />
      
      <ConditionDescription description={data.description} />
      
      <HealthAdviceSection advice={data.advice} />
      
      <ConfidenceBreakdown topPredictions={data.top_predictions} />
      
      <MedicalDisclaimer />
    </div>
  )
}

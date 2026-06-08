import Spinner from './Spinner.jsx'

export default function FullPageLoader({ message = 'Loading MediSense AI...' }) {
  return (
    <div className="fixed inset-0 bg-slate-50 flex flex-col items-center justify-center z-50 gap-4">
      {/* Logo mark */}
      <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-mint-400 to-mint-600 flex items-center justify-center shadow-mint animate-pulse-soft">
        <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
          <path d="M14 4C8.477 4 4 8.477 4 14s4.477 10 10 10 10-4.477 10-10S19.523 4 14 4z" stroke="white" strokeWidth="1.5" />
          <path d="M14 8v6l4 2" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M9 14h2M17 14h2" stroke="white" strokeWidth="1.5" strokeLinecap="round" />
        </svg>
      </div>
      <Spinner size={28} />
      <p className="text-slate-400 font-body text-sm">{message}</p>
    </div>
  )
}

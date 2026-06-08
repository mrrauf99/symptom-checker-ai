import Spinner from './Spinner.jsx'

export default function Button({
  children,
  loading = false,
  variant = 'primary',
  size = 'md',
  className = '',
  ...props
}) {
  const base = variant === 'primary' ? 'btn-primary' : variant === 'secondary' ? 'btn-secondary' : 'btn-ghost'
  const sizeClass = size === 'sm' ? 'py-2 text-xs' : ''

  return (
    <button
      className={`${base} ${sizeClass} ${className}`}
      disabled={loading || props.disabled}
      {...props}
    >
      {loading ? (
        <>
          <Spinner size={16} color={variant === 'primary' ? 'white' : '#64748b'} />
          <span>Please wait...</span>
        </>
      ) : (
        children
      )}
    </button>
  )
}

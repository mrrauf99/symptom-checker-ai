import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext.jsx'
import AuthLayout from '../../components/layout/AuthLayout.jsx'
import Input from '../../components/ui/Input.jsx'
import Button from '../../components/ui/Button.jsx'
import { validateForm, validators } from '../../utils/validators.js'
import { getErrorMessage } from '../../utils/helpers.js'
import { Mail, Lock, Eye, EyeOff, UserIcon } from '../../components/layout/icons.jsx'
import toast from 'react-hot-toast'

export default function RegisterPage() {
  const { register, login } = useAuth()
  const navigate = useNavigate()

  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: null }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    const { errors: validationErrors, isValid } = validateForm(form, {
      name: [validators.name],
      email: [validators.email],
      password: [validators.password],
    })

    if (!isValid) {
      setErrors(validationErrors)
      return
    }

    setLoading(true)
    try {
      await register(form)
      toast.success('Account created! Signing you in...')
      await login({ email: form.email, password: form.password })
      navigate('/dashboard')
    } catch (err) {
      toast.error(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  const passwordStrength =
    form.password.length === 0 ? 0
    : form.password.length < 6 ? 1
    : form.password.length < 10 ? 2
    : 3

  const strengthLabel = ['', 'Weak', 'Fair', 'Strong']
  const strengthColor = ['', 'bg-coral-500', 'bg-amber-400', 'bg-mint-500']

  return (
    <AuthLayout
      title="Create your account"
      subtitle="Join MediSense AI — your personal health guide"
    >
      <form onSubmit={handleSubmit} className="flex flex-col gap-4" noValidate>
        <Input
          label="Full name"
          id="name"
          name="name"
          type="text"
          placeholder="Abdul Rauf"
          value={form.name}
          onChange={handleChange}
          error={errors.name}
          icon={UserIcon}
          autoComplete="name"
          autoFocus
        />

        <Input
          label="Email address"
          id="email"
          name="email"
          type="email"
          placeholder="you@example.com"
          value={form.email}
          onChange={handleChange}
          error={errors.email}
          icon={Mail}
          autoComplete="email"
        />

        <div className="flex flex-col gap-1.5">
          <Input
            label="Password"
            id="password"
            name="password"
            type={showPassword ? 'text' : 'password'}
            placeholder="Min. 6 characters"
            value={form.password}
            onChange={handleChange}
            error={errors.password}
            icon={Lock}
            autoComplete="new-password"
            rightElement={
              <button
                type="button"
                onClick={() => setShowPassword((v) => !v)}
                className="text-slate-400 hover:text-slate-600 transition-colors"
                tabIndex={-1}
              >
                {showPassword ? <Eye size={16} /> : <EyeOff size={16} />}
              </button>
            }
          />
          {/* Password strength */}
          {form.password.length > 0 && (
            <div className="flex items-center gap-1.5">
              {[1, 2, 3].map((level) => (
                <div
                  key={level}
                  className={`h-1 flex-1 rounded-full transition-all duration-300 ${
                    passwordStrength >= level ? strengthColor[passwordStrength] : 'bg-slate-200'
                  }`}
                />
              ))}
              <span className="text-xs text-slate-400 font-body w-10">
                {strengthLabel[passwordStrength]}
              </span>
            </div>
          )}
        </div>

        <div className="pt-1">
          <Button type="submit" loading={loading}>
            Create Free Account
          </Button>
        </div>

        <p className="text-center text-xs text-slate-400 font-body">
          By creating an account you agree to our{' '}
          <span className="text-mint-600 cursor-pointer hover:underline">Terms</span> and{' '}
          <span className="text-mint-600 cursor-pointer hover:underline">Privacy Policy</span>
        </p>

        <p className="text-center text-sm text-slate-500 font-body border-t border-slate-100 pt-4">
          Already have an account?{' '}
          <Link
            to="/login"
            className="text-mint-600 font-semibold hover:text-mint-700 transition-colors"
          >
            Sign in
          </Link>
        </p>
      </form>
    </AuthLayout>
  )
}

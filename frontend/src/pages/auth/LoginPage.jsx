import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext.jsx'
import AuthLayout from '../../components/layout/AuthLayout.jsx'
import Input from '../../components/ui/Input.jsx'
import Button from '../../components/ui/Button.jsx'
import { validateForm, validators } from '../../utils/validators.js'
import { getErrorMessage } from '../../utils/helpers.js'
import { Mail, Lock, Eye, EyeOff } from '../../components/layout/icons.jsx'
import toast from 'react-hot-toast'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()

  const [form, setForm] = useState({ email: '', password: '' })
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
      email: [validators.email],
      password: [validators.password],
    })

    if (!isValid) {
      setErrors(validationErrors)
      return
    }

    setLoading(true)
    try {
      await login(form)
      toast.success('Welcome back!')
      navigate('/dashboard')
    } catch (err) {
      toast.error(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout
      title="Welcome back"
      subtitle="Sign in to your MediSense AI account"
    >
      <form onSubmit={handleSubmit} className="flex flex-col gap-4" noValidate>
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
          autoFocus
        />

        <Input
          label="Password"
          id="password"
          name="password"
          type={showPassword ? 'text' : 'password'}
          placeholder="••••••••"
          value={form.password}
          onChange={handleChange}
          error={errors.password}
          icon={Lock}
          autoComplete="current-password"
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

        <div className="pt-1">
          <Button type="submit" loading={loading}>
            Sign In
          </Button>
        </div>

        <p className="text-center text-sm text-slate-500 font-body pt-1">
          Don't have an account?{' '}
          <Link
            to="/register"
            className="text-mint-600 font-semibold hover:text-mint-700 transition-colors"
          >
            Create one free
          </Link>
        </p>
      </form>
    </AuthLayout>
  )
}

import { useState, useEffect } from 'react'
import { profileAPI } from '../../api/profileAPI.js'
import { validateForm, validators } from '../../utils/validators.js'
import { getErrorMessage } from '../../utils/helpers.js'
import Input from '../../components/ui/Input.jsx'
import Button from '../../components/ui/Button.jsx'
import { UserIcon, Mail, Edit, CheckCircle } from '../../components/layout/icons.jsx'
import Spinner from '../../components/ui/Spinner.jsx'
import toast from 'react-hot-toast'

const GENDER_OPTIONS = ['Male', 'Female', 'Prefer not to say']

export default function ProfilePage() {
  const [profile, setProfile] = useState(null)
  const [form, setForm] = useState({ name: '', age: '', gender: '' })
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    const fetch = async () => {
      try {
        const data = await profileAPI.getProfile()
        setProfile(data)
        setForm({
          name: data.name || '',
          age: data.age ? String(data.age) : '',
          gender: data.gender || '',
        })
      } catch (err) {
        toast.error(getErrorMessage(err))
      } finally {
        setLoading(false)
      }
    }
    fetch()
  }, [])

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: null }))
    setSaved(false)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    const { errors: validationErrors, isValid } = validateForm(form, {
      name: [validators.name],
      age: [validators.age],
    })

    if (!isValid) {
      setErrors(validationErrors)
      return
    }

    setSaving(true)
    try {
      const payload = {
        name: form.name,
        age: form.age ? Number(form.age) : undefined,
        gender: form.gender || undefined,
      }
      const updated = await profileAPI.updateProfile(payload)
      setProfile(updated)
      setSaved(true)
      toast.success('Profile updated successfully')
    } catch (err) {
      toast.error(getErrorMessage(err))
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spinner />
      </div>
    )
  }

  return (
    <div className="p-6 max-w-2xl mx-auto animate-slide-up">
      {/* Header */}
      <div className="mb-8">
        <span className="badge-mint mb-2">Account</span>
        <h1 className="font-display font-bold text-2xl text-slate-800">Your Profile</h1>
        <p className="text-slate-500 font-body text-sm mt-1">
          Keep your information accurate for better health insights
        </p>
      </div>

      {/* Avatar section */}
      <div className="card mb-6 flex items-center gap-5">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-mint-400 to-mint-600 flex items-center justify-center text-white font-display font-bold text-2xl shadow-mint flex-shrink-0">
          {form.name?.[0]?.toUpperCase() || 'U'}
        </div>
        <div>
          <p className="font-display font-semibold text-slate-800 text-lg">{profile?.name}</p>
          <div className="flex items-center gap-2 mt-0.5">
            <Mail size={13} className="text-slate-400" />
            <p className="text-slate-500 font-body text-sm">{profile?.email}</p>
          </div>
        </div>
        <div className="ml-auto">
          <span className="badge-mint">
            <CheckCircle size={10} />
            Verified
          </span>
        </div>
      </div>

      {/* Form */}
      <div className="card">
        <div className="flex items-center gap-2 mb-6">
          <Edit size={16} className="text-mint-600" />
          <h2 className="font-display font-semibold text-slate-800">Edit Information</h2>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-5" noValidate>
          <Input
            label="Full Name"
            id="name"
            name="name"
            type="text"
            placeholder="Your full name"
            value={form.name}
            onChange={handleChange}
            error={errors.name}
            icon={UserIcon}
          />

          {/* Email — read-only */}
          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-display font-medium text-slate-700">
              Email Address
            </label>
            <div className="relative">
              <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
                <Mail size={16} />
              </span>
              <input
                type="email"
                value={profile?.email || ''}
                readOnly
                className="input-base pl-10 bg-slate-50 text-slate-400 cursor-not-allowed"
              />
            </div>
            <p className="text-xs text-slate-400 font-body">Email cannot be changed</p>
          </div>

          {/* Age */}
          <Input
            label="Age (optional)"
            id="age"
            name="age"
            type="number"
            placeholder="e.g. 25"
            value={form.age}
            onChange={handleChange}
            error={errors.age}
            min={1}
            max={120}
          />

          {/* Gender */}
          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-display font-medium text-slate-700">
              Gender (optional)
            </label>
            <div className="flex gap-3">
              {GENDER_OPTIONS.map((g) => (
                <button
                  key={g}
                  type="button"
                  onClick={() => {
                    setForm((prev) => ({ ...prev, gender: g }))
                    setSaved(false)
                  }}
                  className={`flex-1 py-2.5 rounded-xl border text-sm font-display font-medium transition-all duration-200 ${
                    form.gender === g
                      ? 'bg-mint-500 text-white border-mint-500 shadow-mint'
                      : 'bg-white text-slate-600 border-slate-200 hover:border-mint-300'
                  }`}
                >
                  {g}
                </button>
              ))}
            </div>
          </div>

          <div className="pt-2">
            <Button type="submit" loading={saving}>
              {saved ? (
                <span className="flex items-center gap-2">
                  <CheckCircle size={16} />
                  Saved
                </span>
              ) : (
                'Save Changes'
              )}
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}

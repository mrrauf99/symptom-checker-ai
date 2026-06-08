export const validators = {
  required: (value, label = 'This field') =>
    !value || !String(value).trim() ? `${label} is required` : null,

  email: (value) => {
    if (!value) return 'Email is required'
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return re.test(value) ? null : 'Enter a valid email address'
  },

  minLength: (min) => (value, label = 'This field') =>
    !value || value.length < min ? `${label} must be at least ${min} characters` : null,

  name: (value) => {
    if (!value || !value.trim()) return 'Name is required'
    if (value.trim().length < 3) return 'Name must be at least 3 characters'
    return null
  },

  password: (value) => {
    if (!value) return 'Password is required'
    if (value.length < 6) return 'Password must be at least 6 characters'
    return null
  },

  age: (value) => {
    if (!value) return null // optional
    const num = Number(value)
    if (isNaN(num) || num < 1 || num > 120) return 'Enter a valid age (1–120)'
    return null
  },
}

export function validateForm(fields, rules) {
  const errors = {}
  let isValid = true

  for (const [field, validators] of Object.entries(rules)) {
    for (const validate of validators) {
      const error = validate(fields[field])
      if (error) {
        errors[field] = error
        isValid = false
        break
      }
    }
  }

  return { errors, isValid }
}

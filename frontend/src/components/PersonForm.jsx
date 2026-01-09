import { useState, useEffect } from 'react'
import { personAPI } from '../services/api'
import '../styles/form.css'

function PersonForm({ onSubmit, personId }) {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    source_website: '',
    country: '',
    organisation: '',
    domain: '',
    tags: '',
    roles: '',
    ppg: '',
    type: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (personId) {
      fetchPerson()
    }
  }, [personId])

  const fetchPerson = async () => {
    try {
      const response = await personAPI.getById(personId)
      setFormData(response.data)
    } catch (err) {
      setError(err.message)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      setLoading(true)
      await onSubmit(formData)
      setFormData({
        first_name: '',
        last_name: '',
        email: '',
        source_website: '',
        country: '',
        organisation: '',
        domain: '',
        tags: '',
        roles: '',
        ppg: '',
        type: ''
      })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form className="person-form" onSubmit={handleSubmit}>
      <h3>{personId ? 'Modifica Contatto' : 'Nuovo Contatto'}</h3>
      
      {error && <div className="error-msg">{error}</div>}
      
      <div className="form-grid">
        <div className="form-group">
          <label htmlFor="first_name">Nome</label>
          <input
            type="text"
            id="first_name"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            placeholder="Nome"
          />
        </div>

        <div className="form-group">
          <label htmlFor="last_name">Cognome</label>
          <input
            type="text"
            id="last_name"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            placeholder="Cognome"
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email *</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="email@example.com"
            required
            disabled={personId ? true : false}
          />
        </div>

        <div className="form-group">
          <label htmlFor="source_website">Website</label>
          <input
            type="text"
            id="source_website"
            name="source_website"
            value={formData.source_website}
            onChange={handleChange}
            placeholder="es. drupal, wordpress"
          />
        </div>

        <div className="form-group">
          <label htmlFor="country">Paese</label>
          <input
            type="text"
            id="country"
            name="country"
            value={formData.country}
            onChange={handleChange}
            placeholder="Italia"
          />
        </div>

        <div className="form-group">
          <label htmlFor="organisation">Organizzazione</label>
          <input
            type="text"
            id="organisation"
            name="organisation"
            value={formData.organisation}
            onChange={handleChange}
            placeholder="Nome azienda"
          />
        </div>

        <div className="form-group">
          <label htmlFor="domain">Dominio</label>
          <input
            type="text"
            id="domain"
            name="domain"
            value={formData.domain}
            onChange={handleChange}
            placeholder="example.com"
          />
        </div>

        <div className="form-group">
          <label htmlFor="tags">Tags</label>
          <input
            type="text"
            id="tags"
            name="tags"
            value={formData.tags}
            onChange={handleChange}
            placeholder="tag1, tag2, tag3"
          />
        </div>

        <div className="form-group">
          <label htmlFor="roles">Ruoli</label>
          <input
            type="text"
            id="roles"
            name="roles"
            value={formData.roles}
            onChange={handleChange}
            placeholder="admin, user"
          />
        </div>

        <div className="form-group">
          <label htmlFor="ppg">PPG</label>
          <input
            type="text"
            id="ppg"
            name="ppg"
            value={formData.ppg}
            onChange={handleChange}
            placeholder="PPG value"
          />
        </div>

        <div className="form-group">
          <label htmlFor="type">Tipo</label>
          <input
            type="text"
            id="type"
            name="type"
            value={formData.type}
            onChange={handleChange}
            placeholder="Tipo contatto"
          />
        </div>
      </div>

      <div className="form-actions">
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Salvataggio...' : 'Salva'}
        </button>
      </div>
    </form>
  )
}

export default PersonForm

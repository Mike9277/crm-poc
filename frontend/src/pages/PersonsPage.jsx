import { useState, useEffect } from 'react'
import { personAPI } from '../services/api'
import PersonForm from '../components/PersonForm'
import PersonsList from '../components/PersonsList'
import CSVImportModal from '../components/CSVImportModal'
import '../styles/persons.css'

function PersonsPage() {
  const [persons, setPersons] = useState([])
  const [allPersons, setAllPersons] = useState([]) // Tutti i contatti per filtraggio locale
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [showImport, setShowImport] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchPersons()
  }, [])

  // Filtraggio locale con logica "contiene"
  useEffect(() => {
    if (searchTerm.trim() === '') {
      setPersons(allPersons)
    } else {
      const filtered = allPersons.filter(person => {
        const searchLower = searchTerm.toLowerCase()
        return (
          (person.email && person.email.toLowerCase().includes(searchLower)) ||
          (person.first_name && person.first_name.toLowerCase().includes(searchLower)) ||
          (person.last_name && person.last_name.toLowerCase().includes(searchLower)) ||
          (person.organisation && person.organisation.toLowerCase().includes(searchLower))
        )
      })
      setPersons(filtered)
    }
  }, [searchTerm, allPersons])

  const fetchPersons = async () => {
    try {
      setLoading(true)
      const response = await personAPI.getAll()
      const data = response.data.results || response.data
      setAllPersons(data)
      setPersons(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async (data) => {
    try {
      await personAPI.create(data)
      setShowForm(false)
      fetchPersons()
    } catch (err) {
      setError(err.message)
    }
  }

  const handleUpdate = async (data) => {
    try {
      await personAPI.update(editingId, data)
      setEditingId(null)
      setShowForm(false)
      fetchPersons()
    } catch (err) {
      setError(err.message)
    }
  }

  const handleDelete = async (id) => {
    if (confirm('Sei sicuro di voler eliminare questo contatto?')) {
      try {
        await personAPI.delete(id)
        fetchPersons()
      } catch (err) {
        setError(err.message)
      }
    }
  }

  const handleEdit = (person) => {
    setEditingId(person.id)
    setShowForm(true)
  }

  if (error) return <div className="error">Errore: {error}</div>

  return (
    <div className="persons-page">
      <h1>Gestione Contatti</h1>
      
      <div className="controls">
        <input
          type="text"
          placeholder="Cerca per email, nome, cognome o organizzazione..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        <div className="button-group">
          <button 
            onClick={() => { 
              setEditingId(null); 
              setShowForm(!showForm); 
            }} 
            className="btn btn-primary"
          >
            {showForm ? 'Annulla' : '+ Nuovo Contatto'}
          </button>
          <button 
            onClick={() => setShowImport(true)} 
            className="btn btn-info"
          >
            📄 Importa CSV
          </button>
        </div>
      </div>

      {showForm && (
        <PersonForm
          onSubmit={editingId ? handleUpdate : handleCreate}
          personId={editingId}
        />
      )}

      {showImport && (
        <CSVImportModal
          onClose={() => setShowImport(false)}
          onSuccess={() => {
            fetchPersons()
            setShowImport(false)
          }}
        />
      )}

      {loading ? (
        <div className="loading">⏳ Caricamento...</div>
      ) : (
        <>
          {persons.length > 0 && (
            <div style={{ marginTop: '1rem', color: '#718096', fontSize: '0.9rem' }}>
              Risultati: {persons.length} di {allPersons.length} contatti
            </div>
          )}
          <PersonsList
            persons={persons}
            onEdit={handleEdit}
            onDelete={handleDelete}
          />
        </>
      )}
    </div>
  )
}

export default PersonsPage
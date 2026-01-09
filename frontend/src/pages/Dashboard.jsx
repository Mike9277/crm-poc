import { useState, useEffect } from 'react'
import { personAPI, webformAPI } from '../services/api'
import '../styles/dashboard.css'

function Dashboard() {
  const [stats, setStats] = useState({
    totalPersons: 0,
    totalSubmissions: 0,
    recentPersons: []
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true)
        const [personsRes, webformsRes] = await Promise.all([
          personAPI.getAll({ ordering: '-created_at', limit: 5 }),
          webformAPI.getAll()
        ])
        
        setStats({
          totalPersons: personsRes.data.count || 0,
          totalSubmissions: webformsRes.data.count || 0,
          recentPersons: personsRes.data.results || []
        })
      } catch (err) {
        console.error('API Error:', err.response?.status, err.response?.data, err.message)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  if (loading) return <div className="loading">Caricamento...</div>
  if (error) return <div className="error">Errore: {error}</div>

  return (
    <div className="dashboard">
      <h1>Dashboard CRM</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Contatti Totali</h3>
          <p className="stat-number">{stats.totalPersons}</p>
        </div>
        <div className="stat-card">
          <h3>Submissioni Webform</h3>
          <p className="stat-number">{stats.totalSubmissions}</p>
        </div>
      </div>

      <div className="recent-section">
        <h2>Contatti Recenti</h2>
        {stats.recentPersons.length === 0 ? (
          <p className="no-data">Nessun contatto trovato</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Email</th>
                <th>Nome</th>
                <th>Cognome</th>
                <th>Sorgente</th>
                <th>Data Creazione</th>
              </tr>
            </thead>
            <tbody>
              {stats.recentPersons.map(person => (
                <tr key={person.id}>
                  <td>{person.email}</td>
                  <td>{person.first_name || '-'}</td>
                  <td>{person.last_name || '-'}</td>
                  <td>{person.source_website || '-'}</td>
                  <td>{new Date(person.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default Dashboard

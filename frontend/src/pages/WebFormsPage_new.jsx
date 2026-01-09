import { useState, useEffect } from 'react'
import { webformAPI } from '../services/api'
import '../styles/webforms.css'

function WebFormsPage() {
  const [submissions, setSubmissions] = useState([])
  const [webforms, setWebforms] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedSubmission, setSelectedSubmission] = useState(null)
  const [filterWebform, setFilterWebform] = useState('')

  useEffect(() => {
    fetchData()
  }, [filterWebform])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [subRes, webRes] = await Promise.all([
        webformAPI.getAllSubmissions({ webform: filterWebform || undefined }),
        webformAPI.getAll()
      ])
      setSubmissions(subRes.data.results || subRes.data)
      setWebforms(webRes.data.results || webRes.data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (error) return <div className="error">Errore: {error}</div>

  return (
    <div className="webforms-page">
      <h1>Webform Submission</h1>

      <div className="controls">
        <select
          value={filterWebform}
          onChange={(e) => setFilterWebform(e.target.value)}
          className="filter-select"
        >
          <option value="">Tutti i form</option>
          {webforms.map(form => (
            <option key={form.id} value={form.id}>{form.name}</option>
          ))}
        </select>
        <span className="count-badge">{submissions.length} submission{submissions.length !== 1 ? 's' : ''}</span>
      </div>

      {loading ? (
        <div className="loading">Caricamento...</div>
      ) : submissions.length === 0 ? (
        <div className="no-data">Nessuna submission trovata</div>
      ) : (
        <div className="submissions-container">
          <div className="submissions-list">
            {submissions.map(submission => (
              <div
                key={submission.id}
                className={`submission-card ${selectedSubmission?.id === submission.id ? 'active' : ''}`}
                onClick={() => setSelectedSubmission(submission)}
              >
                <div className="submission-header">
                  <span className="submission-id">#{submission.id}</span>
                  <span className="submission-date">
                    {new Date(submission.created_at).toLocaleDateString('it-IT')}
                  </span>
                </div>
                <div className="submission-info">
                  <div className="info-row">
                    <span className="label">Email:</span>
                    <span className="value">{submission.payload?.email || '-'}</span>
                  </div>
                  <div className="info-row">
                    <span className="label">Nome:</span>
                    <span className="value">{submission.payload?.first_name || '-'}</span>
                  </div>
                  <div className="info-row">
                    <span className="label">Form:</span>
                    <span className="value">{submission.webform?.name || '-'}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {selectedSubmission && (
            <div className="submission-detail">
              <div className="detail-header">
                <h2>Dettagli Submission #{selectedSubmission.id}</h2>
                <button
                  className="close-detail"
                  onClick={() => setSelectedSubmission(null)}
                >
                  ×
                </button>
              </div>

              <div className="detail-content">
                <section className="detail-section">
                  <h3>Informazioni Contatto</h3>
                  <div className="detail-grid">
                    <div className="detail-item">
                      <span className="detail-label">Email:</span>
                      <span className="detail-value">{selectedSubmission.payload?.email || '-'}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Nome:</span>
                      <span className="detail-value">{selectedSubmission.payload?.first_name || '-'}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Cognome:</span>
                      <span className="detail-value">{selectedSubmission.payload?.last_name || '-'}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Telefono:</span>
                      <span className="detail-value">{selectedSubmission.payload?.phone || '-'}</span>
                    </div>
                  </div>
                </section>

                <section className="detail-section">
                  <h3>Informazioni Submission</h3>
                  <div className="detail-grid">
                    <div className="detail-item">
                      <span className="detail-label">ID Webform:</span>
                      <span className="detail-value">{selectedSubmission.webform_id || '-'}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Nome Form:</span>
                      <span className="detail-value">{selectedSubmission.webform?.name || '-'}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Contatto ID:</span>
                      <span className="detail-value">{selectedSubmission.person_id || '-'}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Data:</span>
                      <span className="detail-value">{new Date(selectedSubmission.created_at).toLocaleString('it-IT')}</span>
                    </div>
                  </div>
                </section>

                {selectedSubmission.payload && Object.keys(selectedSubmission.payload).length > 0 && (
                  <section className="detail-section">
                    <h3>Dati Submission (JSON)</h3>
                    <pre className="json-display">{JSON.stringify(selectedSubmission.payload, null, 2)}</pre>
                  </section>
                )}

                {selectedSubmission.payload?.message && (
                  <section className="detail-section">
                    <h3>Messaggio</h3>
                    <div className="message-box">
                      {selectedSubmission.payload.message}
                    </div>
                  </section>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default WebFormsPage

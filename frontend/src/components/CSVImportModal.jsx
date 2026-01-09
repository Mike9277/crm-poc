import { useState } from 'react'
import { personAPI } from '../services/api'
import '../styles/csv-import.css'

function CSVImportModal({ onClose, onSuccess }) {
  const [file, setFile] = useState(null)
  const [step, setStep] = useState('upload') // upload, mapping, preview, importing
  const [csvData, setCsvData] = useState([])
  const [fieldMapping, setFieldMapping] = useState({})
  const [importStats, setImportStats] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const availableFields = [
    'email', 'first_name', 'last_name', 'source_website', 'external_id',
    'country', 'organisation', 'domain', 'tags', 'roles', 'ppg', 'type', 'website', 'webform'
  ]
  const csvColumns = csvData.length > 0 ? Object.keys(csvData[0]) : []

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      parseCSV(selectedFile)
    }
  }

  const parseCSV = (file) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const text = e.target.result
        const lines = text.trim().split('\n')
        const headers = lines[0].split(',').map(h => h.trim().toLowerCase())
        
        const data = lines.slice(1).map(line => {
          const values = line.split(',')
          const obj = {}
          headers.forEach((header, index) => {
            obj[header] = values[index]?.trim() || ''
          })
          return obj
        })

        setCsvData(data)
        // Auto-map common field names
        const autoMapping = {}
        headers.forEach(col => {
          if (col.includes('email')) autoMapping[col] = 'email'
          else if (col.includes('first') || col.includes('nome')) autoMapping[col] = 'first_name'
          else if (col.includes('last') || col.includes('cognome')) autoMapping[col] = 'last_name'
          else if (col.includes('website') || col.includes('sito')) autoMapping[col] = 'website'
          else if (col.includes('source')) autoMapping[col] = 'source_website'
          else if (col.includes('country') || col.includes('nazione') || col.includes('paese')) autoMapping[col] = 'country'
          else if (col.includes('organization') || col.includes('organizzazione') || col.includes('azienda')) autoMapping[col] = 'organisation'
          else if (col.includes('domain')) autoMapping[col] = 'domain'
          else if (col.includes('tags') || col.includes('etichette')) autoMapping[col] = 'tags'
          else if (col.includes('roles') || col.includes('ruoli')) autoMapping[col] = 'roles'
          else if (col.includes('ppg')) autoMapping[col] = 'ppg'
          else if (col.includes('type') || col.includes('tipo')) autoMapping[col] = 'type'
          else if (col.includes('webform')) autoMapping[col] = 'webform'
        })
        setFieldMapping(autoMapping)
        setStep('mapping')
        setError(null)
      } catch (err) {
        setError('Errore nel parsing del CSV: ' + err.message)
      }
    }
    reader.readAsText(file)
  }

  const handleMappingChange = (csvCol, crmField) => {
    setFieldMapping({
      ...fieldMapping,
      [csvCol]: crmField || ''
    })
  }

  const handlePreview = () => {
    setStep('preview')
  }

  const handleImport = async () => {
    setLoading(true)
    setError(null)
    try {
      // Prepare data for import
      const records = csvData.map(row => {
        const record = {}
        Object.entries(fieldMapping).forEach(([csvCol, crmField]) => {
          if (crmField && row[csvCol]) {
            record[crmField] = row[csvCol]
          }
        })
        return record
      }).filter(r => r.email) // Only records with email

      if (records.length === 0) {
        setError('Nessun record valido da importare (verificare la mappatura dei campi)')
        setLoading(false)
        return
      }

      // Call import endpoint
      const response = await personAPI.importCSV(records)
      setImportStats(response.data)
      setStep('importing')
      setLoading(false)
      
      // Auto-close after 2 seconds on success
      if (response.data.created > 0 || response.data.updated > 0) {
        setTimeout(() => {
          if (onSuccess) onSuccess()
          onClose()
        }, 2000)
      }
    } catch (err) {
      setError('Errore durante l\'importazione: ' + err.message)
      setLoading(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Importa Contatti da CSV</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          {error && <div className="alert alert-error">{error}</div>}

          {step === 'upload' && (
            <div className="upload-step">
              <div className="upload-area">
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleFileChange}
                  className="file-input"
                  id="csv-file"
                />
                <label htmlFor="csv-file" className="upload-label">
                  <div className="upload-icon">📁</div>
                  <p>Seleziona un file CSV o trascinalo qui</p>
                  <p className="upload-hint">Formato: email, first_name, last_name, source_website, ...</p>
                </label>
              </div>
            </div>
          )}

          {step === 'mapping' && (
            <div className="mapping-step">
              <h3>Mappatura Campi</h3>
              <p className="hint">Seleziona come mappare i colonne del CSV ai campi del CRM</p>
              
              <div className="mapping-table">
                <div className="mapping-header">
                  <div className="mapping-col">Colonna CSV</div>
                  <div className="mapping-col">Campo CRM</div>
                </div>
                
                {csvColumns.map(col => (
                  <div key={col} className="mapping-row">
                    <div className="mapping-col">{col}</div>
                    <div className="mapping-col">
                      <select
                        value={fieldMapping[col] || ''}
                        onChange={(e) => handleMappingChange(col, e.target.value)}
                        className="mapping-select"
                      >
                        <option value="">-- Non importare --</option>
                        {availableFields.map(field => (
                          <option key={field} value={field}>{field}</option>
                        ))}
                      </select>
                    </div>
                  </div>
                ))}
              </div>

              <div className="preview-info">
                <p>Anteprima dei dati:</p>
                <div className="preview-data">
                  {csvData.slice(0, 2).map((row, idx) => (
                    <div key={idx} className="preview-row">
                      {Object.entries(row).slice(0, 3).map(([key, val]) => (
                        <span key={key} className="preview-cell">{key}: {val}</span>
                      ))}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {step === 'preview' && (
            <div className="preview-step">
              <h3>Anteprima Importazione</h3>
              <p>Verranno importati <strong>{csvData.length}</strong> record</p>
              
              <div className="preview-table">
                <table className="table">
                  <thead>
                    <tr>
                      {availableFields.map(field => (
                        Object.values(fieldMapping).includes(field) && (
                          <th key={field}>{field}</th>
                        )
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {csvData.slice(0, 5).map((row, idx) => (
                      <tr key={idx}>
                        {Object.entries(fieldMapping).map(([csvCol, crmField]) => (
                          crmField && (
                            <td key={crmField}>{row[csvCol] || '-'}</td>
                          )
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
                {csvData.length > 5 && (
                  <p className="preview-more">... e altri {csvData.length - 5} record</p>
                )}
              </div>
            </div>
          )}

          {step === 'importing' && (
            <div className="importing-step">
              <h3>Importazione Completata</h3>
              <div className="stats">
                <div className="stat-item success">
                  <div className="stat-number">{importStats?.created || 0}</div>
                  <div className="stat-label">Creati</div>
                </div>
                <div className="stat-item info">
                  <div className="stat-number">{importStats?.updated || 0}</div>
                  <div className="stat-label">Aggiornati</div>
                </div>
                <div className="stat-item warning">
                  <div className="stat-number">{importStats?.skipped || 0}</div>
                  <div className="stat-label">Saltati</div>
                </div>
              </div>
              {importStats?.errors && importStats.errors.length > 0 && (
                <div className="errors-list">
                  <h4>Errori:</h4>
                  <ul>
                    {importStats.errors.slice(0, 5).map((err, idx) => (
                      <li key={idx}>{err}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="modal-footer">
          {step === 'upload' && (
            <>
              <button onClick={onClose} className="btn btn-secondary">Annulla</button>
            </>
          )}
          {step === 'mapping' && (
            <>
              <button onClick={() => setStep('upload')} className="btn btn-secondary">Indietro</button>
              <button onClick={handlePreview} className="btn btn-primary">Avanti</button>
            </>
          )}
          {step === 'preview' && (
            <>
              <button onClick={() => setStep('mapping')} className="btn btn-secondary">Indietro</button>
              <button 
                onClick={handleImport} 
                className="btn btn-success"
                disabled={loading}
              >
                {loading ? 'Importando...' : 'Importa'}
              </button>
            </>
          )}
          {step === 'importing' && (
            <button onClick={onClose} className="btn btn-primary">Chiudi</button>
          )}
        </div>
      </div>
    </div>
  )
}

export default CSVImportModal

import React, { useState } from 'react';

/**
 * Componente pulsante per sincronizzare manualmente submissions da Drupal
 * Risolve il bug del cron di Drupal che non importa correttamente le submissions
 */
export function WebformSyncButton({ onSyncSuccess }) {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showDetails, setShowDetails] = useState(false);

  const handleSync = async () => {
    setIsLoading(true);
    setResult(null);
    setError(null);
    setShowDetails(false);

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/webform-submissions/sync_from_drupal/`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: '{}',
        }
      );

      const data = await response.json();

      if (response.ok) {
        setResult({
          status: 'success',
          message: data.message || 'Sincronizzazione completata con successo',
          output: data.output,
        });
        
        // Ricarica i dati dopo la sincronizzazione
        if (onSyncSuccess) {
          setTimeout(() => {
            onSyncSuccess();
          }, 1500);
        }
      } else {
        setError(data.message || `Errore durante la sincronizzazione (${response.status})`);
      }
    } catch (err) {
      setError(`Errore di connessione: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h3 style={styles.title}>🔄 Sincronizza da Drupal</h3>
        <p style={styles.description}>
          Importa manualmente le nuove submissions dai webform di Drupal.
          Questo risolve il problema con il cron che non sempre funziona.
        </p>

        <button
          onClick={handleSync}
          disabled={isLoading}
          style={{
            ...styles.button,
            opacity: isLoading ? 0.6 : 1,
            cursor: isLoading ? 'not-allowed' : 'pointer',
          }}
        >
          {isLoading ? '⏳ Sincronizzazione in corso...' : '🔄 Importa da Drupal'}
        </button>

        {error && (
          <div style={styles.errorBox}>
            <strong>❌ Errore:</strong> {error}
          </div>
        )}

        {result && result.status === 'success' && (
          <div style={styles.successBox}>
            <strong>✅ Successo:</strong> {result.message}
            {result.output && (
              <>
                <button
                  onClick={() => setShowDetails(!showDetails)}
                  style={styles.detailsToggle}
                >
                  {showDetails ? '▼ Nascondi dettagli' : '▶ Mostra dettagli'}
                </button>
                {showDetails && (
                  <pre style={styles.outputBox}>{result.output}</pre>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    padding: '20px',
    marginBottom: '20px',
  },
  card: {
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '20px',
    backgroundColor: '#f9f9f9',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  title: {
    margin: '0 0 10px 0',
    color: '#333',
    fontSize: '18px',
  },
  description: {
    margin: '0 0 15px 0',
    color: '#666',
    fontSize: '14px',
    lineHeight: '1.5',
  },
  button: {
    padding: '10px 20px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '16px',
    fontWeight: 'bold',
    cursor: 'pointer',
    marginBottom: '15px',
  },
  errorBox: {
    padding: '12px',
    backgroundColor: '#ffebee',
    color: '#c62828',
    borderRadius: '4px',
    marginBottom: '10px',
    fontSize: '14px',
  },
  successBox: {
    padding: '12px',
    backgroundColor: '#e8f5e9',
    color: '#2e7d32',
    borderRadius: '4px',
    marginBottom: '10px',
    fontSize: '14px',
  },
  detailsToggle: {
    background: 'none',
    border: 'none',
    color: '#2e7d32',
    cursor: 'pointer',
    fontSize: '13px',
    fontWeight: 'bold',
    marginTop: '10px',
    padding: '5px 0',
  },
  outputBox: {
    marginTop: '10px',
    padding: '10px',
    backgroundColor: 'white',
    borderRadius: '4px',
    fontSize: '11px',
    overflow: 'auto',
    maxHeight: '300px',
    border: '1px solid #ddd',
    lineHeight: '1.4',
  },
};

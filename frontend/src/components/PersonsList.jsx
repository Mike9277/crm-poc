import '../styles/persons.css'

function PersonsList({ persons, onEdit, onDelete }) {
  if (persons.length === 0) {
    return <div className="no-data">Nessun contatto trovato</div>
  }

  return (
    <div className="persons-table-container">
      <table className="persons-table">
        <thead>
          <tr>
            <th>Nome</th>
            <th>Cognome</th>
            <th>Email</th>
            <th>Website</th>
            <th>Paese</th>
            <th>Organizzazione</th>
            <th>Dominio</th>
            <th>Tags</th>
            <th>Ruoli</th>
            <th>Webform</th>
            <th>PPG</th>
            <th>Tipo</th>
            <th>Azioni</th>
          </tr>
        </thead>
        <tbody>
          {persons.map(person => (
            <tr key={person.id}>
              <td>{person.first_name || '-'}</td>
              <td>{person.last_name || '-'}</td>
              <td>{person.email}</td>
              <td>{person.source_website || '-'}</td>
              <td>{person.country || '-'}</td>
              <td>{person.organisation || '-'}</td>
              <td>{person.domain || '-'}</td>
              <td>{person.tags || '-'}</td>
              <td>{person.roles || '-'}</td>
              <td>{person.webform || '-'}</td>
              <td>{person.ppg || '-'}</td>
              <td>{person.type || '-'}</td>
              <td>
                <div className="action-buttons">
                  <button
                    onClick={() => onEdit(person)}
                    className="action-btn edit"
                  >
                    Modifica
                  </button>
                  <button
                    onClick={() => onDelete(person.id)}
                    className="action-btn delete"
                  >
                    Elimina
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default PersonsList

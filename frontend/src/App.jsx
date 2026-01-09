import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import PersonsPage from './pages/PersonsPage'
import WebFormsPage from './pages/WebFormsPage'
import Header from './components/Header'
import Footer from './components/Footer'
import './App.css'

// Component per il link con classe active
function NavLink({ to, children }) {
  const location = useLocation()
  const isActive = location.pathname === to
  
  return (
    <Link to={to} className={`nav-link ${isActive ? 'active' : ''}`}>
      {children}
    </Link>
  )
}

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <nav className="navbar">
          <div className="nav-container">
            <NavLink to="/">📊 Dashboard</NavLink>
            <NavLink to="/persons">👥 Contatti</NavLink>
            <NavLink to="/webforms">📝 Webform</NavLink>
          </div>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/persons" element={<PersonsPage />} />
            <Route path="/webforms" element={<WebFormsPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  )
}

export default App
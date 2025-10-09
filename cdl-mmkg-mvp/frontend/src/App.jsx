import { useState } from 'react'
import { searchAPI } from './services/api'
import SearchBar from './components/SearchBar'
import ResultList from './components/ResultList'
import DocumentUpload from './components/DocumentUpload'
import DocumentManagement from './components/DocumentManagement'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('search')
  const [results, setResults] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [refreshTrigger, setRefreshTrigger] = useState(0)

  const handleSearch = async (query) => {
    setIsLoading(true)
    setError(null)

    try {
      const data = await searchAPI(query)
      setResults(data)
    } catch (err) {
      setError(err.message || 'An error occurred while searching')
      setResults([])
    } finally {
      setIsLoading(false)
    }
  }

  const handleUploadSuccess = (document) => {
    // Switch to manage tab and refresh
    setActiveTab('manage')
    setRefreshTrigger(prev => prev + 1)
  }

  const renderTabContent = () => {
    switch (activeTab) {
      case 'search':
        return (
          <div className="tab-content">
            <div className="search-section">
              <h2 className="section-title">🔍 Semantic Search</h2>
              <p className="section-description">
                Search across your document library using natural language. Our AI-powered
                search understands context and meaning to deliver the most relevant results.
              </p>
              <SearchBar onSearchSubmit={handleSearch} />
              
              {isLoading && (
                <div className="loading-container">
                  <div className="spinner"></div>
                  <p>Searching documents...</p>
                </div>
              )}
              
              {error && (
                <div className="alert alert-error">
                  ⚠️ {error}
                </div>
              )}
              
              {!isLoading && !error && <ResultList results={results} />}
            </div>
          </div>
        )
      
      case 'upload':
        return (
          <div className="tab-content">
            <DocumentUpload onUploadSuccess={handleUploadSuccess} />
          </div>
        )
      
      case 'manage':
        return (
          <div className="tab-content">
            <DocumentManagement refreshTrigger={refreshTrigger} />
          </div>
        )
      
      default:
        return null
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            <span className="logo-icon">📚</span>
            Cognitive Digital Library
          </h1>
          <p className="app-subtitle">
            Intelligent Document Management & Semantic Search
          </p>
        </div>
      </header>

      <nav className="tab-navigation">
        <button
          className={`tab-button ${activeTab === 'search' ? 'active' : ''}`}
          onClick={() => setActiveTab('search')}
        >
          <span className="tab-icon">🔍</span>
          <span className="tab-label">Search</span>
        </button>
        <button
          className={`tab-button ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          <span className="tab-icon">📤</span>
          <span className="tab-label">Upload</span>
        </button>
        <button
          className={`tab-button ${activeTab === 'manage' ? 'active' : ''}`}
          onClick={() => setActiveTab('manage')}
        >
          <span className="tab-icon">📚</span>
          <span className="tab-label">Manage</span>
        </button>
      </nav>

      <main className="app-main">
        <div className="container">
          {renderTabContent()}
        </div>
      </main>

      <footer className="app-footer">
        <p>Cognitive Digital Library v2.0 - Powered by AI & Semantic Search</p>
      </footer>
    </div>
  )
}

export default App

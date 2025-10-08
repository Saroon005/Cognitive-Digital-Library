import { useState } from 'react'
import { searchAPI } from './services/api'
import SearchBar from './components/SearchBar'
import ResultList from './components/ResultList'
import './App.css'

function App() {
  const [results, setResults] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = async (query) => {
    setIsLoading(true)
    setError(null)

    try {
      const data = await searchAPI(query)
      setResults(data)
    } catch (err) {
      setError(err.message || 'An error occurred while searching')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Cognitive Digital Library</h1>
      <SearchBar onSearchSubmit={handleSearch} />
      
      {isLoading && <p>Loading...</p>}
      
      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      {!isLoading && !error && <ResultList results={results} />}
    </main>
  )
}

export default App

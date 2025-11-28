import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('Loading...')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    // Backend'e istek gönder
    fetch('http://localhost:8000/')
      .then(res => {
        if (!res.ok) throw new Error('Backend bağlantısı başarısız')
        return res.json()
      })
      .then(data => {
        setMessage(data.message)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  return (
    <div className="App">
      <h1>🔐 Phishing Detection Platform</h1>
      
      {loading && <p>⏳ Backend'e bağlanılıyor...</p>}
      
      {error && (
        <div style={{ color: 'red', padding: '10px', border: '1px solid red' }}>
          ❌ Hata: {error}
        </div>
      )}
      
      {!loading && !error && (
        <div style={{ color: 'green', padding: '10px', border: '1px solid green' }}>
          ✅ Backend: {message}
        </div>
      )}
    </div>
  )
}

export default App
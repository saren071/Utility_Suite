import React, { useEffect, useState } from 'react'
import axios from 'axios'

function App() {
  const [packages, setPackages] = useState<any[]>([])
  const [selectedPkg, setSelectedPkg] = useState<any | null>(null)
  const [result, setResult] = useState<any | null>(null)
  const [args, setArgs] = useState<string>('{}')

  useEffect(() => {
    axios.get('/api/packages').then(r => setPackages(r.data.packages || []))
  }, [])

  const runFeature = async (featureId: string) => {
    try {
      const parsed = args ? JSON.parse(args) : {}
      const res = await axios.post('/api/run', {
        package_id: selectedPkg.id,
        feature_id: featureId,
        args: parsed,
      })
      setResult(res.data)
    } catch (e: any) {
      setResult({ success: false, message: e?.message })
    }
  }

  return (
    <div style={{ padding: 16, fontFamily: 'sans-serif' }}>
      <h2>Utility Suite UI</h2>
      <div style={{ display: 'flex', gap: 24 }}>
        <div style={{ minWidth: 320 }}>
          <h3>Packages</h3>
          <ul>
            {packages.map((p) => (
              <li key={p.id}>
                <button onClick={() => { setSelectedPkg(p); setResult(null) }}>{p.name} ({p.id})</button>
              </li>
            ))}
          </ul>
        </div>
        <div style={{ flex: 1 }}>
          {selectedPkg ? (
            <div>
              <h3>{selectedPkg.name}</h3>
              <p>{selectedPkg.description}</p>
              <label>Args (JSON):</label>
              <textarea value={args} onChange={e => setArgs(e.target.value)} rows={6} style={{ width: '100%' }} />
              <h4>Features</h4>
              <ul>
                {selectedPkg.features?.map((f: any) => (
                  <li key={f.id}>
                    <button onClick={() => runFeature(f.id)}>{f.name} ({f.id})</button>
                  </li>
                ))}
              </ul>
            </div>
          ) : (
            <p>Select a package</p>
          )}
        </div>
      </div>
      <div style={{ marginTop: 24 }}>
        <h3>Result</h3>
        <pre style={{ background: '#f5f5f5', padding: 12 }}>
          {result ? JSON.stringify(result, null, 2) : '—'}
        </pre>
      </div>
    </div>
  )
}

export default App

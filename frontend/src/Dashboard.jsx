import React, { useState, useEffect } from 'react';

export default function Dashboard() {
  const [opportunities, setOpportunities] = useState([]);
  const [query, setQuery] = useState("");

  useEffect(() => {
    fetch('/api/opportunities')
      .then(res => res.json())
      .then(data => {
        if(data.opportunities) setOpportunities(data.opportunities);
      })
      .catch(err => console.error(err));
  }, []);

  const handleResearch = async () => {
    try {
      const res = await fetch('/api/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      const result = await res.json();
      alert(`Research job dispatched: ${JSON.stringify(result.query)}`);
      setQuery("");
    } catch(e) {
      alert('Error triggering research');
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <header style={{ marginBottom: '2rem' }}>
        <h1>Internship Intelligence Agent</h1>
        <p>Zero-cost research and outreach orchestrator</p>
      </header>

      <section style={{ marginBottom: '2rem' }}>
        <h2>Natural Language Discovery</h2>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <input
            type="text"
            placeholder="e.g. Find VC-backed startups hiring backend interns..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{ width: '400px', padding: '0.5rem' }}
          />
          <button onClick={handleResearch} style={{ padding: '0.5rem 1rem' }}>Start Research</button>
        </div>
      </section>

      <section>
        <h2>Qualified Opportunities</h2>
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
          <thead>
            <tr style={{ backgroundColor: '#f0f0f0', textAlign: 'left' }}>
              <th style={{ padding: '0.5rem', border: '1px solid #ddd' }}>Company</th>
              <th style={{ padding: '0.5rem', border: '1px solid #ddd' }}>Contact</th>
              <th style={{ padding: '0.5rem', border: '1px solid #ddd' }}>Score</th>
              <th style={{ padding: '0.5rem', border: '1px solid #ddd' }}>Status</th>
              <th style={{ padding: '0.5rem', border: '1px solid #ddd' }}>Date Discovered</th>
            </tr>
          </thead>
          <tbody>
            {opportunities.length === 0 ? (
              <tr><td colSpan="5" style={{ padding: '1rem', textAlign: 'center' }}>No opportunities discovered yet.</td></tr>
            ) : opportunities.map(op => (
              <tr key={op.id}>
                <td style={{ padding: '0.5rem', border: '1px solid #ddd' }}>{op.company}</td>
                <td style={{ padding: '0.5rem', border: '1px solid #ddd' }}>{op.contact}</td>
                <td style={{ padding: '0.5rem', border: '1px solid #ddd' }}>{Math.round(op.score)}/100</td>
                <td style={{ padding: '0.5rem', border: '1px solid #ddd' }}>{op.status}</td>
                <td style={{ padding: '0.5rem', border: '1px solid #ddd' }}>{op.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}

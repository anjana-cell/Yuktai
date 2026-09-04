function AuditPanel({ history, loading, error }) {
  return (
    <section className="audit-section">
      <div className="panel-section__heading">
        <span className="eyebrow">Human action log</span>
        <h3>Audit history</h3>
      </div>
      {loading && <div className="panel-loading panel-loading--small"><span className="spinner" /> Loading history</div>}
      {error && <p className="inline-error">{error}</p>}
      {!loading && !error && history.length === 0 && (
        <p className="audit-empty">No human resolution has been recorded for this exception.</p>
      )}
      {!loading && !error && history.length > 0 && (
        <div className="audit-list">
          {history.map((entry, index) => (
            <div className="audit-entry" key={`${entry.timestamp}-${index}`}>
              <div className="audit-entry__marker" />
              <div>
                <div className="audit-entry__topline">
                  <strong>{entry.decision.replaceAll('_', ' ')}</strong>
                  <time dateTime={entry.timestamp}>{new Date(entry.timestamp).toLocaleString()}</time>
                </div>
                <p>{entry.reason}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}

export default AuditPanel

import { useState } from 'react'
import AuditPanel from './AuditPanel'
import { formatAmount, statusLabels } from './exceptionUtils'

function AIInvestigationPanel({ exception, investigation, investigationLoading, error, audit, auditLoading, auditError, onResolve, onClose }) {
  const [reason, setReason] = useState('')
  const [decision, setDecision] = useState('resolved')
  const [submitting, setSubmitting] = useState(false)

  if (!exception) return null

  async function handleSubmit(event) {
    event.preventDefault()
    if (!reason.trim()) return
    setSubmitting(true)
    try {
      await onResolve(decision, reason.trim())
      setReason('')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <aside className="investigation-panel" aria-label="Exception investigation">
      <div className="panel-header">
        <div>
          <span className="eyebrow">Exception workspace</span>
          <h2>{exception.order_id}</h2>
        </div>
        <button className="icon-button" type="button" onClick={onClose} aria-label="Close investigation panel">×</button>
      </div>

      <div className="exception-summary">
        <span className={`status-badge status-badge--${exception.status}`}>
          {statusLabels[exception.status] || exception.status.replaceAll('_', ' ')}
        </span>
        <div className="summary-grid">
          <div><span>Order amount</span><strong>{formatAmount(exception.amount)}</strong></div>
          <div><span>Difference</span><strong>{formatAmount(exception.difference)}</strong></div>
        </div>
      </div>

      {investigationLoading && (
        <div className="panel-loading"><span className="spinner" /> Gemini is reviewing the exception</div>
      )}
      {error && <div className="panel-error">{error}</div>}

      {investigation && !investigationLoading && (
        <>
          <section className="ai-result">
            <div className="ai-result__heading">
              <div className="ai-spark" aria-hidden="true">✦</div>
              <div><span className="eyebrow">AI investigation</span><h3>{investigation.finding}</h3></div>
              <span className="confidence">{Math.round(investigation.confidence * 100)}% confidence</span>
            </div>
            <div className="ai-result__body">
              <div className="result-block">
                <span className="result-label">Likely cause</span>
                <p>{investigation.likely_cause}</p>
              </div>
              <div className="result-block">
                <span className="result-label">Evidence supplied</span>
                <ul>{investigation.evidence.map((item, index) => <li key={`${item}-${index}`}>{item}</li>)}</ul>
              </div>
              <div className="recommendation">
                <span className="result-label">Recommended action</span>
                <p>{investigation.recommended_action}</p>
              </div>
            </div>
          </section>

          <form className="resolution-form" onSubmit={handleSubmit}>
            <div className="panel-section__heading">
              <span className="eyebrow">Human resolution</span>
              <h3>Record a decision</h3>
            </div>
            <div className="decision-group" role="group" aria-label="Resolution decision">
              {['resolved', 'rejected', 'needs_review'].map((option) => (
                <button key={option} className={decision === option ? 'decision-button is-active' : 'decision-button'} type="button" onClick={() => setDecision(option)}>
                  {option.replaceAll('_', ' ')}
                </button>
              ))}
            </div>
            <label className="field-label" htmlFor="resolution-reason">Reason <span>Required</span></label>
            <textarea id="resolution-reason" value={reason} onChange={(event) => setReason(event.target.value)} placeholder="Add a concise note for the audit trail..." rows="3" required />
            <button className="primary-button" type="submit" disabled={submitting || !reason.trim()}>
              {submitting ? <><span className="spinner spinner--light" /> Saving</> : <>Save resolution <span aria-hidden="true">→</span></>}
            </button>
          </form>

          <AuditPanel history={audit} loading={auditLoading} error={auditError} />
        </>
      )}
    </aside>
  )
}

export default AIInvestigationPanel

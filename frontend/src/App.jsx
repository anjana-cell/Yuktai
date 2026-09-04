import { useEffect, useState } from 'react'
import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import AIInvestigationPanel from './components/AIInvestigationPanel'
import ExceptionTable from './components/ExceptionTable'
import MetricCard from './components/MetricCard'
import { fetchAudit, fetchExceptions, fetchMetrics, investigateException, resolveException } from './services/api'
import './App.css'

const chartColors = { matched: '#1b9b84', exceptions: '#e06b4e' }

function getErrorMessage(error, fallback) {
  return error.response?.data?.detail || error.message || fallback
}

function App() {
  const [metrics, setMetrics] = useState(null)
  const [exceptions, setExceptions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedException, setSelectedException] = useState(null)
  const [investigation, setInvestigation] = useState(null)
  const [investigationLoading, setInvestigationLoading] = useState(false)
  const [investigationError, setInvestigationError] = useState('')
  const [audit, setAudit] = useState([])
  const [auditLoading, setAuditLoading] = useState(false)
  const [auditError, setAuditError] = useState('')
  const [notice, setNotice] = useState('')

  async function loadDashboard() {
    setLoading(true)
    setError('')
    try {
      const [metricsData, exceptionsData] = await Promise.all([fetchMetrics(), fetchExceptions()])
      setMetrics(metricsData)
      setExceptions(exceptionsData)
    } catch (requestError) {
      setError(getErrorMessage(requestError, 'Unable to connect to the reconciliation API.'))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    const request = window.setTimeout(loadDashboard, 0)
    return () => window.clearTimeout(request)
  }, [])

  async function handleInvestigate(exception) {
    setSelectedException(exception)
    setInvestigation(null)
    setInvestigationError('')
    setAudit([])
    setAuditError('')
    setInvestigationLoading(true)
    setAuditLoading(true)
    try {
      const [investigationData, auditData] = await Promise.all([
        investigateException(exception.order_id),
        fetchAudit(exception.order_id),
      ])
      setInvestigation(investigationData)
      setAudit(auditData)
    } catch (requestError) {
      setInvestigationError(getErrorMessage(requestError, 'Unable to investigate this exception.'))
    } finally {
      setInvestigationLoading(false)
      setAuditLoading(false)
    }
  }

  async function handleResolve(decision, reason) {
    if (!selectedException) return
    try {
      await resolveException(selectedException.order_id, decision, reason)
      setNotice(`Resolution saved for ${selectedException.order_id}`)
      setSelectedException(null)
      setInvestigation(null)
      await loadDashboard()
      window.setTimeout(() => setNotice(''), 4000)
    } catch (requestError) {
      setInvestigationError(getErrorMessage(requestError, 'Unable to save the resolution.'))
      throw requestError
    }
  }

  const chartData = metrics ? [
    { name: 'Matched', records: metrics.matched_records, fill: chartColors.matched },
    { name: 'Exceptions', records: metrics.exception_records, fill: chartColors.exceptions },
  ] : []

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand-lockup">
          <div className="brand-mark" aria-hidden="true"><span /><span /><span /></div>
          <div><span className="brand-kicker">Finance operations / 01</span><h1>AI Finance Reconciliation Controller</h1></div>
        </div>
        <div className="system-status"><span className="status-pulse" /> Live data <span className="status-divider" /> {new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })}</div>
      </header>

      <main className="dashboard">
        <section className="intro-row">
          <div><span className="eyebrow">Reconciliation overview</span><h2>Payments, orders, settled.</h2><p className="intro-copy">AI-assisted payment, order and settlement reconciliation.</p></div>
          <button className="refresh-button" type="button" onClick={loadDashboard} disabled={loading}><span className={loading ? 'refresh-icon is-spinning' : 'refresh-icon'} aria-hidden="true">↻</span> Refresh data</button>
        </section>

        {notice && <div className="success-banner"><span>✓</span>{notice}</div>}
        {error && <div className="error-banner"><strong>Connection issue</strong><span>{error}</span><button type="button" onClick={loadDashboard}>Retry</button></div>}

        <section className="metrics-grid" aria-label="Reconciliation metrics">
          <MetricCard label="Total records" value={metrics?.total_records ?? '—'} detail="Across all source files" tone="ink" />
          <MetricCard label="Matched records" value={metrics?.matched_records ?? '—'} detail="Cleanly reconciled" tone="teal" />
          <MetricCard label="Exceptions" value={metrics?.exception_records ?? '—'} detail="Need human attention" tone="coral" />
          <MetricCard label="Match rate" value={metrics ? `${(metrics.match_rate * 100).toFixed(1)}%` : '—'} detail="Automation coverage" tone="amber" />
        </section>

        <section className="analysis-grid">
          <article className="chart-card">
            <div className="section-heading"><div><span className="eyebrow">Portfolio signal</span><h2>Reconciliation health</h2></div><span className="chart-period">Current run</span></div>
            <div className="chart-legend"><span><i className="legend-dot legend-dot--teal" />Matched</span><span><i className="legend-dot legend-dot--coral" />Exceptions</span></div>
            <div className="chart-wrap">
              {loading ? <div className="chart-loading"><span className="spinner" /> Loading metrics</div> : <ResponsiveContainer width="100%" height="100%"><BarChart data={chartData} barCategoryGap="32%" margin={{ top: 10, right: 12, left: -18, bottom: 0 }}><CartesianGrid strokeDasharray="3 4" vertical={false} stroke="#dbe2dc" /><XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#65716c', fontSize: 12, fontWeight: 600 }} /><YAxis axisLine={false} tickLine={false} tick={{ fill: '#65716c', fontSize: 11 }} allowDecimals={false} /><Tooltip cursor={{ fill: '#edf2ed' }} contentStyle={{ border: '1px solid #dbe2dc', borderRadius: 4, boxShadow: '0 8px 20px rgba(18, 35, 28, .1)' }} /><Bar dataKey="records" radius={[3, 3, 0, 0]} barSize={64}>{chartData.map((entry) => <Cell key={entry.name} fill={entry.fill} />)}</Bar></BarChart></ResponsiveContainer>}
            </div>
          </article>
          <article className="signal-card"><div className="signal-card__top"><span className="eyebrow">At a glance</span><span className="signal-arrow">↗</span></div><strong>{metrics ? `${(metrics.exception_rate * 100).toFixed(1)}%` : '—'}</strong><h3>of the current run needs attention</h3><p>Use AI investigation for context, then record the final human decision in the audit trail.</p><div className="signal-rule"><span style={{ width: metrics ? `${metrics.exception_rate * 100}%` : 0 }} /></div></article>
        </section>

        <section className="exceptions-section"><div className="section-heading section-heading--table"><div><span className="eyebrow">Review queue</span><h2>Active exceptions <span>{exceptions.length}</span></h2></div><p>Investigate each record before resolving.</p></div><ExceptionTable exceptions={exceptions} selectedOrderId={selectedException?.order_id} onInvestigate={handleInvestigate} /></section>
      </main>

      {selectedException && <div className="panel-backdrop" onClick={(event) => event.target === event.currentTarget && setSelectedException(null)}><AIInvestigationPanel exception={selectedException} investigation={investigation} investigationLoading={investigationLoading} error={investigationError} audit={audit} auditLoading={auditLoading} auditError={auditError} onResolve={handleResolve} onClose={() => setSelectedException(null)} /></div>}
    </div>
  )
}

export default App

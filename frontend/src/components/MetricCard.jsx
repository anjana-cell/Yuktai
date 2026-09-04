function MetricCard({ label, value, detail, tone = 'teal' }) {
  return (
    <article className={`metric-card metric-card--${tone}`}>
      <div className="metric-card__topline">
        <span className="metric-card__label">{label}</span>
        <span className="metric-card__dot" aria-hidden="true" />
      </div>
      <strong className="metric-card__value">{value}</strong>
      <span className="metric-card__detail">{detail}</span>
    </article>
  )
}

export default MetricCard

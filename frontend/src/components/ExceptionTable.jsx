import { formatAmount, statusLabels } from './exceptionUtils'

function ExceptionTable({ exceptions, selectedOrderId, onInvestigate }) {
  return (
    <div className="table-shell">
      <table className="exception-table">
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Payment ID</th>
            <th>Exception type</th>
            <th>Amount</th>
            <th>Settlement</th>
            <th>Difference</th>
            <th><span className="sr-only">Actions</span></th>
          </tr>
        </thead>
        <tbody>
          {exceptions.map((exception) => (
            <tr key={`${exception.order_id}-${exception.payment_id || 'unpaid'}`} className={selectedOrderId === exception.order_id ? 'is-selected' : ''}>
              <td><span className="order-id">{exception.order_id}</span></td>
              <td><span className="payment-id">{exception.payment_id || '--'}</span></td>
              <td>
                <span className={`status-badge status-badge--${exception.status}`}>
                  {statusLabels[exception.status] || exception.status.replaceAll('_', ' ')}
                </span>
              </td>
              <td>{formatAmount(exception.amount)}</td>
              <td>{formatAmount(exception.settlement_amount)}</td>
              <td className={Number(exception.difference) > 0 ? 'difference difference--negative' : 'difference'}>
                {formatAmount(exception.difference)}
              </td>
              <td>
                <button className="table-action" type="button" onClick={() => onInvestigate(exception)}>
                  <span aria-hidden="true">↗</span> Investigate
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {exceptions.length === 0 && (
        <div className="empty-state">
          <span className="empty-state__mark">OK</span>
          <strong>No active exceptions</strong>
          <p>All reconciliation records are currently accounted for.</p>
        </div>
      )}
    </div>
  )
}

export default ExceptionTable

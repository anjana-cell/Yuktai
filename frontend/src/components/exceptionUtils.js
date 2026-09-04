const statusLabels = {
  amount_mismatch: 'Amount mismatch',
  partial_settlement: 'Partial settlement',
  missing_settlement: 'Missing settlement',
  missing_payment: 'Missing payment',
  duplicate_payment: 'Duplicate payment',
  unmatched_transaction: 'Unmatched transaction',
}

function formatAmount(value) {
  if (value === null || value === undefined || value === '') return '--'
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 2,
  }).format(Number(value))
}

export { formatAmount, statusLabels }

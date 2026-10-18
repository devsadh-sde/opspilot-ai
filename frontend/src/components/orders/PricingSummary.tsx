
import type { PricingResult } from '../../types/order'

type PricingSummaryProps = {
  pricing: PricingResult
}

function PricingSummary({ pricing }: PricingSummaryProps) {
  const formatCurrency = (value: string | number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(Number(value))
  }

  const budgetDifference =
    pricing.budget !== null
      ? Number(pricing.budget) - Number(pricing.total_price)
      : null

  return (
    <section className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">
      <h3 className="text-xl font-semibold">
        Pricing Summary
      </h3>

      <p className="mt-2 text-sm text-slate-400">
        Order pricing and customer budget evaluation.
      </p>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <div className="rounded-lg bg-slate-950 p-4">
          <p className="text-sm text-slate-400">
            Unit Price
          </p>

          <p className="mt-2 text-2xl font-semibold">
            {formatCurrency(pricing.unit_price)}
          </p>
        </div>

        <div className="rounded-lg bg-slate-950 p-4">
          <p className="text-sm text-slate-400">
            Order Subtotal
          </p>

          <p className="mt-2 text-2xl font-semibold text-blue-400">
            {formatCurrency(pricing.total_price)}
          </p>
        </div>

        <div className="rounded-lg bg-slate-950 p-4">
          <p className="text-sm text-slate-400">
            Customer Budget
          </p>

          <p className="mt-2 text-2xl font-semibold">
            {pricing.budget !== null
              ? formatCurrency(pricing.budget)
              : 'Not specified'}
          </p>
        </div>

        <div className="rounded-lg bg-slate-950 p-4">
          <p className="text-sm text-slate-400">
            Budget Difference
          </p>

          <p
            className={`mt-2 text-2xl font-semibold ${
              budgetDifference === null
                ? 'text-slate-400'
                : budgetDifference >= 0
                  ? 'text-green-400'
                  : 'text-red-400'
            }`}
          >
            {budgetDifference !== null
              ? formatCurrency(budgetDifference)
              : 'N/A'}
          </p>
        </div>
      </div>

      <div className="mt-6">
        {pricing.within_budget === true && (
          <div className="rounded-lg border border-green-800 bg-green-950 p-4 text-green-300">
            Within Budget — The proposed order subtotal does not exceed
            the customer's specified budget.
          </div>
        )}

        {pricing.within_budget === false && (
          <div className="rounded-lg border border-red-800 bg-red-950 p-4 text-red-300">
            Over Budget — Customer confirmation is required before proceeding.
          </div>
        )}

        {pricing.within_budget === null && (
          <div className="rounded-lg border border-amber-800 bg-amber-950 p-4 text-amber-200">
            Budget Not Evaluated — No customer budget was provided.
          </div>
        )}
      </div>

      <p className="mt-4 text-xs text-slate-500">
        Subtotal excludes applicable taxes, shipping charges,
        and other additional costs.
      </p>
    </section>
  )
}

export default PricingSummary

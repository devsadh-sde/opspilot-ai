
import type { PolicyEvaluation as PolicyEvaluationResult } from '../../types/order'

type PolicyEvaluationProps = {
  evaluation: PolicyEvaluationResult
  approvalStatus?: string
}

function PolicyEvaluation({
  evaluation,
  approvalStatus,
}: PolicyEvaluationProps) {
  const checks = [
    {
      label: 'Inventory Availability',
      description: 'Enough stock exists to fulfill the requested quantity.',
      passed: evaluation.stock_sufficient,
    },
    {
      label: 'Manager Approval',
      description: 'Additional manager authorization for supplier procurement.',
      passed: !evaluation.manager_approval_required,
      required: evaluation.manager_approval_required,
    },
    {
      label: 'Customer Confirmation',
      description: 'Customer must confirm an order exceeding the budget.',
      passed: !evaluation.customer_confirmation_required,
      required: evaluation.customer_confirmation_required,
    },
    {
      label: 'Human Approval',
      description: 'A person must review the order before execution.',
      passed: false,
      required: evaluation.human_approval_required,
    },
  ]

  return (
    <section className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">
      <h3 className="text-xl font-semibold">
        Policy Evaluation
      </h3>

      <p className="mt-2 text-sm text-slate-400">
        Business rules evaluated by the order fulfillment workflow.
      </p>

      <div className="mt-6 space-y-3">
        {checks.map((check) => (
          <div
            key={check.label}
            className="flex items-start justify-between gap-4 rounded-lg border border-slate-800 bg-slate-950 p-4"
          >
            <div>
              <h4 className="font-medium text-white">
                {check.label}
              </h4>

              <p className="mt-1 text-sm text-slate-400">
                {check.description}
              </p>
            </div>

            <span
              className={`shrink-0 rounded-full px-3 py-1 text-xs font-medium ${
                check.required
                  ? 'bg-amber-950 text-amber-300'
                  : check.passed
                    ? 'bg-green-950 text-green-300'
                    : 'bg-red-950 text-red-300'
              }`}
            >
              {check.required
                ? 'Required'
                : check.passed
                  ? 'Passed'
                  : 'Not Passed'}
            </span>
          </div>
        ))}
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <div className="rounded-lg bg-slate-950 p-4">
          <p className="text-sm text-slate-400">
            Supplier Procurement Cost
          </p>

          <p className="mt-2 text-xl font-semibold">
            {new Intl.NumberFormat('en-US', {
              style: 'currency',
              currency: 'USD',
            }).format(Number(evaluation.supplier_procurement_cost))}
          </p>
        </div>

        <div className="rounded-lg bg-slate-950 p-4">
          <p className="text-sm text-slate-400">
            Eligible for Approval
          </p>

          <p
            className={`mt-2 text-xl font-semibold ${
              evaluation.eligible_for_approval
                ? 'text-green-400'
                : 'text-amber-400'
            }`}
          >
            {evaluation.eligible_for_approval ? 'Yes' : 'No'}
          </p>
        </div>
      </div>

      {approvalStatus && (
        <div className="mt-5 rounded-lg border border-blue-900 bg-blue-950/30 p-4">
          <p className="text-sm text-slate-400">
            Workflow Approval Status
          </p>

          <p className="mt-2 font-medium capitalize text-blue-300">
            {approvalStatus.replaceAll('_', ' ')}
          </p>
        </div>
      )}

      <p className="mt-5 text-xs text-slate-500">
        These checks do not approve or execute an order.
        Inventory is not reserved, and supplier purchases are not placed.
      </p>
    </section>
  )
}

export default PolicyEvaluation


import type { FulfillmentPlan } from '../../types/order'

type FulfillmentTableProps = {
  fulfillment: FulfillmentPlan
}

function FulfillmentTable({ fulfillment }: FulfillmentTableProps) {
  return (
    <section className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">
      <h3 className="text-xl font-semibold">
        Fulfillment Allocation
      </h3>

      <p className="mt-2 text-sm text-slate-400">
        Breakdown of inventory allocated from warehouses and suppliers.
      </p>

      <div className="mt-5 overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-slate-700 text-slate-400">
            <tr>
              <th className="px-4 py-3">Source</th>
              <th className="px-4 py-3">Source ID</th>
              <th className="px-4 py-3">Quantity</th>
              <th className="px-4 py-3">Lead Time</th>
            </tr>
          </thead>

          <tbody>
            {fulfillment.allocations.map((allocation, index) => (
              <tr
                key={`${allocation.source}-${allocation.source_id}-${index}`}
                className="border-b border-slate-800"
              >
                <td className="px-4 py-3 capitalize text-white">
                  {allocation.source}
                </td>

                <td className="px-4 py-3 text-slate-300">
                  {allocation.source_id}
                </td>

                <td className="px-4 py-3 font-medium text-blue-400">
                  {allocation.quantity}
                </td>

                <td className="px-4 py-3 text-slate-300">
                  {allocation.lead_time_days != null
                    ? `${allocation.lead_time_days} days`
                    : 'Not specified'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-5 grid gap-4 sm:grid-cols-3">
        <div className="rounded-lg bg-slate-950 p-4">
          <p className="text-sm text-slate-400">
            Requested
          </p>
          <p className="mt-2 text-xl font-semibold">
            {fulfillment.requested_quantity}
          </p>
        </div>

        <div className="rounded-lg bg-slate-950 p-4">
          <p className="text-sm text-slate-400">
            Allocated
          </p>
          <p className="mt-2 text-xl font-semibold text-green-400">
            {fulfillment.allocated_quantity}
          </p>
        </div>

        <div className="rounded-lg bg-slate-950 p-4">
          <p className="text-sm text-slate-400">
            Unfulfilled
          </p>
          <p className="mt-2 text-xl font-semibold text-amber-400">
            {fulfillment.unfulfilled_quantity}
          </p>
        </div>
      </div>
    </section>
  )
}

export default FulfillmentTable

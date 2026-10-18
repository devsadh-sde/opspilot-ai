
import { useEffect, useState } from 'react'

import {
  getAllOrderProposals,
  getOrderProposal,
} from '../services/api'

import type {
  SavedProposal,
  ProposalDetail,
} from '../services/api'

import ApprovalActions from '../components/orders/ApprovalActions'

function OrderProposals() {
  const [proposals, setProposals] = useState<SavedProposal[]>([])
  const [selectedProposal, setSelectedProposal] =
    useState<ProposalDetail | null>(null)

  const [loading, setLoading] = useState(true)
  const [detailsLoading, setDetailsLoading] = useState(false)
  const [error, setError] = useState('')
  const [detailsError, setDetailsError] = useState('')

  async function loadProposals() {
    setLoading(true)
    setError('')

    try {
      const data = await getAllOrderProposals()
      setProposals(data)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Could not load proposals'
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    let active = true

    async function loadInitialProposals() {
      try {
        const data = await getAllOrderProposals()

        if (active) {
          setProposals(data)
        }
      } catch (err) {
        if (active) {
          setError(
            err instanceof Error
              ? err.message
              : 'Could not load proposals'
          )
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    void loadInitialProposals()

    return () => {
      active = false
    }
  }, [])

  async function handleViewDetails(id: number) {
    setDetailsLoading(true)
    setDetailsError('')
    setSelectedProposal(null)

    try {
      const data = await getOrderProposal(id)
      setSelectedProposal(data)
    } catch (err) {
      setDetailsError(
        err instanceof Error
          ? err.message
          : 'Could not load proposal details'
      )
    } finally {
      setDetailsLoading(false)
    }
  }

  function handleReviewed(updated: SavedProposal) {
    setSelectedProposal((current) =>
      current
        ? { ...current, ...updated }
        : current
    )

    setProposals((current) =>
      current.map((proposal) =>
        proposal.id === updated.id
          ? { ...proposal, ...updated }
          : proposal
      )
    )
  }

  function formatDate(value: string) {
    const date = new Date(value)

    return Number.isNaN(date.getTime())
      ? value
      : date.toLocaleString()
  }

  function statusColor(status: string) {
    switch (status) {
      case 'approved':
        return 'bg-green-950 text-green-300'
      case 'rejected':
        return 'bg-red-950 text-red-300'
      case 'pending_review':
        return 'bg-amber-950 text-amber-300'
      default:
        return 'bg-slate-800 text-slate-300'
    }
  }

  return (
    <section className="max-w-5xl">
      <header>
        <h2 className="text-3xl font-semibold">
          Order Proposals
        </h2>

        <p className="mt-3 text-slate-400">
          View saved proposals and manage human approval decisions.
        </p>
      </header>

      {/* Proposal List */}
      <div className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <h3 className="text-xl font-semibold">
            Saved Proposals
          </h3>

          <button
            type="button"
            onClick={() => void loadProposals()}
            disabled={loading}
            className="cursor-pointer rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-300 transition-colors hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? 'Loading...' : 'Refresh'}
          </button>
        </div>

        {error && (
          <div
            role="alert"
            className="mt-5 rounded-lg border border-red-800 bg-red-950 p-4 text-red-300"
          >
            {error}
          </div>
        )}

        {loading && (
          <p className="mt-6 text-sm text-blue-400">
            Loading saved proposals...
          </p>
        )}

        {!loading && !error && proposals.length === 0 && (
          <p className="mt-6 text-sm text-slate-400">
            No saved proposals yet. Create one from the Dashboard.
          </p>
        )}

        {!loading && proposals.length > 0 && (
          <div className="mt-6 overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="border-b border-slate-700 text-slate-400">
                <tr>
                  <th className="px-4 py-3">Proposal ID</th>
                  <th className="px-4 py-3">Product ID</th>
                  <th className="px-4 py-3">Quantity</th>
                  <th className="px-4 py-3">Status</th>
                  <th className="px-4 py-3">Created</th>
                  <th className="px-4 py-3">Action</th>
                </tr>
              </thead>

              <tbody>
                {proposals.map((proposal) => (
                  <tr
                    key={proposal.id}
                    className="border-b border-slate-800"
                  >
                    <td className="px-4 py-4 font-semibold text-white">
                      #{proposal.id}
                    </td>

                    <td className="px-4 py-4 text-slate-300">
                      {proposal.product_id}
                    </td>

                    <td className="px-4 py-4 text-slate-300">
                      {proposal.quantity}
                    </td>

                    <td className="px-4 py-4">
                      <span
                        className={`rounded-full px-3 py-1 text-xs font-medium ${statusColor(proposal.status)}`}
                      >
                        {proposal.status.replaceAll('_', ' ')}
                      </span>
                    </td>

                    <td className="px-4 py-4 text-slate-400">
                      {formatDate(proposal.created_at)}
                    </td>

                    <td className="px-4 py-4">
                      <button
                        type="button"
                        onClick={() =>
                          void handleViewDetails(proposal.id)
                        }
                        disabled={detailsLoading}
                        className="cursor-pointer font-medium text-blue-400 hover:text-blue-300 disabled:cursor-not-allowed disabled:opacity-50"
                      >
                        View Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Selected Proposal */}
      {detailsLoading && (
        <p className="mt-6 text-blue-400">
          Loading proposal details...
        </p>
      )}

      {detailsError && (
        <div
          role="alert"
          className="mt-6 rounded-lg border border-red-800 bg-red-950 p-4 text-red-300"
        >
          {detailsError}
        </div>
      )}

      {selectedProposal && (
        <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">
          <h3 className="text-xl font-semibold">
            Proposal #{selectedProposal.id}
          </h3>

          <div className="mt-5 grid gap-4 sm:grid-cols-3">
            <div className="rounded-lg bg-slate-950 p-4">
              <p className="text-sm text-slate-400">
                Product ID
              </p>
              <p className="mt-2 text-xl font-semibold">
                {selectedProposal.product_id}
              </p>
            </div>

            <div className="rounded-lg bg-slate-950 p-4">
              <p className="text-sm text-slate-400">
                Quantity
              </p>
              <p className="mt-2 text-xl font-semibold">
                {selectedProposal.quantity}
              </p>
            </div>

            <div className="rounded-lg bg-slate-950 p-4">
              <p className="text-sm text-slate-400">
                Status
              </p>
              <p className="mt-2 text-xl font-semibold capitalize">
                {selectedProposal.status.replaceAll('_', ' ')}
              </p>
            </div>
          </div>

          <ApprovalActions
            proposal={selectedProposal}
            onReviewed={handleReviewed}
          />

          <details className="mt-6 rounded-lg border border-slate-700 p-4">
            <summary className="cursor-pointer text-sm font-medium text-slate-300">
              View Saved LangGraph Analysis
            </summary>

            <pre className="mt-4 max-h-[500px] overflow-auto rounded-lg bg-slate-950 p-4 text-xs text-green-300">
              {JSON.stringify(selectedProposal.analysis, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </section>
  )
}

export default OrderProposals


import { useState } from 'react'

import { reviewOrderProposal } from '../../services/api'
import type {
  ReviewDecision,
  SavedProposal,
} from '../../services/api'

type ApprovalActionsProps = {
  proposal: SavedProposal
  onReviewed: (updatedProposal: SavedProposal) => void
}

function ApprovalActions({
  proposal,
  onReviewed,
}: ApprovalActionsProps) {
  const [reviewing, setReviewing] = useState(false)
  const [error, setError] = useState('')

  async function handleReview(decision: ReviewDecision) {
    if (reviewing || proposal.status !== 'pending_review') return

    const action = decision === 'approve' ? 'approve' : 'reject'

    const confirmed = window.confirm(
      `Are you sure you want to ${action} proposal #${proposal.id}?`
    )

    if (!confirmed) return

    setReviewing(true)
    setError('')

    try {
      const updatedProposal = await reviewOrderProposal(
        proposal.id,
        decision
      )

      onReviewed(updatedProposal)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Could not review proposal'
      )
    } finally {
      setReviewing(false)
    }
  }

  return (
    <div className="mt-5">
      {proposal.status === 'pending_review' ? (
        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            onClick={() => handleReview('approve')}
            disabled={reviewing}
            className="cursor-pointer rounded-lg bg-green-600 px-5 py-3 font-medium text-white transition-colors hover:bg-green-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {reviewing ? 'Processing...' : 'Approve'}
          </button>

          <button
            type="button"
            onClick={() => handleReview('reject')}
            disabled={reviewing}
            className="cursor-pointer rounded-lg bg-red-600 px-5 py-3 font-medium text-white transition-colors hover:bg-red-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {reviewing ? 'Processing...' : 'Reject'}
          </button>
        </div>
      ) : (
        <p className="text-sm text-slate-300">
          Proposal status:{' '}
          <span className="font-semibold capitalize">
            {proposal.status.replaceAll('_', ' ')}
          </span>
        </p>
      )}

      {error && (
        <div
          role="alert"
          className="mt-4 rounded-lg border border-red-800 bg-red-950 p-4 text-red-300"
        >
          {error}
        </div>
      )}

      <p className="mt-4 text-xs text-slate-500">
        Reviewing a proposal updates its database status only.
        No inventory is reserved, no payment is charged,
        and no supplier purchase is executed.
      </p>
    </div>
  )
}

export default ApprovalActions

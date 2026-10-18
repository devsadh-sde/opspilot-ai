
import { useState } from 'react'

import {
  analyzeCustomerRequest,
  createOrderProposal,
} from '../services/api'

import type { SavedProposal } from '../services/api'
import type { OrderGraphResult } from '../types/order'

import FulfillmentTable from '../components/orders/FulfillmentTable'
import PricingSummary from '../components/orders/PricingSummary'
import PolicyEvaluation from '../components/orders/PolicyEvaluation'
import PolicyEvidence from '../components/orders/PolicyEvidence'
import ApprovalActions from '../components/orders/ApprovalActions'

function Dashboard() {
  const [message, setMessage] = useState('')
  const [analysis, setAnalysis] = useState<OrderGraphResult | null>(null)

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const [saving, setSaving] = useState(false)
  const [saveError, setSaveError] = useState('')
  const [savedProposal, setSavedProposal] =
    useState<SavedProposal | null>(null)

  async function handleAnalyze() {
    if (!message.trim() || loading || saving) return

    setLoading(true)
    setError('')
    setSaveError('')
    setAnalysis(null)
    setSavedProposal(null)

    try {
      const result = await analyzeCustomerRequest(message.trim())
      setAnalysis(result)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Something went wrong'
      )
    } finally {
      setLoading(false)
    }
  }

  async function handleSaveProposal() {
    if (
      !analysis ||
      analysis.status !== 'ready_for_review' ||
      analysis.approval_status !== 'pending_human_approval' ||
      saving ||
      loading ||
      savedProposal
    ) {
      return
    }

    setSaving(true)
    setSaveError('')

    try {
      const response = await createOrderProposal(
        analysis.customer_message
      )

      if (!response.saved || !response.proposal) {
        throw new Error(
          response.analysis?.status
            ? `Proposal not saved. Workflow status: ${response.analysis.status}`
            : 'The backend did not save this proposal.'
        )
      }

      setSavedProposal(response.proposal)
    } catch (err) {
      setSaveError(
        err instanceof Error
          ? err.message
          : 'Could not save proposal'
      )
    } finally {
      setSaving(false)
    }
  }

  const canSave =
    analysis?.status === 'ready_for_review' &&
    analysis.approval_status === 'pending_human_approval' &&
    !savedProposal

  return (
    <>
      <header className="mb-10">
        <h2 className="text-3xl font-semibold">
          Order Fulfillment Dashboard
        </h2>

        <p className="mt-2 text-slate-400">
          Analyze customer requests using AI agents.
        </p>
      </header>

      {/* Customer Request Form */}
      <section className="max-w-4xl rounded-xl border border-slate-800 bg-slate-900 p-6">
        <h3 className="text-xl font-semibold">
          New Customer Request
        </h3>

        <p className="mt-2 text-sm text-slate-400">
          Describe the product, quantity, delivery deadline,
          and budget.
        </p>

        <textarea
          className="mt-5 h-36 w-full resize-none rounded-lg border border-slate-700 bg-slate-950 p-4 text-white outline-none focus:border-blue-500"
          placeholder="I need 10 High-End Laptop units with a budget of $20000."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          disabled={loading || saving}
        />

        <button
          type="button"
          onClick={handleAnalyze}
          disabled={!message.trim() || loading || saving}
          className="mt-4 cursor-pointer rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition-colors hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? 'Analyzing...' : 'Analyze Request'}
        </button>
      </section>

      {/* Order Analysis Summary */}
      <section className="mt-8 max-w-4xl rounded-xl border border-slate-800 bg-slate-900 p-6">
        <h3 className="text-xl font-semibold">
          Order Analysis
        </h3>

        {loading && (
          <div className="mt-5 flex items-center gap-3 text-blue-400">
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-blue-400 border-t-transparent" />
            <span>Analyzing your request...</span>
          </div>
        )}

        {error && (
          <div
            role="alert"
            className="mt-5 rounded-lg border border-red-800 bg-red-950 p-4 text-red-300"
          >
            {error}
          </div>
        )}

        {analysis && (
          <div className="mt-5">
            <p className="mb-3 text-sm text-blue-400">
              Workflow status: {analysis.status.replaceAll('_', ' ')}
            </p>

            {analysis.question && (
              <div className="mb-4 rounded-lg border border-amber-800 bg-amber-950 p-4 text-amber-200">
                {analysis.question}
              </div>
            )}

            {analysis.order_analysis && (
              <div className="grid gap-4 sm:grid-cols-3">
                <div className="rounded-lg bg-slate-950 p-4">
                  <p className="text-sm text-slate-400">
                    Requested Units
                  </p>
                  <p className="mt-2 text-2xl font-bold">
                    {analysis.order_analysis.fulfillment.requested_quantity}
                  </p>
                </div>

                <div className="rounded-lg bg-slate-950 p-4">
                  <p className="text-sm text-slate-400">
                    Available Allocation
                  </p>
                  <p className="mt-2 text-2xl font-bold">
                    {analysis.order_analysis.fulfillment.allocated_quantity}
                  </p>
                </div>

                <div className="rounded-lg bg-slate-950 p-4">
                  <p className="text-sm text-slate-400">
                    Order Subtotal
                  </p>
                  <p className="mt-2 text-2xl font-bold">
                    ${analysis.order_analysis.pricing.total_price}
                  </p>
                </div>
              </div>
            )}
          </div>
        )}

        {!loading && !error && !analysis && (
          <div className="py-12 text-center">
            <h4 className="text-lg font-medium">
              No analysis yet
            </h4>

            <p className="mt-2 text-sm text-slate-400">
              Submit a customer request to view inventory,
              supplier options, pricing, and policy checks.
            </p>
          </div>
        )}
      </section>

      {/* Fulfillment Allocation */}
      {analysis?.order_analysis?.fulfillment && (
        <div className="max-w-4xl">
          <FulfillmentTable
            fulfillment={analysis.order_analysis.fulfillment}
          />
        </div>
      )}

      {/* Pricing Summary */}
      {analysis?.order_analysis?.pricing && (
        <div className="max-w-4xl">
          <PricingSummary
            pricing={analysis.order_analysis.pricing}
          />
        </div>
      )}

      {/* Policy Evaluation */}
      {analysis?.policy_evaluation && (
        <div className="max-w-4xl">
          <PolicyEvaluation
            evaluation={analysis.policy_evaluation}
            approvalStatus={analysis.approval_status}
          />
        </div>
      )}

      {/* RAG Policy Evidence */}
      {analysis?.policies && analysis.policies.length > 0 && (
        <div className="max-w-4xl">
          <PolicyEvidence policies={analysis.policies} />
        </div>
      )}

      {/* Save and Review Proposal */}
      {analysis && (
        <section className="mt-6 max-w-4xl rounded-xl border border-slate-800 bg-slate-900 p-6">
          <h3 className="text-xl font-semibold">
            Order Proposal
          </h3>

          <p className="mt-2 text-sm text-slate-400">
            Save an eligible order for human review.
            Review actions update the proposal status only.
          </p>

          {canSave && (
            <button
              type="button"
              onClick={handleSaveProposal}
              disabled={saving || loading}
              className="mt-5 cursor-pointer rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition-colors hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {saving ? 'Saving Proposal...' : 'Save Proposal'}
            </button>
          )}

          {savedProposal && (
            <div className="mt-5 rounded-lg border border-slate-700 bg-slate-950 p-5">
              <p className="text-lg font-semibold text-green-400">
                Proposal #{savedProposal.id}
              </p>

              <p className="mt-2 text-sm text-slate-300">
                Status: {savedProposal.status.replaceAll('_', ' ')}
              </p>

              <ApprovalActions
                proposal={savedProposal}
                onReviewed={(updatedProposal) => {
                  setSavedProposal(updatedProposal)
                }}
              />
            </div>
          )}

          {saveError && (
            <div
              role="alert"
              className="mt-5 rounded-lg border border-red-800 bg-red-950 p-4 text-red-300"
            >
              {saveError}
            </div>
          )}

          {!canSave && !savedProposal && !saveError && (
            <p className="mt-5 text-sm text-amber-300">
              This analysis is not eligible to be saved
              for human review.
            </p>
          )}
        </section>
      )}

      {/* Full Workflow JSON */}
      {analysis && (
        <details className="mt-6 max-w-4xl rounded-lg border border-slate-700 p-4">
          <summary className="cursor-pointer text-sm font-medium text-slate-300">
            View full workflow JSON
          </summary>

          <pre className="mt-4 max-h-[500px] overflow-auto rounded-lg bg-slate-950 p-4 text-xs text-green-300">
            {JSON.stringify(analysis, null, 2)}
          </pre>
        </details>
      )}
    </>
  )
}

export default Dashboard

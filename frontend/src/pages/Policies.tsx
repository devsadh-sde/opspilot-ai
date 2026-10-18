
import { useState } from 'react'

import { searchPolicies } from '../services/api'
import type { PolicySearchResponse } from '../services/api'

function Policies() {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState<PolicySearchResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSearch(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const searchQuery = query.trim()

    if (!searchQuery || loading) return

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await searchPolicies(searchQuery, 5)
      setResult(response)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Could not search policies.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="max-w-5xl">
      {/* Page Header */}
      <header>
        <h2 className="text-3xl font-semibold">
          Business Policies
        </h2>

        <p className="mt-3 text-slate-400">
          Search Northstar Electronics fulfillment policies
          using natural-language questions.
        </p>
      </header>

      {/* Policy Search Form */}
      <div className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-6">
        <h3 className="text-xl font-semibold">
          Policy Knowledge Base
        </h3>

        <p className="mt-2 text-sm text-slate-400">
          Find relevant company policies using semantic search.
        </p>

        <form onSubmit={handleSearch} className="mt-5">
          <label
            htmlFor="policy-query"
            className="mb-2 block text-sm font-medium text-slate-300"
          >
            Ask a policy question
          </label>

          <textarea
            id="policy-query"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="When is manager approval required for supplier procurement?"
            maxLength={1000}
            rows={3}
            disabled={loading}
            className="w-full resize-none rounded-lg border border-slate-700 bg-slate-950 p-4 text-white outline-none focus:border-blue-500 disabled:opacity-60"
          />

          <button
            type="submit"
            disabled={!query.trim() || loading}
            className="mt-4 cursor-pointer rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition-colors hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? 'Searching...' : 'Search Policies'}
          </button>
        </form>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="mt-6 flex items-center gap-3 text-blue-400">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-blue-400 border-t-transparent" />
          <span>Searching the policy knowledge base...</span>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div
          role="alert"
          className="mt-6 rounded-lg border border-red-800 bg-red-950 p-4 text-red-300"
        >
          {error}
        </div>
      )}

      {/* Search Results */}
      {result && (
        <section className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-6">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h3 className="text-xl font-semibold">
              Search Results
            </h3>

            <span className="rounded-full bg-blue-950 px-3 py-1 text-sm text-blue-300">
              {result.total_results} results
            </span>
          </div>

          <p className="mt-3 text-sm text-slate-400">
            Showing relevant policy excerpts for:
          </p>

          <p className="mt-2 font-medium text-white">
            {result.query}
          </p>

          {result.policies.length === 0 ? (
            <p className="mt-6 text-sm text-amber-300">
              No policy excerpts were found.
            </p>
          ) : (
            <div className="mt-6 space-y-4">
              {result.policies.map((policy, index) => (
                <article
                  key={`${policy.metadata?.source ?? 'policy'}-${index}`}
                  className="rounded-lg border border-slate-800 bg-slate-950 p-5"
                >
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <h4 className="font-semibold text-blue-400">
                      Policy Reference {index + 1}
                    </h4>

                    <span className="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300">
                      Reference
                    </span>
                  </div>

                  <p className="mt-4 whitespace-pre-wrap text-sm leading-7 text-slate-300">
                    {policy.document}
                  </p>

                  <div className="mt-4 border-t border-slate-800 pt-3 text-xs text-slate-500">
                    Source: {policy.metadata?.source ?? 'Unknown'}
                  </div>
                </article>
              ))}
            </div>
          )}

          <p className="mt-5 text-xs text-slate-500">
            Results are retrieved using semantic similarity.
            They are source excerpts, not AI-generated answers.
          </p>
        </section>
      )}
    </section>
  )
}

export default Policies

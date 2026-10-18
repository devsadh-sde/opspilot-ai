
import type { PolicyEvidence as PolicyEvidenceResult } from '../../types/order'

type PolicyEvidenceProps = {
  policies: PolicyEvidenceResult[]
}

function PolicyEvidence({ policies }: PolicyEvidenceProps) {
  if (policies.length === 0) {
    return null
  }

  return (
    <section className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">
      <h3 className="text-xl font-semibold">
        Retrieved Policy Evidence
      </h3>

      <p className="mt-2 text-sm text-slate-400">
        Relevant Northstar Electronics policies retrieved
        from the RAG knowledge base.
      </p>

      <div className="mt-6 space-y-4">
        {policies.map((policy, index) => (
          <article
            key={`${policy.metadata?.source ?? 'policy'}-${policy.metadata?.section ?? index}-${index}`}
            className="rounded-lg border border-slate-800 bg-slate-950 p-5"
          >
            <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
              <h4 className="font-semibold text-blue-400">
                Policy Reference {index + 1}
              </h4>

              <span className="rounded-full bg-blue-950 px-3 py-1 text-xs text-blue-300">
                Retrieved Evidence
              </span>
            </div>

            <p className="whitespace-pre-wrap text-sm leading-7 text-slate-300">
              {policy.document}
            </p>

            {policy.metadata?.source && (
              <p className="mt-4 border-t border-slate-800 pt-3 text-xs text-slate-500">
                Source: {policy.metadata.source}
              </p>
            )}
          </article>
        ))}
      </div>

      <p className="mt-5 text-xs text-slate-500">
        Retrieved policy excerpts provide supporting context.
        The backend separately evaluates approval requirements.
      </p>
    </section>
  )
}

export default PolicyEvidence

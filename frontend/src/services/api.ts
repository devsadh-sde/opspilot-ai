
import type {
  OrderGraphResult,
  InventoryResult,
  SupplierResult,
  PolicyEvidence,
} from '../types/order'

// -----------------------------
// Customer Request Analysis
// -----------------------------

export async function analyzeCustomerRequest(
  message: string
): Promise<OrderGraphResult> {
  const response = await fetch('/requests/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message }),
  })

  if (!response.ok) {
    throw new Error(`Analysis failed: HTTP ${response.status}`)
  }

  return response.json()
}

// -----------------------------
// Order Proposal Types
// -----------------------------

export interface SavedProposal {
  id: number
  product_id: number
  quantity: number
  status: string
  created_at: string
}

export interface CreateProposalResponse {
  saved: boolean
  proposal?: SavedProposal
  analysis?: OrderGraphResult
}

export interface ProposalDetail extends SavedProposal {
  analysis: OrderGraphResult
}

export type ReviewDecision = 'approve' | 'reject'

// -----------------------------
// Order Proposal APIs
// -----------------------------

export async function createOrderProposal(
  message: string
): Promise<CreateProposalResponse> {
  const response = await fetch('/orders/proposals', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message }),
  })

  if (!response.ok) {
    throw new Error(
      `Could not create proposal: HTTP ${response.status}`
    )
  }

  return response.json()
}

export async function getAllOrderProposals(): Promise<SavedProposal[]> {
  const response = await fetch('/orders/proposals')

  if (!response.ok) {
    throw new Error(
      `Could not load proposals: HTTP ${response.status}`
    )
  }

  return response.json()
}

export async function getOrderProposal(
  proposalId: number
): Promise<ProposalDetail> {
  const response = await fetch(
    `/orders/proposals/${proposalId}`
  )

  if (!response.ok) {
    throw new Error(
      `Could not load proposal: HTTP ${response.status}`
    )
  }

  return response.json()
}

export async function reviewOrderProposal(
  proposalId: number,
  decision: ReviewDecision
): Promise<SavedProposal> {
  const response = await fetch(
    `/orders/proposals/${proposalId}/review`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ decision }),
    }
  )

  if (!response.ok) {
    throw new Error(
      `Could not ${decision} proposal: HTTP ${response.status}`
    )
  }

  return response.json()
}

// -----------------------------
// Inventory APIs
// -----------------------------

export async function getInventory(
  productId: number
): Promise<InventoryResult> {
  const response = await fetch(`/inventory/${productId}`)

  if (!response.ok) {
    throw new Error(
      `Could not load inventory: HTTP ${response.status}`
    )
  }

  return response.json()
}

export async function getSuppliers(
  productId: number
): Promise<SupplierResult> {
  const response = await fetch(`/suppliers/${productId}`)

  if (!response.ok) {
    throw new Error(
      `Could not load suppliers: HTTP ${response.status}`
    )
  }

  return response.json()
}

// -----------------------------
// Policy Search API
// -----------------------------

export interface PolicySearchResponse {
  query: string
  total_results: number
  policies: PolicyEvidence[]
}

export async function searchPolicies(
  query: string,
  topK: number = 5
): Promise<PolicySearchResponse> {
  const response = await fetch('/policies/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query,
      top_k: topK,
    }),
  })

  if (!response.ok) {
    throw new Error(
      `Policy search failed: HTTP ${response.status}`
    )
  }

  return response.json()
}

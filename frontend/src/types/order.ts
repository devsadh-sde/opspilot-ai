
export interface WarehouseInventory {
  warehouse_id: number
  quantity: number
}

export interface InventoryResult {
  product_id: number
  total_quantity: number
  warehouses: WarehouseInventory[]
}

export interface SupplierOffer {
  supplier_id: number
  available_quantity: number
  unit_cost: string
  lead_time_days: number
}

export interface SupplierResult {
  product_id: number
  suppliers: SupplierOffer[]
}

export interface Allocation {
  source: 'warehouse' | 'supplier'
  source_id: number
  quantity: number
  unit_cost?: string
  lead_time_days?: number
}

export interface FulfillmentPlan {
  product_id: number
  requested_quantity: number
  allocated_quantity: number
  unfulfilled_quantity: number
  status: string
  allocations: Allocation[]
}

export interface PricingResult {
  product_id: number
  quantity: number
  unit_price: string
  total_price: string
  budget: string | null
  within_budget: boolean | null
}

export interface OrderAnalysis {
  status: string
  fulfillment: FulfillmentPlan
  pricing: PricingResult
}

export interface PolicyEvidence {
  document: string
  metadata: {
    source: string
    section: number
  }
  distance: number
}

export interface PolicyEvaluation {
  supplier_procurement_cost: string
  manager_approval_required: boolean
  customer_confirmation_required: boolean
  human_approval_required: boolean
  stock_sufficient: boolean
  eligible_for_approval: boolean
}

export interface OrderGraphResult {
  customer_message: string
  product_name?: string | null
  product_id?: number
  quantity?: number | null
  budget?: string | null
  deadline?: string | null
  status: string
  question?: string | null
  inventory?: InventoryResult
  suppliers?: SupplierResult
  order_analysis?: OrderAnalysis
  policies?: PolicyEvidence[]
  policy_evaluation?: PolicyEvaluation
  approval_status?: string
}

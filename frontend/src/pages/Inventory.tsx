
import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'

import { getInventory, getSuppliers } from '../services/api'
import type { InventoryResult } from '../types/order'

type SupplierOffer = {
  supplier_id: number
  available_quantity: number
  unit_cost: string
  lead_time_days: number
}

type SupplierApiResponse = {
  product_id: number
  offers: SupplierOffer[]
}

function Inventory() {
  const [productId, setProductId] = useState('1')

  const [inventory, setInventory] =
    useState<InventoryResult | null>(null)

  const [suppliers, setSuppliers] =
    useState<SupplierApiResponse | null>(null)

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // Load inventory when the page first opens.
  useEffect(() => {
    let cancelled = false

    async function loadInitialInventory() {
      try {
        const [inventoryData, supplierData] = await Promise.all([
          getInventory(1),
          getSuppliers(1),
        ])

        if (!cancelled) {
          setInventory(inventoryData)
          setSuppliers(
            supplierData as unknown as SupplierApiResponse
          )
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : 'Could not load inventory data.'
          )
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    void loadInitialInventory()

    return () => {
      cancelled = true
    }
  }, [])

  // Load inventory when a user searches for a product.
  async function loadData(id: number) {
    setLoading(true)
    setError('')
    setInventory(null)
    setSuppliers(null)

    try {
      const [inventoryData, supplierData] = await Promise.all([
        getInventory(id),
        getSuppliers(id),
      ])

      setInventory(inventoryData)
      setSuppliers(
        supplierData as unknown as SupplierApiResponse
      )
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Could not load inventory data.'
      )
    } finally {
      setLoading(false)
    }
  }

  function handleSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const id = Number(productId)

    if (!Number.isSafeInteger(id) || id <= 0) {
      setError('Please enter a valid positive product ID.')
      return
    }

    void loadData(id)
  }

  const supplierOffers = suppliers?.offers ?? []

  const totalSupplierStock = supplierOffers.reduce(
    (total, offer) => total + offer.available_quantity,
    0
  )

  const formatCurrency = (value: string | number) =>
    new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(Number(value))

  return (
    <section className="max-w-5xl">
      {/* Page Header */}
      <header>
        <h2 className="text-3xl font-semibold">
          Inventory Management
        </h2>

        <p className="mt-3 text-slate-400">
          Monitor warehouse quantities and supplier availability.
        </p>
      </header>

      {/* Product Search */}
      <form
        onSubmit={handleSearch}
        className="mt-8 flex flex-wrap gap-3 rounded-xl border border-slate-800 bg-slate-900 p-6"
      >
        <label className="flex flex-1 flex-col gap-2 text-sm text-slate-300">
          Product ID

          <input
            type="number"
            min="1"
            step="1"
            value={productId}
            onChange={(event) => setProductId(event.target.value)}
            className="rounded-lg border border-slate-700 bg-slate-950 p-3 text-white outline-none focus:border-blue-500"
          />
        </label>

        <button
          type="submit"
          disabled={loading}
          className="self-end cursor-pointer rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition-colors hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? 'Loading...' : 'Load Inventory'}
        </button>
      </form>

      {/* Loading */}
      {loading && (
        <div className="mt-6 flex items-center gap-3 text-blue-400">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-blue-400 border-t-transparent" />
          <span>Loading inventory and supplier information...</span>
        </div>
      )}

      {/* Error */}
      {error && (
        <div
          role="alert"
          className="mt-6 rounded-lg border border-red-800 bg-red-950 p-4 text-red-300"
        >
          {error}
        </div>
      )}

      {/* Inventory Results */}
      {!loading && inventory && suppliers && (
        <>
          {/* Summary Cards */}
          <div className="mt-6 grid gap-4 sm:grid-cols-3">
            <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
              <p className="text-sm text-slate-400">
                Warehouse Stock
              </p>

              <p className="mt-2 text-3xl font-bold">
                {inventory.total_quantity}
              </p>
            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
              <p className="text-sm text-slate-400">
                Supplier Availability
              </p>

              <p className="mt-2 text-3xl font-bold">
                {totalSupplierStock}
              </p>
            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
              <p className="text-sm text-slate-400">
                Potential Total Supply
              </p>

              <p className="mt-2 text-3xl font-bold text-blue-400">
                {inventory.total_quantity + totalSupplierStock}
              </p>
            </div>
          </div>

          {/* Warehouse Inventory */}
          <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">
            <h3 className="text-xl font-semibold">
              Warehouse Inventory
            </h3>

            <div className="mt-5 overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="border-b border-slate-700 text-slate-400">
                  <tr>
                    <th className="px-4 py-3">
                      Warehouse ID
                    </th>

                    <th className="px-4 py-3">
                      Available Units
                    </th>
                  </tr>
                </thead>

                <tbody>
                  {inventory.warehouses.map((warehouse) => (
                    <tr
                      key={warehouse.warehouse_id}
                      className="border-b border-slate-800"
                    >
                      <td className="px-4 py-4">
                        Warehouse #{warehouse.warehouse_id}
                      </td>

                      <td className="px-4 py-4 font-semibold text-green-400">
                        {warehouse.quantity}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {inventory.warehouses.length === 0 && (
                <p className="mt-5 text-sm text-slate-400">
                  No warehouse inventory found.
                </p>
              )}
            </div>
          </div>

          {/* Supplier Availability */}
          <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">
            <h3 className="text-xl font-semibold">
              Supplier Availability
            </h3>

            <div className="mt-5 overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="border-b border-slate-700 text-slate-400">
                  <tr>
                    <th className="px-4 py-3">
                      Supplier ID
                    </th>

                    <th className="px-4 py-3">
                      Available Units
                    </th>

                    <th className="px-4 py-3">
                      Unit Cost
                    </th>

                    <th className="px-4 py-3">
                      Lead Time
                    </th>
                  </tr>
                </thead>

                <tbody>
                  {supplierOffers.map((offer) => (
                    <tr
                      key={offer.supplier_id}
                      className="border-b border-slate-800"
                    >
                      <td className="px-4 py-4">
                        Supplier #{offer.supplier_id}
                      </td>

                      <td className="px-4 py-4 font-semibold text-green-400">
                        {offer.available_quantity}
                      </td>

                      <td className="px-4 py-4">
                        {formatCurrency(offer.unit_cost)}
                      </td>

                      <td className="px-4 py-4">
                        {offer.lead_time_days} days
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {supplierOffers.length === 0 && (
                <p className="mt-5 text-sm text-slate-400">
                  No supplier offers found.
                </p>
              )}
            </div>
          </div>

          <p className="mt-5 text-xs text-slate-500">
            Inventory quantities are retrieved from SQLite.
            Supplier availability is not guaranteed.
            No stock is reserved by this page.
          </p>
        </>
      )}
    </section>
  )
}

export default Inventory


type SidebarProps = {
  activePage: string
  setActivePage: (page: string) => void
}

const pages = [
  'Dashboard',
  'Order Proposals',
  'Inventory',
  'Policies',
]

function Sidebar({ activePage, setActivePage }: SidebarProps) {
  return (
    <aside className="w-64 shrink-0 border-r border-slate-800 bg-slate-900 p-6">
      <h1 className="text-2xl font-bold text-blue-400">
        OpsPilot AI
      </h1>

      <p className="mt-2 text-sm text-slate-400">
        Northstar Electronics
      </p>

      <nav className="mt-10 space-y-2">
        {pages.map((page) => (
          <button
            key={page}
            type="button"
            onClick={() => setActivePage(page)}
            className={`w-full cursor-pointer rounded-lg p-3 text-left font-medium transition-all duration-200 ${
              activePage === page
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/30'
                : 'text-slate-400 hover:bg-slate-800 hover:text-white'
            }`}
          >
            {page}
          </button>
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar

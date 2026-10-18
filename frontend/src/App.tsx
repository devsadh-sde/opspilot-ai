
import { useState } from 'react'

import Sidebar from './components/layout/Sidebar'
import Dashboard from './pages/Dashboard'
import OrderProposals from './pages/OrderProposals'
import Inventory from './pages/Inventory'
import Policies from './pages/Policies'

function App() {
  const [activePage, setActivePage] = useState('Dashboard')

  return (
    <div className="flex min-h-screen bg-slate-950 text-white">
      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
      />

      <main className="min-w-0 flex-1 p-8">
        {activePage === 'Dashboard' && <Dashboard />}
        {activePage === 'Order Proposals' && <OrderProposals />}
        {activePage === 'Inventory' && <Inventory />}
        {activePage === 'Policies' && <Policies />}
      </main>
    </div>
  )
}

export default App

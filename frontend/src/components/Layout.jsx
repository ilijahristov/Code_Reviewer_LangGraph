import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar.jsx'
import Header from './Header.jsx'

// Owns the collapsible-sidebar state and frames every page.
export default function Layout() {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <div className="app">
      <Sidebar collapsed={collapsed} onToggle={() => setCollapsed((c) => !c)} />
      <div className="main">
        <Header collapsed={collapsed} onExpand={() => setCollapsed(false)} />
        <div className="content">
          <Outlet />
        </div>
      </div>
    </div>
  )
}

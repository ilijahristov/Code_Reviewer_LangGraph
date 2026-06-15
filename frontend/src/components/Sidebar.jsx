import { useEffect, useState } from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import { getRepositories } from '../api.js'

// Collapsible sidebar. The "chats" subsection lists repository names
// pulled from the repositories table; each links to /{name}.
export default function Sidebar({ collapsed, onToggle }) {
  const [repos, setRepos] = useState([])
  const location = useLocation()

  // Refetch when the route changes so a brand-new repo appears after its
  // first review without a manual refresh.
  useEffect(() => {
    getRepositories()
      .then(setRepos)
      .catch(() => setRepos([]))
  }, [location.pathname])

  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-head">
        <button className="icon-btn" onClick={onToggle} title="Collapse sidebar" aria-label="Toggle sidebar">
          ☰
        </button>
        {!collapsed && <span className="brand">PR Reviewer</span>}
      </div>

      {!collapsed && (
        <>
          <NavLink to="/" className="new-chat">
            + New review
          </NavLink>

          <div className="section-label">Chats</div>
          <nav className="chat-list">
            {repos.map((r) => (
              <NavLink
                key={r.id}
                to={`/${encodeURIComponent(r.name)}`}
                className={({ isActive }) => `chat-item ${isActive ? 'active' : ''}`}
                title={r.url}
              >
                <span className="chat-dot" />
                <span className="chat-name">{r.name}</span>
              </NavLink>
            ))}
            {repos.length === 0 && <div className="empty">No chats yet</div>}
          </nav>
        </>
      )}
    </aside>
  )
}

import { useLocation } from 'react-router-dom'

// Top bar showing which chat you're on. On "/" it shows "New review";
// on "/{repoName}" it shows the repository name.
export default function Header({ collapsed, onExpand }) {
  const { pathname } = useLocation()
  const repoName = pathname === '/' ? null : decodeURIComponent(pathname.slice(1))

  return (
    <header className="header">
      {collapsed && (
        <button className="icon-btn" onClick={onExpand} title="Open sidebar" aria-label="Open sidebar">
          ☰
        </button>
      )}
      <h1 className="header-title">{repoName || 'New review'}</h1>
    </header>
  )
}

// Thin wrapper around the FastAPI backend. URLs are relative because the
// Vite dev server proxies them to http://127.0.0.1:8000 (see vite.config.js).

async function http(path, options) {
  const res = await fetch(path, options)
  if (!res.ok) {
    throw new Error(`Request failed (${res.status})`)
  }
  return res.json()
}

// Sidebar: list of repositories (each becomes a "chat").
export function getRepositories() {
  return http('/repositories')
}

// Chat page: all reviews for one repository, oldest first.
export function getReviews(repoName) {
  return http(`/repositories/${encodeURIComponent(repoName)}/reviews`)
}

// Submit a new PR for review (pr_url is a query param on the backend).
export function submitReview(prUrl) {
  return http(`/review?pr_url=${encodeURIComponent(prUrl)}`, { method: 'POST' })
}

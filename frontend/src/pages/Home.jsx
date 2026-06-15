import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { submitReview } from '../api.js'
import ChatInput from '../components/ChatInput.jsx'

// Landing page (route "/"): a centered input for a PR URL. On submit we run
// the review, derive the repo name from the response, and move to /{repoName}.
export default function Home() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(prUrl) {
    setLoading(true)
    setError(null)
    try {
      const data = await submitReview(prUrl)
      const repoUrl = data?.review_summary?.repo_url || ''
      const repoName = repoUrl.replace(/\/$/, '').split('/').pop()
      if (repoName) {
        navigate(`/${encodeURIComponent(repoName)}`)
      } else {
        setError('Could not determine the repository from the response.')
      }
    } catch (e) {
      setError('Review failed. Make sure the backend is running on :8000.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="home">
      <div className="home-hero">
        <h2>Review a pull request</h2>
        <p className="subtle">Paste a GitHub PR URL and the agents will review it.</p>
        <ChatInput
          onSubmit={handleSubmit}
          loading={loading}
          placeholder="Paste a GitHub PR URL, e.g. https://github.com/owner/repo/pull/123"
          autoFocus
        />
        {loading && <div className="hint">Running the review… this can take a moment.</div>}
        {error && <div className="error">{error}</div>}
      </div>
    </div>
  )
}

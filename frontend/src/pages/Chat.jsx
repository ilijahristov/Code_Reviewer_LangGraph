import { useEffect, useRef, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getReviews, submitReview } from '../api.js'
import Message from '../components/Message.jsx'
import ChatInput from '../components/ChatInput.jsx'

// Conversation page (route "/:repoName"): a scrollable message area with the
// review history, and the input pinned to the bottom.
export default function Chat() {
  const { repoName } = useParams()
  const [reviews, setReviews] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const bottomRef = useRef(null)

  async function load() {
    try {
      const data = await getReviews(repoName)
      setReviews(Array.isArray(data) ? data : [])
    } catch {
      setReviews([])
    }
  }

  useEffect(() => {
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [repoName])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [reviews, loading])

  async function handleSubmit(prUrl) {
    setLoading(true)
    setError(null)
    try {
      await submitReview(prUrl)
      await load()
    } catch {
      setError('Review failed. Make sure the backend is running on :8000.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat">
      <div className="messages">
        {reviews.length === 0 && !loading && (
          <div className="empty-chat">No reviews yet for this repository. Paste a PR URL below to start.</div>
        )}

        {reviews.map((r, i) => (
          <div key={i} className="turn">
            <Message role="human" review={r} />
            <Message role="ai" review={r} />
          </div>
        ))}

        {loading && <Message role="ai" loading />}
        <div ref={bottomRef} />
      </div>

      <div className="chat-input-wrap">
        <ChatInput onSubmit={handleSubmit} loading={loading} placeholder="Paste another PR URL to review…" />
        {error && <div className="error">{error}</div>}
      </div>
    </div>
  )
}

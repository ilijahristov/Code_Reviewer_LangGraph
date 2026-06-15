// A single chat bubble.
//   role="human" -> right-aligned, shows the PR URL that was submitted
//   role="ai"    -> left-aligned, renders the structured OverallReview
export default function Message({ role, review, loading }) {
  if (role === 'human') {
    return (
      <div className="msg-row right">
        <div className="bubble human">
          <div className="pr-label">Review request</div>
          <a href={review.pr_url} target="_blank" rel="noreferrer">
            {review.pr_url}
          </a>
        </div>
      </div>
    )
  }

  return (
    <div className="msg-row left">
      <div className="bubble ai">
        {loading ? <span className="typing">Reviewing the pull request…</span> : <ReviewCard review={review} />}
      </div>
    </div>
  )
}

function ReviewCard({ review }) {
  const overall = review.final_summary

  // Fallback if the structured summary isn't available.
  if (!overall || typeof overall !== 'object') {
    return <div>{review.title || 'Review complete.'}</div>
  }

  return (
    <div className="review-card">
      {review.title && <div className="review-title">{review.title}</div>}

      <div className="badges">
        {overall.verdict && (
          <span className={`badge verdict ${overall.verdict}`}>{overall.verdict.replace(/_/g, ' ')}</span>
        )}
        {overall.overall_severity && (
          <span className={`badge sev ${overall.overall_severity}`}>{overall.overall_severity}</span>
        )}
      </div>

      {overall.summary && <p className="summary-text">{overall.summary}</p>}

      <ListBlock title="Key issues" items={overall.key_issues} />
      <ListBlock title="Recommendations" items={overall.recommendations} />
      <ListBlock title="Strengths" items={overall.strengths} />
    </div>
  )
}

function ListBlock({ title, items }) {
  if (!items || items.length === 0) return null
  return (
    <div className="list-block">
      <h4>{title}</h4>
      <ul>
        {items.map((x, i) => (
          <li key={i}>{x}</li>
        ))}
      </ul>
    </div>
  )
}

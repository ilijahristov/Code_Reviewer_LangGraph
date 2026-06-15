import { useEffect, useRef, useState } from 'react'

// Reusable input row: an auto-growing textarea plus a send button.
// Enter submits, Shift+Enter inserts a newline.
export default function ChatInput({ onSubmit, loading, placeholder, autoFocus }) {
  const [value, setValue] = useState('')
  const ref = useRef(null)

  // Auto-grow the textarea up to a max height.
  useEffect(() => {
    const el = ref.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = Math.min(el.scrollHeight, 200) + 'px'
  }, [value])

  function submit() {
    const v = value.trim()
    if (!v || loading) return
    onSubmit(v)
    setValue('')
  }

  function onKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  return (
    <div className="chat-input">
      <textarea
        ref={ref}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={onKeyDown}
        placeholder={placeholder}
        rows={1}
        autoFocus={autoFocus}
      />
      <button
        className="send-btn"
        onClick={submit}
        disabled={loading || !value.trim()}
        title="Send"
        aria-label="Send"
      >
        {loading ? '…' : '↑'}
      </button>
    </div>
  )
}

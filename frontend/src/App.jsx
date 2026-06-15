import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout.jsx'
import Home from './pages/Home.jsx'
import Chat from './pages/Chat.jsx'

// Two pages share one layout (sidebar + header):
//   /            -> Home   (new review, centered input)
//   /:repoName   -> Chat   (conversation for one repository)
export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/:repoName" element={<Chat />} />
      </Route>
    </Routes>
  )
}

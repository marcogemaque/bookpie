import { useState } from 'react'
import axios from 'axios'
import { API_BASE_URL } from '../config'

function Login() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState(null)
  const [token, setToken] = useState(null)

  async function handleLogin() {
    try {
      const res = await axios.post(`${API_BASE_URL}/users/login`, {
        username,
        password
      })
      setToken(res.data.access_token)
      setError(null)
    } catch (err) {
      setError("Invalid credentials")
    }
  }

  if (token) return <h2>Logged in! Token: {token}</h2>

  return (
    <div>
      <h1>Bookworm</h1>
      <input
        placeholder="Username"
        value={username}
        onChange={e => setUsername(e.target.value)}
      />
      <br />
      <input
        placeholder="Password"
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <br />
      <button onClick={handleLogin}>Login</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  )
}

export default Login

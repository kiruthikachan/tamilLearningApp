import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { login } from "../services/auth"
function LoginPage()
{
    const navigate = useNavigate()
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState ("")
    const [error, setError] = useState ("")
    const [isLoading, setIsLoading] = useState(false)

    async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault()
        setError("")
        setIsLoading(true)
        try {
            await login(username,password)
            navigate ("/dashboard")
        } catch (error) {
            if (error instanceof Error) {
                setError (error.message)
            } else {
                setError ("Unable to log in.")
            }
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <main>
            <h1>Log in</h1>

            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="username">Username</label>
                    <input
                        id = "username"
                        type = "text"
                        value = {username}
                        onChange ={(event) => setUsername(event.target.value)}
                        autoComplete="username"
                        required
                    />
                </div>
                <div>
                    <label htmlFor="password">Password</label>
                    <input
                        id = "password"
                        type = "password"
                        value = {password}
                        onChange={(event) => setPassword(event.target.value)}
                        autoComplete="current-password"
                        required
                    />
                </div>
                {error && <p>{error}</p>}
                <button type="submit" disabled={isLoading}>
                    {isLoading ? "Logging in...": "Log in"}
                </button>
            </form>
        </main>
    )
}
export default LoginPage
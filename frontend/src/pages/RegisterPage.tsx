import React, {useState} from "react"
import { useNavigate } from "react-router-dom"
import { register } from "../services/auth"

function RegisterPage()
{
    const navigate = useNavigate()

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [email, setEmail] = useState("")
    const [error, setError] = useState("")
    const [isLoading, setIsLoading] = useState(false)

    async function handelSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault()
        setError("")
        setIsLoading(true)

        if (password !== confirmPassword) {
            setError("Passwords do not match.")
            setIsLoading(false)
            return
        }
        try {
            await register(username, email, password)
            navigate("/login")
        } catch (error) {
            if (error instanceof Error) {
                setError(error.message)
            } else {
                setError("Unable to create account.")
            }
        } finally {
            setIsLoading(false)
        }
    }
    return (
        <main>
            <h1>Create Account</h1>
            <form onSubmit={handelSubmit}>
                <div>
                    <label htmlFor="username">
                        Username
                    </label>
                    <input
                        id="username"
                        type="text"
                        value={username}
                        onChange={(event) => setUsername(event.target.value)}
                        autoComplete="username"
                        required
                    />
                </div>
                <div>
                    <label htmlFor="email">
                        Email
                    </label>
                    <input
                        id="email"
                        type="email"
                        value={email}
                        onChange={(event) => setEmail(event.target.value)}
                        autoComplete="email"
                        required
                    />
                </div>
                <div>
                    <label htmlFor="password">
                        Password
                    </label>
                    <input
                        id="password"
                        type="password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                        autoComplete="new-password"
                        required
                    />
                </div>
                <div>
                    <label htmlFor="confirm-password">
                        Confirm Password
                    </label>
                    <input
                        id="confirm-password"
                        type="password"
                        value={confirmPassword}
                        onChange={(event) => setConfirmPassword(event.target.value)}
                        autoComplete="new-password"
                        required
                    />
                </div>
                {error && <p>{error}</p>}
                <button
                    type="submit"
                    disabled={isLoading}
                >
                    {isLoading
                        ? "Creating account..."
                        : "Create account"}
                </button>
            </form>
        </main>
    )
}
export default RegisterPage
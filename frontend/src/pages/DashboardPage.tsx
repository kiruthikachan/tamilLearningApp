import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { getCurrentUser,logout } from "../services/auth"

type User = {
    id: number
    username: string
    email: string
}

function DashboardPage()
{
    const navigate = useNavigate()
    const [user, setUser] = useState<User | null>(null)
    const [isLoading, setIsLoading] = useState(true)

    async function handleLogout() {
    try {
        await logout()
        navigate("/login")
    }
    catch (error) {
        console.error(error)
    }
}

    useEffect(() => {
        async function loadCurrentUser() {
            try {
                const currentUser = await getCurrentUser()
                setUser(currentUser)
            } catch {
                navigate("/login")
            } finally {
                setIsLoading(false)
            }
        }
        loadCurrentUser()
    }, [navigate])
    if (isLoading) {
        return <p>Loading...</p>
    }
    return (
        <main>
            <h1>Dashboard</h1>
            <p>Welcome, {user?.username}</p>
            <button onClick={handleLogout}>
                Log out
            </button>
        </main>
    )
}
export default DashboardPage
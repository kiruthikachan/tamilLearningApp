const API_BASE_URL = "http://localhost:8000/api/v1"

function getCookie(name: string): string | null {
    const cookies = document.cookie.split(";")

    for (const cookie of cookies) {
        const trimmedCookie = cookie.trim()
        if (trimmedCookie.startsWith( `${name}=`)) {
            return decodeURIComponent (
                trimmedCookie.substring(name.length + 1)
            )
        }
    }
    return null
}

export async function getCsrfToken(): Promise<string> {
    const response = await fetch(
        `${API_BASE_URL}/auth/csrf/`,
        {
            method: "GET",
            credentials: "include",
        }
    )
    if (!response.ok) {
        throw new Error("Unable to initialize CSRF protection.")
    }
    const csrfToken = getCookie("csrftoken")
    if(!csrfToken) {
        throw new Error("CSRF token was not found.")
    }
    return csrfToken
}

export async function login (username:string, password: string) {
    const csrfToken = await getCsrfToken()
    const response = await fetch(
        `${API_BASE_URL}/auth/login/`,
        {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({
                username,
                password,
            }),
        }
    )
    const data = await response.json()

    if (!response.ok) {
        throw new Error(
            data.detail || "Unable to log in."
        )
    }
    return data
}

export async function getCurrentUser () {
    const response = await fetch(
        `${API_BASE_URL}/auth/me/`,
        {
            method: "GET",
            credentials: "include",
        }
    )
    if (!response.ok) {
        throw new Error("Unable to get current user.")
    }
    return response.json()
}

export async function logout() {
    const csrfToken = await getCsrfToken()
    const response = await fetch(
        `${API_BASE_URL}/auth/logout/`,
        {
            method: "POST",
            credentials: "include",
            headers: {
                "X-CSRFToken": csrfToken,
            },
        }
    )
    if (!response.ok) {
        throw new Error("Unable to log out.")
    }
}

export async function register(username: string, email: string, password: string){
    const csrfToken = await getCsrfToken()
    const response = await fetch(
        `${API_BASE_URL}/auth/register/`,
        {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({
                username,
                email,
                password,
            }),
        }
    )
    const data = await response.json()
    if(!response.ok) {
        const message = 
            data.email?.[0] ||
            data.username?.[0] ||
            data.password?.[0] ||
            data.detail ||
            "Unable to create account."
        throw new Error(message)
    }
    return data
}
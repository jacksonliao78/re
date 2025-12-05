export const API_URL = "http://localhost:8000/api";

export async function apiFetch( path: string, options: RequestInit = {} ) {
    const res = await fetch('${API_URL}${path}', options )

    if( !res.ok ) {
        const text = await res.text()
        throw new Error( 'API error: ${res.status} - ${text}' )
    }

    return res.json()
}
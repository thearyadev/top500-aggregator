
export async function fetchSeasonList(): Promise<string[]> {
    const response = await fetch("/api/d/seasons")
    return await response.json()
}


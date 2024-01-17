/** @type {import('next').NextConfig} */
const backendUrl = process.env.NODE_ENV === "development" ? "http://localhost:7771" : "http://server:8000"

const nextConfig = {
    async rewrites() {
        return [
            {
                source: "/api/:path*",
                destination: `${backendUrl}/:path*`
            }
        ]
    },
    env: {
        BACKEND_URL: backendUrl
    },
    compress: true
}

module.exports = nextConfig

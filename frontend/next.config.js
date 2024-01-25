/** @type {import('next').NextConfig} */
let backendUrl =
    process.env.NODE_ENV === "development"
        ? "http://localhost:7771"
        : "http://server:8000";

backendUrl = "http://localhost:7771";

const nextConfig = {
    env: {
        BACKEND_URL: backendUrl,
    },
    compress: true,
    output: "export",
};

module.exports = nextConfig;

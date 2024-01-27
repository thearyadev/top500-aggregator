/** @type {import('next').NextConfig} */

backendUrl = "http://localhost:7771";

const nextConfig = {
    env: {
        BACKEND_URL: backendUrl,
    },
    compress: true,
    output: "export",
};

module.exports = nextConfig;

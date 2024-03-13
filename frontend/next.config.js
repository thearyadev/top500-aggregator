/** @type {import('next').NextConfig} */
backendUrl = "http://localhost:7771";

const nextConfig = {
    env: {},
    compress: true,
    output: "export",
    images: {
        unoptimized: true
    }
};

module.exports = nextConfig;

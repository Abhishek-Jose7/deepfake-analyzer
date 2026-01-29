import type { NextConfig } from "next";

const nextConfig: NextConfig = {
    // Environment variables
    env: {
        NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:7860',
    },

    // Enable CORS for images from any domain (for heatmaps)
    images: {
        remotePatterns: [
            {
                protocol: 'https',
                hostname: '**',
            },
        ],
    },

    // Optimize for production
    output: 'standalone',

    // Disable x-powered-by header
    poweredByHeader: false,
};

export default nextConfig;

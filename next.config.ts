import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  turbopack: {
    root: __dirname,
  },
  images: {
    // Configure Sanity CDN for optimized image delivery
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.sanity.io',
        pathname: '/images/**',
      },
    ],
    // Optimize image formats for better compression
    formats: ['image/avif', 'image/webp'],
    // Configure device sizes for responsive images
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    // Configure image sizes for srcset generation
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    // Minimize Cumulative Layout Shift
    minimumCacheTTL: 60 * 60 * 24 * 365, // 1 year cache
  },
  // Production optimizations
  poweredByHeader: false, // Remove X-Powered-By header for security
  compress: true, // Enable gzip compression
  // Strict mode for production stability
  reactStrictMode: true,
  // Enable experimental features for performance
  experimental: {
    // Optimize package imports for smaller bundles
    optimizePackageImports: ['motion', '@sanity/icons'],
  },
};

export default nextConfig;

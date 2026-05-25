/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    serverActions: true,
  },
  async rewrites() {
    return [
      {
        source: '/api/scanner/:path*',
        destination: 'http://localhost:8080/:path*',
      },
    ];
  },
};

module.exports = nextConfig;

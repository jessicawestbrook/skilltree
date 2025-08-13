import { NextResponse } from 'next/server';

export async function GET() {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://neuroquest.app';
  const isDevelopment = process.env.NODE_ENV === 'development';

  const robotsTxt = `User-agent: *
${isDevelopment ? 'Disallow: /' : 'Allow: /'}

# Disallow authentication and private pages
Disallow: /api/
Disallow: /dashboard/
Disallow: /profile/
Disallow: /settings/
Disallow: /admin/
Disallow: /login
Disallow: /register
Disallow: /reset-password
Disallow: /verify-email

# Disallow temporary or test files
Disallow: /temp/
Disallow: /test/
Disallow: /_next/
Disallow: /static/

# Allow important pages
Allow: /
Allow: /about
Allow: /features
Allow: /contact
Allow: /node/
Allow: /domain/
Allow: /path/

# Crawl delay (optional - removes load on server)
Crawl-delay: 1

# Sitemap location
Sitemap: ${baseUrl}/sitemap.xml

# Additional sitemaps (if you have specialized ones)
Sitemap: ${baseUrl}/sitemap-nodes.xml
Sitemap: ${baseUrl}/sitemap-images.xml`;

  return new NextResponse(robotsTxt, {
    headers: {
      'Content-Type': 'text/plain',
      'Cache-Control': 'public, max-age=86400, s-maxage=86400', // Cache for 24 hours
    },
  });
}
import { NextResponse } from 'next/server';
import { getAllHierarchicalNodes } from '../../data/hierarchicalKnowledgeGraph';

interface SitemapEntry {
  url: string;
  lastModified: string;
  changeFrequency: 'always' | 'hourly' | 'daily' | 'weekly' | 'monthly' | 'yearly' | 'never';
  priority: number;
}

export async function GET() {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://neuroquest.app';
  const currentDate = new Date().toISOString();

  // Static pages
  const staticPages: SitemapEntry[] = [
    {
      url: `${baseUrl}/`,
      lastModified: currentDate,
      changeFrequency: 'weekly',
      priority: 1.0
    },
    {
      url: `${baseUrl}/about`,
      lastModified: currentDate,
      changeFrequency: 'monthly',
      priority: 0.8
    },
    {
      url: `${baseUrl}/features`,
      lastModified: currentDate,
      changeFrequency: 'monthly',
      priority: 0.7
    },
    {
      url: `${baseUrl}/contact`,
      lastModified: currentDate,
      changeFrequency: 'monthly',
      priority: 0.6
    },
    {
      url: `${baseUrl}/privacy`,
      lastModified: currentDate,
      changeFrequency: 'yearly',
      priority: 0.3
    },
    {
      url: `${baseUrl}/terms`,
      lastModified: currentDate,
      changeFrequency: 'yearly',
      priority: 0.3
    }
  ];

  // Dynamic pages - Learning nodes
  const expandedNodes = new Set<string>(); // Get all nodes
  const allNodes = getAllHierarchicalNodes(expandedNodes);
  
  const nodePages: SitemapEntry[] = allNodes
    .filter(node => !node.isParent) // Only include actual learning nodes, not parent categories
    .map(node => ({
      url: `${baseUrl}/node/${node.id}`,
      lastModified: currentDate,
      changeFrequency: 'weekly' as const,
      priority: 0.8
    }));

  // Domain pages
  const domains = [...new Set(allNodes.map(node => node.domain))];
  const domainPages: SitemapEntry[] = domains.map(domain => ({
    url: `${baseUrl}/domain/${domain}`,
    lastModified: currentDate,
    changeFrequency: 'weekly' as const,
    priority: 0.7
  }));

  // Learning path pages (if you have predefined paths)
  const learningPaths = [
    'mathematics-foundation',
    'science-basics',
    'technology-fundamentals',
    'critical-thinking',
    'communication-skills'
  ];
  
  const pathPages: SitemapEntry[] = learningPaths.map(pathId => ({
    url: `${baseUrl}/path/${pathId}`,
    lastModified: currentDate,
    changeFrequency: 'weekly' as const,
    priority: 0.8
  }));

  // Combine all pages
  const allPages = [...staticPages, ...nodePages, ...domainPages, ...pathPages];

  // Generate XML sitemap
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
${allPages.map(page => `  <url>
    <loc>${page.url}</loc>
    <lastmod>${page.lastModified}</lastmod>
    <changefreq>${page.changeFrequency}</changefreq>
    <priority>${page.priority}</priority>
  </url>`).join('\n')}
</urlset>`;

  return new NextResponse(sitemap, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, max-age=3600, s-maxage=3600', // Cache for 1 hour
    },
  });
}
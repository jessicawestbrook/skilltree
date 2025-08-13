'use client';

import Head from 'next/head';
import { generateWebsiteStructuredData, generateOrganizationStructuredData } from '../../utils/seo/structuredData';

interface SEOHeadProps {
  structuredData?: object[];
  additionalMeta?: Array<{
    name?: string;
    property?: string;
    content: string;
  }>;
  noIndex?: boolean;
  canonicalUrl?: string;
}

export function SEOHead({ 
  structuredData = [], 
  additionalMeta = [], 
  noIndex = false,
  canonicalUrl 
}: SEOHeadProps) {
  const websiteData = generateWebsiteStructuredData();
  const organizationData = generateOrganizationStructuredData();
  
  const allStructuredData = [
    websiteData,
    organizationData,
    ...structuredData
  ];

  return (
    <Head>
      {/* Structured Data */}
      {allStructuredData.map((data, index) => (
        <script
          key={`structured-data-${index}`}
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(data, null, 2)
          }}
        />
      ))}

      {/* Additional Meta Tags */}
      {additionalMeta.map((meta, index) => (
        <meta
          key={`additional-meta-${index}`}
          {...(meta.name && { name: meta.name })}
          {...(meta.property && { property: meta.property })}
          content={meta.content}
        />
      ))}

      {/* Robots meta tag */}
      {noIndex && <meta name="robots" content="noindex, nofollow" />}

      {/* Canonical URL */}
      {canonicalUrl && <link rel="canonical" href={canonicalUrl} />}

      {/* Preconnect to external domains for performance */}
      <link rel="preconnect" href="https://www.google-analytics.com" />
      <link rel="preconnect" href="https://www.googletagmanager.com" />
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />

      {/* DNS prefetch for faster loading */}
      <link rel="dns-prefetch" href="https://www.google-analytics.com" />
      <link rel="dns-prefetch" href="https://www.googletagmanager.com" />

      {/* Security headers */}
      <meta httpEquiv="X-Content-Type-Options" content="nosniff" />
      <meta httpEquiv="X-Frame-Options" content="DENY" />
      <meta httpEquiv="X-XSS-Protection" content="1; mode=block" />
      <meta httpEquiv="Referrer-Policy" content="strict-origin-when-cross-origin" />

      {/* Performance hints */}
      <meta httpEquiv="Accept-CH" content="DPR, Viewport-Width, Width, Save-Data" />
    </Head>
  );
}

export default SEOHead;
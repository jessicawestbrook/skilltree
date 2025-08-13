import { Metadata } from 'next';

export interface SEOConfig {
  title: string;
  description: string;
  keywords?: string[];
  image?: string;
  url?: string;
  type?: 'website' | 'article' | 'profile';
  publishedTime?: string;
  modifiedTime?: string;
  author?: string;
  section?: string;
  tags?: string[];
  noIndex?: boolean;
  noFollow?: boolean;
}

const DEFAULT_CONFIG = {
  siteName: 'NeuroQuest',
  siteUrl: process.env.NEXT_PUBLIC_SITE_URL || 'https://neuroquest.app',
  defaultTitle: 'NeuroQuest - Master All Human Knowledge',
  defaultDescription: 'An innovative interactive learning platform that transforms education through neural network visualization. Master knowledge across all domains with personalized learning paths.',
  defaultImage: '/og-image.jpg',
  twitterHandle: '@neuroquest',
  keywords: [
    'learning platform',
    'education',
    'knowledge graph',
    'interactive learning',
    'neural network',
    'gamified education',
    'skill development',
    'online courses',
    'personalized learning',
    'knowledge mastery'
  ]
};

export function generateMetadata({
  title,
  description,
  keywords = [],
  image,
  url,
  type = 'website',
  publishedTime,
  modifiedTime,
  author,
  section,
  tags = [],
  noIndex = false,
  noFollow = false
}: SEOConfig): Metadata {
  const fullTitle = title === DEFAULT_CONFIG.defaultTitle 
    ? title 
    : `${title} | ${DEFAULT_CONFIG.siteName}`;
  
  const fullUrl = url ? `${DEFAULT_CONFIG.siteUrl}${url}` : DEFAULT_CONFIG.siteUrl;
  const imageUrl = image ? `${DEFAULT_CONFIG.siteUrl}${image}` : `${DEFAULT_CONFIG.siteUrl}${DEFAULT_CONFIG.defaultImage}`;
  
  const allKeywords = [...DEFAULT_CONFIG.keywords, ...keywords, ...tags].join(', ');

  const robots = [];
  if (noIndex) robots.push('noindex');
  if (noFollow) robots.push('nofollow');
  if (robots.length === 0) robots.push('index', 'follow');

  const metadata: Metadata = {
    title: fullTitle,
    description,
    keywords: allKeywords,
    robots: robots.join(', '),
    
    // Open Graph
    openGraph: {
      title: fullTitle,
      description,
      url: fullUrl,
      siteName: DEFAULT_CONFIG.siteName,
      images: [
        {
          url: imageUrl,
          width: 1200,
          height: 630,
          alt: fullTitle,
        }
      ],
      locale: 'en_US',
      type,
      ...(publishedTime && { publishedTime }),
      ...(modifiedTime && { modifiedTime }),
      ...(author && { authors: [author] }),
      ...(section && { section }),
      ...(tags.length > 0 && { tags })
    },

    // Twitter
    twitter: {
      card: 'summary_large_image',
      title: fullTitle,
      description,
      images: [imageUrl],
      creator: DEFAULT_CONFIG.twitterHandle,
      site: DEFAULT_CONFIG.twitterHandle,
    },

    // Additional metadata
    alternates: {
      canonical: fullUrl,
    },

    // App metadata
    applicationName: DEFAULT_CONFIG.siteName,
    authors: author ? [{ name: author }] : [{ name: 'NeuroQuest Team' }],
    creator: 'NeuroQuest Team',
    publisher: 'NeuroQuest',
    category: 'Education',

    // Icons
    icons: {
      icon: [
        { url: '/favicon-16x16.png', sizes: '16x16', type: 'image/png' },
        { url: '/favicon-32x32.png', sizes: '32x32', type: 'image/png' },
        { url: '/favicon.svg', type: 'image/svg+xml' }
      ],
      apple: [
        { url: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' }
      ],
      other: [
        { rel: 'mask-icon', url: '/safari-pinned-tab.svg', color: '#667eea' }
      ]
    },

    // Manifest
    manifest: '/manifest.json',

    // Verification
    verification: {
      google: process.env.GOOGLE_SITE_VERIFICATION,
      yandex: process.env.YANDEX_VERIFICATION,
      yahoo: process.env.YAHOO_VERIFICATION,
      other: {
        'msvalidate.01': process.env.BING_VERIFICATION || '',
      },
    },

    // Apple Web App
    appleWebApp: {
      capable: true,
      title: DEFAULT_CONFIG.siteName,
      statusBarStyle: 'default',
    },

    // Format detection
    formatDetection: {
      telephone: false,
      date: false,
      address: false,
      email: false,
      url: false,
    },

    // Other
    referrer: 'origin-when-cross-origin',
  };

  return metadata;
}

// Predefined metadata generators for common pages
export const homePageMetadata = (): Metadata => 
  generateMetadata({
    title: DEFAULT_CONFIG.defaultTitle,
    description: DEFAULT_CONFIG.defaultDescription,
    keywords: ['homepage', 'getting started', 'features'],
    url: '/',
  });

export const aboutPageMetadata = (): Metadata =>
  generateMetadata({
    title: 'About NeuroQuest - Revolutionary Learning Platform',
    description: 'Learn about NeuroQuest\'s mission to revolutionize education through interactive neural network visualization and gamified learning experiences.',
    keywords: ['about', 'mission', 'vision', 'team', 'education revolution'],
    url: '/about',
  });

export const dashboardMetadata = (): Metadata =>
  generateMetadata({
    title: 'Learning Dashboard - Track Your Progress',
    description: 'Monitor your learning journey with detailed progress tracking, achievement badges, and personalized recommendations on your NeuroQuest dashboard.',
    keywords: ['dashboard', 'progress', 'achievements', 'learning analytics'],
    url: '/dashboard',
    noIndex: true, // Private page
  });

export const loginMetadata = (): Metadata =>
  generateMetadata({
    title: 'Sign In to NeuroQuest',
    description: 'Access your personalized learning journey. Sign in to continue mastering knowledge across all domains with NeuroQuest.',
    keywords: ['login', 'sign in', 'access account'],
    url: '/login',
    noIndex: true,
  });

export const registerMetadata = (): Metadata =>
  generateMetadata({
    title: 'Join NeuroQuest - Start Your Learning Journey',
    description: 'Create your free NeuroQuest account and begin your personalized journey to master all human knowledge through interactive learning.',
    keywords: ['register', 'sign up', 'create account', 'join'],
    url: '/register',
  });

export const resetPasswordMetadata = (): Metadata =>
  generateMetadata({
    title: 'Reset Your Password - NeuroQuest',
    description: 'Reset your NeuroQuest account password to regain access to your personalized learning dashboard and continue your knowledge journey.',
    keywords: ['reset password', 'account recovery', 'forgot password'],
    url: '/reset-password',
    noIndex: true,
  });

export const verifyEmailMetadata = (): Metadata =>
  generateMetadata({
    title: 'Verify Your Email - NeuroQuest',
    description: 'Complete your NeuroQuest account setup by verifying your email address to unlock all learning features and personalization.',
    keywords: ['verify email', 'email confirmation', 'account activation'],
    url: '/verify-email',
    noIndex: true,
  });

// Dynamic metadata generators
export const nodeMetadata = (nodeId: string, nodeName: string, nodeDescription?: string): Metadata =>
  generateMetadata({
    title: `${nodeName} - Master This Concept`,
    description: nodeDescription || `Learn and master ${nodeName} through interactive challenges and personalized learning paths on NeuroQuest.`,
    keywords: ['learning node', 'concept mastery', nodeName.toLowerCase()],
    url: `/node/${nodeId}`,
    type: 'article',
    section: 'Learning Content',
    tags: [nodeName, 'interactive learning', 'knowledge mastery'],
  });

export const pathMetadata = (pathId: string, pathName: string, pathDescription?: string): Metadata =>
  generateMetadata({
    title: `${pathName} - Learning Path`,
    description: pathDescription || `Follow the ${pathName} learning path to systematically build your expertise through curated content and challenges.`,
    keywords: ['learning path', 'structured learning', pathName.toLowerCase()],
    url: `/path/${pathId}`,
    type: 'article',
    section: 'Learning Paths',
    tags: [pathName, 'learning path', 'skill development'],
  });

export const domainMetadata = (domain: string, domainDescription?: string): Metadata =>
  generateMetadata({
    title: `${domain} - Explore Knowledge Domain`,
    description: domainDescription || `Explore the ${domain} knowledge domain with interactive learning nodes, challenging quizzes, and comprehensive skill development.`,
    keywords: ['knowledge domain', domain.toLowerCase(), 'subject area', 'learning category'],
    url: `/domain/${domain}`,
    type: 'article',
    section: 'Knowledge Domains',
    tags: [domain, 'knowledge domain', 'subject mastery'],
  });

export default {
  generateMetadata,
  homePageMetadata,
  aboutPageMetadata,
  dashboardMetadata,
  loginMetadata,
  registerMetadata,
  resetPasswordMetadata,
  verifyEmailMetadata,
  nodeMetadata,
  pathMetadata,
  domainMetadata,
  DEFAULT_CONFIG,
};
export interface BreadcrumbItem {
  name: string;
  url: string;
}

export interface CourseStructuredData {
  name: string;
  description: string;
  provider: string;
  educationalLevel?: string;
  timeRequired?: string;
  skillLevel?: 'Beginner' | 'Intermediate' | 'Advanced';
  subject?: string;
}

export interface QuestionStructuredData {
  question: string;
  answer: string;
  category?: string;
}

export interface PersonStructuredData {
  name: string;
  jobTitle?: string;
  description?: string;
  image?: string;
  sameAs?: string[];
}

// Generate JSON-LD structured data for the website
export function generateWebsiteStructuredData() {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://skilltree.app';
  
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: 'SkillTree',
    description: 'A nature-themed homeschooling and supplemental learning platform that helps students grow their skills through interactive learning paths',
    url: siteUrl,
    potentialAction: {
      '@type': 'SearchAction',
      target: `${siteUrl}/search?q={search_term_string}`,
      'query-input': 'required name=search_term_string'
    },
    publisher: {
      '@type': 'Organization',
      name: 'SkillTree',
      url: siteUrl,
      logo: `${siteUrl}/logo.png`,
      sameAs: [
        'https://twitter.com/skilltree',
        'https://linkedin.com/company/skilltree',
        'https://github.com/skilltree'
      ]
    }
  };
}

// Generate JSON-LD structured data for educational organization
export function generateOrganizationStructuredData() {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://skilltree.app';
  
  return {
    '@context': 'https://schema.org',
    '@type': 'EducationalOrganization',
    name: 'SkillTree',
    description: 'Grow Your Skills. Master Your Future. A nature-themed homeschooling and supplemental learning platform',
    url: siteUrl,
    logo: `${siteUrl}/logo.png`,
    image: `${siteUrl}/og-image.jpg`,
    sameAs: [
      'https://twitter.com/skilltree',
      'https://linkedin.com/company/skilltree'
    ],
    contactPoint: {
      '@type': 'ContactPoint',
      contactType: 'customer service',
      email: 'support@skilltree.app'
    },
    address: {
      '@type': 'PostalAddress',
      addressCountry: 'US'
    }
  };
}

// Generate breadcrumb structured data
export function generateBreadcrumbStructuredData(items: BreadcrumbItem[]) {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://skilltree.app';
  
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.url.startsWith('http') ? item.url : `${siteUrl}${item.url}`
    }))
  };
}

// Generate course structured data
export function generateCourseStructuredData(course: CourseStructuredData) {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://neuroquest.app';
  
  return {
    '@context': 'https://schema.org',
    '@type': 'Course',
    name: course.name,
    description: course.description,
    provider: {
      '@type': 'Organization',
      name: course.provider,
      url: siteUrl
    },
    ...(course.educationalLevel && { educationalLevel: course.educationalLevel }),
    ...(course.timeRequired && { timeRequired: course.timeRequired }),
    ...(course.skillLevel && { courseMode: course.skillLevel }),
    ...(course.subject && { about: course.subject }),
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'USD',
      availability: 'https://schema.org/InStock'
    }
  };
}

// Generate FAQ structured data
export function generateFAQStructuredData(questions: QuestionStructuredData[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: questions.map(q => ({
      '@type': 'Question',
      name: q.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: q.answer
      }
    }))
  };
}

// Generate learning path structured data
export function generateLearningPathStructuredData(path: {
  name: string;
  description: string;
  nodes: Array<{ name: string; description?: string }>;
  difficulty: string;
  estimatedTime?: string;
}) {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://neuroquest.app';
  
  return {
    '@context': 'https://schema.org',
    '@type': 'Course',
    name: path.name,
    description: path.description,
    provider: {
      '@type': 'Organization',
      name: 'NeuroQuest',
      url: siteUrl
    },
    educationalLevel: path.difficulty,
    ...(path.estimatedTime && { timeRequired: path.estimatedTime }),
    hasPart: path.nodes.map((node, index) => ({
      '@type': 'LearningResource',
      name: node.name,
      description: node.description || `Learn ${node.name} as part of ${path.name}`,
      position: index + 1,
      learningResourceType: 'Interactive Module'
    })),
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'USD',
      availability: 'https://schema.org/InStock'
    }
  };
}

// Generate article structured data for blog posts or educational content
export function generateArticleStructuredData(article: {
  title: string;
  description: string;
  author?: string;
  publishedDate?: string;
  modifiedDate?: string;
  image?: string;
  url?: string;
  category?: string;
}) {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://neuroquest.app';
  const fullUrl = article.url ? `${siteUrl}${article.url}` : siteUrl;
  const imageUrl = article.image ? `${siteUrl}${article.image}` : `${siteUrl}/og-image.jpg`;
  
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: article.title,
    description: article.description,
    image: imageUrl,
    url: fullUrl,
    ...(article.publishedDate && { datePublished: article.publishedDate }),
    ...(article.modifiedDate && { dateModified: article.modifiedDate }),
    author: {
      '@type': 'Person',
      name: article.author || 'NeuroQuest Team'
    },
    publisher: {
      '@type': 'Organization',
      name: 'NeuroQuest',
      url: siteUrl,
      logo: `${siteUrl}/logo.png`
    },
    ...(article.category && { articleSection: article.category })
  };
}

// Generate knowledge graph node structured data
export function generateKnowledgeNodeStructuredData(node: {
  id: string;
  name: string;
  description?: string;
  domain: string;
  difficulty: number;
  points: number;
  prerequisites?: string[];
}) {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://neuroquest.app';
  
  return {
    '@context': 'https://schema.org',
    '@type': 'LearningResource',
    name: node.name,
    description: node.description || `Master ${node.name} through interactive learning on NeuroQuest`,
    url: `${siteUrl}/node/${node.id}`,
    learningResourceType: 'Interactive Module',
    educationalUse: 'instruction',
    educationalLevel: node.difficulty <= 2 ? 'Beginner' : node.difficulty <= 4 ? 'Intermediate' : 'Advanced',
    about: {
      '@type': 'Thing',
      name: node.domain
    },
    teaches: node.name,
    provider: {
      '@type': 'Organization',
      name: 'NeuroQuest',
      url: siteUrl
    },
    ...(node.prerequisites && node.prerequisites.length > 0 && {
      coursePrerequisites: node.prerequisites.join(', ')
    })
  };
}

// Generate person/profile structured data
export function generatePersonStructuredData(person: PersonStructuredData) {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://neuroquest.app';
  
  return {
    '@context': 'https://schema.org',
    '@type': 'Person',
    name: person.name,
    ...(person.jobTitle && { jobTitle: person.jobTitle }),
    ...(person.description && { description: person.description }),
    ...(person.image && { image: person.image.startsWith('http') ? person.image : `${siteUrl}${person.image}` }),
    ...(person.sameAs && { sameAs: person.sameAs }),
    worksFor: {
      '@type': 'Organization',
      name: 'NeuroQuest',
      url: siteUrl
    }
  };
}

// Utility function to inject structured data into page
export function generateStructuredDataScript(data: object): string {
  return `<script type="application/ld+json">${JSON.stringify(data, null, 2)}</script>`;
}

export default {
  generateWebsiteStructuredData,
  generateOrganizationStructuredData,
  generateBreadcrumbStructuredData,
  generateCourseStructuredData,
  generateFAQStructuredData,
  generateLearningPathStructuredData,
  generateArticleStructuredData,
  generateKnowledgeNodeStructuredData,
  generatePersonStructuredData,
  generateStructuredDataScript,
};
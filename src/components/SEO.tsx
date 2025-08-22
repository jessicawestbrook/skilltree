import React from 'react'
import { Helmet } from 'react-helmet-async'

interface SEOProps {
  title?: string
  description?: string
  keywords?: string[]
  image?: string
  url?: string
  type?: 'website' | 'article' | 'course'
  structuredData?: object
  noIndex?: boolean
  canonicalUrl?: string
}

const SEO: React.FC<SEOProps> = ({
  title,
  description,
  keywords = [],
  image = '/og-image.png',
  url,
  type = 'website',
  structuredData,
  noIndex = false,
  canonicalUrl
}) => {
  const baseUrl = 'https://skilltree.app'
  const defaultTitle = 'SkillTree - Gamified Learning Platform for All Ages | Interactive Education'
  const defaultDescription = 'Master any skill with SkillTree\'s interactive learning platform. Gamified education with skill trees, adaptive assessments, and personalized learning paths for homeschooling, test prep, and lifelong learning.'
  
  const seoTitle = title ? `${title} | SkillTree` : defaultTitle
  const seoDescription = description || defaultDescription
  const seoUrl = url ? `${baseUrl}${url}` : baseUrl
  const seoImage = image.startsWith('http') ? image : `${baseUrl}${image}`
  const seoCanonical = canonicalUrl || seoUrl
  
  const defaultKeywords = [
    'online learning',
    'education platform',
    'skill tree',
    'gamified learning',
    'homeschooling',
    'test preparation',
    'adaptive assessment',
    'interactive education',
    'personalized learning',
    'STEM education',
    'language learning'
  ]
  
  const allKeywords = [...defaultKeywords, ...keywords].join(', ')

  return (
    <Helmet>
      {/* Primary Meta Tags */}
      <title>{seoTitle}</title>
      <meta name="title" content={seoTitle} />
      <meta name="description" content={seoDescription} />
      <meta name="keywords" content={allKeywords} />
      <link rel="canonical" href={seoCanonical} />
      
      {/* Robots */}
      {noIndex ? (
        <meta name="robots" content="noindex, nofollow" />
      ) : (
        <meta name="robots" content="index, follow" />
      )}
      
      {/* Open Graph / Facebook */}
      <meta property="og:type" content={type} />
      <meta property="og:url" content={seoUrl} />
      <meta property="og:title" content={seoTitle} />
      <meta property="og:description" content={seoDescription} />
      <meta property="og:image" content={seoImage} />
      <meta property="og:site_name" content="SkillTree" />
      <meta property="og:locale" content="en_US" />
      
      {/* Twitter */}
      <meta property="twitter:card" content="summary_large_image" />
      <meta property="twitter:url" content={seoUrl} />
      <meta property="twitter:title" content={seoTitle} />
      <meta property="twitter:description" content={seoDescription} />
      <meta property="twitter:image" content={seoImage} />
      <meta property="twitter:creator" content="@skilltreeapp" />
      
      {/* Article specific meta tags */}
      {type === 'article' && (
        <>
          <meta property="article:author" content="SkillTree" />
          <meta property="article:publisher" content="SkillTree" />
        </>
      )}
      
      {/* Course specific meta tags */}
      {type === 'course' && (
        <>
          <meta property="og:video:tag" content="education" />
          <meta property="og:video:tag" content="learning" />
        </>
      )}
      
      {/* Structured Data */}
      {structuredData && (
        <script type="application/ld+json">
          {JSON.stringify(structuredData)}
        </script>
      )}
    </Helmet>
  )
}

export default SEO
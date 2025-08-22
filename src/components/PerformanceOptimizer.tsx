import React from 'react'
import { Helmet } from 'react-helmet-async'

interface PerformanceOptimizerProps {
  preloadImages?: string[]
  preloadFonts?: string[]
  criticalCSS?: string
}

const PerformanceOptimizer: React.FC<PerformanceOptimizerProps> = ({
  preloadImages = [],
  preloadFonts = [],
  criticalCSS
}) => {
  return (
    <Helmet>
      {/* Preload critical images */}
      {preloadImages.map((src, index) => (
        <link
          key={index}
          rel="preload"
          as="image"
          href={src}
          type="image/webp"
        />
      ))}

      {/* Preload critical fonts */}
      {preloadFonts.map((href, index) => (
        <link
          key={index}
          rel="preload"
          as="font"
          href={href}
          type="font/woff2"
          crossOrigin="anonymous"
        />
      ))}

      {/* DNS prefetch for external domains */}
      <link rel="dns-prefetch" href="//fonts.googleapis.com" />
      <link rel="dns-prefetch" href="//fonts.gstatic.com" />
      
      {/* Preconnect to critical third-party origins */}
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
      
      {/* Critical CSS inline */}
      {criticalCSS && (
        <style type="text/css">
          {criticalCSS}
        </style>
      )}

      {/* Optimize third-party scripts */}
      <meta httpEquiv="x-dns-prefetch-control" content="on" />
      
      {/* Improve loading performance */}
      <meta name="format-detection" content="telephone=no" />
      <meta name="format-detection" content="date=no" />
      <meta name="format-detection" content="address=no" />
      <meta name="format-detection" content="email=no" />
    </Helmet>
  )
}

export default PerformanceOptimizer
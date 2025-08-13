// Image optimization utilities for SEO
export interface ImageSEOConfig {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  priority?: boolean;
  loading?: 'lazy' | 'eager';
  sizes?: string;
  quality?: number;
  format?: 'webp' | 'avif' | 'auto';
}

// Generate responsive image sizes for different viewports
export const generateImageSizes = (
  baseWidth: number,
  breakpoints: number[] = [640, 768, 1024, 1280, 1536]
): string => {
  const sizes = breakpoints.map(bp => `(max-width: ${bp}px) ${Math.min(baseWidth, bp)}px`);
  sizes.push(`${baseWidth}px`);
  return sizes.join(', ');
};

// Generate srcSet for responsive images
export const generateSrcSet = (
  baseSrc: string,
  widths: number[] = [320, 640, 768, 1024, 1280, 1536],
  format: string = 'webp'
): string => {
  return widths
    .map(width => {
      const src = baseSrc.includes('?') 
        ? `${baseSrc}&w=${width}&f=${format}`
        : `${baseSrc}?w=${width}&f=${format}`;
      return `${src} ${width}w`;
    })
    .join(', ');
};

// Optimize alt text for SEO
export const generateOptimizedAltText = (
  baseAlt: string,
  context?: {
    page?: string;
    domain?: string;
    nodeId?: string;
  }
): string => {
  let optimizedAlt = baseAlt;
  
  if (context?.domain) {
    optimizedAlt += ` - ${context.domain} learning`;
  }
  
  if (context?.page) {
    optimizedAlt += ` on NeuroQuest`;
  }
  
  return optimizedAlt;
};

// Generate Open Graph image URL with fallbacks
export const generateOGImageUrl = (
  title: string,
  subtitle?: string,
  theme: 'light' | 'dark' = 'light'
): string => {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://neuroquest.app';
  
  // If you have a dynamic OG image generation service
  const params = new URLSearchParams({
    title: title.slice(0, 60), // Limit title length
    ...(subtitle && { subtitle: subtitle.slice(0, 80) }),
    theme,
  });
  
  return `${baseUrl}/api/og-image?${params.toString()}`;
};

// Image loading priorities for different page types
export const getImagePriority = (
  position: 'hero' | 'above-fold' | 'below-fold' | 'footer',
  isLCP?: boolean
): { priority: boolean; loading: 'eager' | 'lazy' } => {
  if (isLCP || position === 'hero') {
    return { priority: true, loading: 'eager' };
  }
  
  if (position === 'above-fold') {
    return { priority: false, loading: 'eager' };
  }
  
  return { priority: false, loading: 'lazy' };
};

// Common image configurations for NeuroQuest
export const imageConfigs = {
  // Logo images
  logo: {
    sizes: generateImageSizes(200, [320, 640]),
    quality: 90,
    format: 'webp' as const,
    priority: true,
    loading: 'eager' as const,
  },
  
  // Hero section images
  hero: {
    sizes: generateImageSizes(1200, [640, 768, 1024, 1280, 1536]),
    quality: 85,
    format: 'webp' as const,
    priority: true,
    loading: 'eager' as const,
  },
  
  // Knowledge node icons
  nodeIcon: {
    sizes: generateImageSizes(64, [320, 640]),
    quality: 90,
    format: 'webp' as const,
    priority: false,
    loading: 'lazy' as const,
  },
  
  // Domain category images
  domainImage: {
    sizes: generateImageSizes(300, [320, 640, 768]),
    quality: 80,
    format: 'webp' as const,
    priority: false,
    loading: 'lazy' as const,
  },
  
  // Avatar/profile images
  avatar: {
    sizes: generateImageSizes(120, [320, 640]),
    quality: 85,
    format: 'webp' as const,
    priority: false,
    loading: 'lazy' as const,
  },
  
  // Open Graph images
  ogImage: {
    width: 1200,
    height: 630,
    quality: 90,
    format: 'webp' as const,
  },
  
  // Thumbnail images
  thumbnail: {
    sizes: generateImageSizes(200, [320, 640]),
    quality: 75,
    format: 'webp' as const,
    priority: false,
    loading: 'lazy' as const,
  },
};

// Validate image for SEO best practices
export const validateImageSEO = (config: ImageSEOConfig): {
  isValid: boolean;
  warnings: string[];
  errors: string[];
} => {
  const warnings: string[] = [];
  const errors: string[] = [];
  
  // Check alt text
  if (!config.alt) {
    errors.push('Alt text is required for accessibility and SEO');
  } else if (config.alt.length < 10) {
    warnings.push('Alt text should be more descriptive (at least 10 characters)');
  } else if (config.alt.length > 125) {
    warnings.push('Alt text should be under 125 characters for optimal SEO');
  }
  
  // Check dimensions
  if (!config.width || !config.height) {
    warnings.push('Explicit width and height improve loading performance');
  }
  
  // Check loading strategy
  if (config.priority && config.loading === 'lazy') {
    warnings.push('Priority images should use eager loading');
  }
  
  // Check format
  if (!config.format || config.format === 'auto') {
    warnings.push('Consider specifying webp format for better compression');
  }
  
  // Check quality
  if (config.quality && config.quality > 90) {
    warnings.push('Image quality over 90 may result in unnecessarily large files');
  }
  
  return {
    isValid: errors.length === 0,
    warnings,
    errors,
  };
};

// Generate image schema markup
export const generateImageSchemaMarkup = (
  imageUrl: string,
  alt: string,
  caption?: string,
  license?: string
) => {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://neuroquest.app';
  const fullImageUrl = imageUrl.startsWith('http') ? imageUrl : `${baseUrl}${imageUrl}`;
  
  return {
    '@context': 'https://schema.org',
    '@type': 'ImageObject',
    url: fullImageUrl,
    name: alt,
    ...(caption && { caption }),
    ...(license && { license }),
    creator: {
      '@type': 'Organization',
      name: 'NeuroQuest',
      url: baseUrl,
    },
  };
};

// Placeholder generation for better UX
export const generateImagePlaceholder = (
  width: number,
  height: number,
  color: string = '#f3f4f6'
): string => {
  const svg = `
    <svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="${color}"/>
    </svg>
  `;
  
  return `data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}`;
};

// Export commonly used functions
export default {
  generateImageSizes,
  generateSrcSet,
  generateOptimizedAltText,
  generateOGImageUrl,
  getImagePriority,
  imageConfigs,
  validateImageSEO,
  generateImageSchemaMarkup,
  generateImagePlaceholder,
};
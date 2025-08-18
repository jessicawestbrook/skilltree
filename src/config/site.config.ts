// Site configuration settings
export const siteConfig = {
  // Site metadata
  siteName: 'SkillTree',
  siteDescription: 'Interactive learning platform with gamified skill progression',
  siteUrl: process.env.REACT_APP_SITE_URL || 'http://localhost:3000',
  
  // Authentication settings
  auth: {
    // Number of random questions before prompting login
    randomQuestionsBeforeLogin: 10,
    // Require email verification to use site
    requireEmailVerification: false,
    // Password requirements
    passwordMinLength: 6,
    passwordRequireUppercase: false,
    passwordRequireNumbers: false,
    passwordRequireSpecialChars: false,
  },
  
  // Learning settings
  learning: {
    // Number of pre-quiz questions
    preQuizQuestionCount: 3,
    // Minimum score to pass a module (percentage)
    passingScore: 100,
    // Cache TTL in milliseconds
    cacheTTL: 5 * 60 * 1000, // 5 minutes
    // Number of top categories to expand by default
    defaultExpandedCategories: 3,
  },
  
  // UI settings
  ui: {
    // Maximum number of recommendations to show
    maxRecommendations: 10,
    // Number of recommendations to display in compact view
    compactRecommendations: 5,
    // Animation durations in milliseconds
    animationDuration: 200,
    // Tooltip delay in milliseconds
    tooltipDelay: 500,
  },
  
  // Performance settings
  performance: {
    // Maximum nodes to render at once in tree view
    maxTreeNodes: 500,
    // Debounce delay for search in milliseconds
    searchDebounceDelay: 300,
    // Maximum search results
    maxSearchResults: 50,
  },
  
  // Feature flags
  features: {
    // Enable/disable features
    enableSpellingBee: false,
    enableIQTesting: false,
    enableStandardizedTesting: false,
    enableReadingComprehension: true,
    enableEmailVerification: false,
    enableSocialFeatures: false,
    enableAchievements: false,
  },
  
  // API settings
  api: {
    // Supabase settings (from environment variables)
    supabaseUrl: process.env.REACT_APP_SUPABASE_URL || '',
    supabaseAnonKey: process.env.REACT_APP_SUPABASE_ANON_KEY || '',
    // API timeouts in milliseconds
    defaultTimeout: 30000,
    uploadTimeout: 60000,
  },
  
  // Color scheme
  colors: {
    primary: {
      light: '#22c55e', // green-500
      DEFAULT: '#16a34a', // green-600
      dark: '#15803d', // green-700
    },
    secondary: {
      light: '#fbbf24', // amber-400
      DEFAULT: '#f59e0b', // amber-500
      dark: '#d97706', // amber-600
    },
    gold: {
      light: '#fde047', // yellow-300
      DEFAULT: '#facc15', // yellow-400
      dark: '#eab308', // yellow-500
    },
  },
  
  // Version info
  version: '1.0.0',
  lastUpdated: '2024-01-01',
}

// Type-safe config getter
export function getConfig<T extends keyof typeof siteConfig>(key: T): typeof siteConfig[T] {
  return siteConfig[key]
}

// Helper to get nested config values
export function getConfigValue(path: string): any {
  const keys = path.split('.')
  let result: any = siteConfig
  
  for (const key of keys) {
    if (result && typeof result === 'object' && key in result) {
      result = result[key]
    } else {
      return undefined
    }
  }
  
  return result
}

export default siteConfig
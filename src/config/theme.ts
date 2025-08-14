// Centralized theme configuration for SkillTree
// Update these values to change colors across the entire application

export const themeConfig = {
  // Primary brand colors
  primary: {
    name: 'forest',
    light: {
      50: 'forest-50',
      100: 'forest-100',
      200: 'forest-200',
      300: 'forest-300',
      400: 'forest-400',
      500: 'forest-500',
      600: 'forest-600',
      700: 'forest-700',
      800: 'forest-800',
      900: 'forest-900',
    },
    gradient: 'from-forest-600 to-sky-600',
    gradientHover: 'from-forest-700 to-sky-700',
  },
  
  // Secondary brand colors
  secondary: {
    name: 'sky',
    light: {
      50: 'sky-50',
      100: 'sky-100',
      200: 'sky-200',
      300: 'sky-300',
      400: 'sky-400',
      500: 'sky-500',
      600: 'sky-600',
      700: 'sky-700',
      800: 'sky-800',
      900: 'sky-900',
    },
  },

  // Common gradient combinations
  gradients: {
    primary: 'bg-gradient-to-r from-forest-600 to-sky-600',
    primaryLight: 'bg-gradient-to-r from-forest-50 to-sky-50',
    primaryMedium: 'bg-gradient-to-r from-forest-500 to-sky-500',
    primaryDark: 'bg-gradient-to-r from-forest-700 to-sky-700',
    hover: 'hover:from-forest-700 hover:to-sky-700',
  },

  // Button styles
  buttons: {
    primary: 'bg-gradient-to-r from-forest-600 to-sky-600 text-white hover:from-forest-700 hover:to-sky-700',
    secondary: 'bg-gradient-to-r from-forest-50 to-sky-50 text-forest-700 hover:from-forest-100 hover:to-sky-100',
    danger: 'bg-red-600 text-white hover:bg-red-700',
  },

  // Text styles
  text: {
    gradient: 'bg-gradient-to-r from-forest-600 to-sky-600 bg-clip-text text-transparent',
    primary: 'text-forest-600 dark:text-forest-400',
    secondary: 'text-sky-600 dark:text-sky-400',
  },

  // Badge/Progress colors
  progress: {
    bar: 'bg-gradient-to-r from-forest-500 to-sky-500',
    background: 'bg-gray-200 dark:bg-gray-700',
  },

  // Modal/Dialog theming
  modal: {
    header: 'bg-gradient-to-r from-forest-600 to-sky-600 text-white',
    headerText: 'text-forest-100',
    body: 'bg-white dark:bg-gray-900',
  },
};

// Helper function to get gradient class
export const getGradient = (type: 'primary' | 'light' | 'medium' | 'dark' = 'primary') => {
  const gradientMap = {
    primary: themeConfig.gradients.primary,
    light: themeConfig.gradients.primaryLight,
    medium: themeConfig.gradients.primaryMedium,
    dark: themeConfig.gradients.primaryDark,
  };
  return gradientMap[type];
};

// Helper function to get button class
export const getButtonClass = (type: 'primary' | 'secondary' | 'danger' = 'primary') => {
  return `${themeConfig.buttons[type]} px-6 py-3 rounded-lg font-semibold hover:shadow-lg transition-all`;
};
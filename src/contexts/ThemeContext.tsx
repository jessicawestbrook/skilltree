import React, { createContext, useContext, useEffect, useState } from 'react'

interface ThemeContextType {
  darkMode: boolean
  toggleDarkMode: () => void
  menuPinned: boolean
  toggleMenuPinned: () => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return context
}

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [darkMode, setDarkMode] = useState(() => {
    const savedTheme = localStorage.getItem('darkMode')
    return savedTheme ? JSON.parse(savedTheme) : false
  })

  const [menuPinned, setMenuPinned] = useState(() => {
    // Clear any existing saved state and default to pinned
    localStorage.removeItem('menuPinned')
    return true
  })

  useEffect(() => {
    localStorage.setItem('darkMode', JSON.stringify(darkMode))
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [darkMode])

  useEffect(() => {
    localStorage.setItem('menuPinned', JSON.stringify(menuPinned))
  }, [menuPinned])

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
  }

  const toggleMenuPinned = () => {
    setMenuPinned(!menuPinned)
  }

  return (
    <ThemeContext.Provider value={{ darkMode, toggleDarkMode, menuPinned, toggleMenuPinned }}>
      {children}
    </ThemeContext.Provider>
  )
}
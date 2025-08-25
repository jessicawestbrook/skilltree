import React, { createContext, useContext, useState, ReactNode } from 'react'

interface SpellingContextType {
  selectedDifficulties: string[]
  setSelectedDifficulties: (difficulties: string[]) => void
  toggleDifficulty: (difficulty: string) => void
  useAdaptiveTesting: boolean
  setUseAdaptiveTesting: (value: boolean) => void
}

const SpellingContext = createContext<SpellingContextType | undefined>(undefined)

export const SpellingProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [selectedDifficulties, setSelectedDifficulties] = useState<string[]>([
    'Beginner', 'Elementary', 'Intermediate', 'Advanced', 'Expert'
  ])
  const [useAdaptiveTesting, setUseAdaptiveTesting] = useState(true)

  const toggleDifficulty = (difficulty: string) => {
    setSelectedDifficulties(prev => {
      if (prev.includes(difficulty)) {
        // Don't allow deselecting all difficulties
        if (prev.length === 1) return prev
        return prev.filter(d => d !== difficulty)
      } else {
        return [...prev, difficulty]
      }
    })
  }

  return (
    <SpellingContext.Provider value={{ 
      selectedDifficulties, 
      setSelectedDifficulties,
      toggleDifficulty,
      useAdaptiveTesting,
      setUseAdaptiveTesting
    }}>
      {children}
    </SpellingContext.Provider>
  )
}

export const useSpelling = () => {
  const context = useContext(SpellingContext)
  if (context === undefined) {
    throw new Error('useSpelling must be used within a SpellingProvider')
  }
  return context
}
import React, { createContext, useContext, useState, ReactNode } from 'react'

interface SpellingBeeContextType {
  selectedDifficulties: string[]
  setSelectedDifficulties: (difficulties: string[]) => void
  toggleDifficulty: (difficulty: string) => void
  useAdaptiveTesting: boolean
  setUseAdaptiveTesting: (value: boolean) => void
}

const SpellingBeeContext = createContext<SpellingBeeContextType | undefined>(undefined)

export const SpellingBeeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
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
    <SpellingBeeContext.Provider value={{ 
      selectedDifficulties, 
      setSelectedDifficulties,
      toggleDifficulty,
      useAdaptiveTesting,
      setUseAdaptiveTesting
    }}>
      {children}
    </SpellingBeeContext.Provider>
  )
}

export const useSpellingBee = () => {
  const context = useContext(SpellingBeeContext)
  if (context === undefined) {
    throw new Error('useSpellingBee must be used within a SpellingBeeProvider')
  }
  return context
}
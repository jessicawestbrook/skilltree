import React, { useState, useEffect, useCallback } from 'react'
import { useLocation } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { spacedRepetitionService } from '../services/spacedRepetitionService'
import { useAuth } from '../contexts/AuthContext'
import { useSpelling } from '../contexts/SpellingContext'
import { checkSpellingTables, createSpellingTables } from '../utils/createSpellingTables'
import { replaceWordAndVariationsWithBlanks } from '../utils/vocabularyHelpers'
import { getSpellingDifficultyLevels } from '../services/difficultyLevels'
import { SpellingWordWithDifficulties, SpellingDifficultyLevel } from '../types/difficultyLevels'
import { 
  SpeakerWaveIcon, 
  CheckCircleIcon, 
  XCircleIcon,
  InformationCircleIcon,
  AcademicCapIcon,
  ClockIcon,
  FlagIcon,
  ChevronDownIcon
} from '@heroicons/react/24/outline'
import FlagContentModal from '../components/FlagContentModal'
import StudyListActions from '../components/StudyListActions'
import SkipButton from '../components/flashcards/SkipButton'
import { studyListService } from '../services/studyListService'
import { StudyList } from '../types/database.types'

// Using the new type from difficultyLevels.ts
type SpellingWord = SpellingWordWithDifficulties;

// Extend StudyList type to include item count
interface StudyListWithCount extends StudyList {
  itemCount?: number
}

interface SpellingPageProps {
  showTabs?: boolean
  onTabChange?: (tab: 'vocabulary' | 'spelling') => void
}

const SpellingPage: React.FC<SpellingPageProps> = ({ showTabs, onTabChange }) => {
  const { user } = useAuth()
  const location = useLocation()
  const { selectedDifficulties, setSelectedDifficulties, toggleDifficulty, useAdaptiveTesting, setUseAdaptiveTesting } = useSpelling()
  const [currentWord, setCurrentWord] = useState<SpellingWord | null>(null)
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [difficultyLevels, setDifficultyLevels] = useState<SpellingDifficultyLevel[]>([])
  const [userInput, setUserInput] = useState('')
  const [showResult, setShowResult] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)
  const [loading, setLoading] = useState(true)
  const [wordBank, setWordBank] = useState<SpellingWord[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [stats, setStats] = useState({ correct: 0, total: 0 })
  const [sessionStats, setSessionStats] = useState({ correct: 0, total: 0 })
  const [showFlagModal, setShowFlagModal] = useState(false)
  
  // Study list functionality
  const [studyLists, setStudyLists] = useState<StudyListWithCount[]>([])
  const [selectedStudyList, setSelectedStudyList] = useState<StudyListWithCount | null>(null)
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(0)
  const [totalWords, setTotalWords] = useState(0)
  const WORDS_PER_PAGE = 50

  // Session storage key
  const SPELLING_SESSION_KEY = 'spellingBeeSession'

  // Save session state
  const saveSessionState = useCallback((word: SpellingWord | null, index: number, userInput: string, showResult: boolean, isCorrect: boolean, page: number = 0, studyListId?: string, difficulties?: string[]) => {
    const sessionState = {
      currentWord: word,
      currentIndex: index,
      currentPage: page,
      userInput,
      showResult,
      isCorrect,
      selectedStudyListId: studyListId || null,
      selectedDifficulties: difficulties || selectedDifficulties,
      useAdaptiveTesting,
      timestamp: Date.now()
    }
    sessionStorage.setItem(SPELLING_SESSION_KEY, JSON.stringify(sessionState))
  }, [SPELLING_SESSION_KEY, selectedDifficulties, useAdaptiveTesting])

  // Load session state
  const loadSessionState = useCallback(() => {
    try {
      const saved = sessionStorage.getItem(SPELLING_SESSION_KEY)
      if (saved) {
        const sessionState = JSON.parse(saved)
        // Only restore if saved within last 30 minutes
        if (Date.now() - sessionState.timestamp < 30 * 60 * 1000) {
          return sessionState
        }
      }
    } catch (error) {
      console.error('Error loading session state:', error)
    }
    return null
  }, [SPELLING_SESSION_KEY])

  // Clear session state
  const clearSessionState = useCallback(() => {
    sessionStorage.removeItem(SPELLING_SESSION_KEY)
  }, [SPELLING_SESSION_KEY])

  // Helper function to organize and sort study lists
  const organizeStudyLists = (lists: StudyListWithCount[]) => {
    const scrippsLists = lists.filter(list => list.name.includes('Scripps'))
    
    // Sort Scripps lists by name (One Bee, Two Bee, Three Bee)
    const sortedScrippsLists = scrippsLists.sort((a, b) => {
      const order = ['One Bee', 'Two Bee', 'Three Bee']
      const aOrder = order.findIndex(o => a.name.includes(o))
      const bOrder = order.findIndex(o => b.name.includes(o))
      return aOrder - bOrder
    })
    
    return { scrippsLists: sortedScrippsLists }
  }

  // Load available study lists
  const loadStudyLists = useCallback(async () => {
    try {
      // Get public study lists for spelling (Scripps only)
      const { data, error } = await supabase
        .from('study_lists')
        .select('*')
        .eq('is_public', true)
        .ilike('name', '%Scripps%')
        .order('name')

      if (error) {
        console.error('Error loading study lists:', error)
        return
      }

      // Also get user's personal study lists if logged in
      let userLists: StudyList[] = []
      if (user) {
        const userListsData = await studyListService.getUserStudyLists(user.id)
        userLists = userListsData.filter(list => 
          list.name.toLowerCase().includes('spelling') || 
          list.name.toLowerCase().includes('bee')
        )
      }

      const allLists = [...(data || []), ...userLists]
      
      // Fetch counts for each list
      const listsWithCounts: StudyListWithCount[] = await Promise.all(
        allLists.map(async (list) => {
          const { count } = await supabase
            .from('study_list_items')
            .select('*', { count: 'exact', head: true })
            .eq('study_list_id', list.id)
            .eq('item_type', 'spelling_word')
          
          return {
            ...list,
            itemCount: count || 0
          }
        })
      )
      
      setStudyLists(listsWithCounts)
    } catch (error) {
      console.error('Error loading study lists:', error)
    }
  }, [user])

  const fetchWords = useCallback(async (page: number = 0) => {
    try {
      const offset = page * WORDS_PER_PAGE
      
      // If a study list is selected, get words from the study list with pagination
      if (selectedStudyList) {
        // First get total count if not already set
        if (page === 0) {
          setTotalWords(selectedStudyList.itemCount || 0)
        }
        
        // Get paginated study list items
        const { data: studyListItems, error: studyListError } = await supabase
          .from('study_list_items')
          .select('item_id')
          .eq('study_list_id', selectedStudyList.id)
          .eq('item_type', 'spelling_word')
          .range(offset, offset + WORDS_PER_PAGE - 1)

        if (studyListError) {
          console.error('Error fetching study list items:', studyListError)
          setLoading(false)
          return
        }

        if (studyListItems && studyListItems.length > 0) {
          const wordIds = studyListItems.map(item => item.item_id)
          
          // Fetch the actual words for this page
          const { data: words, error: wordsError } = await supabase
            .from('spelling_words')
            .select(`
              *,
              spelling_difficulty_levels!spelling_difficulty_id(id, name, description, grade_equivalent)
            `)
            .in('id', wordIds)
            .eq('is_spelling_word', true)  // Filter for spelling words only

          if (wordsError) {
            console.error('Error fetching words from study list:', wordsError)
            // Try fallback without join
            const { data: fallbackWords, error: fallbackError } = await supabase
              .from('spelling_words')
              .select('*')
              .in('id', wordIds)
              .eq('is_spelling_word', true)
              
            if (fallbackError) {
              console.error('Fallback query also failed:', fallbackError)
              setLoading(false)
              return
            }
            
            if (fallbackWords && fallbackWords.length > 0) {
              // Shuffle for variety
              const shuffled = [...fallbackWords].sort(() => Math.random() - 0.5)
              setWordBank(shuffled)
              setCurrentPage(page)
              
              // Check for saved session state
              const savedSession = loadSessionState()
              if (savedSession && savedSession.currentWord && savedSession.currentPage === page) {
                // Restore saved session if we're on the same page
                setCurrentWord(savedSession.currentWord)
                setCurrentIndex(savedSession.currentIndex)
                setUserInput(savedSession.userInput)
                setShowResult(savedSession.showResult)
                setIsCorrect(savedSession.isCorrect)
              } else if (page === 0) {
                setCurrentWord(shuffled[0])
                setCurrentIndex(0)
              }
            }
          } else if (words && words.length > 0) {
            // Shuffle for variety
            const shuffled = [...words].sort(() => Math.random() - 0.5)
            setWordBank(shuffled)
            setCurrentPage(page)
            
            // Check for saved session state
            const savedSession = loadSessionState()
            if (savedSession && savedSession.currentWord && savedSession.currentPage === page) {
              // Restore saved session if we're on the same page
              setCurrentWord(savedSession.currentWord)
              setCurrentIndex(savedSession.currentIndex)
              setUserInput(savedSession.userInput)
              setShowResult(savedSession.showResult)
              setIsCorrect(savedSession.isCorrect)
            } else if (page === 0) {
              setCurrentWord(shuffled[0])
              setCurrentIndex(0)
            }
          }
          
          setLoading(false)
          return
        }
      }

      // Regular word fetching (existing logic) with pagination
      // First get total count for non-study-list mode
      if (page === 0) {
        let countQuery = supabase
          .from('spelling_words')
          .select('*', { count: 'exact', head: true })
          .eq('is_spelling_word', true)
          
        if (selectedDifficulties.length > 0 && selectedDifficulties.length < 5) {
          const difficultyMap: Record<string, number> = { 'Beginner': 1, 'Elementary': 2, 'Intermediate': 3, 'Advanced': 4, 'Expert': 5 };
          countQuery = countQuery.in('spelling_difficulty_id', selectedDifficulties.map(name => difficultyMap[name] || 1))
        }
        
        const { count } = await countQuery
        setTotalWords(count || 0)
      }
      
      // Try to query with joins to the new difficulty tables first
      let query = supabase
        .from('spelling_words')
        .select(`
          *,
          spelling_difficulty_levels!spelling_difficulty_id(id, name, description, grade_equivalent)
        `)
        .eq('is_spelling_word', true)  // Filter for spelling words only
        .order('spelling_difficulty_id')
        .range(offset, offset + WORDS_PER_PAGE - 1)

      // Apply difficulty filter from selected difficulties
      if (selectedDifficulties.length > 0 && selectedDifficulties.length < 5) {
        // Filter by the foreign key ID based on selected difficulty names
        query = query.in('spelling_difficulty_id', selectedDifficulties.map(name => {
          const difficultyMap: Record<string, number> = { 'Beginner': 1, 'Elementary': 2, 'Intermediate': 3, 'Advanced': 4, 'Expert': 5 };
          return difficultyMap[name] || 1;
        }))
      }

      let { data, error } = await query

      // If the join fails (tables don't exist yet), fall back to old structure
      if (error && error.message?.includes('spelling_difficulty_levels')) {
        console.log('New difficulty tables not found, using legacy structure...')
        
        query = supabase
          .from('spelling_words')
          .select('*')
          .eq('is_spelling_word', true)  // Filter for spelling words only
          .order('spelling_difficulty_id')
          .range(offset, offset + WORDS_PER_PAGE - 1)

        if (selectedDifficulties.length > 0 && selectedDifficulties.length < 5) {
          // Map difficulty names to IDs for filtering
          const difficultyMap: Record<string, number> = { 'Beginner': 1, 'Elementary': 2, 'Intermediate': 3, 'Advanced': 4, 'Expert': 5 };
          const difficultyIds = selectedDifficulties.map(name => difficultyMap[name] || 1);
          query = query.in('spelling_difficulty_id', difficultyIds)
        }

        const fallbackResult = await query
        data = fallbackResult.data
        error = fallbackResult.error
      }

      if (error) {
        console.error('Error fetching words:', error)
        setLoading(false)
        return
      }

      if (data && data.length > 0) {
        // Shuffle words for variety
        const shuffled = [...data].sort(() => Math.random() - 0.5)
        setWordBank(shuffled)
        setCurrentPage(page)
        
        // Check for saved session state
        const savedSession = loadSessionState()
        if (savedSession && savedSession.currentWord && savedSession.currentPage === page) {
          // Restore saved session if we're on the same page
          setCurrentWord(savedSession.currentWord)
          setCurrentIndex(savedSession.currentIndex)
          setUserInput(savedSession.userInput)
          setShowResult(savedSession.showResult)
          setIsCorrect(savedSession.isCorrect)
        } else if (page === 0) {
          setCurrentWord(shuffled[0])
          setCurrentIndex(0)
        }
      }
    } catch (error) {
      console.error('Error fetching words:', error)
    } finally {
      setLoading(false)
    }
  }, [selectedDifficulties, selectedStudyList, WORDS_PER_PAGE, loadSessionState])


  const fetchUserStats = useCallback(async () => {
    if (!user) return

    try {
      const { data, error } = await supabase
        .from('user_spelling_attempts')
        .select('*')
        .eq('user_id', user.id)
        .order('created_at', { ascending: false })

      if (!error && data) {
        const correct = data.filter(a => a.correct).length
        setStats({ correct, total: data.length })
      }
    } catch (error) {
      console.error('Error fetching user stats:', error)
    }
  }, [user])

  const initializeSpellingBee = useCallback(async () => {
    // Check if tables exist, create if not
    const tablesExist = await checkSpellingTables()
    if (!tablesExist) {
      console.log('Creating spelling tables...')
      await createSpellingTables()
    }
    
    await fetchWords()
    if (user) {
      await fetchUserStats()
    }
  }, [user, fetchWords, fetchUserStats])

  // Restore session on mount
  useEffect(() => {
    const savedSession = loadSessionState()
    if (savedSession) {
      // Restore selected difficulties and other settings
      if (savedSession.selectedDifficulties) {
        setSelectedDifficulties(savedSession.selectedDifficulties)
      }
      if (savedSession.currentPage !== undefined) {
        setCurrentPage(savedSession.currentPage)
      }
      if (savedSession.useAdaptiveTesting !== undefined) {
        setUseAdaptiveTesting(savedSession.useAdaptiveTesting)
      }
      // Note: We'll restore the study list and word state after data is loaded
    }
    initializeSpellingBee()
  }, [initializeSpellingBee, loadSessionState, setSelectedDifficulties, setUseAdaptiveTesting])

  // Load difficulty levels on component mount
  useEffect(() => {
    const loadDifficultyLevels = async () => {
      try {
        const levels = await getSpellingDifficultyLevels()
        setDifficultyLevels(levels)
      } catch (error) {
        console.error('Error loading difficulty levels:', error)
      }
    }
    loadDifficultyLevels()
  }, [])

  // Load study lists on mount and when user changes
  useEffect(() => {
    loadStudyLists().then(() => {
      // After loading lists, restore selected study list from session if any
      const savedSession = loadSessionState()
      if (savedSession && savedSession.selectedStudyListId && studyLists.length > 0) {
        const savedList = studyLists.find(list => list.id === savedSession.selectedStudyListId)
        if (savedList) {
          setSelectedStudyList(savedList)
        }
      }
    })
  }, [loadStudyLists, loadSessionState, studyLists])

  // Handle navigation from study list page
  useEffect(() => {
    if (location.state) {
      const state = location.state as any
      if (state.studyListWords && state.studyListWords.length > 0) {
        // Load words from the study list navigation
        const loadStudyListWords = async () => {
          setLoading(true)
          const wordIds = state.studyListWords.map((w: any) => w.id)
          const startIndex = state.startIndex || 0
          
          const { data: words, error } = await supabase
            .from('spelling_words')
            .select(`
              *,
              spelling_difficulty_levels!spelling_difficulty_id(id, name, description)
            `)
            .eq('is_spelling_word', true)  // Filter for spelling words only
            .in('id', wordIds)
          
          if (error) {
            console.error('Error fetching study list words:', error)
            setLoading(false)
            return
          }
          
          if (words && words.length > 0) {
            // Sort words to match the order from study list
            const sortedWords = wordIds.map((id: string) => 
              words.find((w: SpellingWord) => w.id === id)
            ).filter(Boolean) as SpellingWord[]
            
            setWordBank(sortedWords)
            setCurrentIndex(startIndex)
            setCurrentWord(sortedWords[startIndex])
            setLoading(false)
          }
        }
        
        loadStudyListWords()
        return
      }
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.state])

  // Refetch words when selected difficulties or study list change
  useEffect(() => {
    // Don't refetch if we came from study list navigation
    if (location.state?.studyListWords) {
      return
    }
    setLoading(true)
    setCurrentPage(0)  // Reset to first page
    setTotalWords(0)   // Reset total count
    fetchWords(0)      // Fetch first page
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedDifficulties, selectedStudyList])

  // Play word when it changes (including initial load)
  useEffect(() => {
    const autoplayEnabled = localStorage.getItem('audioAutoplay') !== 'false'
    if (currentWord && !showResult && autoplayEnabled) {
      // Small delay to ensure page is ready
      const timer = setTimeout(() => {
        playAudioForWord(currentWord)
      }, 1000)
      return () => clearTimeout(timer)
    }
  }, [currentWord, showResult])

  const playAudio = async () => {
    if (!currentWord) return
    playAudioForWord(currentWord)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!currentWord || !userInput.trim()) return

    const correct = userInput.trim().toLowerCase() === currentWord.word.toLowerCase()
    setIsCorrect(correct)
    setShowResult(true)

    // Update session stats
    setSessionStats(prev => ({
      correct: prev.correct + (correct ? 1 : 0),
      total: prev.total + 1
    }))

    // Save session state after submission
    saveSessionState(currentWord, currentIndex, userInput, true, correct, currentPage, selectedStudyList?.id, selectedDifficulties)

    // Save attempt if user is logged in
    if (user) {
      // Add this spelling word to flashcard review
      try {
        await spacedRepetitionService.addFlashcardsToReview(user.id, [{
          id: currentWord.id,
          type: 'spelling'
        }])
      } catch (error) {
        console.error('Error adding spelling word to flashcard review:', error)
      }
      
      await supabase.from('user_spelling_attempts').insert({
        user_id: user.id,
        word_id: currentWord.id,
        correct,
        user_spelling: userInput.trim()
      })

      setStats(prev => ({
        correct: prev.correct + (correct ? 1 : 0),
        total: prev.total + 1
      }))
    }
  }

  const nextWord = () => {
    // Clear session state when moving to next word
    clearSessionState()
    
    // Check if we need to load the next page
    if (currentIndex + 1 >= wordBank.length) {
      // Check if there are more pages available
      const nextPageStartIndex = (currentPage + 1) * WORDS_PER_PAGE
      if (nextPageStartIndex < totalWords) {
        // Load next page
        setLoading(true)
        fetchWords(currentPage + 1)
        setCurrentIndex(0)
      } else {
        // Wrap around to beginning
        setCurrentIndex(0)
        setCurrentWord(wordBank[0])
      }
    } else {
      const nextIndex = currentIndex + 1
      setCurrentIndex(nextIndex)
      setCurrentWord(wordBank[nextIndex])
    }
    
    setUserInput('')
    setShowResult(false)
    
    // Automatically play the next word (if autoplay enabled)
    const autoplayEnabled = localStorage.getItem('audioAutoplay') !== 'false'
    if (autoplayEnabled) {
      setTimeout(() => {
        if (currentWord) {
          playAudioForWord(currentWord)
        }
      }, 500) // Small delay for better UX
    }
  }

  const skipQuestion = () => {
    // Clear session state when skipping
    clearSessionState()
    
    // Check if we need to load the next page
    if (currentIndex + 1 >= wordBank.length) {
      // Check if there are more pages available
      const nextPageStartIndex = (currentPage + 1) * WORDS_PER_PAGE
      if (nextPageStartIndex < totalWords) {
        // Load next page
        setLoading(true)
        fetchWords(currentPage + 1)
        setCurrentIndex(0)
      } else {
        // Wrap around to beginning
        setCurrentIndex(0)
        setCurrentWord(wordBank[0])
      }
    } else {
      const nextIndex = currentIndex + 1
      setCurrentIndex(nextIndex)
      setCurrentWord(wordBank[nextIndex])
    }
    
    setUserInput('')
    setShowResult(false)
    
    // Automatically play the next word (if autoplay enabled)
    const autoplayEnabled = localStorage.getItem('audioAutoplay') !== 'false'
    if (autoplayEnabled) {
      setTimeout(() => {
        if (currentWord) {
          playAudioForWord(currentWord)
        }
      }, 500) // Small delay for better UX
    }
  }
  
  const playAudioForWord = (word: SpellingWord) => {
    if (!word) return

    // Use Web Speech API for text-to-speech
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(word.word)
      utterance.rate = 0.8 // Slower for spelling
      utterance.pitch = 1
      utterance.volume = 1
      
      // Try to use a clearer voice if available
      const voices = speechSynthesis.getVoices()
      const englishVoice = voices.find(voice => 
        voice.lang.startsWith('en-') && voice.name.includes('Google')
      ) || voices.find(voice => voice.lang.startsWith('en-'))
      
      if (englishVoice) {
        utterance.voice = englishVoice
      }
      
      speechSynthesis.speak(utterance)
    }
  }


  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!currentWord) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6 text-center">
          <p className="text-lg">No spelling words available. Please check back later!</p>
        </div>
      </div>
    )
  }

  return (
    <div className={showTabs ? "max-w-4xl mx-auto p-1 sm:p-2 pt-2 sm:pt-2 space-y-1 sm:space-y-2" : ""}>
      {/* Tab Bar */}
      {showTabs && (
        <div className="bg-white dark:bg-neutral-900 rounded-lg shadow-md p-2 flex justify-center gap-2">
          <button
            onClick={() => onTabChange?.('vocabulary')}
            className="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-700"
          >
            <AcademicCapIcon className="h-4 w-4" />
            Vocabulary
          </button>
          <button
            onClick={() => onTabChange?.('spelling')}
            className="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 bg-primary-600 text-white"
          >
            <SpeakerWaveIcon className="h-4 w-4" />
            Spelling
          </button>
        </div>
      )}
      
      {/* Combined Spelling Practice Card */}
      <div className="bg-white dark:bg-neutral-900 rounded-lg sm:rounded-xl shadow-lg p-2 sm:p-3 relative">
        {/* Header with Action Buttons and Title */}
        <div className="flex items-center mb-1 sm:mb-2">
          <div className="w-10">
            {currentWord && (
              <button
                onClick={() => setShowFlagModal(true)}
                className="p-1.5 text-neutral-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors bg-white dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700"
                title="Report an issue with this question"
              >
                <FlagIcon className="h-4 w-4" />
              </button>
            )}
          </div>
          
          <h1 className="flex-1 text-center text-lg sm:text-xl font-bold text-neutral-800 dark:text-neutral-200">
            Spelling Practice
          </h1>
          
          <div className="w-10 flex justify-end">
            {currentWord && (
              <StudyListActions
                itemType="spelling_word"
                itemId={currentWord.id}
                itemData={currentWord}
                itemTitle={`Spelling: ${currentWord.word}`}
                className="bg-white dark:bg-neutral-800 rounded-lg shadow-sm border border-neutral-200 dark:border-neutral-700 px-2 py-1"
              />
            )}
          </div>
        </div>
        
        {/* Settings and Stats Row */}
        <div className="flex justify-between items-start mb-1 sm:mb-2">
          {/* Practice Settings */}
          <div className="flex flex-col gap-2 flex-1 mr-2 sm:mr-0">
            {/* Top row with Study List */}
            <div className="flex flex-col lg:flex-row gap-1 sm:gap-2 items-start lg:items-center">

              {/* Study List Selection */}
              {studyLists.length > 0 && (
              <div className="flex items-center gap-1">
                <span className="text-xs font-medium text-neutral-700 dark:text-neutral-300">Study List:</span>
                <div className="relative">
                  <select
                    value={selectedStudyList?.id || ''}
                    onChange={(e) => {
                      const list = studyLists.find(l => l.id === e.target.value) || null
                      setSelectedStudyList(list)
                      // Turn off adaptive learning when a study list is selected
                      if (list && useAdaptiveTesting) {
                        setUseAdaptiveTesting(false)
                      }
                      setCurrentIndex(0)
                      setCurrentWord(null)
                      setUserInput('')
                      setShowResult(false)
                    }}
                    className="bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 px-2 py-1 rounded text-xs border-0 focus:ring-1 focus:ring-neutral-500 appearance-none pr-6"
                  >
                    <option value="">All Words</option>
                    {(() => {
                      const { scrippsLists } = organizeStudyLists(studyLists)
                      return (
                        <>
                          {scrippsLists.length > 0 && (
                            <optgroup label="Scripps National Spelling">
                              {scrippsLists.map((list) => (
                                <option key={list.id} value={list.id}>
                                  {list.name} {list.itemCount !== undefined && `(${list.itemCount.toLocaleString()})`}
                                </option>
                              ))}
                            </optgroup>
                          )}
                        </>
                      )
                    })()}
                  </select>
                  <ChevronDownIcon className="absolute right-1 top-1/2 transform -translate-y-1/2 h-3 w-3 text-neutral-500 dark:text-neutral-400 pointer-events-none" />
                </div>
                </div>
              )}
            </div>

            {/* Bottom row with Adaptive and Difficulty */}
            <div className="flex flex-col gap-1">
              {/* Adaptive Learning Toggle */}
              <div className="flex items-center gap-1">
                <label className={`flex items-center gap-1 ${selectedStudyList ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'}`}>
                  <input
                    type="checkbox"
                    checked={useAdaptiveTesting}
                    onChange={(e) => {
                      // Don't allow enabling adaptive testing when a study list is selected
                      if (!selectedStudyList) {
                        setUseAdaptiveTesting(e.target.checked)
                      }
                    }}
                    disabled={!!selectedStudyList}
                    className="rounded border-neutral-300 text-primary-600 focus:ring-primary-500 h-3 w-3 disabled:opacity-50"
                  />
                  <span className="text-xs font-medium">Adaptive Learning</span>
                </label>
                {useAdaptiveTesting && (
                  <span className="text-xs text-neutral-500">Auto-adjusts</span>
                )}
                {selectedStudyList && (
                  <span className="text-xs text-neutral-500 italic">(disabled with study list)</span>
                )}
              </div>

              {/* Difficulty Selection - Always visible below adaptive */}
              {!selectedStudyList && (
                <div className={`flex items-center gap-1 flex-wrap ml-4 ${useAdaptiveTesting ? 'opacity-50' : ''}`}>
                  <span className="text-xs font-medium text-neutral-700 dark:text-neutral-300">Difficulty:</span>
                  <div className="flex flex-wrap gap-0.5">
                    {['Beginner', 'Elementary', 'Intermediate', 'Advanced', 'Expert'].map((level) => (
                      <label key={level} className={`flex items-center gap-0.5 ${useAdaptiveTesting ? 'cursor-not-allowed' : 'cursor-pointer'}`}>
                        <input
                          type="checkbox"
                          checked={selectedDifficulties.includes(level)}
                          onChange={() => !useAdaptiveTesting && toggleDifficulty(level)}
                          disabled={useAdaptiveTesting}
                          className="rounded border-neutral-300 text-primary-600 focus:ring-primary-500 h-3 w-3 disabled:opacity-50"
                        />
                        <span className="text-xs">{level.substring(0, 3)}</span>
                      </label>
                    ))}
                  </div>
                  {useAdaptiveTesting && (
                    <span className="text-xs text-neutral-500 italic ml-1">(auto-selected)</span>
                  )}
                  <div className="flex gap-0.5">
                    <button
                      type="button"
                      onClick={() => setSelectedDifficulties(['Beginner', 'Elementary', 'Intermediate', 'Advanced', 'Expert'])}
                      className="text-xs text-primary-600 hover:text-primary-700 font-medium px-1 py-0.5 rounded hover:bg-primary-50"
                    >
                      All
                    </button>
                    <button
                      type="button"
                      onClick={() => setSelectedDifficulties(['Beginner'])}
                      className="text-xs text-neutral-500 hover:text-neutral-700 px-1 py-0.5 rounded hover:bg-neutral-100"
                    >
                      Clear
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Unified Stats Section */}
          <div className="flex-shrink-0">
            <h4 className="text-xs font-medium mb-1 flex items-center gap-0.5">
              <ClockIcon className="h-3 w-3 text-neutral-600" />
              Statistics
            </h4>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-1 text-xs">
              {/* Session Words */}
              <div className="bg-neutral-50 dark:bg-neutral-800 rounded px-1.5 py-0.5 text-center">
                <span className="font-bold text-primary-600">{sessionStats.total}</span>
                <span className="text-neutral-500 ml-0.5">words</span>
              </div>
              
              {/* Session Accuracy */}
              <div className="bg-neutral-50 dark:bg-neutral-800 rounded px-1.5 py-0.5 text-center">
                <span className="font-bold text-green-600">
                  {sessionStats.total > 0 ? Math.round((sessionStats.correct / sessionStats.total) * 100) : 0}%
                </span>
                <span className="text-neutral-500 ml-0.5">today</span>
              </div>
              
              {/* Overall Correct */}
              {user && stats.total > 0 && (
                <>
                  <div className="bg-neutral-50 dark:bg-neutral-800 rounded px-1.5 py-0.5 text-center">
                    <span className="font-bold text-green-500">{stats.correct}</span>
                    <span className="text-neutral-500 ml-0.5">✓</span>
                  </div>
                  
                  {/* Overall Percentage */}
                  <div className="bg-neutral-50 dark:bg-neutral-800 rounded px-1.5 py-0.5 text-center">
                    <span className="font-bold text-primary-600">
                      {Math.round((stats.correct / stats.total) * 100)}%
                    </span>
                    <span className="text-neutral-500 ml-0.5">total</span>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
        {!showResult ? (
          <>
            {/* Skip link and counter */}
            <div className="flex justify-between items-center mb-2">
              <SkipButton onSkip={skipQuestion} />
              {wordBank.length > 0 && (
                <span className="text-xs text-neutral-600 dark:text-neutral-400">
                  {(currentPage * WORDS_PER_PAGE + currentIndex + 1).toLocaleString()} / {(totalWords || wordBank.length).toLocaleString()}
                </span>
              )}
            </div>
            
            {/* Audio Controls */}
            <div className="text-center mb-2 sm:mb-4">
              <button
                onClick={playAudio}
                className="inline-flex items-center gap-3 px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-lg font-medium"
              >
                <SpeakerWaveIcon className="h-6 w-6" />
                Play Word
              </button>
            </div>

            {/* Context Information - More Compact */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5 sm:gap-3 mb-2 sm:mb-4">
              <div className="bg-blue-50 dark:bg-blue-900/20 rounded p-1.5 sm:p-3">
                <h3 className="font-semibold text-xs mb-0.5 sm:mb-1 flex items-center gap-1">
                  <InformationCircleIcon className="h-3 w-3 sm:h-4 sm:w-4 text-blue-600 dark:text-blue-400" />
                  Definition
                </h3>
                <p className="text-xs text-neutral-700 dark:text-neutral-300">
                  {replaceWordAndVariationsWithBlanks(currentWord.definition, currentWord.word)}
                </p>
              </div>

              <div className="bg-gold-50 dark:bg-gold-900/20 rounded p-1.5 sm:p-3">
                <h3 className="font-semibold text-xs mb-0.5 sm:mb-1">Example</h3>
                <p className="text-xs text-neutral-700 dark:text-neutral-300 italic">
                  "{replaceWordAndVariationsWithBlanks(currentWord.example_sentence, currentWord.word)}"
                </p>
              </div>
            </div>

            <div className="text-center mb-1 sm:mb-4 space-y-1">
              <div className="flex justify-center items-center gap-2 sm:gap-3 text-xs">
                {(currentWord as any).spelling_difficulty_levels?.name && (
                  <span className={`px-1 sm:px-2 py-0.5 sm:py-1 rounded text-xs font-medium ${
                    (currentWord as any).spelling_difficulty_levels?.name === 'Beginner' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' :
                    (currentWord as any).spelling_difficulty_levels?.name === 'Elementary' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' :
                    (currentWord as any).spelling_difficulty_levels?.name === 'Intermediate' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' :
                    (currentWord as any).spelling_difficulty_levels?.name === 'Advanced' ? 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400' :
                    'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                  }`}>
                    {(currentWord as any).spelling_difficulty_levels?.name}
                  </span>
                )}
                {currentWord.part_of_speech && (
                  <span className="text-neutral-600 dark:text-neutral-400 italic">
                    {currentWord.part_of_speech}
                  </span>
                )}
              </div>
            </div>

            {/* Input Form */}
            <form onSubmit={handleSubmit} className="space-y-1.5 sm:space-y-3">
              <div>
                <label className="block text-xs font-medium mb-0.5 sm:mb-1">
                  Type your spelling:
                </label>
                <input
                  type="text"
                  value={userInput}
                  onChange={(e) => {
                    setUserInput(e.target.value)
                    // Save session state as user types
                    if (currentWord) {
                      saveSessionState(currentWord, currentIndex, e.target.value, showResult, isCorrect, currentPage, selectedStudyList?.id, selectedDifficulties)
                    }
                  }}
                  className="w-full px-2 sm:px-3 py-1.5 sm:py-2 text-base sm:text-lg font-mono border-2 border-neutral-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-neutral-800"
                  placeholder=""
                  autoFocus
                />
              </div>
              <button
                type="submit"
                disabled={!userInput.trim()}
                className="w-full py-2 bg-primary-700 text-white rounded-lg hover:bg-primary-800 disabled:bg-neutral-400 disabled:cursor-not-allowed transition-colors text-sm font-semibold shadow-md"
              >
                Submit
              </button>
              
            </form>
          </>
        ) : (
          <>
            {/* Result Display - Eye-catching and Compact */}
            <div className={`mb-3 p-3 rounded-lg border-2 ${
              isCorrect 
                ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-700' 
                : 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-700'
            }`}>
              {isCorrect ? (
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-1">
                    <CheckCircleIcon className="h-6 w-6 text-green-500" />
                    <span className="text-xl font-bold text-green-700 dark:text-green-400">
                      Excellent!
                    </span>
                  </div>
                  <div className="text-base font-semibold text-green-600 dark:text-green-300">
                    You spelled "{currentWord.word}" correctly!
                  </div>
                </div>
              ) : (
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-2">
                    <XCircleIcon className="h-6 w-6 text-red-500" />
                    <span className="text-xl font-bold text-red-700 dark:text-red-400">Almost there!</span>
                  </div>
                  
                  {/* Large, prominent correction display */}
                  <div className="bg-white dark:bg-neutral-800 rounded-lg p-3 border border-neutral-200 dark:border-neutral-600">
                    <div className="text-xs font-medium text-neutral-600 dark:text-neutral-400 mb-1">
                      Your spelling vs. Correct spelling
                    </div>
                    <div className="flex items-center justify-center gap-3 text-xl font-mono">
                      <span className="text-red-600 dark:text-red-400 line-through decoration-2 decoration-red-500">
                        {userInput}
                      </span>
                      <span className="text-2xl">→</span>
                      <span className="text-green-600 dark:text-green-400 font-bold text-2xl bg-green-100 dark:bg-green-900/30 px-3 py-1 rounded border border-green-300 dark:border-green-600">
                        {currentWord.word}
                      </span>
                    </div>
                  </div>
                </div>
              )}
              
              {currentWord.pronunciation_guide && (
                <div className="text-center mt-2 pt-2 border-t border-neutral-200 dark:border-neutral-700">
                  <div className="text-xs font-medium text-neutral-600 dark:text-neutral-400 mb-0.5">
                    Pronunciation Guide
                  </div>
                  <div className="text-sm font-mono font-bold text-primary-600 dark:text-primary-400">
                    {currentWord.pronunciation_guide}
                  </div>
                </div>
              )}
            </div>

            {/* Learning Tips - Compact */}
            <div className="space-y-1.5 mb-3">
              {(currentWord.memory_tips || currentWord.pronunciation_tips) && (
                <div className="bg-primary-50 dark:bg-primary-900/20 rounded p-2">
                  <h3 className="font-semibold text-xs mb-0.5 flex items-center gap-1">
                    <AcademicCapIcon className="h-3 w-3 text-primary-600 dark:text-primary-400" />
                    Memory Tips
                  </h3>
                  <p className="text-xs text-neutral-700 dark:text-neutral-300">
                    {currentWord.memory_tips || currentWord.pronunciation_tips}
                  </p>
                </div>
              )}

              {/* Etymology Section - Always Open */}
              {currentWord.etymology && (
                <div className="bg-neutral-50 dark:bg-neutral-800 rounded p-2">
                  <h3 className="font-semibold text-xs mb-0.5">
                    Word Origin & Etymology
                  </h3>
                  <p className="text-xs text-neutral-700 dark:text-neutral-300">
                    {currentWord.etymology}
                  </p>
                </div>
              )}

              {currentWord.common_misspellings && currentWord.common_misspellings.length > 0 && (
                <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded p-2">
                  <h3 className="font-semibold text-xs mb-0.5">Common Misspellings</h3>
                  <div className="flex flex-wrap gap-1">
                    {currentWord.common_misspellings.map((spelling, idx) => (
                      <span 
                        key={idx}
                        className="px-1 py-0.5 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 rounded text-xs font-mono line-through"
                      >
                        {spelling}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <button
              onClick={nextWord}
              className="w-full py-1.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm"
            >
              Next Word →
            </button>
          </>
        )}
      </div>

      {/* Flag Content Modal */}
      {showFlagModal && currentWord && (
        <FlagContentModal
          isOpen={showFlagModal}
          onClose={() => setShowFlagModal(false)}
          contentType="question"
          contentId={currentWord.id}
          contentTitle={`Spelling: ${currentWord.word}`}
        />
      )}
    </div>
  )
}

export default SpellingPage
import React, { useState, useEffect, useCallback } from 'react'
import { useLocation } from 'react-router-dom'
import { supabase } from '../services/supabase'
// import { spacedRepetitionService } from '../services/spacedRepetitionService'
import { useAuth } from '../contexts/AuthContext'
import { useSpelling } from '../contexts/SpellingContext'
import { checkSpellingTables, createSpellingTables } from '../utils/createSpellingTables'
import { replaceWordAndVariationsWithBlanks } from '../utils/vocabularyHelpers'
import { getVocabularyDifficultyLevels } from '../services/difficultyLevels'
import { SpellingWordWithDifficulties, VocabularyDifficultyLevel } from '../types/difficultyLevels'
import { 
  CheckCircleIcon, 
  XCircleIcon,
  AcademicCapIcon,
  ClockIcon,
  FlagIcon,
  SpeakerWaveIcon,
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

interface VocabularyQuestion {
  word: SpellingWord
  options: string[]
  correctAnswer: string
  isWordToDefinition?: boolean
}

interface VocabularyTrainerPageProps {
  showTabs?: boolean
  onTabChange?: (tab: 'vocabulary' | 'spelling') => void
}

const VocabularyTrainerPage: React.FC<VocabularyTrainerPageProps> = ({ showTabs, onTabChange }) => {
  const { user } = useAuth()
  const location = useLocation()
  const { selectedDifficulties, setSelectedDifficulties, toggleDifficulty, useAdaptiveTesting, setUseAdaptiveTesting } = useSpelling()
  const [currentQuestion, setCurrentQuestion] = useState<VocabularyQuestion | null>(null)
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [difficultyLevels, setDifficultyLevels] = useState<VocabularyDifficultyLevel[]>([])
  const [selectedAnswer, setSelectedAnswer] = useState<string>('')
  const [showResult, setShowResult] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)
  const [loading, setLoading] = useState(true)
  const [wordBank, setWordBank] = useState<SpellingWord[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [stats, setStats] = useState({ correct: 0, total: 0 })
  const [sessionStats] = useState({ correct: 0, total: 0 })
  const [showFlagModal, setShowFlagModal] = useState(false)
  const [isWordToDefinition, setIsWordToDefinition] = useState(true)
  
  // Study list functionality
  const [studyLists, setStudyLists] = useState<StudyListWithCount[]>([])
  const [selectedStudyList, setSelectedStudyList] = useState<StudyListWithCount | null>(null)
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(0)
  const [totalWords, setTotalWords] = useState(0)
  const WORDS_PER_PAGE = 50

  // Session storage keys
  const VOCAB_SESSION_KEY = 'vocabularyTrainerSession'

  // Helper function to organize and sort study lists
  const organizeStudyLists = (lists: StudyListWithCount[]) => {
    // Filter for vocabulary difficulty lists based on the descriptions
    const difficultyLists = lists.filter(list => 
      list.name.includes('Basic') || 
      list.name.includes('Elementary') || 
      list.name.includes('Intermediate') || 
      list.name.includes('Advanced') || 
      list.name.includes('Expert')
    )
    
    // Other vocabulary lists (not grade or difficulty based)
    const otherVocabLists = lists.filter(list => 
      list.name.includes('Vocab') && 
      !list.name.includes('Grade') && 
      !difficultyLists.find(d => d.id === list.id)
    )
    
    // Sort difficulty lists by their numerical order (1-5)
    const difficultyOrder = ['Basic', 'Elementary', 'Intermediate', 'Advanced', 'Expert']
    const sortedDifficultyLists = difficultyLists.sort((a, b) => {
      const aIndex = difficultyOrder.findIndex(level => a.name.includes(level))
      const bIndex = difficultyOrder.findIndex(level => b.name.includes(level))
      return (aIndex === -1 ? 999 : aIndex) - (bIndex === -1 ? 999 : bIndex)
    })
    
    // Sort other vocab lists by name
    const sortedOtherLists = otherVocabLists.sort((a, b) => a.name.localeCompare(b.name))
    
    return { difficultyLists: sortedDifficultyLists, otherVocabLists: sortedOtherLists }
  }

  // Load available study lists
  const loadStudyLists = useCallback(async () => {
    try {
      // Get public study lists for vocabulary (existing Vocab + Grade Level Vocabulary)
      const { data, error } = await supabase
        .from('study_lists')
        .select('*')
        .eq('is_public', true)
        .or('name.ilike.%Vocab%,name.ilike.%Vocabulary%')
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
          list.name.toLowerCase().includes('vocabulary') || 
          list.name.toLowerCase().includes('vocab')
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

  // Save session state
  const saveSessionState = useCallback((question: VocabularyQuestion, index: number, selectedAnswer: string, showResult: boolean, isCorrect: boolean, page: number = 0, studyListId?: string, difficulties?: string[]) => {
    const sessionState = {
      currentQuestion: question,
      currentIndex: index,
      currentPage: page,
      selectedAnswer,
      showResult,
      isCorrect,
      selectedStudyListId: studyListId || null,
      selectedDifficulties: difficulties || selectedDifficulties,
      timestamp: Date.now()
    }
    sessionStorage.setItem(VOCAB_SESSION_KEY, JSON.stringify(sessionState))
  }, [VOCAB_SESSION_KEY, selectedDifficulties])

  // Load session state
  const loadSessionState = useCallback(() => {
    try {
      const saved = sessionStorage.getItem(VOCAB_SESSION_KEY)
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
  }, [VOCAB_SESSION_KEY])

  // Clear session state
  const clearSessionState = useCallback(() => {
    sessionStorage.removeItem(VOCAB_SESSION_KEY)
  }, [VOCAB_SESSION_KEY])

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
              vocabulary_difficulty_levels!vocabulary_difficulty_id(id, name, description)
            `)
            .in('id', wordIds)

          if (wordsError) {
            console.error('Error fetching words from study list:', wordsError)
            // Try fallback without join
            const { data: fallbackWords, error: fallbackError } = await supabase
              .from('spelling_words')
              .select('*')
              .in('id', wordIds)
              
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
              if (page === 0) {
                generateQuestion(shuffled, 0)
                setCurrentIndex(0)
              }
            }
          } else if (words && words.length > 0) {
            // Shuffle for variety
            const shuffled = [...words].sort(() => Math.random() - 0.5)
            setWordBank(shuffled)
            setCurrentPage(page)
            if (page === 0) {
              generateQuestion(shuffled, 0)
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
          .eq('is_vocabulary_word', true)
          
        if (selectedDifficulties.length > 0 && selectedDifficulties.length < 5) {
          const difficultyMap: Record<string, number> = { 'Basic': 1, 'Elementary': 2, 'Intermediate': 3, 'Advanced': 4, 'Expert': 5 };
          countQuery = countQuery.in('vocabulary_difficulty_id', selectedDifficulties.map(name => difficultyMap[name] || 1))
        }
        
        const { count } = await countQuery
        setTotalWords(count || 0)
      }
      
      // Try to query with joins to the new difficulty tables first
      let query = supabase
        .from('spelling_words')
        .select(`
          *,
          vocabulary_difficulty_levels!vocabulary_difficulty_id(id, name, description)
        `)
        .eq('is_vocabulary_word', true)  // Filter for vocabulary words only
        .order('vocabulary_difficulty_id')
        .range(offset, offset + WORDS_PER_PAGE - 1)

      // Apply difficulty filter from selected difficulties
      if (selectedDifficulties.length > 0 && selectedDifficulties.length < 5) {
        // Filter by the foreign key ID based on selected difficulty names
        query = query.in('vocabulary_difficulty_id', selectedDifficulties.map(name => {
          const difficultyMap: Record<string, number> = { 'Basic': 1, 'Elementary': 2, 'Intermediate': 3, 'Advanced': 4, 'Expert': 5 };
          return difficultyMap[name] || 1;
        }))
      }

      let { data, error } = await query

      // If the join fails, fall back to old structure
      if (error && error.message?.includes('vocabulary_difficulty_levels!')) {
        console.log('New difficulty tables not found, using legacy structure...')
        
        query = supabase
          .from('spelling_words')
          .select('*')
          .eq('is_vocabulary_word', true)  // Filter for vocabulary words only
          .order('vocabulary_difficulty_id')
          .range(offset, offset + WORDS_PER_PAGE - 1)

        if (selectedDifficulties.length > 0 && selectedDifficulties.length < 5) {
          // Map difficulty names to IDs for filtering
          const difficultyMap: Record<string, number> = { 'Basic': 1, 'Elementary': 2, 'Intermediate': 3, 'Advanced': 4, 'Expert': 5 };
          const difficultyIds = selectedDifficulties.map(name => difficultyMap[name] || 1);
          query = query.in('vocabulary_difficulty_id', difficultyIds)
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
        
        // Check for saved session state first
        const savedSession = loadSessionState()
        if (savedSession && savedSession.currentQuestion && savedSession.currentPage === page) {
          // Restore saved session if we're on the same page
          setCurrentQuestion(savedSession.currentQuestion)
          setCurrentIndex(savedSession.currentIndex)
          setSelectedAnswer(savedSession.selectedAnswer)
          setShowResult(savedSession.showResult)
          setIsCorrect(savedSession.isCorrect)
          
          // Auto-play audio if restoring a result state (if autoplay enabled)
          const autoplayEnabled = localStorage.getItem('audioAutoplay') !== 'false'
          if (savedSession.showResult && autoplayEnabled) {
            setTimeout(() => {
              speakWord(savedSession.currentQuestion.word.word)
            }, 1000) // Longer delay for page restoration
          }
        } else if (page === 0) {
          // Start fresh on first page
          generateQuestion(shuffled, 0)
          setCurrentIndex(0)
        }
      }
    } catch (error) {
      console.error('Error fetching words:', error)
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedDifficulties, selectedStudyList, loadSessionState, WORDS_PER_PAGE])

  // Helper function to extract primary language origin from etymology
  const getLanguageOrigin = (etymology: string | undefined): string => {
    if (!etymology) return 'unknown'
    
    const lowerEtymology = etymology.toLowerCase()
    
    // Common language patterns in etymology
    const languagePatterns = [
      { pattern: /\b(japanese|japan)\b/, origin: 'japanese' },
      { pattern: /\b(chinese|china|mandarin|cantonese)\b/, origin: 'chinese' },
      { pattern: /\b(french|france|old french|middle french)\b/, origin: 'french' },
      { pattern: /\b(german|germanic|old german|middle german)\b/, origin: 'german' },
      { pattern: /\b(spanish|spain|castilian)\b/, origin: 'spanish' },
      { pattern: /\b(italian|italy)\b/, origin: 'italian' },
      { pattern: /\b(greek|ancient greek|modern greek)\b/, origin: 'greek' },
      { pattern: /\b(latin|roman)\b/, origin: 'latin' },
      { pattern: /\b(arabic|arab)\b/, origin: 'arabic' },
      { pattern: /\b(sanskrit|hindi|urdu|persian)\b/, origin: 'indo-iranian' },
      { pattern: /\b(dutch|netherlands|flemish)\b/, origin: 'dutch' },
      { pattern: /\b(russian|slavic|polish|czech)\b/, origin: 'slavic' },
      { pattern: /\b(portuguese|portugal)\b/, origin: 'portuguese' },
      { pattern: /\b(hebrew|yiddish)\b/, origin: 'hebrew' },
      { pattern: /\b(turkish|ottoman)\b/, origin: 'turkish' },
      { pattern: /\b(english|anglo|old english|middle english)\b/, origin: 'english' },
      { pattern: /\b(norse|norwegian|swedish|danish|iceland)\b/, origin: 'norse' },
    ]
    
    for (const { pattern, origin } of languagePatterns) {
      if (pattern.test(lowerEtymology)) {
        return origin
      }
    }
    
    return 'other'
  }

  const generateQuestion = (words: SpellingWord[], index: number) => {
    if (!words || words.length === 0) return

    const targetWord = words[index]
    const targetOrigin = getLanguageOrigin(targetWord.etymology)
    const targetPartOfSpeech = targetWord.part_of_speech?.toLowerCase()
    
    // First priority: words with same part of speech
    const samePartOfSpeech = words.filter(w => 
      w.id !== targetWord.id && 
      w.part_of_speech?.toLowerCase() === targetPartOfSpeech &&
      targetPartOfSpeech // Only filter if part of speech exists
    )
    
    // Second priority: words from same etymology/origin with same part of speech
    const sameOriginAndPOS = samePartOfSpeech.filter(w => 
      getLanguageOrigin(w.etymology) === targetOrigin &&
      targetOrigin !== 'unknown' && targetOrigin !== 'other'
    )
    
    // Third priority: words from same difficulty level with same part of speech
    const sameLevelAndPOS = samePartOfSpeech.filter(w => 
      w.vocabulary_difficulty_id === targetWord.vocabulary_difficulty_id
    )
    
    // Fourth priority: words from same difficulty level (any part of speech)
    const sameLevel = words.filter(w => 
      w.id !== targetWord.id && 
      w.vocabulary_difficulty_id === targetWord.vocabulary_difficulty_id
    )
    
    // Fifth priority: all other words
    const allOthers = words.filter(w => w.id !== targetWord.id)
    
    let alternatives: SpellingWord[] = []
    
    // Try to get 3 alternatives with same part of speech first
    if (samePartOfSpeech.length >= 3) {
      // Prefer same origin and POS if available
      if (sameOriginAndPOS.length >= 3) {
        alternatives = [...sameOriginAndPOS].sort(() => Math.random() - 0.5).slice(0, 3)
      }
      // Then same difficulty and POS
      else if (sameLevelAndPOS.length >= 3) {
        alternatives = [...sameLevelAndPOS].sort(() => Math.random() - 0.5).slice(0, 3)
      }
      // Otherwise any words with same POS
      else {
        alternatives = [...samePartOfSpeech].sort(() => Math.random() - 0.5).slice(0, 3)
      }
    }
    // If not enough same part of speech, mix with same difficulty level
    else if (samePartOfSpeech.length > 0) {
      const remainingNeeded = 3 - samePartOfSpeech.length
      const additionalOptions = sameLevel
        .filter(w => !samePartOfSpeech.find(sp => sp.id === w.id))
        .sort(() => Math.random() - 0.5)
        .slice(0, remainingNeeded)
      alternatives = [...samePartOfSpeech, ...additionalOptions]
    }
    // Fall back to same difficulty level
    else if (sameLevel.length >= 3) {
      alternatives = [...sameLevel].sort(() => Math.random() - 0.5).slice(0, 3)
    }
    // Final fallback to any words
    else {
      alternatives = [...allOthers].sort(() => Math.random() - 0.5).slice(0, 3)
    }
    
    if (isWordToDefinition) {
      // Word-to-definition mode: show word, select from definitions
      const wrongDefinitions = alternatives.map(w => w.definition)
      const allDefinitions = [targetWord.definition, ...wrongDefinitions]
      const shuffledDefinitions = [...allDefinitions].sort(() => Math.random() - 0.5)
      
      setCurrentQuestion({
        word: targetWord,
        options: shuffledDefinitions,
        correctAnswer: targetWord.definition,
        isWordToDefinition: true
      })
    } else {
      // Definition-to-word mode (original): show definition, select from words
      const wrongOptions = alternatives.map(w => w.word)
      const allOptions = [targetWord.word, ...wrongOptions]
      const shuffledOptions = [...allOptions].sort(() => Math.random() - 0.5)

      setCurrentQuestion({
        word: targetWord,
        options: shuffledOptions,
        correctAnswer: targetWord.word,
        isWordToDefinition: false
      })
    }
  }

  const fetchUserStats = useCallback(async () => {
    if (!user) return

    try {
      const { data, error } = await supabase
        .from('user_vocabulary_attempts')
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

  const initializeVocabularyTrainer = useCallback(async () => {
    // Check if tables exist, create if not
    const tablesExist = await checkSpellingTables()
    if (!tablesExist) {
      console.log('Creating spelling bee tables...')
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
      // Restore selected difficulties and study list
      if (savedSession.selectedDifficulties) {
        setSelectedDifficulties(savedSession.selectedDifficulties)
      }
      if (savedSession.currentPage !== undefined) {
        setCurrentPage(savedSession.currentPage)
      }
      // Note: We'll restore the study list after lists are loaded
    }
    initializeVocabularyTrainer()
  }, [initializeVocabularyTrainer, loadSessionState, setSelectedDifficulties])

  // Load difficulty levels on component mount
  useEffect(() => {
    const loadDifficultyLevels = async () => {
      try {
        const levels = await getVocabularyDifficultyLevels()
        setDifficultyLevels(levels)
      } catch (error) {
        console.error('Error loading vocabulary difficulty levels:', error)
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
          
          // Fetch words in batches to avoid URL length limits
          const batchSize = 50
          const allWords: SpellingWord[] = []
          
          for (let i = 0; i < wordIds.length; i += batchSize) {
            const batchIds = wordIds.slice(i, i + batchSize)
            
            const { data: words, error } = await supabase
              .from('spelling_words')
              .select(`
                *,
                vocabulary_difficulty_levels!vocabulary_difficulty_id(id, name, description)
              `)
              .in('id', batchIds)
            
            if (error) {
              console.error('Error fetching study list words batch:', error)
              // Try fallback without join
              const { data: fallbackWords } = await supabase
                .from('spelling_words')
                .select('*')
                .in('id', batchIds)
              
              if (fallbackWords) {
                allWords.push(...fallbackWords)
              }
            } else if (words) {
              allWords.push(...words)
            }
          }
          
          if (allWords.length > 0) {
            // Sort words to match the order from study list
            const sortedWords = wordIds.map((id: string) => 
              allWords.find(w => w.id === id)
            ).filter(Boolean)
            
            setWordBank(sortedWords)
            setCurrentIndex(startIndex)
            generateQuestion(sortedWords, startIndex)
            setLoading(false)
          }
        }
        
        loadStudyListWords()
        return
      }
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.state])

  // Refetch words when selected difficulties or study list changes
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
  
  // Regenerate current question when mode changes
  useEffect(() => {
    if (wordBank.length > 0 && !showResult) {
      generateQuestion(wordBank, currentIndex)
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isWordToDefinition])

  const handleAnswerSelect = (answer: string) => {
    if (showResult) return
    setSelectedAnswer(answer)
    // Save session state when answer is selected
    if (currentQuestion) {
      saveSessionState(currentQuestion, currentIndex, answer, showResult, isCorrect, currentPage, selectedStudyList?.id, selectedDifficulties)
    }
    // Auto-submit the answer after a brief delay
    setTimeout(() => {
      handleSubmitAnswer(answer)
    }, 100)
  }
  
  const handleSubmitAnswer = async (answer: string) => {
    if (!currentQuestion) return
    
    const correct = answer === currentQuestion.correctAnswer
    setIsCorrect(correct)
    setShowResult(true)
    
    // Update session stats
    setStats(prev => ({
      ...prev,
      correct: correct ? prev.correct + 1 : prev.correct,
      total: prev.total + 1
    }))
    
    // Save session state after submission
    saveSessionState(currentQuestion, currentIndex, answer, true, correct, currentPage, selectedStudyList?.id, selectedDifficulties)
    
    // Auto-play audio for the correct word when result is shown (if autoplay enabled)
    const autoplayEnabled = localStorage.getItem('audioAutoplay') !== 'false'
    
    if (autoplayEnabled && currentQuestion.word.word) {
      setTimeout(() => {
        speakWord(currentQuestion.word.word)
      }, 200) // Shorter delay for quicker audio playback
    }
  }


  const nextQuestion = () => {
    // Clear session state when moving to next question
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
        generateQuestion(wordBank, 0)
      }
    } else {
      const nextIndex = currentIndex + 1
      setCurrentIndex(nextIndex)
      generateQuestion(wordBank, nextIndex)
    }
    
    setSelectedAnswer('')
    setShowResult(false)
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
        generateQuestion(wordBank, 0)
      }
    } else {
      const nextIndex = currentIndex + 1
      setCurrentIndex(nextIndex)
      generateQuestion(wordBank, nextIndex)
    }
    
    setSelectedAnswer('')
    setShowResult(false)
  }

  const speakWord = (word: string) => {
    if ('speechSynthesis' in window) {
      // Cancel any previous speech
      window.speechSynthesis.cancel()
      
      const utterance = new SpeechSynthesisUtterance(word)
      utterance.rate = 0.8
      utterance.volume = 0.8
      utterance.pitch = 1.0
      
      window.speechSynthesis.speak(utterance)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!currentQuestion) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6 text-center">
          <p className="text-lg">No vocabulary words available. Please check back later!</p>
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
            className="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 bg-primary-600 text-white"
          >
            <AcademicCapIcon className="h-4 w-4" />
            Vocabulary
          </button>
          <button
            onClick={() => onTabChange?.('spelling')}
            className="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-700"
          >
            <SpeakerWaveIcon className="h-4 w-4" />
            Spelling
          </button>
        </div>
      )}
      
      {/* Combined Vocabulary Practice Card */}
      <div className="bg-white dark:bg-neutral-900 rounded-lg sm:rounded-xl shadow-lg p-2 sm:p-3 relative">
        {/* Header with Action Buttons and Title */}
        <div className="flex items-center mb-1 sm:mb-2">
          <div className="w-10">
            {currentQuestion && (
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
            Vocabulary Trainer
          </h1>
          
          <div className="w-10 flex justify-end">
            {currentQuestion && (
              <StudyListActions
                itemType="vocabulary_word"
                itemId={currentQuestion.word.id}
                itemData={currentQuestion.word}
                itemTitle={`Vocabulary: ${currentQuestion.word.word}`}
                className="bg-white dark:bg-neutral-800 rounded-lg shadow-sm border border-neutral-200 dark:border-neutral-700 px-2 py-1"
              />
            )}
          </div>
        </div>
        
        {/* Settings and Stats Row */}
        <div className="flex justify-between items-start mb-1">
          {/* Practice Settings */}
          <div className="flex flex-col gap-1 sm:gap-2 items-start flex-1 mr-2 sm:mr-0">
            {/* First Row: Mode Toggle and Study List */}
            <div className="flex flex-col lg:flex-row gap-1 sm:gap-2">
              {/* Mode Toggle */}
              <div className="flex items-center gap-1">
                <label className="flex items-center gap-1 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={isWordToDefinition}
                    onChange={(e) => setIsWordToDefinition(e.target.checked)}
                    className="rounded border-neutral-300 text-primary-600 focus:ring-primary-500 h-3 w-3"
                  />
                  <span className="text-xs font-medium">Word → Definition</span>
                </label>
              </div>

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
                      setCurrentQuestion(null)
                      setSelectedAnswer('')
                      setShowResult(false)
                    }}
                    className="bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 px-2 py-1 rounded text-xs border-0 focus:ring-1 focus:ring-neutral-500 appearance-none pr-6"
                  >
                    <option value="">All Words</option>
                    {(() => {
                      const { difficultyLists, otherVocabLists } = organizeStudyLists(studyLists)
                      return (
                        <>
                          {difficultyLists.length > 0 && (
                            <optgroup label="Vocabulary Difficulty Levels">
                              {difficultyLists.map((list) => (
                                <option key={list.id} value={list.id}>
                                  {list.name} {list.itemCount !== undefined && `(${list.itemCount.toLocaleString()})`}
                                </option>
                              ))}
                            </optgroup>
                          )}
                          {otherVocabLists.length > 0 && (
                            <optgroup label="Other Vocabulary Lists">
                              {otherVocabLists.map((list) => (
                                <option key={list.id} value={list.id}>
                                  {list.name} {list.itemCount !== undefined && `(${list.itemCount})`}
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

            {/* Second Row: Adaptive and Difficulty */}
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
                    {['Basic', 'Elementary', 'Intermediate', 'Advanced', 'Expert'].map((level) => (
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
                  {useAdaptiveTesting ? (
                    <span className="text-xs text-neutral-500 italic ml-1">(auto-selected)</span>
                  ) : (
                    <div className="flex gap-0.5">
                      <button
                        type="button"
                        onClick={() => setSelectedDifficulties(['Basic', 'Elementary', 'Intermediate', 'Advanced', 'Expert'])}
                        className="text-xs text-primary-600 hover:text-primary-700 font-medium px-1 py-0.5 rounded hover:bg-primary-50"
                      >
                        All
                      </button>
                      <button
                        type="button"
                        onClick={() => setSelectedDifficulties(['Basic'])}
                        className="text-xs text-neutral-500 hover:text-neutral-700 px-1 py-0.5 rounded hover:bg-neutral-100"
                      >
                        Clear
                      </button>
                    </div>
                  )}
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
            
            {/* Question Content */}
            <div className="space-y-2 mb-2">
              {currentQuestion.isWordToDefinition ? (
                // Word-to-definition mode: Display the word prominently (without example)
                <div className="bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/30 dark:to-primary-800/20 rounded-lg p-3 sm:p-4 border-2 border-primary-200 dark:border-primary-700 shadow-lg">
                  <div className="text-center">
                    <p className="text-3xl sm:text-4xl font-bold text-primary-700 dark:text-primary-400 mb-2">
                      {currentQuestion.word.word}
                    </p>
                    {currentQuestion.word.part_of_speech && (
                      <span className="text-sm text-neutral-600 dark:text-neutral-400 italic">
                        ({currentQuestion.word.part_of_speech})
                      </span>
                    )}
                  </div>
                </div>
              ) : (
                // Definition-to-word mode: Display the definition (original behavior)
                <>
                  <div className="bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/30 dark:to-primary-800/20 rounded-lg p-3 sm:p-4 border-2 border-primary-200 dark:border-primary-700 shadow-lg">
                    <p className="text-base sm:text-lg font-medium text-neutral-800 dark:text-neutral-200 leading-snug text-center">
                      {replaceWordAndVariationsWithBlanks(currentQuestion.word.definition, currentQuestion.word.word)}
                    </p>
                  </div>

                  <div className="bg-gold-50 dark:bg-gold-900/20 rounded-lg p-2 text-center border border-gold-200 dark:border-gold-800">
                    <h3 className="font-semibold text-sm mb-2 text-gold-700 dark:text-gold-400">Example</h3>
                    <p className="text-sm text-neutral-700 dark:text-neutral-300 italic">
                      "{replaceWordAndVariationsWithBlanks(currentQuestion.word.example_sentence, currentQuestion.word.word)}"
                    </p>
                  </div>
                </>
              )}
            </div>

            <div className="text-center mb-2 space-y-1">
              <div className="flex justify-center items-center gap-2 sm:gap-3 text-xs">
                {(currentQuestion.word as any).vocabulary_difficulty_levels?.name && (
                  <span className={`px-1 sm:px-2 py-0.5 sm:py-1 rounded text-xs font-medium ${
                    (currentQuestion.word as any).vocabulary_difficulty_levels?.name === 'Basic' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' :
                    (currentQuestion.word as any).vocabulary_difficulty_levels?.name === 'Elementary' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' :
                    (currentQuestion.word as any).vocabulary_difficulty_levels?.name === 'Intermediate' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' :
                    (currentQuestion.word as any).vocabulary_difficulty_levels?.name === 'Advanced' ? 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400' :
                    'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                  }`}>
                    {(currentQuestion.word as any).vocabulary_difficulty_levels?.name}
                  </span>
                )}
                {currentQuestion.word.part_of_speech && (
                  <span className="text-neutral-600 dark:text-neutral-400 italic">
                    {currentQuestion.word.part_of_speech}
                  </span>
                )}
              </div>
            </div>

            {/* Multiple Choice Options */}
            <div className="space-y-1.5 mb-2">
              <h3 className="font-semibold text-sm">
                {currentQuestion.isWordToDefinition 
                  ? "Which definition matches the word above?" 
                  : "Which word matches the definition above?"}
              </h3>
              <div className={`grid gap-1.5 ${currentQuestion.isWordToDefinition ? 'grid-cols-1' : 'grid-cols-1 sm:grid-cols-2'}`}>
                {currentQuestion.options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => handleAnswerSelect(option)}
                    className={`${currentQuestion.isWordToDefinition ? 'p-2' : 'p-1.5'} text-left border-2 rounded-lg transition-colors ${
                      selectedAnswer === option
                        ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/20'
                        : 'border-neutral-300 dark:border-neutral-600 hover:border-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/10 bg-white dark:bg-neutral-800'
                    }`}
                  >
                    <span className={`text-sm ${currentQuestion.isWordToDefinition ? 'line-clamp-2' : ''}`}>
                      {option}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          </>
        ) : (
          <>
            {/* Result Display */}
            <div className={`mb-2 p-2 rounded-lg ${
              isCorrect 
                ? 'bg-green-50 dark:bg-green-900/20' 
                : 'bg-red-50 dark:bg-red-900/20'
            }`}>
              {isCorrect ? (
                <div className="flex flex-col items-center gap-3">
                  <div className="flex items-center gap-2">
                    <CheckCircleIcon className="h-5 w-5 text-green-500" />
                    <span className="text-sm font-bold text-green-700 dark:text-green-400">
                      Correct!
                    </span>
                  </div>
                  <div className="text-center">
                    {currentQuestion.isWordToDefinition ? (
                      <>
                        <p className="text-2xl font-bold text-green-700 dark:text-green-400 mb-2">
                          {currentQuestion.word.word}
                        </p>
                        <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-2">
                          {currentQuestion.word.definition}
                        </p>
                        {currentQuestion.word.example_sentence && (
                          <div className="bg-gold-50 dark:bg-gold-900/20 rounded-lg p-2 text-center border border-gold-200 dark:border-gold-800 mt-2">
                            <h3 className="font-semibold text-xs mb-1 text-gold-700 dark:text-gold-400">Example:</h3>
                            <p className="text-xs text-neutral-700 dark:text-neutral-300 italic">
                              "{currentQuestion.word.example_sentence}"
                            </p>
                          </div>
                        )}
                      </>
                    ) : (
                      <>
                        <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-2">
                          {replaceWordAndVariationsWithBlanks(currentQuestion.word.definition, currentQuestion.word.word)}
                        </p>
                        <span className="text-5xl font-bold text-green-700 dark:text-green-400">
                          {currentQuestion.word.word}
                        </span>
                      </>
                    )}
                  </div>
                  <div className="flex items-center justify-center gap-3">
                    <button
                      onClick={() => speakWord(currentQuestion.word.word)}
                      className="p-1 hover:bg-green-100 dark:hover:bg-green-800/20 rounded-md transition-colors"
                      title="Hear pronunciation"
                    >
                      <SpeakerWaveIcon className="h-4 w-4 text-green-600 dark:text-green-400" />
                    </button>
                  </div>
                </div>
              ) : (
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-2">
                    <XCircleIcon className="h-5 w-5 text-red-500" />
                    <span className="text-sm font-bold text-red-700 dark:text-red-400">Incorrect</span>
                  </div>
                  <div className="text-center mb-2">
                    <p className="text-sm text-neutral-600 dark:text-neutral-400">
                      {currentQuestion.isWordToDefinition 
                        ? `The word "${currentQuestion.word.word}" means:`
                        : replaceWordAndVariationsWithBlanks(currentQuestion.word.definition, currentQuestion.word.word)}
                    </p>
                  </div>
                  <div className="flex flex-col items-center justify-center gap-3">
                    {currentQuestion.isWordToDefinition ? (
                      <>
                        <div className="text-sm text-red-600 dark:text-red-400 max-w-md text-center line-clamp-2">
                          Your answer: {selectedAnswer}
                        </div>
                        <div className="text-sm text-green-600 dark:text-green-400 max-w-md text-center">
                          <span className="font-semibold">Correct answer:</span> {currentQuestion.word.definition}
                        </div>
                        {currentQuestion.word.example_sentence && (
                          <div className="bg-gold-50 dark:bg-gold-900/20 rounded-lg p-2 text-center border border-gold-200 dark:border-gold-800 mt-1 max-w-md">
                            <h3 className="font-semibold text-xs mb-1 text-gold-700 dark:text-gold-400">Example:</h3>
                            <p className="text-xs text-neutral-700 dark:text-neutral-300 italic">
                              "{currentQuestion.word.example_sentence}"
                            </p>
                          </div>
                        )}
                      </>
                    ) : (
                      <div className="flex items-center gap-3">
                        <div className="text-xl text-red-600 dark:text-red-400">{selectedAnswer}</div>
                        <div className="text-lg text-neutral-500">→</div>
                        <div className="text-3xl font-mono text-green-600 dark:text-green-400 font-bold">{currentQuestion.word.word}</div>
                      </div>
                    )}
                    <button
                      onClick={() => speakWord(currentQuestion.word.word)}
                      className="p-1 hover:bg-green-100 dark:hover:bg-green-800/20 rounded-md transition-colors"
                      title="Hear pronunciation"
                    >
                      <SpeakerWaveIcon className="h-4 w-4 text-green-600 dark:text-green-400" />
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Learning Information */}
            <div className="space-y-1.5 mb-2">
              {(currentQuestion.word.memory_tips || currentQuestion.word.pronunciation_tips) && (
                <div className="bg-primary-50 dark:bg-primary-900/20 rounded-lg p-3">
                  <h3 className="font-semibold text-xs mb-1 flex items-center gap-1">
                    <AcademicCapIcon className="h-4 w-4 text-primary-600 dark:text-primary-400" />
                    Memory Tips
                  </h3>
                  <p className="text-xs text-neutral-700 dark:text-neutral-300">
                    {currentQuestion.word.memory_tips || currentQuestion.word.pronunciation_tips}
                  </p>
                </div>
              )}

              {currentQuestion.word.etymology && (
                <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-3">
                  <h3 className="font-semibold text-xs mb-1">
                    Word Origin & Etymology
                  </h3>
                  <p className="text-xs text-neutral-700 dark:text-neutral-300">
                    {currentQuestion.word.etymology}
                  </p>
                </div>
              )}
            </div>

            <button
              onClick={nextQuestion}
              className="w-full py-2 bg-primary-700 text-white rounded-lg hover:bg-primary-800 active:bg-primary-900 transition-colors text-sm font-semibold shadow-md"
            >
              Next Word →
            </button>
          </>
        )}
      </div>

      {/* Flag Content Modal */}
      {showFlagModal && currentQuestion && (
        <FlagContentModal
          isOpen={showFlagModal}
          onClose={() => setShowFlagModal(false)}
          contentType="question"
          contentId={currentQuestion.word.id}
          contentTitle={`Vocabulary: ${currentQuestion.word.word}`}
        />
      )}
    </div>
  )
}

export default VocabularyTrainerPage
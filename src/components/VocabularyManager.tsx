import React, { useState, useEffect, useCallback } from 'react'
import { supabase } from '../services/supabase'
import { 
  MagnifyingGlassIcon,
  PencilIcon,
  CheckIcon,
  XMarkIcon,
  ArrowPathIcon,
  LanguageIcon
} from '@heroicons/react/24/outline'

interface VocabularyWord {
  id: string
  language: string
  word: string
  english_translation: string
  definition_english: string
  part_of_speech: string
  difficulty_id: number
  zipf_frequency: number
  pronunciation_guide?: string
  translation_source?: string
}

const VocabularyManager: React.FC = () => {
  const [words, setWords] = useState<VocabularyWord[]>([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedLanguage, setSelectedLanguage] = useState('es')
  const [selectedPartOfSpeech, setSelectedPartOfSpeech] = useState('all')
  const [selectedDifficulty, setSelectedDifficulty] = useState('all')
  const [editingWord, setEditingWord] = useState<VocabularyWord | null>(null)
  const [editForm, setEditForm] = useState<Partial<VocabularyWord>>({})
  const [currentPage, setCurrentPage] = useState(1)
  const [totalCount, setTotalCount] = useState(0)
  const itemsPerPage = 50

  const fetchWords = useCallback(async () => {
    setLoading(true)
    try {
      // Build query
      let query = supabase
        .from('language_vocabulary')
        .select('*', { count: 'exact' })
        .eq('language', selectedLanguage)
        .order('zipf_frequency', { ascending: false })
        .range((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage - 1)

      // Apply filters
      if (selectedPartOfSpeech !== 'all') {
        query = query.eq('part_of_speech', selectedPartOfSpeech)
      }
      if (selectedDifficulty !== 'all') {
        query = query.eq('difficulty_id', parseInt(selectedDifficulty))
      }

      const { data, error, count } = await query

      if (error) throw error

      setWords(data || [])
      setTotalCount(count || 0)
    } catch (error) {
      console.error('Error fetching vocabulary:', error)
    } finally {
      setLoading(false)
    }
  }, [selectedLanguage, selectedPartOfSpeech, selectedDifficulty, currentPage])

  useEffect(() => {
    fetchWords()
  }, [fetchWords])

  const searchWords = async () => {
    if (!searchTerm.trim()) {
      fetchWords()
      return
    }

    setLoading(true)
    try {
      const { data, error } = await supabase
        .from('language_vocabulary')
        .select('*')
        .eq('language', selectedLanguage)
        .or(`word.ilike.%${searchTerm}%,english_translation.ilike.%${searchTerm}%`)
        .order('zipf_frequency', { ascending: false })
        .limit(50)

      if (error) throw error

      setWords(data || [])
      setTotalCount(data?.length || 0)
    } catch (error) {
      console.error('Error searching vocabulary:', error)
    } finally {
      setLoading(false)
    }
  }

  const updateWord = async () => {
    if (!editingWord || !editForm) return

    setLoading(true)
    try {
      const { error } = await supabase
        .from('language_vocabulary')
        .update({
          word: editForm.word,
          english_translation: editForm.english_translation,
          definition_english: editForm.definition_english,
          part_of_speech: editForm.part_of_speech,
          pronunciation_guide: editForm.pronunciation_guide
        })
        .eq('id', editingWord.id)

      if (error) throw error

      // Update local state
      setWords(words.map(w => 
        w.id === editingWord.id 
          ? { ...w, ...editForm }
          : w
      ))
      
      setEditingWord(null)
      setEditForm({})
    } catch (error) {
      console.error('Error updating word:', error)
      alert('Failed to update word')
    } finally {
      setLoading(false)
    }
  }

  const getDifficultyName = (id: number) => {
    const names: { [key: number]: string } = {
      1: 'Basic',
      2: 'Elementary',
      3: 'Intermediate',
      4: 'Advanced',
      5: 'Expert'
    }
    return names[id] || 'Unknown'
  }

  const getDifficultyColor = (id: number) => {
    const colors: { [key: number]: string } = {
      1: 'bg-green-100 text-green-800',
      2: 'bg-blue-100 text-blue-800',
      3: 'bg-yellow-100 text-yellow-800',
      4: 'bg-orange-100 text-orange-800',
      5: 'bg-red-100 text-red-800'
    }
    return colors[id] || 'bg-gray-100 text-gray-800'
  }

  const filteredWords = words.filter(word => {
    if (!searchTerm) return true
    const search = searchTerm.toLowerCase()
    return (
      word.word.toLowerCase().includes(search) ||
      word.english_translation?.toLowerCase().includes(search) ||
      word.definition_english?.toLowerCase().includes(search)
    )
  })

  const totalPages = Math.ceil(totalCount / itemsPerPage)

  return (
    <div className="space-y-6">
      <div className="card p-6">
        <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
          <LanguageIcon className="h-6 w-6" />
          Vocabulary Manager
        </h2>

        {/* Filters */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium mb-1">Language</label>
            <select
              value={selectedLanguage}
              onChange={(e) => {
                setSelectedLanguage(e.target.value)
                setCurrentPage(1)
              }}
              className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800"
            >
              <option value="es">Spanish</option>
              <option value="en">English</option>
              <option value="fr">French</option>
              <option value="de">German</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Part of Speech</label>
            <select
              value={selectedPartOfSpeech}
              onChange={(e) => {
                setSelectedPartOfSpeech(e.target.value)
                setCurrentPage(1)
              }}
              className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800"
            >
              <option value="all">All</option>
              <option value="noun">Noun</option>
              <option value="verb">Verb</option>
              <option value="adjective">Adjective</option>
              <option value="adverb">Adverb</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Difficulty</label>
            <select
              value={selectedDifficulty}
              onChange={(e) => {
                setSelectedDifficulty(e.target.value)
                setCurrentPage(1)
              }}
              className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800"
            >
              <option value="all">All</option>
              <option value="1">Basic</option>
              <option value="2">Elementary</option>
              <option value="3">Intermediate</option>
              <option value="4">Advanced</option>
              <option value="5">Expert</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Search</label>
            <div className="flex gap-2">
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && searchWords()}
                placeholder="Search words..."
                className="flex-1 px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800"
              />
              <button
                onClick={searchWords}
                className="px-3 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
              >
                <MagnifyingGlassIcon className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>

        {/* Results count */}
        <div className="flex justify-between items-center mb-4">
          <span className="text-sm text-neutral-600 dark:text-neutral-400">
            Showing {filteredWords.length} of {totalCount} words
          </span>
          {loading && (
            <ArrowPathIcon className="h-5 w-5 animate-spin text-primary-600" />
          )}
        </div>

        {/* Words table */}
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-neutral-50 dark:bg-neutral-800">
              <tr>
                <th className="px-4 py-2 text-left text-xs font-medium text-neutral-500 uppercase">Word</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-neutral-500 uppercase">Translation</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-neutral-500 uppercase">Definition</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-neutral-500 uppercase">Part of Speech</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-neutral-500 uppercase">Difficulty</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-neutral-500 uppercase">Zipf</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-neutral-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-200 dark:divide-neutral-700">
              {filteredWords.map((word) => (
                <tr key={word.id} className="hover:bg-neutral-50 dark:hover:bg-neutral-800">
                  <td className="px-4 py-2">
                    {editingWord?.id === word.id ? (
                      <input
                        type="text"
                        value={editForm.word || ''}
                        onChange={(e) => setEditForm({ ...editForm, word: e.target.value })}
                        className="w-full px-2 py-1 border border-neutral-300 dark:border-neutral-600 rounded"
                      />
                    ) : (
                      <span className="font-medium">{word.word}</span>
                    )}
                  </td>
                  <td className="px-4 py-2">
                    {editingWord?.id === word.id ? (
                      <input
                        type="text"
                        value={editForm.english_translation || ''}
                        onChange={(e) => setEditForm({ ...editForm, english_translation: e.target.value })}
                        className="w-full px-2 py-1 border border-neutral-300 dark:border-neutral-600 rounded"
                      />
                    ) : (
                      word.english_translation
                    )}
                  </td>
                  <td className="px-4 py-2 max-w-xs">
                    {editingWord?.id === word.id ? (
                      <input
                        type="text"
                        value={editForm.definition_english || ''}
                        onChange={(e) => setEditForm({ ...editForm, definition_english: e.target.value })}
                        className="w-full px-2 py-1 border border-neutral-300 dark:border-neutral-600 rounded"
                      />
                    ) : (
                      <span className="truncate block" title={word.definition_english}>
                        {word.definition_english}
                      </span>
                    )}
                  </td>
                  <td className="px-4 py-2">
                    {editingWord?.id === word.id ? (
                      <select
                        value={editForm.part_of_speech || ''}
                        onChange={(e) => setEditForm({ ...editForm, part_of_speech: e.target.value })}
                        className="px-2 py-1 border border-neutral-300 dark:border-neutral-600 rounded"
                      >
                        <option value="noun">Noun</option>
                        <option value="verb">Verb</option>
                        <option value="adjective">Adjective</option>
                        <option value="adverb">Adverb</option>
                        <option value="other">Other</option>
                      </select>
                    ) : (
                      <span className="text-sm">{word.part_of_speech}</span>
                    )}
                  </td>
                  <td className="px-4 py-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(word.difficulty_id)}`}>
                      {getDifficultyName(word.difficulty_id)}
                    </span>
                  </td>
                  <td className="px-4 py-2">
                    <span className="text-sm text-neutral-600">{word.zipf_frequency.toFixed(1)}</span>
                  </td>
                  <td className="px-4 py-2">
                    {editingWord?.id === word.id ? (
                      <div className="flex gap-1">
                        <button
                          onClick={updateWord}
                          className="p-1 text-green-600 hover:bg-green-100 rounded"
                          disabled={loading}
                        >
                          <CheckIcon className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => {
                            setEditingWord(null)
                            setEditForm({})
                          }}
                          className="p-1 text-red-600 hover:bg-red-100 rounded"
                        >
                          <XMarkIcon className="h-4 w-4" />
                        </button>
                      </div>
                    ) : (
                      <button
                        onClick={() => {
                          setEditingWord(word)
                          setEditForm(word)
                        }}
                        className="p-1 text-primary-600 hover:bg-primary-100 rounded"
                      >
                        <PencilIcon className="h-4 w-4" />
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex justify-center items-center gap-2 mt-6">
            <button
              onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
              disabled={currentPage === 1}
              className="px-3 py-1 border border-neutral-300 dark:border-neutral-600 rounded-lg disabled:opacity-50"
            >
              Previous
            </button>
            <span className="text-sm">
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
              disabled={currentPage === totalPages}
              className="px-3 py-1 border border-neutral-300 dark:border-neutral-600 rounded-lg disabled:opacity-50"
            >
              Next
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default VocabularyManager
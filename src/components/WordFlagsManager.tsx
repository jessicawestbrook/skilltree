import React, { useState, useEffect } from 'react'
import { supabase } from '../services/supabase'
import { CheckIcon, XMarkIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline'

interface SpellingWord {
  id: string
  word: string
  definition?: string
  is_spelling_word?: boolean
  is_vocabulary_word?: boolean
  spelling_difficulty_id?: number
  vocabulary_difficulty_id?: number
}

const WordFlagsManager: React.FC = () => {
  const [words, setWords] = useState<SpellingWord[]>([])
  const [filteredWords, setFilteredWords] = useState<SpellingWord[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState<string | null>(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [filterType, setFilterType] = useState<'all' | 'spelling' | 'vocabulary' | 'both' | 'neither'>('all')
  const wordsPerPage = 50

  useEffect(() => {
    fetchWords()
  }, [])

  useEffect(() => {
    filterWords()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [words, searchTerm, filterType])

  const fetchWords = async () => {
    setLoading(true)
    try {
      const { data, error } = await supabase
        .from('spelling_words')
        .select('id, word, definition, is_spelling_word, is_vocabulary_word, spelling_difficulty_id, vocabulary_difficulty_id')
        .order('word')

      if (error) throw error
      setWords(data || [])
    } catch (error) {
      console.error('Error fetching words:', error)
    } finally {
      setLoading(false)
    }
  }

  const filterWords = () => {
    let filtered = [...words]

    // Apply search filter
    if (searchTerm) {
      filtered = filtered.filter(w => 
        w.word.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (w.definition && w.definition.toLowerCase().includes(searchTerm.toLowerCase()))
      )
    }

    // Apply type filter
    switch (filterType) {
      case 'spelling':
        filtered = filtered.filter(w => w.is_spelling_word && !w.is_vocabulary_word)
        break
      case 'vocabulary':
        filtered = filtered.filter(w => !w.is_spelling_word && w.is_vocabulary_word)
        break
      case 'both':
        filtered = filtered.filter(w => w.is_spelling_word && w.is_vocabulary_word)
        break
      case 'neither':
        filtered = filtered.filter(w => !w.is_spelling_word && !w.is_vocabulary_word)
        break
    }

    setFilteredWords(filtered)
    setCurrentPage(1)
  }

  const toggleFlag = async (wordId: string, flagType: 'is_spelling_word' | 'is_vocabulary_word') => {
    setSaving(wordId)
    
    const word = words.find(w => w.id === wordId)
    if (!word) return

    const newValue = !word[flagType]

    try {
      const { error } = await supabase
        .from('spelling_words')
        .update({ [flagType]: newValue })
        .eq('id', wordId)

      if (error) throw error

      // Update local state
      setWords(prevWords => 
        prevWords.map(w => 
          w.id === wordId ? { ...w, [flagType]: newValue } : w
        )
      )
    } catch (error) {
      console.error('Error updating word flag:', error)
      alert('Failed to update word flag')
    } finally {
      setSaving(null)
    }
  }

  const bulkUpdate = async (action: 'allSpelling' | 'allVocab' | 'clearSpelling' | 'clearVocab') => {
    if (!window.confirm(`Are you sure you want to update ALL ${filteredWords.length} filtered words?`)) {
      return
    }

    setLoading(true)
    const wordIds = filteredWords.map(w => w.id)
    
    let updateData: any = {}
    switch (action) {
      case 'allSpelling':
        updateData = { is_spelling_word: true }
        break
      case 'allVocab':
        updateData = { is_vocabulary_word: true }
        break
      case 'clearSpelling':
        updateData = { is_spelling_word: false }
        break
      case 'clearVocab':
        updateData = { is_vocabulary_word: false }
        break
    }

    try {
      const { error } = await supabase
        .from('spelling_words')
        .update(updateData)
        .in('id', wordIds)

      if (error) throw error
      
      await fetchWords()
      alert(`Updated ${wordIds.length} words successfully`)
    } catch (error) {
      console.error('Error bulk updating:', error)
      alert('Failed to bulk update words')
    } finally {
      setLoading(false)
    }
  }

  // Pagination
  const totalPages = Math.ceil(filteredWords.length / wordsPerPage)
  const paginatedWords = filteredWords.slice(
    (currentPage - 1) * wordsPerPage,
    currentPage * wordsPerPage
  )

  return (
    <div className="bg-white dark:bg-neutral-800 rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4 text-neutral-900 dark:text-white">
        Word Flags Manager
      </h2>
      
      {/* Search and Filters */}
      <div className="mb-6 space-y-4">
        <div className="flex gap-4">
          <div className="flex-1 relative">
            <MagnifyingGlassIcon className="absolute left-3 top-3 h-5 w-5 text-neutral-400" />
            <input
              type="text"
              placeholder="Search words..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg 
                       bg-white dark:bg-neutral-700 text-neutral-900 dark:text-white"
            />
          </div>
          
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value as any)}
            className="px-4 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg 
                     bg-white dark:bg-neutral-700 text-neutral-900 dark:text-white"
          >
            <option value="all">All Words</option>
            <option value="spelling">Spelling Only</option>
            <option value="vocabulary">Vocabulary Only</option>
            <option value="both">Both Types</option>
            <option value="neither">Neither Type</option>
          </select>
        </div>

        {/* Bulk Actions */}
        <div className="flex gap-2 flex-wrap">
          <button
            onClick={() => bulkUpdate('allSpelling')}
            disabled={loading}
            className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700 disabled:opacity-50"
          >
            Mark All as Spelling
          </button>
          <button
            onClick={() => bulkUpdate('allVocab')}
            disabled={loading}
            className="px-3 py-1 bg-purple-600 text-white rounded text-sm hover:bg-purple-700 disabled:opacity-50"
          >
            Mark All as Vocabulary
          </button>
          <button
            onClick={() => bulkUpdate('clearSpelling')}
            disabled={loading}
            className="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700 disabled:opacity-50"
          >
            Clear Spelling Flag
          </button>
          <button
            onClick={() => bulkUpdate('clearVocab')}
            disabled={loading}
            className="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700 disabled:opacity-50"
          >
            Clear Vocabulary Flag
          </button>
        </div>

        <div className="text-sm text-neutral-600 dark:text-neutral-400">
          Showing {paginatedWords.length} of {filteredWords.length} filtered words 
          ({words.length} total)
        </div>
      </div>

      {/* Words Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-neutral-200 dark:border-neutral-700">
              <th className="text-left py-2 px-2 text-neutral-700 dark:text-neutral-300">Word</th>
              <th className="text-left py-2 px-2 text-neutral-700 dark:text-neutral-300">Definition</th>
              <th className="text-center py-2 px-2 text-neutral-700 dark:text-neutral-300">Spelling</th>
              <th className="text-center py-2 px-2 text-neutral-700 dark:text-neutral-300">Vocabulary</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={4} className="text-center py-8 text-neutral-500">
                  Loading words...
                </td>
              </tr>
            ) : paginatedWords.length === 0 ? (
              <tr>
                <td colSpan={4} className="text-center py-8 text-neutral-500">
                  No words found
                </td>
              </tr>
            ) : (
              paginatedWords.map(word => (
                <tr key={word.id} className="border-b border-neutral-100 dark:border-neutral-700">
                  <td className="py-2 px-2 font-medium text-neutral-900 dark:text-white">
                    {word.word}
                  </td>
                  <td className="py-2 px-2 text-sm text-neutral-600 dark:text-neutral-400">
                    {word.definition ? (word.definition.length > 100 
                      ? word.definition.substring(0, 100) + '...' 
                      : word.definition) 
                      : '-'}
                  </td>
                  <td className="py-2 px-2 text-center">
                    <button
                      onClick={() => toggleFlag(word.id, 'is_spelling_word')}
                      disabled={saving === word.id}
                      className={`p-1 rounded ${
                        word.is_spelling_word 
                          ? 'bg-blue-100 text-blue-600 hover:bg-blue-200 dark:bg-blue-900/30 dark:text-blue-400' 
                          : 'bg-neutral-100 text-neutral-400 hover:bg-neutral-200 dark:bg-neutral-700 dark:text-neutral-500'
                      } disabled:opacity-50`}
                    >
                      {word.is_spelling_word ? (
                        <CheckIcon className="h-5 w-5" />
                      ) : (
                        <XMarkIcon className="h-5 w-5" />
                      )}
                    </button>
                  </td>
                  <td className="py-2 px-2 text-center">
                    <button
                      onClick={() => toggleFlag(word.id, 'is_vocabulary_word')}
                      disabled={saving === word.id}
                      className={`p-1 rounded ${
                        word.is_vocabulary_word 
                          ? 'bg-purple-100 text-purple-600 hover:bg-purple-200 dark:bg-purple-900/30 dark:text-purple-400' 
                          : 'bg-neutral-100 text-neutral-400 hover:bg-neutral-200 dark:bg-neutral-700 dark:text-neutral-500'
                      } disabled:opacity-50`}
                    >
                      {word.is_vocabulary_word ? (
                        <CheckIcon className="h-5 w-5" />
                      ) : (
                        <XMarkIcon className="h-5 w-5" />
                      )}
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="mt-4 flex justify-center gap-2">
          <button
            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
            disabled={currentPage === 1}
            className="px-3 py-1 border border-neutral-300 dark:border-neutral-600 rounded 
                     disabled:opacity-50 hover:bg-neutral-100 dark:hover:bg-neutral-700"
          >
            Previous
          </button>
          <span className="px-3 py-1 text-neutral-700 dark:text-neutral-300">
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
            disabled={currentPage === totalPages}
            className="px-3 py-1 border border-neutral-300 dark:border-neutral-600 rounded 
                     disabled:opacity-50 hover:bg-neutral-100 dark:hover:bg-neutral-700"
          >
            Next
          </button>
        </div>
      )}
    </div>
  )
}

export default WordFlagsManager
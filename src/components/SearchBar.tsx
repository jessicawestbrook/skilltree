import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  MagnifyingGlassIcon, 
  XMarkIcon,
  SparklesIcon,
  ClockIcon,
  AcademicCapIcon,
  BookOpenIcon,
  BeakerIcon,
  CalculatorIcon
} from '@heroicons/react/24/outline'
import { searchService, SearchResult } from '../services/searchService'

// Simple debounce implementation
function debounce<T extends (...args: any[]) => void>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null
  return (...args: Parameters<T>) => {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

interface SearchBarProps {
  onResultSelect?: (result: SearchResult) => void
  placeholder?: string
  autoFocus?: boolean
  className?: string
}

const SearchBar: React.FC<SearchBarProps> = ({
  onResultSelect,
  placeholder = "Search topics, concepts, or keywords...",
  autoFocus = false,
  className = ""
}) => {
  const navigate = useNavigate()
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isFocused, setIsFocused] = useState(false)
  const [selectedIndex, setSelectedIndex] = useState(-1)
  const [recentSearches, setRecentSearches] = useState<string[]>([])
  const searchRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  // Load recent searches from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('recentSearches')
    if (saved) {
      setRecentSearches(JSON.parse(saved))
    }
  }, [])

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setIsFocused(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // Search function with debouncing
  const performSearch = useCallback(async (searchQuery: string) => {
    if (searchQuery.length < 2) {
      setResults([])
      setSuggestions([])
      return
    }

    setIsLoading(true)
    try {
      const [searchResults, searchSuggestions] = await Promise.all([
        searchService.search(searchQuery, {
          limit: 8,
          threshold: 0.2,
          searchIn: ['title', 'learning_area']
        }),
        searchService.getSuggestions(searchQuery, 5)
      ])
      
      setResults(searchResults)
      setSuggestions(searchSuggestions)
    } catch (error) {
      console.error('Search error:', error)
    } finally {
      setIsLoading(false)
    }
  }, [])

  const debouncedSearch = useMemo(
    () => debounce((searchQuery: string) => {
      performSearch(searchQuery)
    }, 300),
    [performSearch]
  )

  // Handle input change
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setQuery(value)
    setSelectedIndex(-1)
    
    if (value.trim()) {
      debouncedSearch(value)
    } else {
      setResults([])
      setSuggestions([])
    }
  }

  // Handle search submit
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (query.trim()) {
      // Save to recent searches
      const updated = [query, ...recentSearches.filter(s => s !== query)].slice(0, 5)
      setRecentSearches(updated)
      localStorage.setItem('recentSearches', JSON.stringify(updated))
      
      // If there's a selected result, navigate to it
      if (selectedIndex >= 0 && results[selectedIndex]) {
        handleResultClick(results[selectedIndex])
      } else if (results.length > 0) {
        handleResultClick(results[0])
      }
    }
  }

  // Handle result selection
  const handleResultClick = (result: SearchResult) => {
    if (onResultSelect) {
      onResultSelect(result)
    } else {
      // Navigate to the content if it has simple_content_id
      if (result.node.simple_content_id) {
        navigate(`/learning/${result.node.simple_content_id}`)
      }
    }
    
    setQuery('')
    setResults([])
    setSuggestions([])
    setIsFocused(false)
  }

  // Handle keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault()
      setSelectedIndex(prev => 
        prev < results.length - 1 ? prev + 1 : prev
      )
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      setSelectedIndex(prev => prev > -1 ? prev - 1 : -1)
    } else if (e.key === 'Enter' && selectedIndex >= 0) {
      e.preventDefault()
      handleResultClick(results[selectedIndex])
    } else if (e.key === 'Escape') {
      setIsFocused(false)
      inputRef.current?.blur()
    }
  }

  // Get icon for node type
  const getNodeIcon = (nodeType: string) => {
    switch (nodeType) {
      case 'math': return <CalculatorIcon className="h-4 w-4" />
      case 'science': return <BeakerIcon className="h-4 w-4" />
      case 'humanities': return <BookOpenIcon className="h-4 w-4" />
      default: return <AcademicCapIcon className="h-4 w-4" />
    }
  }

  // Get match type badge
  const getMatchBadge = (matchType: string) => {
    switch (matchType) {
      case 'exact':
        return <span className="text-xs px-1.5 py-0.5 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded">Exact</span>
      case 'semantic':
        return <span className="text-xs px-1.5 py-0.5 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 rounded">Related</span>
      default:
        return null
    }
  }

  const showDropdown = isFocused && (query.length > 0 || recentSearches.length > 0)

  return (
    <div ref={searchRef} className={`relative ${className}`}>
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-neutral-400" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={handleInputChange}
            onFocus={() => setIsFocused(true)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            autoFocus={autoFocus}
            className="w-full pl-10 pr-10 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
          {query && (
            <button
              type="button"
              onClick={() => {
                setQuery('')
                setResults([])
                setSuggestions([])
                inputRef.current?.focus()
              }}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 p-1 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded"
            >
              <XMarkIcon className="h-4 w-4 text-neutral-400" />
            </button>
          )}
          {isLoading && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
            </div>
          )}
        </div>
      </form>

      {showDropdown && (
        <div className="absolute z-50 w-full mt-2 bg-white dark:bg-neutral-800 rounded-lg shadow-xl border border-neutral-200 dark:border-neutral-700 max-h-96 overflow-y-auto">
          {/* Search results */}
          {results.length > 0 && (
            <div className="p-2">
              <div className="text-xs font-semibold text-neutral-500 px-2 py-1">Results</div>
              {results.map((result, index) => (
                <button
                  key={result.node.id}
                  onClick={() => handleResultClick(result)}
                  onMouseEnter={() => setSelectedIndex(index)}
                  className={`w-full text-left px-3 py-2 rounded-lg transition-colors ${
                    selectedIndex === index
                      ? 'bg-primary-50 dark:bg-primary-900/20'
                      : 'hover:bg-neutral-50 dark:hover:bg-neutral-700/50'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <div className="text-neutral-400 mt-0.5">
                      {getNodeIcon(result.node.node_type)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <div 
                          className="font-medium text-sm truncate"
                          dangerouslySetInnerHTML={{ 
                            __html: result.highlights.title || result.node.title 
                          }}
                        />
                        {getMatchBadge(result.matchType)}
                      </div>
                      {result.highlights.learning_area && (
                        <div 
                          className="text-xs text-neutral-500 mt-0.5 line-clamp-2"
                          dangerouslySetInnerHTML={{ __html: result.highlights.learning_area }}
                        />
                      )}
                      <div className="flex items-center gap-3 mt-1">
                        <span className="text-xs text-neutral-400">
                          Score: {Math.round(result.score * 100)}%
                        </span>
                        {result.node.difficulty_level && (
                          <span className="text-xs text-neutral-400">
                            Level {result.node.difficulty_level}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          )}

          {/* Suggestions */}
          {suggestions.length > 0 && query.length > 0 && (
            <div className="border-t border-neutral-200 dark:border-neutral-700 p-2">
              <div className="text-xs font-semibold text-neutral-500 px-2 py-1 flex items-center gap-1">
                <SparklesIcon className="h-3 w-3" />
                Suggestions
              </div>
              {suggestions.map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => {
                    setQuery(suggestion)
                    debouncedSearch(suggestion)
                  }}
                  className="w-full text-left px-3 py-1.5 text-sm text-neutral-600 dark:text-neutral-400 hover:bg-neutral-50 dark:hover:bg-neutral-700/50 rounded"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          )}

          {/* Recent searches */}
          {recentSearches.length > 0 && query.length === 0 && (
            <div className="p-2">
              <div className="text-xs font-semibold text-neutral-500 px-2 py-1 flex items-center gap-1">
                <ClockIcon className="h-3 w-3" />
                Recent
              </div>
              {recentSearches.map((search, index) => (
                <button
                  key={index}
                  onClick={() => {
                    setQuery(search)
                    debouncedSearch(search)
                  }}
                  className="w-full text-left px-3 py-1.5 text-sm text-neutral-600 dark:text-neutral-400 hover:bg-neutral-50 dark:hover:bg-neutral-700/50 rounded flex items-center justify-between group"
                >
                  <span>{search}</span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      const updated = recentSearches.filter(s => s !== search)
                      setRecentSearches(updated)
                      localStorage.setItem('recentSearches', JSON.stringify(updated))
                    }}
                    className="opacity-0 group-hover:opacity-100 p-0.5 hover:bg-neutral-200 dark:hover:bg-neutral-600 rounded"
                  >
                    <XMarkIcon className="h-3 w-3" />
                  </button>
                </button>
              ))}
            </div>
          )}

          {/* No results */}
          {query.length >= 2 && results.length === 0 && !isLoading && (
            <div className="p-4 text-center text-sm text-neutral-500">
              No results found for "{query}"
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default SearchBar
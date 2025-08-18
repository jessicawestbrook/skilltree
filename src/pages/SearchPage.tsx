import React, { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { 
  MagnifyingGlassIcon,
  FunnelIcon,
  AcademicCapIcon,
  BookOpenIcon,
  BeakerIcon,
  CalculatorIcon,
  ChartBarIcon,
  XMarkIcon
} from '@heroicons/react/24/outline'
import { searchService, SearchResult, KnowledgeNode } from '../services/searchService'
import SearchBar from '../components/SearchBar'

const SearchPage: React.FC = () => {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const [results, setResults] = useState<SearchResult[]>([])
  const [advancedResults, setAdvancedResults] = useState<KnowledgeNode[]>([])
  const [, setAllResults] = useState<any>({ nodes: [], questions: [], learningContent: [] })
  const [isLoading, setIsLoading] = useState(false)
  const [showFilters, setShowFilters] = useState(false)
  // const [activeTab, setActiveTab] = useState<'nodes' | 'questions' | 'content' | 'all'>('all')
  
  // Search state
  const [query] = useState(searchParams.get('q') || '')
  const [searchMode, setSearchMode] = useState<'smart' | 'advanced' | 'all'>('all')
  
  // Filter state
  const [filters, setFilters] = useState({
    nodeTypes: [] as string[],
    difficultyRange: [1, 10] as [number, number],
    hasContent: null as boolean | null,
    searchIn: ['title', 'learning_area'] as string[]
  })

  // Statistics
  const [stats, setStats] = useState({
    totalResults: 0,
    byType: {} as Record<string, number>,
    avgDifficulty: 0
  })

  // Perform search when query or filters change
  useEffect(() => {
    if (query.trim()) {
      performSearch()
    } else {
      setResults([])
      setAdvancedResults([])
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [query, searchMode, filters])

  const performSearch = async () => {
    setIsLoading(true)
    
    try {
      if (searchMode === 'all') {
        // Search across all content types
        const allSearchResults = await searchService.searchAll(query, {
          includeNodes: true,
          includeQuestions: true,
          includeContent: true,
          limit: 20
        })
        
        setAllResults(allSearchResults)
        
        // Calculate combined stats
        const totalItems = 
          allSearchResults.nodes.length + 
          allSearchResults.questions.length + 
          allSearchResults.learningContent.length
        
        setStats({
          totalResults: totalItems,
          byType: {
            nodes: allSearchResults.nodes.length,
            questions: allSearchResults.questions.length,
            content: allSearchResults.learningContent.length
          },
          avgDifficulty: 0
        })
      } else if (searchMode === 'smart') {
        // Smart search with fuzzy/semantic matching
        const searchResults = await searchService.search(query, {
          limit: 50,
          threshold: 0.15,
          searchIn: filters.searchIn as ('title' | 'learning_area')[],
          nodeTypes: filters.nodeTypes.length > 0 ? filters.nodeTypes : undefined
        })
        
        // Apply difficulty filter
        const filtered = searchResults.filter(r => {
          const level = r.node.difficulty_level || 5
          return level >= filters.difficultyRange[0] && level <= filters.difficultyRange[1]
        })
        
        // Apply content filter
        const finalResults = filters.hasContent !== null
          ? filtered.filter(r => 
              filters.hasContent ? r.node.simple_content_id !== null : r.node.simple_content_id === null
            )
          : filtered
        
        setResults(finalResults)
        calculateStats(finalResults.map(r => r.node))
      } else {
        // Advanced search with exact criteria
        const nodes = await searchService.advancedSearch({
          query: query || undefined,
          nodeTypes: filters.nodeTypes.length > 0 ? filters.nodeTypes : undefined,
          minDifficulty: filters.difficultyRange[0],
          maxDifficulty: filters.difficultyRange[1],
          hasContent: filters.hasContent !== null ? filters.hasContent : undefined
        })
        
        setAdvancedResults(nodes)
        calculateStats(nodes)
      }
    } catch (error) {
      console.error('Search error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const calculateStats = (nodes: KnowledgeNode[]) => {
    const byType: Record<string, number> = {}
    let totalDifficulty = 0
    
    nodes.forEach(node => {
      byType[node.node_type] = (byType[node.node_type] || 0) + 1
      totalDifficulty += node.difficulty_level || 5
    })
    
    setStats({
      totalResults: nodes.length,
      byType,
      avgDifficulty: nodes.length > 0 ? totalDifficulty / nodes.length : 0
    })
  }

  // const handleSearch = (newQuery: string) => {
  //   setQuery(newQuery)
  //   setSearchParams({ q: newQuery })
  // }

  const toggleNodeType = (type: string) => {
    setFilters(prev => ({
      ...prev,
      nodeTypes: prev.nodeTypes.includes(type)
        ? prev.nodeTypes.filter(t => t !== type)
        : [...prev.nodeTypes, type]
    }))
  }

  const getNodeIcon = (nodeType: string) => {
    switch (nodeType) {
      case 'math': return <CalculatorIcon className="h-5 w-5" />
      case 'science': return <BeakerIcon className="h-5 w-5" />
      case 'humanities': return <BookOpenIcon className="h-5 w-5" />
      default: return <AcademicCapIcon className="h-5 w-5" />
    }
  }

  const nodeTypeColors = {
    math: 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400',
    science: 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400',
    humanities: 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400',
    default: 'bg-neutral-100 dark:bg-neutral-900/30 text-neutral-700 dark:text-neutral-400'
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Knowledge Search</h1>
        <p className="text-neutral-600 dark:text-neutral-400">
          Find topics, concepts, and learning materials across all subjects
        </p>
      </div>

      {/* Search Bar */}
      <div className="mb-6">
        <div className="flex gap-3">
          <div className="flex-1">
            <SearchBar
              placeholder="Search for any topic, concept, or keyword..."
              onResultSelect={(result) => {
                if (result.node.simple_content_id) {
                  navigate(`/learning/${result.node.simple_content_id}`)
                }
              }}
            />
          </div>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`btn-secondary px-4 py-2 flex items-center gap-2 ${
              showFilters ? 'bg-primary-100 dark:bg-primary-900/30' : ''
            }`}
          >
            <FunnelIcon className="h-5 w-5" />
            Filters
            {(filters.nodeTypes.length > 0 || filters.hasContent !== null) && (
              <span className="ml-1 px-1.5 py-0.5 bg-primary-600 text-white text-xs rounded-full">
                {filters.nodeTypes.length + (filters.hasContent !== null ? 1 : 0)}
              </span>
            )}
          </button>
        </div>

        {/* Search Mode Toggle */}
        <div className="mt-4 flex items-center gap-4">
          <span className="text-sm text-neutral-600 dark:text-neutral-400">Search Mode:</span>
          <div className="flex bg-neutral-100 dark:bg-neutral-800 rounded-lg p-1">
            <button
              onClick={() => setSearchMode('smart')}
              className={`px-3 py-1 text-sm rounded ${
                searchMode === 'smart'
                  ? 'bg-white dark:bg-neutral-700 shadow font-medium'
                  : 'text-neutral-600 dark:text-neutral-400'
              }`}
            >
              Smart Search
            </button>
            <button
              onClick={() => setSearchMode('advanced')}
              className={`px-3 py-1 text-sm rounded ${
                searchMode === 'advanced'
                  ? 'bg-white dark:bg-neutral-700 shadow font-medium'
                  : 'text-neutral-600 dark:text-neutral-400'
              }`}
            >
              Advanced
            </button>
          </div>
          {searchMode === 'smart' && (
            <span className="text-xs text-neutral-500">
              Uses fuzzy matching and finds related content
            </span>
          )}
        </div>
      </div>

      {/* Filters Panel */}
      {showFilters && (
        <div className="mb-6 card p-4 bg-neutral-50 dark:bg-neutral-900">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Node Types */}
            <div>
              <h3 className="font-semibold mb-3">Subject Areas</h3>
              <div className="space-y-2">
                {['math', 'science', 'humanities'].map(type => (
                  <label key={type} className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={filters.nodeTypes.includes(type)}
                      onChange={() => toggleNodeType(type)}
                      className="rounded text-primary-600 focus:ring-primary-500"
                    />
                    <span className="flex items-center gap-2">
                      {getNodeIcon(type)}
                      <span className="capitalize">{type}</span>
                    </span>
                  </label>
                ))}
              </div>
            </div>

            {/* Difficulty Range */}
            <div>
              <h3 className="font-semibold mb-3">Difficulty Level</h3>
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <input
                    type="number"
                    min="1"
                    max="10"
                    value={filters.difficultyRange[0]}
                    onChange={(e) => setFilters(prev => ({
                      ...prev,
                      difficultyRange: [parseInt(e.target.value) || 1, prev.difficultyRange[1]]
                    }))}
                    className="w-16 px-2 py-1 border border-neutral-300 dark:border-neutral-600 rounded"
                  />
                  <span className="text-neutral-500">to</span>
                  <input
                    type="number"
                    min="1"
                    max="10"
                    value={filters.difficultyRange[1]}
                    onChange={(e) => setFilters(prev => ({
                      ...prev,
                      difficultyRange: [prev.difficultyRange[0], parseInt(e.target.value) || 10]
                    }))}
                    className="w-16 px-2 py-1 border border-neutral-300 dark:border-neutral-600 rounded"
                  />
                </div>
                <div className="text-xs text-neutral-500">
                  Range: {filters.difficultyRange[0]} - {filters.difficultyRange[1]}
                </div>
              </div>
            </div>

            {/* Content Availability */}
            <div>
              <h3 className="font-semibold mb-3">Content Availability</h3>
              <div className="space-y-2">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="hasContent"
                    checked={filters.hasContent === null}
                    onChange={() => setFilters(prev => ({ ...prev, hasContent: null }))}
                    className="text-primary-600 focus:ring-primary-500"
                  />
                  <span>All</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="hasContent"
                    checked={filters.hasContent === true}
                    onChange={() => setFilters(prev => ({ ...prev, hasContent: true }))}
                    className="text-primary-600 focus:ring-primary-500"
                  />
                  <span>With Content</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="hasContent"
                    checked={filters.hasContent === false}
                    onChange={() => setFilters(prev => ({ ...prev, hasContent: false }))}
                    className="text-primary-600 focus:ring-primary-500"
                  />
                  <span>Structure Only</span>
                </label>
              </div>
            </div>
          </div>

          {/* Clear Filters */}
          <div className="mt-4 flex justify-end">
            <button
              onClick={() => setFilters({
                nodeTypes: [],
                difficultyRange: [1, 10],
                hasContent: null,
                searchIn: ['title', 'description']
              })}
              className="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1"
            >
              <XMarkIcon className="h-4 w-4" />
              Clear Filters
            </button>
          </div>
        </div>
      )}

      {/* Results Stats */}
      {stats.totalResults > 0 && (
        <div className="mb-6 flex items-center gap-6 text-sm text-neutral-600 dark:text-neutral-400">
          <div className="flex items-center gap-2">
            <ChartBarIcon className="h-4 w-4" />
            <span>{stats.totalResults} results</span>
          </div>
          {Object.entries(stats.byType).map(([type, count]) => (
            <div key={type} className="flex items-center gap-2">
              {getNodeIcon(type)}
              <span>{count}</span>
            </div>
          ))}
          <div>
            Avg. Difficulty: {stats.avgDifficulty.toFixed(1)}
          </div>
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      )}

      {/* Search Results */}
      {!isLoading && (
        <div className="space-y-4">
          {searchMode === 'smart' ? (
            // Smart search results with scores
            results.map((result) => (
              <div
                key={result.node.id}
                onClick={() => {
                  if (result.node.simple_content_id) {
                    navigate(`/learning/${result.node.simple_content_id}`)
                  }
                }}
                className={`card p-4 ${
                  result.node.simple_content_id 
                    ? 'cursor-pointer hover:shadow-lg transition-shadow' 
                    : ''
                }`}
              >
                <div className="flex items-start gap-4">
                  <div className={`p-2 rounded-lg ${
                    nodeTypeColors[result.node.node_type as keyof typeof nodeTypeColors] || nodeTypeColors.default
                  }`}>
                    {getNodeIcon(result.node.node_type)}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 
                          className="font-semibold text-lg"
                          dangerouslySetInnerHTML={{ 
                            __html: result.highlights.title || result.node.title 
                          }}
                        />
                        {result.highlights.learning_area && (
                          <p 
                            className="text-neutral-600 dark:text-neutral-400 mt-1"
                            dangerouslySetInnerHTML={{ __html: result.highlights.learning_area }}
                          />
                        )}
                      </div>
                      <div className="flex flex-col items-end gap-1">
                        <span className={`text-xs px-2 py-1 rounded ${
                          result.matchType === 'exact' 
                            ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400'
                            : result.matchType === 'semantic'
                            ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400'
                            : 'bg-neutral-100 dark:bg-neutral-900/30 text-neutral-700 dark:text-neutral-400'
                        }`}>
                          {result.matchType === 'exact' ? 'Exact Match' : 
                           result.matchType === 'semantic' ? 'Related' : 'Similar'}
                        </span>
                        <span className="text-xs text-neutral-500">
                          {Math.round(result.score * 100)}% match
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center gap-4 mt-3 text-sm text-neutral-500">
                      {result.node.difficulty_level && (
                        <span>Level {result.node.difficulty_level}</span>
                      )}
                      {result.node.simple_content_id ? (
                        <span className="text-green-600 dark:text-green-400">Has Content</span>
                      ) : (
                        <span className="text-neutral-400">Structure Only</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))
          ) : (
            // Advanced search results
            advancedResults.map((node) => (
              <div
                key={node.id}
                onClick={() => {
                  if (node.simple_content_id) {
                    navigate(`/learning/${node.simple_content_id}`)
                  }
                }}
                className={`card p-4 ${
                  node.simple_content_id 
                    ? 'cursor-pointer hover:shadow-lg transition-shadow' 
                    : ''
                }`}
              >
                <div className="flex items-start gap-4">
                  <div className={`p-2 rounded-lg ${
                    nodeTypeColors[node.node_type as keyof typeof nodeTypeColors] || nodeTypeColors.default
                  }`}>
                    {getNodeIcon(node.node_type)}
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg">{node.title}</h3>
                    {node.learning_area && (
                      <p className="text-neutral-600 dark:text-neutral-400 mt-1">
                        {node.learning_area}
                      </p>
                    )}
                    <div className="flex items-center gap-4 mt-3 text-sm text-neutral-500">
                      {node.difficulty_level && (
                        <span>Level {node.difficulty_level}</span>
                      )}
                      {node.simple_content_id ? (
                        <span className="text-green-600 dark:text-green-400">Has Content</span>
                      ) : (
                        <span className="text-neutral-400">Structure Only</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* No Results */}
      {!isLoading && query && results.length === 0 && advancedResults.length === 0 && (
        <div className="text-center py-12">
          <MagnifyingGlassIcon className="h-12 w-12 text-neutral-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold mb-2">No results found</h3>
          <p className="text-neutral-600 dark:text-neutral-400">
            Try adjusting your search terms or filters
          </p>
        </div>
      )}
    </div>
  )
}

export default SearchPage
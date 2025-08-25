import React, { useState } from 'react'
import { loadSpellingData, checkSpellingData } from '../utils/loadSpellingData'

export default function AdminSpellingPage() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [currentData, setCurrentData] = useState<any[]>([])
  const [stats, setStats] = useState<any>(null)

  const handleLoadData = async () => {
    setLoading(true)
    try {
      const result = await loadSpellingData()
      setResult(result)
      alert(`Data loaded successfully! Added ${result.success} words.`)
    } catch (error) {
      console.error('Failed to load data:', error)
      alert('Failed to load data. Check console for details.')
    } finally {
      setLoading(false)
    }
  }

  const handleCheckData = async () => {
    const data = await checkSpellingData()
    if (data) {
      setCurrentData(data)
      
      // Calculate statistics
      const difficultyStats: any = {}
      data.forEach((word: any) => {
        const diff = word.difficulty_name || 'Unknown'
        if (!difficultyStats[diff]) {
          difficultyStats[diff] = { count: 0, withEtymology: 0, withMemoryTips: 0, withSources: 0 }
        }
        difficultyStats[diff].count++
        if (word.etymology) difficultyStats[diff].withEtymology++
        if (word.memory_tips) difficultyStats[diff].withMemoryTips++
        if (word.source_names && word.source_names.length > 0) difficultyStats[diff].withSources++
      })
      
      setStats({
        total: data.length,
        byDifficulty: difficultyStats,
        withPronunciation: data.filter((w: any) => w.pronunciation_guide).length,
        withPartOfSpeech: data.filter((w: any) => w.part_of_speech).length,
        withEtymology: data.filter((w: any) => w.etymology).length,
        withMemoryTips: data.filter((w: any) => w.memory_tips).length
      })
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Spelling Bee Admin</h1>
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Load Spelling Bee Data</h2>
        <p className="text-gray-600 mb-4">
          This will load the prepared spelling bee words into the database.
        </p>
        
        <div className="flex gap-4">
          <button
            onClick={handleLoadData}
            disabled={loading}
            className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
          >
            {loading ? 'Loading...' : 'Load Spelling Bee Words'}
          </button>
          
          <button
            onClick={handleCheckData}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Check Current Data
          </button>
        </div>
        
        {result && (
          <div className="mt-4 p-4 bg-green-50 rounded-lg">
            <p>✅ Successfully loaded {result.success} words</p>
            {result.data && <p>Data entries: {result.data.length}</p>}
          </div>
        )}
      </div>

      {/* Statistics Panel */}
      {stats && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Database Statistics</h2>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-gray-50 p-3 rounded">
              <div className="text-2xl font-bold text-blue-600">{stats.total}</div>
              <div className="text-sm text-gray-600">Total Words</div>
            </div>
            <div className="bg-gray-50 p-3 rounded">
              <div className="text-2xl font-bold text-green-600">
                {Math.round((stats.withEtymology / stats.total) * 100)}%
              </div>
              <div className="text-sm text-gray-600">With Etymology</div>
            </div>
            <div className="bg-gray-50 p-3 rounded">
              <div className="text-2xl font-bold text-purple-600">
                {Math.round((stats.withMemoryTips / stats.total) * 100)}%
              </div>
              <div className="text-sm text-gray-600">With Memory Tips</div>
            </div>
            <div className="bg-gray-50 p-3 rounded">
              <div className="text-2xl font-bold text-orange-600">
                {Math.round((stats.withPronunciation / stats.total) * 100)}%
              </div>
              <div className="text-sm text-gray-600">With Pronunciation</div>
            </div>
          </div>
          
          <h3 className="text-lg font-semibold mb-3">Words by Difficulty Level</h3>
          <div className="space-y-2">
            {Object.entries(stats.byDifficulty).map(([level, data]: [string, any]) => (
              <div key={level} className="flex items-center justify-between bg-gray-50 p-2 rounded">
                <div className="flex items-center gap-3">
                  <span className={`px-2 py-1 rounded text-sm font-medium ${
                    level === 'Beginner' ? 'bg-green-100 text-green-800' :
                    level === 'Elementary' ? 'bg-blue-100 text-blue-800' :
                    level === 'Intermediate' ? 'bg-yellow-100 text-yellow-800' :
                    level === 'Advanced' ? 'bg-orange-100 text-orange-800' :
                    level === 'Expert' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {level}
                  </span>
                  <span className="font-semibold">{data.count} words</span>
                </div>
                <div className="flex gap-4 text-xs text-gray-600">
                  <span>Etymology: {Math.round((data.withEtymology / data.count) * 100)}%</span>
                  <span>Tips: {Math.round((data.withMemoryTips / data.count) * 100)}%</span>
                  <span>Sources: {Math.round((data.withSources / data.count) * 100)}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {currentData.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Current Spelling Words (Sample)</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full table-auto">
              <thead>
                <tr className="bg-gray-50">
                  <th className="px-4 py-2 text-left">Word</th>
                  <th className="px-4 py-2 text-left">Part of Speech</th>
                  <th className="px-4 py-2 text-left">Difficulty</th>
                  <th className="px-4 py-2 text-left">AI Difficulty</th>
                  <th className="px-4 py-2 text-left">Scripps Difficulty</th>
                  <th className="px-4 py-2 text-left">Sources</th>
                  <th className="px-4 py-2 text-left">Etymology</th>
                </tr>
              </thead>
              <tbody>
                {currentData.slice(0, 20).map((item, index) => (
                  <tr key={index} className="border-t hover:bg-gray-50">
                    <td className="px-4 py-2">
                      <div>
                        <div className="font-medium">{item.word}</div>
                        {item.pronunciation_guide && (
                          <div className="text-xs text-gray-500 font-mono">{item.pronunciation_guide}</div>
                        )}
                      </div>
                    </td>
                    <td className="px-4 py-2 text-gray-600 text-sm italic">
                      {item.part_of_speech || '-'}
                    </td>
                    <td className="px-4 py-2">
                      {item.difficulty_name && (
                        <span className={`px-2 py-1 rounded text-xs ${
                          item.difficulty_name === 'Beginner' ? 'bg-green-100 text-green-800' :
                          item.difficulty_name === 'Elementary' ? 'bg-blue-100 text-blue-800' :
                          item.difficulty_name === 'Intermediate' ? 'bg-yellow-100 text-yellow-800' :
                          item.difficulty_name === 'Advanced' ? 'bg-orange-100 text-orange-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {item.difficulty_name}
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-2">
                      {item.ai_difficulty_name && (
                        <span className={`px-2 py-1 rounded text-xs ${
                          item.ai_difficulty_name === 'Beginner' ? 'bg-green-100 text-green-800' :
                          item.ai_difficulty_name === 'Elementary' ? 'bg-blue-100 text-blue-800' :
                          item.ai_difficulty_name === 'Intermediate' ? 'bg-yellow-100 text-yellow-800' :
                          item.ai_difficulty_name === 'Advanced' ? 'bg-orange-100 text-orange-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {item.ai_difficulty_name}
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-2 text-gray-600 text-sm">
                      {item.source_difficulty || '-'}
                    </td>
                    <td className="px-4 py-2">
                      <div className="text-xs">
                        {item.source_names && item.source_names.length > 0 ? (
                          <span className="text-blue-600">
                            {item.source_names.length} source{item.source_names.length > 1 ? 's' : ''}
                          </span>
                        ) : '-'}
                      </div>
                    </td>
                    <td className="px-4 py-2">
                      <div className="text-xs text-gray-600">
                        {item.etymology_source ? (
                          <span title={item.etymology || ''}>
                            {item.etymology_source}
                          </span>
                        ) : '-'}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {currentData.length > 20 && (
            <div className="mt-4 text-center text-sm text-gray-500">
              Showing 20 of {currentData.length} words
            </div>
          )}
        </div>
      )}
    </div>
  )
}
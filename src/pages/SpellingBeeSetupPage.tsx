import React, { useState, useEffect } from 'react'
import { setupSpellingBeeTables, checkTableExists } from '../utils/setupSpellingBeeTables'
import { loadSpellingBeeData } from '../utils/loadSpellingBeeData'
import { loadRemainingWords } from '../utils/loadRemainingWords'
import { loadSpellingWordsInBatches } from '../utils/spellingWordCollection'

export default function SpellingBeeSetupPage() {
  const [tableExists, setTableExists] = useState<boolean | null>(null)
  const [setupSQL, setSetupSQL] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [loadResult, setLoadResult] = useState<any>(null)

  useEffect(() => {
    checkExistingTable()
  }, [])

  const checkExistingTable = async () => {
    const exists = await checkTableExists()
    setTableExists(exists)
    
    if (!exists) {
      const result = await setupSpellingBeeTables()
      if (result.sql) {
        setSetupSQL(result.sql)
      }
    }
  }

  const handleLoadData = async () => {
    setLoading(true)
    try {
      const result = await loadSpellingBeeData()
      setLoadResult(result)
      alert(`Data loaded! Success: ${result.success}`)
      // Recheck if table exists after loading
      checkExistingTable()
    } catch (error) {
      console.error('Failed to load data:', error)
      alert('Failed to load data. Check console for details.')
    } finally {
      setLoading(false)
    }
  }

  const copySQL = () => {
    navigator.clipboard.writeText(setupSQL)
    alert('SQL copied to clipboard!')
  }


  const handleLoadRemainingWords = async () => {
    setLoading(true)
    try {
      const result = await loadRemainingWords()
      setLoadResult(result)
      alert(`Remaining words loaded! Success: ${result.success}, Count: ${result.count}`)
      // Recheck if table exists after loading
      checkExistingTable()
    } catch (error) {
      console.error('Failed to load remaining words:', error)
      alert('Failed to load remaining words. Check console for details.')
    } finally {
      setLoading(false)
    }
  }

  const handleLoadComprehensiveCollection = async () => {
    if (!window.confirm('This will load 150+ spelling words. Continue?')) {
      return
    }
    
    setLoading(true)
    try {
      const result = await loadSpellingWordsInBatches([], 50)
      setLoadResult(result)
      const successfulBatches = result.filter(r => r.success).length
      const failedBatches = result.filter(r => !r.success).length
      alert(`Collection loaded! Successful batches: ${successfulBatches}, Failed batches: ${failedBatches}`)
      // Recheck if table exists after loading
      checkExistingTable()
    } catch (error) {
      console.error('Failed to load comprehensive collection:', error)
      alert('Failed to load collection. Check console for details.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Spelling Bee Setup</h1>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Database Status</h2>
        
        {tableExists === null && (
          <p className="text-gray-600">Checking database...</p>
        )}
        
        {tableExists === false && (
          <div className="space-y-4">
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-yellow-800 font-medium mb-2">
                ⚠️ The spelling_words table does not exist yet.
              </p>
              <p className="text-yellow-700 text-sm mb-4">
                Please create it by running the following SQL in your Supabase SQL Editor:
              </p>
              <ol className="list-decimal list-inside text-yellow-700 text-sm space-y-1">
                <li>Go to your Supabase Dashboard</li>
                <li>Navigate to SQL Editor</li>
                <li>Copy the SQL below</li>
                <li>Paste and run it in the SQL Editor</li>
                <li>Refresh this page when done</li>
              </ol>
            </div>

            <div className="relative">
              <button
                onClick={copySQL}
                className="absolute top-2 right-2 px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
              >
                Copy SQL
              </button>
              <pre className="p-4 bg-gray-50 rounded-lg overflow-x-auto text-xs">
                {setupSQL}
              </pre>
            </div>

            <button
              onClick={checkExistingTable}
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            >
              Check Again
            </button>
          </div>
        )}

        {tableExists === true && (
          <div className="space-y-4">
            <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-green-800 font-medium">
                ✅ The spelling_words table exists and is ready!
              </p>
            </div>

            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Load Spelling Bee Data</h3>
              <p className="text-gray-600">
                Click the button below to load the prepared spelling bee words into the database.
              </p>
              
              <div className="flex gap-4 flex-wrap">
                <button
                  onClick={handleLoadData}
                  disabled={loading}
                  className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
                >
                  {loading ? 'Loading...' : 'Load Spelling Bee Words'}
                </button>
                
                <button
                  onClick={handleLoadRemainingWords}
                  disabled={loading}
                  className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
                >
                  {loading ? 'Loading...' : 'Load Remaining Words (38)'}
                </button>
                
                <button
                  onClick={handleLoadComprehensiveCollection}
                  disabled={loading}
                  className="px-6 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 disabled:opacity-50"
                >
                  {loading ? 'Loading...' : 'Load Comprehensive Collection (150+ words)'}
                </button>
              </div>

              {loadResult && (
                <div className="p-4 bg-blue-50 rounded-lg">
                  {Array.isArray(loadResult) ? (
                    <div>
                      <p>✅ Batch loading completed</p>
                      <p>Successful batches: {loadResult.filter(r => r.success).length}</p>
                      <p>Failed batches: {loadResult.filter(r => !r.success).length}</p>
                    </div>
                  ) : (
                    <div>
                      <p>✅ Loading completed</p>
                      {loadResult.success && <p>Success: {loadResult.success}</p>}
                      {loadResult.count && <p>Count: {loadResult.count}</p>}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Setup Instructions</h2>
        <div className="prose max-w-none">
          <ol className="list-decimal list-inside space-y-2">
            <li>First, ensure the spelling_words table is created in your Supabase database</li>
            <li>If the table doesn't exist, copy the SQL provided above and run it in Supabase SQL Editor</li>
            <li>Once the table is created, click "Load Spelling Bee Words" to populate the data</li>
            <li>The system will load sample words with difficulty levels, etymology, and pronunciation tips</li>
          </ol>

          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold mb-2">Difficulty Levels:</h3>
            <ul className="space-y-1 text-sm">
              <li><span className="font-medium">1 - Beginner:</span> Grades 1-3, common everyday words</li>
              <li><span className="font-medium">2 - Elementary:</span> Grades 4-5, standard school vocabulary</li>
              <li><span className="font-medium">3 - Intermediate:</span> Grades 6-8, complex patterns</li>
              <li><span className="font-medium">4 - Advanced:</span> Grades 9-12, regional competition level</li>
              <li><span className="font-medium">5 - Expert:</span> National championship level</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
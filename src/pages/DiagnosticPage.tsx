import React, { useState, useEffect } from 'react'
import { supabase } from '../services/supabase'

const DiagnosticPage: React.FC = () => {
  const [diagnostics, setDiagnostics] = useState<any>({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    runDiagnostics()
  }, [])

  const runDiagnostics = async () => {
    const results: any = {}
    
    // Test each table
    const tables = [
      'skill_tree_nodes',
      'questions', 
      'learning_content',
      'user_progress',
      'feedback',
      'starred_categories',
      'user_question_responses'
    ]
    
    for (const table of tables) {
      try {
        const { data, error, count } = await supabase
          .from(table)
          .select('*', { count: 'exact', head: false })
          .limit(1)
        
        results[table] = {
          exists: !error,
          error: error?.message,
          count: count || 0,
          sample: data?.[0]
        }
      } catch (e: any) {
        results[table] = {
          exists: false,
          error: e.message
        }
      }
    }
    
    // Test authentication
    try {
      const { data: { user } } = await (supabase.auth as any).getUser()
      results.auth = {
        authenticated: !!user,
        user: user?.email
      }
    } catch (e: any) {
      results.auth = {
        authenticated: false,
        error: e.message
      }
    }
    
    setDiagnostics(results)
    setLoading(false)
  }

  if (loading) {
    return <div className="p-8">Running diagnostics...</div>
  }

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">System Diagnostics</h1>
      
      <div className="space-y-6">
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Authentication Status</h2>
          <pre className="bg-neutral-100 dark:bg-neutral-900 p-4 rounded overflow-auto">
            {JSON.stringify(diagnostics.auth, null, 2)}
          </pre>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Database Tables</h2>
          <div className="space-y-4">
            {Object.entries(diagnostics).filter(([key]) => key !== 'auth').map(([table, info]: any) => (
              <div key={table} className="border border-neutral-200 dark:border-neutral-700 rounded p-4">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium text-lg">{table}</h3>
                  <span className={`px-2 py-1 rounded text-sm ${
                    info.exists 
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                  }`}>
                    {info.exists ? `✓ Exists (${info.count} rows)` : '✗ Not Found'}
                  </span>
                </div>
                
                {info.error && (
                  <div className="text-red-600 dark:text-red-400 text-sm mb-2">
                    Error: {info.error}
                  </div>
                )}
                
                {info.sample && (
                  <details className="mt-2">
                    <summary className="cursor-pointer text-sm text-neutral-600 dark:text-neutral-400">
                      View sample data
                    </summary>
                    <pre className="mt-2 text-xs bg-neutral-100 dark:bg-neutral-900 p-2 rounded overflow-auto">
                      {JSON.stringify(info.sample, null, 2)}
                    </pre>
                  </details>
                )}
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Environment</h2>
          <pre className="bg-neutral-100 dark:bg-neutral-900 p-4 rounded overflow-auto text-sm">
            {JSON.stringify({
              supabaseUrl: process.env.REACT_APP_SUPABASE_URL,
              hasAnonKey: !!process.env.REACT_APP_SUPABASE_ANON_KEY,
              nodeEnv: process.env.NODE_ENV,
              userAgent: navigator.userAgent
            }, null, 2)}
          </pre>
        </div>
      </div>
    </div>
  )
}

export default DiagnosticPage
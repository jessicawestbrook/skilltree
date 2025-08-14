'use client';

import { useState, useEffect } from 'react';
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs';
import { useAuth } from '@/contexts/AuthContext';
import Link from 'next/link';
import { Home, ArrowLeft, Database } from 'lucide-react';

function DatabaseSetupPageContent() {
  const [status, setStatus] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const { isAuthenticated, user } = useAuth();
  const supabase = createClientComponentClient();

  const applyMigration = async () => {
    setLoading(true);
    setStatus('Applying migration...');

    try {
      // Check if user is authenticated using the auth context
      if (!isAuthenticated || !user) {
        setStatus('Error: You must be logged in to run migrations. Please log in first at the main page.');
        setLoading(false);
        return;
      }

      // Since we can't execute DDL via RPC, let's directly try to create the function using raw SQL
      try {
        // This will likely fail, but let's try
        const response = await fetch('/api/admin/apply-migration', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY}`
          }
        });
        
        if (response.ok) {
          setStatus('Migration applied successfully via API!');
        } else {
          const error = await response.json();
          setStatus(`API migration failed: ${error.error}. Please use the manual SQL method below.`);
        }
      } catch (apiError) {
        setStatus('API method failed. Please copy the SQL below and run it in the Supabase SQL Editor.');
        console.error('API Error:', apiError);
      }
    } catch (error) {
      console.error('Error:', error);
      setStatus('Error applying migration. See console for details.');
    } finally {
      setLoading(false);
    }
  };

  const testFunction = async () => {
    setLoading(true);
    setStatus('Testing friend suggestions function...');

    try {
      if (!isAuthenticated || !user) {
        setStatus('Error: You must be logged in to test. Please log in first at the main page.');
        setLoading(false);
        return;
      }

      const { data, error } = await supabase
        .rpc('get_friend_suggestions', { p_user_id: user.id });

      if (error) {
        setStatus(`Function test failed: ${error.message}`);
        console.error('Test error:', error);
      } else {
        setStatus(`Function works! Found ${data?.length || 0} suggestions: ${JSON.stringify(data, null, 2)}`);
      }
    } catch (error) {
      console.error('Error:', error);
      setStatus('Error testing function. See console for details.');
    } finally {
      setLoading(false);
    }
  };

  const getSQLMigration = () => {
    return `-- Drop existing view if it exists
DROP VIEW IF EXISTS friend_suggestions;

-- Create or replace the get_friend_suggestions function
CREATE OR REPLACE FUNCTION get_friend_suggestions(p_user_id UUID)
RETURNS TABLE (
  suggested_user_id UUID,
  username VARCHAR(50),
  neural_level INTEGER,
  total_points INTEGER,
  common_groups BIGINT,
  common_nodes BIGINT
) 
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  RETURN QUERY
  WITH user_friends AS (
    SELECT friend_id 
    FROM friends 
    WHERE user_id = p_user_id
  ),
  friend_requests_sent AS (
    SELECT receiver_id 
    FROM friend_requests 
    WHERE sender_id = p_user_id 
      AND status IN ('pending', 'accepted')
  ),
  friend_requests_received AS (
    SELECT sender_id 
    FROM friend_requests 
    WHERE receiver_id = p_user_id 
      AND status IN ('pending', 'accepted')
  ),
  excluded_users AS (
    SELECT friend_id AS user_id FROM user_friends
    UNION
    SELECT receiver_id AS user_id FROM friend_requests_sent
    UNION
    SELECT sender_id AS user_id FROM friend_requests_received
    UNION
    SELECT p_user_id AS user_id
  ),
  eligible_users AS (
    SELECT DISTINCT p.id, p.username, p.neural_level, p.total_points
    FROM user_profiles p
    WHERE p.id NOT IN (SELECT user_id FROM excluded_users)
      AND p.id IS NOT NULL
  )
  SELECT 
    eu.id AS suggested_user_id,
    eu.username,
    eu.neural_level,
    eu.total_points,
    0::BIGINT AS common_groups,
    0::BIGINT AS common_nodes
  FROM eligible_users eu
  ORDER BY 
    eu.neural_level DESC,
    eu.total_points DESC
  LIMIT 10;
END;
$$;

-- Grant execute permission
GRANT EXECUTE ON FUNCTION get_friend_suggestions(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION get_friend_suggestions(UUID) TO anon;`;
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center gap-4 mb-6">
          <Link 
            href="/"
            className="flex items-center gap-2 px-3 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
          >
            <ArrowLeft size={20} />
            <Home size={20} />
            <span className="font-medium">Back to Learning</span>
          </Link>
          <Link 
            href="/admin"
            className="flex items-center gap-2 px-3 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
          >
            <Database size={20} />
            <span className="font-medium">Admin Dashboard</span>
          </Link>
        </div>
        <h1 className="text-3xl font-bold mb-8">Database Setup - Friend Suggestions</h1>
        
        {/* Auth Status */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 mb-6">
          <h2 className="text-lg font-semibold mb-2">Authentication Status</h2>
          <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
            isAuthenticated 
              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
              : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
          }`}>
            {isAuthenticated ? '✅ Logged In' : '❌ Not Logged In'}
          </div>
          {isAuthenticated && user && (
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
              User: {user.email || user.id}
            </p>
          )}
          {!isAuthenticated && (
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
              Please <a href="/login" className="text-blue-600 hover:underline">log in</a> to access database functions.
            </p>
          )}
        </div>
        
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
          
          <div className="space-y-4">
            <button
              onClick={applyMigration}
              disabled={loading}
              className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 mr-4"
            >
              {loading ? 'Working...' : 'Try Apply Migration'}
            </button>
            
            <button
              onClick={testFunction}
              disabled={loading}
              className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:bg-gray-400"
            >
              {loading ? 'Testing...' : 'Test Function'}
            </button>
          </div>

          {status && (
            <div className="mt-6 p-4 bg-gray-100 dark:bg-gray-700 rounded-lg">
              <pre className="whitespace-pre-wrap text-sm">{status}</pre>
            </div>
          )}
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Manual SQL Migration</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            If the automatic migration doesn't work, copy this SQL and run it in your Supabase Dashboard:
          </p>
          
          <ol className="list-decimal list-inside mb-4 space-y-2">
            <li>Go to your Supabase Dashboard</li>
            <li>Navigate to SQL Editor</li>
            <li>Create a new query</li>
            <li>Paste the SQL below</li>
            <li>Click "Run"</li>
          </ol>

          <div className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
            <pre className="text-xs">{getSQLMigration()}</pre>
          </div>
          
          <button
            onClick={() => navigator.clipboard.writeText(getSQLMigration())}
            className="mt-4 px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
          >
            Copy SQL to Clipboard
          </button>
        </div>

        <div className="mt-8 p-4 bg-yellow-100 dark:bg-yellow-900 rounded-lg">
          <p className="text-sm">
            <strong>Note:</strong> After applying the migration, go to the Social page and check the "Find Friends" tab.
            The friend suggestions should now be populated.
          </p>
        </div>
      </div>
    </div>
  );
}

// Wrap with auth context
export default function DatabaseSetupPage() {
  return (
    <DatabaseSetupPageContent />
  );
}
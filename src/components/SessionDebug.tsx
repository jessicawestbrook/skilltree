'use client';

import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { getStoredSession } from '../utils/sessionStorage';

export const SessionDebug: React.FC = () => {
  const { user, isAuthenticated, sessionReady, refreshSession } = useAuth();
  
  const handleRefreshSession = async () => {
    const result = await refreshSession();
    console.log('Manual refresh result:', result);
  };
  
  const checkStoredSession = () => {
    const stored = getStoredSession();
    console.log('Stored session:', stored);
  };
  
  if (!sessionReady) {
    return (
      <div className="p-4 bg-yellow-100 border border-yellow-400 rounded">
        <p>Session still loading...</p>
      </div>
    );
  }
  
  return (
    <div className="p-4 bg-gray-100 border border-gray-300 rounded">
      <h3 className="font-bold mb-2">Session Debug Info</h3>
      <div className="space-y-2 text-sm">
        <p><strong>Authenticated:</strong> {isAuthenticated ? 'Yes' : 'No'}</p>
        <p><strong>Session Ready:</strong> {sessionReady ? 'Yes' : 'No'}</p>
        <p><strong>User ID:</strong> {user?.id || 'None'}</p>
        <p><strong>Username:</strong> {user?.username || 'None'}</p>
        <p><strong>Email:</strong> {user?.email || 'None'}</p>
      </div>
      <div className="mt-4 space-x-2">
        <button 
          onClick={handleRefreshSession}
          className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Refresh Session
        </button>
        <button 
          onClick={checkStoredSession}
          className="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Check Stored Session
        </button>
      </div>
    </div>
  );
};
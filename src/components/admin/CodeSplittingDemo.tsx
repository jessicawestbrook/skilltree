'use client';

import React, { Suspense } from 'react';
import dynamic from 'next/dynamic';
import { LoadingSpinner } from './LoadingSpinner';

// Demonstrate code splitting by dynamically importing a heavy component
const HeavyAdminComponent = dynamic(
  () => import('./HeavyAdminComponent').then(mod => mod.HeavyAdminComponent),
  {
    loading: () => <LoadingSpinner message="Loading heavy admin component..." />,
    ssr: false
  }
);

export const CodeSplittingDemo: React.FC = () => {
  const [showHeavy, setShowHeavy] = React.useState(false);

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Code Splitting Demo</h2>
      <p className="text-gray-600 mb-4">
        This demonstrates code splitting in action. The heavy component is only loaded when needed.
      </p>
      
      <button
        onClick={() => setShowHeavy(!showHeavy)}
        className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition-colors"
      >
        {showHeavy ? 'Hide' : 'Load'} Heavy Component
      </button>

      {showHeavy && (
        <div className="mt-4">
          <Suspense fallback={<LoadingSpinner message="Loading heavy component..." />}>
            <HeavyAdminComponent />
          </Suspense>
        </div>
      )}
    </div>
  );
};
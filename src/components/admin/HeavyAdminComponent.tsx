'use client';

import React from 'react';

// Simulate a heavy component that would benefit from code splitting
export const HeavyAdminComponent: React.FC = () => {
  const [data, setData] = React.useState<number[]>([]);

  React.useEffect(() => {
    // Simulate loading heavy data
    const heavyData = Array.from({ length: 1000 }, (_, i) => i);
    setData(heavyData);
  }, []);

  return (
    <div className="p-4 border border-gray-200 rounded-lg bg-gray-50">
      <h3 className="text-lg font-semibold mb-2">Heavy Admin Component</h3>
      <p className="text-sm text-gray-600 mb-2">
        This component simulates a heavy admin interface with lots of data processing.
      </p>
      <div className="grid grid-cols-10 gap-1 max-h-32 overflow-y-auto">
        {data.slice(0, 100).map(item => (
          <div key={item} className="w-8 h-8 bg-indigo-100 rounded text-xs flex items-center justify-center">
            {item}
          </div>
        ))}
      </div>
      <p className="text-xs text-gray-500 mt-2">
        Loaded {data.length} items (showing first 100)
      </p>
    </div>
  );
};
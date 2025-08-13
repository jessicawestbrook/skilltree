'use client';

import React, { useState, Suspense } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LoadingSpinner } from '@/components/admin/LoadingSpinner';

// Navigation configuration
const navItems = [
  { href: '/admin', label: 'Dashboard', icon: '📊', preload: true },
  { href: '/admin/content', label: 'Course Content', icon: '📚', preload: false },
  { href: '/admin/questions', label: 'Questions', icon: '❓', preload: false },
  { href: '/admin/nodes', label: 'Knowledge Nodes', icon: '🧠', preload: false },
  { href: '/admin/paths', label: 'Learning Paths', icon: '🛤️', preload: false },
  { href: '/admin/users', label: 'Users', icon: '👥', preload: false },
  { href: '/admin/upload', label: 'Batch Upload', icon: '📤', preload: false },
  { href: '/admin/settings', label: 'Settings', icon: '⚙️', preload: false },
];

export default function OptimizedAdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  // Preload function for route prefetching
  const handleMouseEnter = () => {
    // Prefetch the route on hover for faster navigation
    if (typeof window !== 'undefined' && 'requestIdleCallback' in window) {
      requestIdleCallback(() => {
        // Next.js will handle prefetching automatically with Link component
      });
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex">
      {/* Sidebar */}
      <aside 
        className={`${
          isSidebarOpen ? 'w-64' : 'w-16'
        } bg-indigo-900 text-white transition-all duration-300 ease-in-out transform-gpu`}
      >
        <div className="p-4">
          <div className="flex items-center justify-between mb-8">
            <h1 className={`font-bold text-xl transition-opacity duration-300 ${
              !isSidebarOpen ? 'opacity-0 hidden' : 'opacity-100'
            }`}>
              NeuroQuest Admin
            </h1>
            <button
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="p-2 hover:bg-indigo-800 rounded transition-colors"
              aria-label={isSidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
            >
              <span className="inline-block transition-transform duration-300">
                {isSidebarOpen ? '◀' : '▶'}
              </span>
            </button>
          </div>
          
          <nav>
            <ul className="space-y-2">
              {navItems.map((item) => {
                const isActive = pathname === item.href || 
                  (item.href !== '/admin' && pathname.startsWith(item.href));
                
                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-all duration-200 ${
                        isActive
                          ? 'bg-indigo-800 text-white shadow-lg'
                          : 'hover:bg-indigo-800 text-indigo-100 hover:shadow-md'
                      }`}
                      onMouseEnter={handleMouseEnter}
                      prefetch={item.preload}
                    >
                      <span className="text-xl flex-shrink-0">{item.icon}</span>
                      <span className={`transition-all duration-300 ${
                        isSidebarOpen 
                          ? 'opacity-100 translate-x-0' 
                          : 'opacity-0 -translate-x-4 sr-only'
                      }`}>
                        {item.label}
                      </span>
                    </Link>
                  </li>
                );
              })}
            </ul>
          </nav>

          <div className={`mt-auto pt-8 transition-all duration-300 ${
            !isSidebarOpen ? 'opacity-0 hidden' : 'opacity-100'
          }`}>
            <Link
              href="/"
              className="flex items-center gap-2 px-3 py-2 text-indigo-200 hover:text-white hover:bg-indigo-800 rounded-lg transition-colors"
            >
              ← Back to App
            </Link>
          </div>
        </div>
      </aside>

      {/* Main Content with Suspense boundary */}
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          <Suspense fallback={<LoadingSpinner message="Loading admin panel..." />}>
            {children}
          </Suspense>
        </div>
      </main>
    </div>
  );
}
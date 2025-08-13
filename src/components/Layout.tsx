'use client';

import React, { ReactNode } from 'react';

interface LayoutProps {
  children: ReactNode;
  sidebar?: ReactNode;
  rightPanel?: ReactNode;
  isMobile?: boolean;
}

export default function Layout({ children, sidebar, rightPanel, isMobile = false }: LayoutProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Main Container */}
      <div className="h-full">
        {/* Content Grid */}
        <div className={`
          ${isMobile ? 'block' : 'grid grid-cols-[300px_1fr_320px]'}
          gap-6 max-w-[1600px] mx-auto p-4 md:p-6
        `}>
          {/* Left Sidebar */}
          {!isMobile && sidebar && (
            <aside className="space-y-4">
              <div className="sticky top-6">
                {sidebar}
              </div>
            </aside>
          )}

          {/* Main Content Area */}
          <main className="min-w-0">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden">
              {children}
            </div>
          </main>

          {/* Right Panel */}
          {!isMobile && rightPanel && (
            <aside className="space-y-4">
              <div className="sticky top-6">
                {rightPanel}
              </div>
            </aside>
          )}
        </div>
      </div>
    </div>
  );
}
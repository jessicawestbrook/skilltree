'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const navItems = [
    { href: '/admin', label: 'Dashboard', icon: '📊' },
    { href: '/admin/content', label: 'Course Content', icon: '📚' },
    { href: '/admin/questions', label: 'Questions', icon: '❓' },
    { href: '/admin/nodes', label: 'Knowledge Nodes', icon: '🧠' },
    { href: '/admin/paths', label: 'Learning Paths', icon: '🛤️' },
    { href: '/admin/users', label: 'Users', icon: '👥' },
    { href: '/admin/upload', label: 'Batch Upload', icon: '📤' },
    { href: '/admin/settings', label: 'Settings', icon: '⚙️' },
  ];

  return (
    <div className="min-h-screen bg-gray-100 flex">
      {/* Sidebar */}
      <aside className={`${isSidebarOpen ? 'w-64' : 'w-16'} bg-indigo-900 text-white transition-all duration-300 ease-in-out`}>
        <div className="p-4">
          <div className="flex items-center justify-between mb-8">
            <h1 className={`font-bold text-xl ${!isSidebarOpen && 'hidden'}`}>
              NeuroQuest Admin
            </h1>
            <button
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="p-2 hover:bg-indigo-800 rounded"
            >
              {isSidebarOpen ? '◀' : '▶'}
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
                      className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                        isActive
                          ? 'bg-indigo-800 text-white'
                          : 'hover:bg-indigo-800 text-indigo-100'
                      }`}
                    >
                      <span className="text-xl">{item.icon}</span>
                      {isSidebarOpen && <span>{item.label}</span>}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </nav>

          <div className={`mt-auto pt-8 ${!isSidebarOpen && 'hidden'}`}>
            <Link
              href="/"
              className="flex items-center gap-2 px-3 py-2 text-indigo-200 hover:text-white hover:bg-indigo-800 rounded-lg"
            >
              ← Back to App
            </Link>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  );
}
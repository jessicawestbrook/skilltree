'use client';

import React, { useState, useEffect, Suspense } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { preloadCriticalAdminAssets } from '@/utils/adminPrefetch';
import { LoadingSpinner } from '@/components/admin/LoadingSpinner';
import {
  LayoutDashboard,
  BookOpen,
  HelpCircle,
  Brain,
  Route,
  Users,
  Upload,
  Settings,
  ChevronLeft,
  ChevronRight,
  LogOut,
  Bell,
  Search,
  Menu
} from 'lucide-react';

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Preload critical admin assets on mount
  useEffect(() => {
    preloadCriticalAdminAssets();
  }, []);

  const navItems = [
    { href: '/admin', label: 'Dashboard', icon: LayoutDashboard, color: 'text-blue-600' },
    { href: '/admin/content', label: 'Course Content', icon: BookOpen, color: 'text-green-600' },
    { href: '/admin/questions', label: 'Questions', icon: HelpCircle, color: 'text-purple-600' },
    { href: '/admin/nodes', label: 'Knowledge Nodes', icon: Brain, color: 'text-pink-600' },
    { href: '/admin/paths', label: 'Learning Paths', icon: Route, color: 'text-orange-600' },
    { href: '/admin/users', label: 'Users', icon: Users, color: 'text-cyan-600' },
    { href: '/admin/upload', label: 'Batch Upload', icon: Upload, color: 'text-yellow-600' },
    { href: '/admin/settings', label: 'Settings', icon: Settings, color: 'text-gray-600' },
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Mobile Menu Overlay */}
      {isMobileMenuOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed lg:static inset-y-0 left-0 z-50
        ${isSidebarOpen ? 'w-64' : 'w-20'} 
        ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        bg-white border-r border-gray-200 transition-all duration-300 ease-in-out shadow-lg lg:shadow-none
      `}>
        <div className="flex flex-col h-full">
          {/* Logo Section */}
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <div className={`flex items-center gap-3 ${!isSidebarOpen && 'lg:justify-center'}`}>
                <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <Brain className="w-6 h-6 text-white" />
                </div>
                {isSidebarOpen && (
                  <div>
                    <h1 className="font-bold text-gray-900">NeuroQuest</h1>
                    <p className="text-xs text-gray-500">Admin Panel</p>
                  </div>
                )}
              </div>
              <button
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                className="hidden lg:block p-1.5 hover:bg-gray-100 rounded-lg transition-colors"
              >
                {isSidebarOpen ? 
                  <ChevronLeft className="w-5 h-5 text-gray-600" /> : 
                  <ChevronRight className="w-5 h-5 text-gray-600" />
                }
              </button>
            </div>
          </div>
          
          {/* Navigation */}
          <nav className="flex-1 px-4 py-6">
            <ul className="space-y-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = pathname === item.href || 
                  (item.href !== '/admin' && pathname.startsWith(item.href));
                
                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all group ${
                        isActive
                          ? 'bg-gradient-to-r from-indigo-50 to-purple-50 border-l-4 border-indigo-600'
                          : 'hover:bg-gray-50'
                      }`}
                      onClick={() => setIsMobileMenuOpen(false)}
                    >
                      <div className={`p-1.5 rounded-lg ${
                        isActive ? 'bg-white shadow-sm' : 'group-hover:bg-white'
                      }`}>
                        <Icon className={`w-5 h-5 ${
                          isActive ? item.color : 'text-gray-500 group-hover:' + item.color
                        }`} />
                      </div>
                      {isSidebarOpen && (
                        <div className="flex-1">
                          <span className={`font-medium ${
                            isActive ? 'text-gray-900' : 'text-gray-700'
                          }`}>
                            {item.label}
                          </span>
                        </div>
                      )}
                      {isSidebarOpen && isActive && (
                        <div className="w-2 h-2 bg-indigo-600 rounded-full animate-pulse" />
                      )}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-gray-200">
            {isSidebarOpen ? (
              <Link
                href="/"
                className="flex items-center gap-3 px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors"
              >
                <LogOut className="w-5 h-5" />
                <span className="font-medium">Exit Admin</span>
              </Link>
            ) : (
              <Link
                href="/"
                className="flex items-center justify-center p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg"
                title="Exit Admin"
              >
                <LogOut className="w-5 h-5" />
              </Link>
            )}
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="bg-white border-b border-gray-200 px-4 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="lg:hidden p-2 hover:bg-gray-100 rounded-lg"
              >
                <Menu className="w-5 h-5 text-gray-600" />
              </button>
              <div className="hidden md:flex items-center gap-2 bg-gray-50 px-4 py-2 rounded-lg">
                <Search className="w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search..."
                  className="bg-transparent outline-none text-sm text-gray-700 placeholder-gray-400 w-64"
                />
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button className="relative p-2 hover:bg-gray-100 rounded-lg transition-colors">
                <Bell className="w-5 h-5 text-gray-600" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
              </button>
              <div className="flex items-center gap-3 pl-3 border-l border-gray-200">
                <div className="text-right hidden sm:block">
                  <p className="text-sm font-medium text-gray-900">Admin User</p>
                  <p className="text-xs text-gray-500">Super Admin</p>
                </div>
                <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center">
                  <span className="text-white font-bold">A</span>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex-1 overflow-auto bg-gray-50">
          <div className="p-4 lg:p-8">
            <Suspense fallback={<LoadingSpinner message="Loading admin content..." />}>
              {children}
            </Suspense>
          </div>
        </main>
      </div>
    </div>
  );
}
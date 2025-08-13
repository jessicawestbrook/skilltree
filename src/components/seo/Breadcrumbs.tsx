'use client';

import React from 'react';
import Link from 'next/link';
import { ChevronRight, Home } from 'lucide-react';
import { StructuredData } from './StructuredData';
import { generateBreadcrumbStructuredData, type BreadcrumbItem } from '../../utils/seo/structuredData';

interface BreadcrumbsProps {
  items: BreadcrumbItem[];
  className?: string;
  showHome?: boolean;
  separator?: React.ReactNode;
}

export function Breadcrumbs({ 
  items, 
  className = '', 
  showHome = true,
  separator = <ChevronRight size={16} className="text-gray-400 mx-2" />
}: BreadcrumbsProps) {
  const allItems = showHome 
    ? [{ name: 'Home', url: '/' }, ...items]
    : items;

  const structuredData = generateBreadcrumbStructuredData(allItems);

  return (
    <>
      <StructuredData data={structuredData} />
      <nav 
        className={`flex items-center space-x-1 text-sm ${className}`} 
        aria-label="Breadcrumb"
      >
        <ol className="flex items-center space-x-1">
          {allItems.map((item, index) => {
            const isLast = index === allItems.length - 1;
            const isHome = index === 0 && showHome;
            
            return (
              <li key={item.url} className="flex items-center">
                {index > 0 && separator}
                {isLast ? (
                  <span 
                    className="text-gray-900 dark:text-gray-100 font-medium"
                    aria-current="page"
                  >
                    {isHome ? <Home size={16} /> : item.name}
                  </span>
                ) : (
                  <Link
                    href={item.url}
                    className="text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors duration-200 flex items-center"
                  >
                    {isHome ? <Home size={16} /> : item.name}
                  </Link>
                )}
              </li>
            );
          })}
        </ol>
      </nav>
    </>
  );
}

export default Breadcrumbs;
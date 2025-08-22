import React from 'react'
import { Link } from 'react-router-dom'
import { ChevronRightIcon } from '@heroicons/react/24/outline'
import { Helmet } from 'react-helmet-async'
import { createBreadcrumbStructuredData } from '../utils/structuredData'

interface BreadcrumbItem {
  name: string
  url: string
  current?: boolean
}

interface BreadcrumbProps {
  items: BreadcrumbItem[]
  className?: string
}

const Breadcrumb: React.FC<BreadcrumbProps> = ({ items, className = '' }) => {
  const breadcrumbStructuredData = createBreadcrumbStructuredData(
    items.map(item => ({ name: item.name, url: item.url }))
  )

  return (
    <>
      <Helmet>
        <script type="application/ld+json">
          {JSON.stringify(breadcrumbStructuredData)}
        </script>
      </Helmet>
      
      <nav className={`mb-6 ${className}`} aria-label="Breadcrumb">
        <ol className="flex items-center space-x-2 text-sm">
          {items.map((item, index) => (
            <li key={index} className="flex items-center">
              {index > 0 && (
                <ChevronRightIcon className="h-3 w-3 text-neutral-400 mx-2" />
              )}
              
              {item.current || index === items.length - 1 ? (
                <span className="text-neutral-600 dark:text-neutral-400 font-medium">
                  {item.name}
                </span>
              ) : (
                <Link
                  to={item.url}
                  className="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 transition-colors"
                >
                  {item.name}
                </Link>
              )}
            </li>
          ))}
        </ol>
      </nav>
    </>
  )
}

export default Breadcrumb
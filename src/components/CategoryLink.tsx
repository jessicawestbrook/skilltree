import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getCachedCategoryPath } from '../utils/categoryPaths'

interface CategoryLinkProps {
  categoryId: string
  children: React.ReactNode
  className?: string
  to?: string // Allow override for custom paths
  onClick?: (e: React.MouseEvent) => void
}

const CategoryLink: React.FC<CategoryLinkProps> = ({ 
  categoryId, 
  children, 
  className,
  to,
  onClick
}) => {
  const [categoryPath, setCategoryPath] = useState<string>('')

  useEffect(() => {
    if (to) {
      // Use provided path
      setCategoryPath(to)
    } else {
      // Build path from category ID
      const buildPath = async () => {
        try {
          const path = await getCachedCategoryPath(categoryId)
          // Ensure path starts with /
          setCategoryPath(path ? `/${path}` : '')
        } catch (error) {
          console.warn('Failed to build category path:', error)
          // No fallback - show as non-clickable
          setCategoryPath('')
        }
      }
      
      buildPath()
    }
  }, [categoryId, to])

  if (!categoryPath) {
    // Show loading state or return the content without link
    return <span className={className}>{children}</span>
  }

  return (
    <Link 
      to={categoryPath} 
      className={className}
      onClick={onClick}
    >
      {children}
    </Link>
  )
}

export default CategoryLink
import { supabase } from '../services/supabase'

interface CategoryNode {
  id: string
  name: string
  parent_id: string | null
}

/**
 * Convert a category name to a URL-safe slug
 */
export function nameToSlug(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '') // Remove special characters except spaces and hyphens
    .replace(/\s+/g, '_') // Replace spaces with underscores
    .replace(/-+/g, '_') // Replace hyphens with underscores
    .replace(/_{2,}/g, '_') // Replace multiple underscores with single
    .replace(/^_|_$/g, '') // Remove leading/trailing underscores
}

/**
 * Convert a URL slug back to a potential category name (for searching)
 */
export function slugToSearchTerms(slug: string): string[] {
  // Create variations to search for
  const baseSlug = slug.replace(/_/g, ' ')
  return [
    baseSlug,
    baseSlug.replace(/\s+/g, ''), // No spaces
    baseSlug.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '), // Title case
    baseSlug.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(''), // Title case no spaces
  ]
}

/**
 * Build the full path for a category by traversing up the hierarchy
 */
export async function buildCategoryPath(categoryId: string): Promise<string> {
  const pathSegments: string[] = []
  let currentId: string | null = categoryId

  // Traverse up the hierarchy to build the path
  while (currentId) {
    const response = await supabase
      .from('skill_tree_nodes')
      .select('id, name, parent_id')
      .eq('id', currentId)
      .limit(1)
    
    const { data: node, error } = response as { data: CategoryNode[] | null, error: any }

    if (error || !node || node.length === 0) {
      break
    }

    const category = node[0]
    
    // Skip the root "Knowledge" node if it exists
    if (category.name !== 'Knowledge' && category.parent_id) {
      pathSegments.unshift(nameToSlug(category.name))
    } else if (!category.parent_id && category.name !== 'Knowledge') {
      // This is a top-level category (not Knowledge), include it
      pathSegments.unshift(nameToSlug(category.name))
    }

    currentId = category.parent_id
  }

  // Return path without leading slash if it's empty, otherwise with slash
  return pathSegments.length > 0 ? pathSegments.join('/') : ''
}

/**
 * Resolve a category path to an ID by traversing down the hierarchy
 */
export async function resolveCategoryPath(path: string): Promise<string | null> {
  // Remove leading slash and split into segments
  const segments = path.replace(/^\/+/, '').split('/').filter(segment => segment.length > 0)
  
  if (segments.length === 0) {
    return null
  }

  // Start from root level (parent_id is null)
  let currentParentId: string | null = null
  
  for (let i = 0; i < segments.length; i++) {
    const segment = segments[i]
    const searchTerms = slugToSearchTerms(segment)
    
    // Search for a node with matching name at this level
    const response = await supabase
      .from('skill_tree_nodes')
      .select('id, name, parent_id')
      .eq('parent_id', currentParentId)
      .in('name', searchTerms)
    
    const { data: nodes, error } = response as { data: CategoryNode[] | null, error: any }
    
    if (error || !nodes || nodes.length === 0) {
      // Try a broader search if exact parent match fails
      const broadResponse = await supabase
        .from('skill_tree_nodes')
        .select('id, name, parent_id')
        .in('name', searchTerms)
      
      const { data: broadNodes, error: broadError } = broadResponse as { data: CategoryNode[] | null, error: any }
      
      if (broadError || !broadNodes || broadNodes.length === 0) {
        return null
      }
      
      // Find the one with the correct parent
      const parentIdToMatch: string | null = currentParentId
      const matchingNode: CategoryNode | undefined = broadNodes.find(node => node.parent_id === parentIdToMatch)
      if (!matchingNode) {
        return null
      }
      
      currentParentId = matchingNode.id
    } else {
      // Found exact match
      currentParentId = nodes[0].id
    }
  }
  
  return currentParentId
}

/**
 * Get breadcrumb trail for a category
 */
export async function getCategoryBreadcrumbs(categoryId: string): Promise<Array<{ name: string, id: string, path: string }>> {
  const breadcrumbs: Array<{ name: string, id: string, path: string }> = []
  let currentId: string | null = categoryId

  // First, collect all ancestors
  const ancestors: CategoryNode[] = []
  while (currentId) {
    const response = await supabase
      .from('skill_tree_nodes')
      .select('id, name, parent_id')
      .eq('id', currentId)
      .limit(1)
    
    const { data: node, error } = response as { data: CategoryNode[] | null, error: any }

    if (error || !node || node.length === 0) {
      break
    }

    const category = node[0]
    
    // Skip the root "Knowledge" node
    if (category.name !== 'Knowledge') {
      ancestors.unshift(category)
    }

    currentId = category.parent_id
  }

  // Build breadcrumbs with cumulative paths
  for (let i = 0; i < ancestors.length; i++) {
    const pathSegments = ancestors.slice(0, i + 1).map(ancestor => nameToSlug(ancestor.name))
    const path = '/' + pathSegments.join('/')
    
    breadcrumbs.push({
      name: ancestors[i].name,
      id: ancestors[i].id,
      path: path
    })
  }

  return breadcrumbs
}

/**
 * Cache for category paths to avoid repeated database calls
 */
const categoryPathCache = new Map<string, string>()

/**
 * Get category path with caching
 */
export async function getCachedCategoryPath(categoryId: string): Promise<string> {
  if (categoryPathCache.has(categoryId)) {
    return categoryPathCache.get(categoryId)!
  }
  
  const path = await buildCategoryPath(categoryId)
  categoryPathCache.set(categoryId, path)
  return path
}
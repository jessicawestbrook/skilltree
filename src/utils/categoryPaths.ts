import { supabase } from '../services/supabase'

interface CategoryNode {
  id: string
  name: string
  parent_id: string | null
}

// Cache for all nodes to avoid repeated database calls
let allNodesCache: CategoryNode[] | null = null
let cacheTimestamp: number = 0
const CACHE_DURATION = 5 * 60 * 1000 // 5 minutes

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
 * Load all nodes into cache if needed
 */
async function ensureNodesCache(): Promise<CategoryNode[]> {
  const now = Date.now()
  
  // Return cached data if still valid
  if (allNodesCache && (now - cacheTimestamp) < CACHE_DURATION) {
    return allNodesCache
  }

  // Fetch all nodes at once (including those with learning content)
  const { data: nodes, error } = await supabase
    .from('skill_tree_nodes')
    .select('id, name, parent_id')
    .limit(10000) // Reasonable limit

  if (error || !nodes) {
    console.error('Error loading category nodes:', error)
    return allNodesCache || []
  }

  allNodesCache = nodes as CategoryNode[]
  cacheTimestamp = now
  return allNodesCache
}

/**
 * Build the full path for a category by traversing up the hierarchy
 */
export async function buildCategoryPath(categoryId: string): Promise<string> {
  const nodes = await ensureNodesCache()
  const nodeMap = new Map(nodes.map(n => [n.id, n]))
  
  const pathSegments: string[] = []
  let currentId: string | null = categoryId

  // Traverse up the hierarchy using cached data
  while (currentId) {
    const category = nodeMap.get(currentId)
    if (!category) break

    // Skip the root "Knowledge" node if it exists
    if (category.name !== 'Knowledge' && category.parent_id) {
      pathSegments.unshift(nameToSlug(category.name))
    } else if (!category.parent_id && category.name !== 'Knowledge') {
      // This is a top-level category (not Knowledge), include it
      pathSegments.unshift(nameToSlug(category.name))
    }

    currentId = category.parent_id
  }

  return pathSegments.length > 0 ? pathSegments.join('/') : ''
}

/**
 * Resolve a category path to an ID by traversing down the hierarchy
 */
export async function resolveCategoryPath(path: string): Promise<string | null> {
  const segments = path.replace(/^\/+/, '').split('/').filter(segment => segment.length > 0)
  
  if (segments.length === 0) {
    return null
  }

  const nodes = await ensureNodesCache()
  
  // Start from root level (parent_id is null)
  let currentParentId: string | null = null
  
  for (const segment of segments) {
    const searchTerms = slugToSearchTerms(segment)
    
    // Find matching node at this level
    // eslint-disable-next-line no-loop-func
    const matchingNode = nodes.find(node => {
      // Handle null parent_id comparison correctly
      const parentMatches = (node.parent_id === currentParentId) || 
                           (node.parent_id == null && currentParentId == null)
      return parentMatches && searchTerms.some(term => node.name === term)
    })
    
    if (!matchingNode) {
      return null
    }
    
    currentParentId = matchingNode.id
  }
  
  return currentParentId
}

/**
 * Get breadcrumb trail for a category
 */
export async function getCategoryBreadcrumbs(categoryId: string): Promise<Array<{ name: string, id: string, path: string }>> {
  const nodes = await ensureNodesCache()
  const nodeMap = new Map(nodes.map(n => [n.id, n]))
  
  const ancestors: CategoryNode[] = []
  let currentId: string | null = categoryId

  // Collect all ancestors using cached data
  while (currentId) {
    const category = nodeMap.get(currentId)
    if (!category) break
    
    // Skip the root "Knowledge" node
    if (category.name !== 'Knowledge') {
      ancestors.unshift(category)
    }

    currentId = category.parent_id
  }

  // Build breadcrumbs with cumulative paths
  const breadcrumbs: Array<{ name: string, id: string, path: string }> = []
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

/**
 * Clear the cache (useful for when data changes)
 */
export function clearCategoryCache(): void {
  allNodesCache = null
  cacheTimestamp = 0
  categoryPathCache.clear()
}
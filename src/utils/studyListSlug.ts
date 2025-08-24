/**
 * Utility functions for handling study list slugs
 */

/**
 * Convert a study list name to a URL-safe slug
 */
export function nameToSlug(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '') // Remove special characters except spaces and hyphens
    .replace(/\s+/g, '-') // Replace spaces with hyphens
    .replace(/-+/g, '-') // Replace multiple hyphens with single
    .replace(/^-|-$/g, '') // Remove leading/trailing hyphens
}

/**
 * Generate a unique slug by appending a number if necessary
 */
export function generateUniqueSlug(name: string, existingSlugs: string[]): string {
  let baseSlug = nameToSlug(name)
  let slug = baseSlug
  let counter = 1
  
  while (existingSlugs.includes(slug)) {
    slug = `${baseSlug}-${counter}`
    counter++
  }
  
  return slug
}

/**
 * Check if a slug is valid
 */
export function isValidSlug(slug: string): boolean {
  return /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)
}
/**
 * Utility functions for vocabulary and spelling bee applications
 */

/**
 * Replaces occurrences of a vocabulary word with blanks in the definition
 * @param definition The definition text
 * @param word The word to replace with blanks
 * @returns The definition with the word replaced by "___"
 */
export const replaceWordWithBlanks = (definition: string, word: string): string => {
  if (!definition || !word) return definition

  // Create a case-insensitive regex that matches the word (with word boundaries)
  // This ensures we match the whole word and not parts of other words
  const wordRegex = new RegExp(`\\b${word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'gi')
  
  // Replace all occurrences with blanks
  return definition.replace(wordRegex, '___')
}

/**
 * Replaces occurrences of a vocabulary word and its variations with blanks
 * @param definition The definition text  
 * @param word The base word to replace
 * @returns The definition with the word and variations replaced by "___"
 */
export const replaceWordAndVariationsWithBlanks = (definition: string, word: string): string => {
  if (!definition || !word) return definition

  let result = definition

  // Replace the base word
  result = replaceWordWithBlanks(result, word)
  
  // Replace common variations
  const variations = [
    word.toLowerCase(),
    word.toUpperCase(), 
    word.charAt(0).toUpperCase() + word.slice(1).toLowerCase(),
    // Add plural form if word doesn't end in s
    word.endsWith('s') ? word : word + 's',
    word.endsWith('s') ? word : word + 'es',
    // Add -ed form for verbs
    word.endsWith('e') ? word + 'd' : word + 'ed',
    // Add -ing form for verbs  
    word.endsWith('e') ? word.slice(0, -1) + 'ing' : word + 'ing',
    // Add -ly form for adverbs
    word.endsWith('e') ? word.slice(0, -1) + 'ly' : word + 'ly',
    word + 'ly'
  ]

  // Remove duplicates and filter out empty strings
  const uniqueVariations = Array.from(new Set(variations)).filter(v => v && v !== word)

  // Replace each variation
  uniqueVariations.forEach(variation => {
    result = replaceWordWithBlanks(result, variation)
  })

  return result
}
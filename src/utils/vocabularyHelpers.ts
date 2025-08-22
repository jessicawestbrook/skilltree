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
    // Plural forms
    word.endsWith('s') ? word : word + 's',
    word.endsWith('s') ? word : word + 'es',
    word.endsWith('y') && !['a','e','i','o','u'].includes(word.charAt(word.length - 2)) ? word.slice(0, -1) + 'ies' : '',
    // Past tense and participle forms
    word.endsWith('e') ? word + 'd' : word + 'ed',
    word.endsWith('y') && !['a','e','i','o','u'].includes(word.charAt(word.length - 2)) ? word.slice(0, -1) + 'ied' : '',
    // Present participle forms
    word.endsWith('e') && word.length > 3 ? word.slice(0, -1) + 'ing' : word + 'ing',
    // Adverb forms
    word.endsWith('e') ? word.slice(0, -1) + 'ly' : word + 'ly',
    word + 'ly',
    word.endsWith('y') && !['a','e','i','o','u'].includes(word.charAt(word.length - 2)) ? word.slice(0, -1) + 'ily' : '',
    // Comparative and superlative forms
    word.endsWith('e') ? word + 'r' : word + 'er',
    word.endsWith('e') ? word + 'st' : word + 'est',
    word.endsWith('y') && !['a','e','i','o','u'].includes(word.charAt(word.length - 2)) ? word.slice(0, -1) + 'ier' : '',
    word.endsWith('y') && !['a','e','i','o','u'].includes(word.charAt(word.length - 2)) ? word.slice(0, -1) + 'iest' : '',
    // Third person singular
    word.endsWith('s') || word.endsWith('sh') || word.endsWith('ch') || word.endsWith('x') || word.endsWith('z') ? word + 'es' : word + 's',
    word.endsWith('y') && !['a','e','i','o','u'].includes(word.charAt(word.length - 2)) ? word.slice(0, -1) + 'ies' : ''
  ]

  // Remove duplicates and filter out empty strings
  const uniqueVariations = Array.from(new Set(variations)).filter(v => v && v !== word)

  // Replace each variation
  uniqueVariations.forEach(variation => {
    result = replaceWordWithBlanks(result, variation)
  })

  return result
}
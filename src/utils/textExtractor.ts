/**
 * Utility functions for extracting clean text from HTML content
 */

/**
 * Extract clean, readable text from HTML content for text-to-speech
 * @param html - HTML content string
 * @param title - Optional title to prepend
 * @returns Clean text suitable for text-to-speech
 */
export function extractTextForSpeech(html: string, title?: string): string {
  // Create a DOM parser
  const parser = new DOMParser()
  const doc = parser.parseFromString(html, 'text/html')
  
  // Remove unwanted elements
  const unwantedElements = doc.querySelectorAll(
    'script, style, noscript, svg, path, img, video, audio, iframe, ' +
    '.no-speech, .skip-speech, [aria-hidden="true"]'
  )
  unwantedElements.forEach(el => el.remove())
  
  // Process special elements that need custom handling
  const codeBlocks = doc.querySelectorAll('pre, code')
  codeBlocks.forEach(el => {
    el.textContent = ' code block '
  })
  
  // Process math elements
  const mathElements = doc.querySelectorAll('.math-equation, .katex, .MathJax')
  mathElements.forEach(el => {
    el.textContent = ' mathematical expression '
  })
  
  // Build the text content with proper structure
  let textContent = title ? `${title}. ` : ''
  
  // Get all content elements in order
  const contentElements = doc.querySelectorAll(
    'h1, h2, h3, h4, h5, h6, p, li, td, th, blockquote, ' +
    '.question-text, .answer-choice, .hint-box, .tip-box, .key-points'
  )
  
  let previousTag = ''
  contentElements.forEach(el => {
    const text = el.textContent?.trim()
    if (!text) return
    
    const tag = el.tagName.toLowerCase()
    
    // Add appropriate pauses and emphasis based on element type
    if (tag.match(/^h[1-6]$/)) {
      // Headers - add longer pause before and after
      textContent += `. ${text}. `
      previousTag = tag
    } else if (tag === 'li') {
      // List items
      const listParent = el.closest('ol, ul')
      const isOrdered = listParent?.tagName === 'OL'
      
      if (isOrdered) {
        // For ordered lists, try to get the item number
        const index = Array.from(listParent?.children || []).indexOf(el as Element) + 1
        textContent += `${index}. ${text}. `
      } else {
        textContent += `${text}. `
      }
      previousTag = tag
    } else if (tag === 'blockquote') {
      // Quotes - add "quote" context
      textContent += `Quote: ${text}. End quote. `
      previousTag = tag
    } else if (el.classList.contains('hint-box') || el.classList.contains('tip-box')) {
      // Special callout boxes
      textContent += `Tip: ${text}. `
      previousTag = 'tip'
    } else if (el.classList.contains('answer-choice')) {
      // Answer choices in quiz
      textContent += `Option: ${text}. `
      previousTag = 'choice'
    } else if (tag === 'p') {
      // Paragraphs - standard pause
      textContent += `${text}. `
      previousTag = tag
    } else if (tag === 'td' || tag === 'th') {
      // Table cells - brief pause
      textContent += `${text}, `
      previousTag = tag
    } else {
      // Default - standard pause
      textContent += `${text}. `
      previousTag = tag
    }
  })
  
  // Clean up the final text
  textContent = textContent
    // Remove multiple spaces
    .replace(/\s+/g, ' ')
    // Remove multiple periods
    .replace(/\.+/g, '.')
    // Remove period comma combinations
    .replace(/\.,/g, ',')
    // Remove comma period combinations
    .replace(/,\./g, '.')
    // Fix spacing around punctuation
    .replace(/\s+([.,!?])/g, '$1')
    .replace(/([.,!?])([A-Za-z])/g, '$1 $2')
    // Remove leading/trailing whitespace
    .trim()
  
  return textContent
}

/**
 * Extract plain text from HTML without speech formatting
 * @param html - HTML content string
 * @returns Plain text content
 */
export function extractPlainText(html: string): string {
  const parser = new DOMParser()
  const doc = parser.parseFromString(html, 'text/html')
  
  // Remove unwanted elements
  const unwantedElements = doc.querySelectorAll('script, style, noscript')
  unwantedElements.forEach(el => el.remove())
  
  return doc.body.textContent?.trim() || ''
}

/**
 * Extract text summary from HTML content
 * @param html - HTML content string
 * @param maxLength - Maximum length of summary
 * @returns Summarized text
 */
export function extractSummary(html: string, maxLength: number = 200): string {
  const plainText = extractPlainText(html)
  
  if (plainText.length <= maxLength) {
    return plainText
  }
  
  // Try to cut at a sentence boundary
  const truncated = plainText.substring(0, maxLength)
  const lastPeriod = truncated.lastIndexOf('.')
  const lastSpace = truncated.lastIndexOf(' ')
  
  if (lastPeriod > maxLength * 0.8) {
    return truncated.substring(0, lastPeriod + 1)
  } else if (lastSpace > 0) {
    return truncated.substring(0, lastSpace) + '...'
  } else {
    return truncated + '...'
  }
}

/**
 * Count words in HTML content
 * @param html - HTML content string
 * @returns Word count
 */
export function countWords(html: string): number {
  const plainText = extractPlainText(html)
  const words = plainText.split(/\s+/).filter(word => word.length > 0)
  return words.length
}

/**
 * Estimate reading time for HTML content
 * @param html - HTML content string
 * @param wordsPerMinute - Reading speed (default 250)
 * @returns Estimated reading time in minutes
 */
export function estimateReadingTime(html: string, wordsPerMinute: number = 250): number {
  const wordCount = countWords(html)
  return Math.ceil(wordCount / wordsPerMinute)
}
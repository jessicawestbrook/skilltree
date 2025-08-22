const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

// Common word endings that suggest combined words
const COMMON_SUFFIXES = [
  'the', 'noun', 'verb', 'adj', 'adverb', 'adjective',
  'ing', 'ed', 'er', 'est', 'ly', 'ness', 'ment', 'tion', 'sion',
  'able', 'ible', 'ful', 'less', 'ward', 'wise'
];

// Non-spelling bee words to exclude
const NON_SPELLING_WORDS = [
  'the', 'a', 'an', 'and', 'or', 'but', 'if', 'then', 'else',
  'this', 'that', 'these', 'those', 'he', 'she', 'it', 'we', 'they',
  'i', 'you', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his',
  'noun', 'verb', 'adjective', 'adverb', 'pronoun', 'preposition',
  'conjunction', 'interjection', 'article', 'determiner'
];

function findWordBoundaries(combinedWord) {
  const word = combinedWord.toLowerCase();
  const possibilities = [];
  
  // Try to find common suffixes
  for (const suffix of COMMON_SUFFIXES) {
    if (word.endsWith(suffix) && word.length > suffix.length + 2) {
      const prefix = word.slice(0, -suffix.length);
      if (prefix.length >= 3) {
        possibilities.push({
          parts: [prefix, suffix],
          confidence: suffix === 'the' || suffix === 'noun' || suffix === 'verb' ? 'high' : 'medium'
        });
      }
    }
  }
  
  // Try to find common prefixes combined with known words
  const knownWords = ['the', 'and', 'with', 'that', 'this', 'from', 'they', 'have', 'been'];
  for (const knownWord of knownWords) {
    const index = word.indexOf(knownWord);
    if (index > 2 && index + knownWord.length === word.length) {
      const prefix = word.slice(0, index);
      possibilities.push({
        parts: [prefix, knownWord],
        confidence: 'high'
      });
    }
  }
  
  // Look for obvious patterns like camelCase or obvious combinations
  const camelCaseMatch = word.match(/^([a-z]+)([A-Z][a-z]+)$/);
  if (camelCaseMatch) {
    possibilities.push({
      parts: [camelCaseMatch[1].toLowerCase(), camelCaseMatch[2].toLowerCase()],
      confidence: 'high'
    });
  }
  
  return possibilities;
}

function isValidSpellingWord(word) {
  const cleanWord = word.toLowerCase().trim();
  
  // Length checks
  if (cleanWord.length < 3) return { valid: false, reason: 'too-short' };
  if (cleanWord.length > 25) return { valid: false, reason: 'too-long' };
  
  // Character checks
  if (/[^a-zA-Z'-]/.test(cleanWord)) return { valid: false, reason: 'invalid-characters' };
  if (/\d/.test(cleanWord)) return { valid: false, reason: 'contains-numbers' };
  
  // Non-spelling bee words
  if (NON_SPELLING_WORDS.includes(cleanWord)) {
    return { valid: false, reason: 'non-spelling-word' };
  }
  
  // Enhanced combined word detection
  const boundaries = findWordBoundaries(cleanWord);
  if (boundaries.some(b => b.confidence === 'high')) {
    return { valid: false, reason: 'combined-word', boundaries: boundaries };
  }
  
  // Additional pattern checks for combined words
  if (isLikelyCombinedWord(cleanWord)) {
    return { valid: false, reason: 'likely-combined-word' };
  }
  
  // Check for proper nouns (shouldn't be in spelling bee typically)
  if (/^[A-Z]/.test(word) && word !== word.toLowerCase()) {
    return { valid: false, reason: 'proper-noun' };
  }
  
  // Check for nonsense/invalid words
  if (isNonsenseWord(cleanWord)) {
    return { valid: false, reason: 'nonsense-word' };
  }
  
  return { valid: true };
}

function isLikelyCombinedWord(word) {
  // Look for patterns that suggest word combination
  
  // Multiple capital letters in middle (camelCase remnants)
  if (/[a-z][A-Z]/.test(word)) return true;
  
  // Very long words that look like combinations
  if (word.length > 18) return true;
  
  // Specific known combined word patterns
  const knownCombinations = [
    'obligeviscount', 'obviouspulse', 'oceaniancharitable', 'sherifftarry',
    'runesancestors', 'ryelanddomesticity', 'nostrilsthe', 'nulliusnoun',
    'ogivalnoun', 'renvoinoun', 'rescissiblejungian', 'reiterateremorseful'
  ];
  
  if (knownCombinations.includes(word)) return true;
  
  // Pattern-based detection for word combinations
  const wordParts = [
    'oblige', 'viscount', 'obvious', 'pulse', 'oceanian', 'charitable',
    'sheriff', 'tarry', 'runes', 'ancestors', 'ryeland', 'domesticity',
    'nostrils', 'nullius', 'noun', 'ogival', 'renvoi', 'rescissible',
    'jungian', 'reiterate', 'remorseful', 'menial', 'aerials', 'reveille',
    'difficulty', 'referral'
  ];
  
  // Check if word contains multiple word parts
  let foundParts = 0;
  for (const part of wordParts) {
    if (word.includes(part)) {
      foundParts++;
      if (foundParts >= 2) return true;
    }
  }
  
  // Words with multiple common endings
  if (word.match(/(ing|ed|er|ly|tion|sion|ness|ment).*?(ing|ed|er|ly|tion|sion|ness|ment)/)) {
    return true;
  }
  
  // Check for unusual consonant/vowel patterns that suggest combination
  if (word.length > 15) {
    // Too many consonants in a row (suggests word boundaries)
    if (/[bcdfghjklmnpqrstvwxyz]{4,}/.test(word)) return true;
    
    // Unusual patterns like multiple common prefixes/suffixes
    if (word.match(/(re|pre|un|dis|over).*(re|pre|un|dis|over)/)) return true;
  }
  
  return false;
}

function isNonsenseWord(word) {
  // Words that are clearly not real words
  const nonsensePatterns = [
    /^shhh+$/,  // Just shushing sounds
    /(.)\1{4,}/, // Same letter repeated 5+ times
    /^[bcdfghjklmnpqrstvwxyz]{8,}$/, // All consonants, too long
    /^[aeiou]{5,}$/ // All vowels, too long
  ];
  
  return nonsensePatterns.some(pattern => pattern.test(word));
}

async function analyzeMalformedWords() {
  try {
    console.log('Analyzing all words missing pronunciations...');
    
    const { data: missingWords, error } = await supabase
      .from('spelling_words')
      .select('id, word, pronunciation_guide')
      .or('pronunciation_guide.is.null,pronunciation_guide.eq.')
      .order('word');
    
    if (error) {
      throw error;
    }
    
    console.log(`\nFound ${missingWords.length} words missing pronunciations`);
    
    const analysis = {
      valid: [],
      invalid: [],
      combinedWords: [],
      separatedWords: []
    };
    
    for (const item of missingWords) {
      const validation = isValidSpellingWord(item.word);
      
      if (validation.valid) {
        analysis.valid.push(item);
      } else {
        analysis.invalid.push({
          ...item,
          reason: validation.reason,
          boundaries: validation.boundaries
        });
        
        // If it's a combined word, try to separate it
        if (validation.reason === 'combined-word' && validation.boundaries) {
          const bestSeparation = validation.boundaries.find(b => b.confidence === 'high') || 
                                validation.boundaries[0];
          
          if (bestSeparation) {
            analysis.combinedWords.push({
              original: item.word,
              parts: bestSeparation.parts,
              confidence: bestSeparation.confidence
            });
            
            // Add valid parts as separated words
            bestSeparation.parts.forEach(part => {
              const partValidation = isValidSpellingWord(part);
              if (partValidation.valid) {
                analysis.separatedWords.push({
                  word: part,
                  originalId: item.id,
                  originalWord: item.word
                });
              }
            });
          }
        }
      }
    }
    
    // Generate report
    console.log('\n=== ANALYSIS RESULTS ===');
    console.log(`Valid spelling words: ${analysis.valid.length}`);
    console.log(`Invalid words: ${analysis.invalid.length}`);
    console.log(`Combined words found: ${analysis.combinedWords.length}`);
    console.log(`Words that can be separated: ${analysis.separatedWords.length}`);
    
    // Show invalid word breakdown
    const invalidReasons = {};
    analysis.invalid.forEach(item => {
      invalidReasons[item.reason] = (invalidReasons[item.reason] || 0) + 1;
    });
    
    console.log('\nInvalid word breakdown:');
    Object.entries(invalidReasons).forEach(([reason, count]) => {
      console.log(`- ${reason}: ${count} words`);
    });
    
    // Show some examples
    console.log('\nExamples of combined words:');
    analysis.combinedWords.slice(0, 10).forEach(item => {
      console.log(`- "${item.original}" → [${item.parts.join('", "')}] (${item.confidence})`);
    });
    
    console.log('\nExamples of words that would be separated:');
    analysis.separatedWords.slice(0, 10).forEach(item => {
      console.log(`- "${item.word}" (from "${item.originalWord}")`);
    });
    
    console.log('\nExamples of invalid words to remove:');
    analysis.invalid.slice(0, 10).forEach(item => {
      console.log(`- "${item.word}" (${item.reason})`);
    });
    
    // Save results
    fs.writeFileSync('scripts/word_analysis_results.json', JSON.stringify(analysis, null, 2));
    console.log('\nFull analysis saved to scripts/word_analysis_results.json');
    
    return analysis;
    
  } catch (error) {
    console.error('Analysis failed:', error);
    return null;
  }
}

async function cleanSpellingWords() {
  try {
    console.log('Starting spelling words cleanup process...');
    
    const analysis = await analyzeMalformedWords();
    if (!analysis) return;
    
    console.log('\n=== CLEANUP ACTIONS ===');
    
    // 1. Remove invalid words (don't delete, just mark them)
    console.log(`\n1. Marking ${analysis.invalid.length} invalid words...`);
    let markedCount = 0;
    
    for (const invalidWord of analysis.invalid) {
      const { error } = await supabase
        .from('spelling_words')
        .update({ 
          pronunciation_guide: `INVALID_${invalidWord.reason.toUpperCase()}`,
          // Keep original data but mark as invalid
        })
        .eq('id', invalidWord.id);
      
      if (!error) {
        markedCount++;
        if (markedCount <= 5) {
          console.log(`   Marked: "${invalidWord.word}" (${invalidWord.reason})`);
        }
      }
    }
    
    console.log(`   Marked ${markedCount}/${analysis.invalid.length} invalid words`);
    
    // 2. Add separated words as new entries
    console.log(`\n2. Adding ${analysis.separatedWords.length} separated words...`);
    let addedCount = 0;
    
    for (const separatedWord of analysis.separatedWords) {
      // Check if word already exists
      const { data: existing, error: checkError } = await supabase
        .from('spelling_words')
        .select('id')
        .eq('word', separatedWord.word)
        .limit(1);
      
      if (checkError) {
        console.log(`Error checking for existing word: ${separatedWord.word}`);
        continue;
      }
      
      if (existing && existing.length > 0) {
        console.log(`   Skipped "${separatedWord.word}" (already exists)`);
        continue;
      }
      
      // Add the separated word
      const { error: insertError } = await supabase
        .from('spelling_words')
        .insert({
          word: separatedWord.word,
          // Set basic fields, pronunciation_guide will be null (to be filled later)
          definition: null,
          example_sentence: null,
          source_difficulty: 'Unknown',
          spelling_difficulty_level: 3,
          spelling_difficulty_name: 'Intermediate',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        });
      
      if (!insertError) {
        addedCount++;
        if (addedCount <= 5) {
          console.log(`   Added: "${separatedWord.word}" (from "${separatedWord.originalWord}")`);
        }
      }
    }
    
    console.log(`   Added ${addedCount}/${analysis.separatedWords.length} separated words`);
    
    console.log('\n=== CLEANUP COMPLETE ===');
    console.log(`- Marked ${markedCount} invalid words`);
    console.log(`- Added ${addedCount} separated words`);
    console.log(`- ${analysis.valid.length} valid words ready for pronunciation generation`);
    
    // Final verification
    const { count: newMissingCount, error: countError } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .is('pronunciation_guide', null);
    
    if (!countError) {
      console.log(`\nNew count of words needing pronunciations: ${newMissingCount}`);
    }
    
  } catch (error) {
    console.error('Cleanup failed:', error);
  }
}

// Export functions
module.exports = {
  analyzeMalformedWords,
  cleanSpellingWords,
  isValidSpellingWord,
  findWordBoundaries
};

// Run if called directly
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.includes('--analyze')) {
    analyzeMalformedWords();
  } else if (args.includes('--clean')) {
    cleanSpellingWords();
  } else {
    console.log('Usage:');
    console.log('  node clean_and_separate_spelling_words.js --analyze');
    console.log('  node clean_and_separate_spelling_words.js --clean');
  }
}
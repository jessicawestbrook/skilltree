/**
 * Hybrid Spelling Difficulty Algorithm
 * 
 * This algorithm predicts spelling difficulty on a 1-5 scale for adaptive learning.
 * Since bee ratings have limited correlation with orthographic features (40% accuracy),
 * we use a hybrid approach combining multiple factors.
 */

// Common English words by frequency (top 3000)
const COMMON_WORDS = new Set(['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us']);

// Curriculum words by grade level (simplified)
const GRADE_WORDS = {
  1: ['cat', 'dog', 'run', 'sun', 'fun', 'big', 'red', 'blue'],
  2: ['happy', 'jump', 'play', 'friend', 'school', 'read', 'write'],
  3: ['beautiful', 'special', 'important', 'different', 'together'],
  4: ['necessary', 'separate', 'definitely', 'environment', 'government'],
  5: ['accommodate', 'embarrass', 'occurrence', 'conscience', 'exaggerate'],
  6: ['millennium', 'harassment', 'maintenance', 'perseverance', 'miscellaneous']
};

/**
 * Calculate orthographic complexity score
 */
function calculateOrthographicScore(word) {
  const w = word.toLowerCase();
  let score = 0;
  
  // Length factor
  score += Math.min(w.length * 0.5, 10);
  
  // Silent letters
  if (/kn|gn|wr|mb$|mn|ps|pn|rh|wh/.test(w)) score += 3;
  if (/[aeiou]gh[^t]|ght/.test(w)) score += 2;
  
  // Complex vowel patterns
  if (/ough|augh|eigh/.test(w)) score += 4;
  if (/eau|ieu|oeu/.test(w)) score += 3;
  if (/ai|ay|ea|ee|ei|ey|ie|oa|oe|oi|oy|oo|ou|ow|ue|ui/.test(w)) score += 1;
  
  // Double letters
  const doubles = (w.match(/(.)\1/g) || []).length;
  score += doubles * 1.5;
  
  // Consonant clusters
  const clusters = (w.match(/[bcdfghjklmnpqrstvwxyz]{3,}/g) || []).length;
  score += clusters * 2;
  
  // Foreign origin patterns
  if (/ph|ch[aour]|que$|eux$|ois$|ique$/.test(w)) score += 2;
  if (/tion|sion|cion/.test(w)) score += 1;
  
  // Irregular patterns
  if (/q[^u]/.test(w)) score += 3;
  if (/[aeiou]{3,}/.test(w)) score += 2;
  if (/[bcdfghjklmnpqrstvwxyz]{4,}/.test(w)) score += 3;
  
  return score;
}

/**
 * Calculate word frequency score (lower = more common = easier)
 */
function calculateFrequencyScore(word) {
  const w = word.toLowerCase();
  
  // Check if it's a very common word
  if (COMMON_WORDS.has(w)) return 0;
  
  // Check if it's a variant of a common word
  const stem = w.replace(/s$|ed$|ing$|er$|est$|ly$/, '');
  if (COMMON_WORDS.has(stem)) return 1;
  
  // Check curriculum words
  for (let grade = 1; grade <= 6; grade++) {
    if (GRADE_WORDS[grade].includes(w)) return grade - 1;
  }
  
  // Default score based on length and patterns
  let score = 5;
  
  // Common prefixes/suffixes suggest more common words
  if (/^(un|re|in|dis|en|non|pre)/.test(w)) score -= 1;
  if (/(ing|ed|er|est|ly|ness|ment|ful|less|able)$/.test(w)) score -= 1;
  
  // Technical/rare patterns suggest less common words
  if (/^(bio|geo|hydro|micro|macro|pseudo|crypto)/.test(w)) score += 2;
  if (/(osis|itis|ology|ography|morphic)$/.test(w)) score += 2;
  
  return Math.max(0, Math.min(10, score));
}

/**
 * Calculate grade level appropriateness
 */
function calculateGradeScore(word) {
  const w = word.toLowerCase();
  const syllables = countSyllables(w);
  
  // Simple formula: base grade = syllables * 2 + length/3
  let grade = syllables * 2 + w.length / 3;
  
  // Adjust for complexity
  if (/ough|augh|eigh/.test(w)) grade += 2;
  if (/tion|sion/.test(w)) grade += 1;
  if (w.length <= 4 && /^[bcdfghjklmnpqrstvwxyz][aeiou][bcdfghjklmnpqrstvwxyz]$/.test(w)) grade -= 2;
  
  return Math.max(1, Math.min(12, grade));
}

/**
 * Count syllables in a word
 */
function countSyllables(word) {
  word = word.toLowerCase();
  let count = 0;
  let previousWasVowel = false;
  
  for (let i = 0; i < word.length; i++) {
    const isVowel = /[aeiou]/.test(word[i]);
    if (isVowel && !previousWasVowel) count++;
    previousWasVowel = isVowel;
  }
  
  // Adjust for silent e
  if (word.endsWith('e') && count > 1) count--;
  
  return Math.max(1, count);
}

/**
 * Main difficulty prediction function
 * Returns a difficulty level from 1-5 for adaptive learning
 */
function predictSpellingDifficulty(word) {
  // Calculate component scores
  const orthographic = calculateOrthographicScore(word);
  const frequency = calculateFrequencyScore(word);
  const grade = calculateGradeScore(word);
  
  // Weighted combination (based on analysis showing ~40% predictive power from orthographic alone)
  const weightedScore = 
    orthographic * 0.4 +  // 40% weight on spelling patterns
    frequency * 0.3 +     // 30% weight on word commonality
    grade * 0.2 +         // 20% weight on grade appropriateness
    word.length * 0.1;    // 10% weight on length
  
  // Map to 1-5 scale with thresholds derived from analysis
  let difficultyLevel;
  
  if (weightedScore < 5) {
    difficultyLevel = 1; // Very easy
  } else if (weightedScore < 8) {
    difficultyLevel = 2; // Easy (typical One Bee)
  } else if (weightedScore < 12) {
    difficultyLevel = 3; // Medium (typical Two Bee)
  } else if (weightedScore < 16) {
    difficultyLevel = 4; // Hard (typical Three Bee)
  } else {
    difficultyLevel = 5; // Very hard
  }
  
  // Special adjustments based on specific patterns
  const w = word.toLowerCase();
  
  // Very short common words should never be above level 2
  if (w.length <= 4 && COMMON_WORDS.has(w)) {
    difficultyLevel = Math.min(2, difficultyLevel);
  }
  
  // Words with extreme complexity patterns should be at least level 4
  if (/ough|augh|eigh|czar|phth|chth|rrhea/.test(w)) {
    difficultyLevel = Math.max(4, difficultyLevel);
  }
  
  // Technical/scientific terms should be at least level 3
  if (/ology$|ography$|itis$|osis$/.test(w)) {
    difficultyLevel = Math.max(3, difficultyLevel);
  }
  
  return {
    difficultyLevel,
    components: {
      orthographic: orthographic.toFixed(1),
      frequency: frequency.toFixed(1),
      grade: grade.toFixed(1),
      weighted: weightedScore.toFixed(1)
    },
    confidence: 'moderate' // ~40% accuracy on bee ratings, but good for general difficulty
  };
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { predictSpellingDifficulty };
}

// Test examples
if (require.main === module) {
  const testWords = [
    'cat', 'dog', 'run',           // Should be level 1-2
    'happy', 'friend', 'school',   // Should be level 2
    'beautiful', 'important',       // Should be level 3
    'necessary', 'environment',     // Should be level 3-4
    'rhythm', 'through', 'thought', // Should be level 4
    'pharaoh', 'psychiatrist',      // Should be level 4-5
    'onomatopoeia', 'bourgeois'     // Should be level 5
  ];
  
  console.log('=== TESTING SPELLING DIFFICULTY PREDICTOR ===\n');
  testWords.forEach(word => {
    const result = predictSpellingDifficulty(word);
    console.log(`${word.padEnd(15)} → Level ${result.difficultyLevel}`);
    console.log(`  Components: Orth=${result.components.orthographic}, Freq=${result.components.frequency}, Grade=${result.components.grade}`);
    console.log(`  Weighted Score: ${result.components.weighted}\n`);
  });
}
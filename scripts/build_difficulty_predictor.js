const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });
const fs = require('fs');

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

// Enhanced feature extraction
function extractFeatures(word) {
  const w = word.toLowerCase();
  
  // Common English phonograms by frequency
  const commonPatterns = ['ing', 'er', 'ed', 'ly', 'es', 'en', 'al', 'le', 'st', 'nd'];
  const rarePatterns = ['ough', 'augh', 'eigh', 'ieux', 'oeuvre', 'czar', 'phth', 'chth', 'rrhea', 'sthm'];
  
  // Spelling bee specific patterns (from actual bee word lists)
  const easyPatterns = ['at', 'an', 'in', 'it', 'on', 'up', 'go', 'no', 'so', 'by', 'my', 'or'];
  const hardPatterns = ['sch', 'tsch', 'tzsch', 'cqu', 'xion', 'cion', 'gion', 'geon', 'gean'];
  
  const features = {
    // Length-based
    length: w.length,
    length_squared: w.length * w.length,
    is_short: w.length <= 5 ? 1 : 0,
    is_medium: w.length >= 6 && w.length <= 9 ? 1 : 0,
    is_long: w.length >= 10 ? 1 : 0,
    
    // Vowel patterns
    vowel_count: (w.match(/[aeiou]/g) || []).length,
    y_as_vowel: (w.match(/[^aeiou]y/g) || []).length,
    vowel_ratio: 0,
    consecutive_vowels: (w.match(/[aeiou]{2,}/g) || []).length,
    consecutive_consonants: (w.match(/[bcdfghjklmnpqrstvwxyz]{3,}/g) || []).length,
    
    // Double letters
    double_letters: (w.match(/(.)\1/g) || []).length,
    double_vowels: (w.match(/([aeiou])\1/g) || []).length,
    double_consonants: (w.match(/([bcdfghjklmnpqrstvwxyz])\1/g) || []).length,
    
    // Silent letter indicators
    ends_with_e: w.endsWith('e') ? 1 : 0,
    has_silent_gh: /[^g]gh[^t]|ght/.test(w) ? 1 : 0,
    has_silent_k: /kn/.test(w) ? 1 : 0,
    has_silent_w: /wr/.test(w) ? 1 : 0,
    has_silent_b: /mb$/.test(w) ? 1 : 0,
    has_silent_l: /[ao]l[kfmv]/.test(w) ? 1 : 0,
    
    // Foreign origin indicators
    has_ph: w.includes('ph') ? 1 : 0,
    has_ch_k_sound: /ch[aour]|cho/.test(w) ? 1 : 0,
    has_que: w.includes('que') ? 1 : 0,
    has_tion: w.includes('tion') ? 1 : 0,
    has_sion: w.includes('sion') ? 1 : 0,
    has_ous: w.endsWith('ous') ? 1 : 0,
    has_eux: w.endsWith('eux') ? 1 : 0,
    has_eau: w.includes('eau') ? 1 : 0,
    
    // Complexity indicators
    common_pattern_count: 0,
    rare_pattern_count: 0,
    easy_pattern_count: 0,
    hard_pattern_count: 0,
    
    // Morphological
    likely_compound: w.length > 8 && /[aeiou][bcdfghjklmnpqrstvwxyz]{2,}[aeiou]/.test(w) ? 1 : 0,
    has_prefix: /^(un|re|in|dis|en|non|pre|anti|de|over|under|out)/.test(w) ? 1 : 0,
    has_suffix: /(tion|sion|ment|ness|ful|less|able|ible|ous|ive|ity|ify)$/.test(w) ? 1 : 0,
    
    // Letter frequency score (common letters = lower score)
    letter_frequency_score: 0,
    
    // Predictability score
    follows_common_rules: 0,
    breaks_common_rules: 0
  };
  
  // Calculate vowel ratio
  features.vowel_ratio = features.vowel_count / w.length;
  
  // Count pattern occurrences
  commonPatterns.forEach(p => {
    if (w.includes(p)) features.common_pattern_count++;
  });
  
  rarePatterns.forEach(p => {
    if (w.includes(p)) features.rare_pattern_count++;
  });
  
  easyPatterns.forEach(p => {
    if (w.includes(p)) features.easy_pattern_count++;
  });
  
  hardPatterns.forEach(p => {
    if (w.includes(p)) features.hard_pattern_count++;
  });
  
  // Calculate letter frequency score (based on English letter frequency)
  const letterFreq = {
    'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7, 's': 6.3,
    'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'c': 2.8, 'u': 2.8, 'm': 2.4,
    'w': 2.4, 'f': 2.2, 'g': 2.0, 'y': 2.0, 'p': 1.9, 'b': 1.5, 'v': 1.0,
    'k': 0.8, 'j': 0.15, 'x': 0.15, 'q': 0.10, 'z': 0.07
  };
  
  for (let char of w) {
    features.letter_frequency_score += (letterFreq[char] || 0.05);
  }
  features.letter_frequency_score /= w.length;
  
  // Check spelling rules
  // Common rules that make words easier
  if (/^[bcdfghjklmnpqrstvwxyz][aeiou][bcdfghjklmnpqrstvwxyz]$/.test(w)) features.follows_common_rules++; // CVC pattern
  if (/ing$/.test(w) && w.length > 4) features.follows_common_rules++;
  if (/ed$/.test(w) && w.length > 3) features.follows_common_rules++;
  
  // Rules that make words harder
  if (/[aeiou]{3,}/.test(w)) features.breaks_common_rules++; // 3+ vowels in a row
  if (/[bcdfghjklmnpqrstvwxyz]{4,}/.test(w)) features.breaks_common_rules++; // 4+ consonants
  if (/q[^u]/.test(w)) features.breaks_common_rules++; // Q not followed by U
  
  return features;
}

// Weighted scoring algorithm based on feature analysis
function calculateDifficultyScore(features) {
  let score = 0;
  
  // Length impact (calibrated from data)
  if (features.length <= 5) score -= 5;
  else if (features.length <= 7) score += 0;
  else if (features.length <= 9) score += 3;
  else score += 5;
  
  // Vowel ratio impact (optimal is around 0.4)
  const vowelDiff = Math.abs(features.vowel_ratio - 0.4);
  score += vowelDiff * 10;
  
  // Pattern-based scoring
  score -= features.common_pattern_count * 2;
  score += features.rare_pattern_count * 8;
  score -= features.easy_pattern_count * 3;
  score += features.hard_pattern_count * 6;
  
  // Silent letters add difficulty
  score += features.has_silent_gh * 4;
  score += features.has_silent_k * 3;
  score += features.has_silent_w * 3;
  score += features.has_silent_b * 3;
  score += features.has_silent_l * 2;
  
  // Foreign origin adds difficulty
  score += features.has_ph * 2;
  score += features.has_ch_k_sound * 3;
  score += features.has_que * 4;
  score += features.has_eux * 5;
  score += features.has_eau * 4;
  
  // Double letters and consecutive patterns
  score += features.double_letters * 1.5;
  score += features.consecutive_consonants * 3;
  
  // Morphological complexity
  score += features.likely_compound * 2;
  
  // Letter frequency (lower = harder)
  score += (7 - features.letter_frequency_score) * 2;
  
  // Rule following/breaking
  score -= features.follows_common_rules * 2;
  score += features.breaks_common_rules * 4;
  
  return score;
}

async function buildPredictor() {
  try {
    console.log('=== BUILDING SPELLING DIFFICULTY PREDICTOR ===\n');
    
    // Get training data
    const { data: words, error } = await supabase
      .from('spelling_words')
      .select('word, source_difficulty')
      .in('source_difficulty', ['One Bee', 'Two Bee', 'Three Bee'])
      .order('word');
    
    if (error) throw error;
    
    console.log(`Training on ${words.length} words...\n`);
    
    // Extract features and calculate scores
    const scoredWords = words.map(w => ({
      word: w.word,
      actual: w.source_difficulty,
      features: extractFeatures(w.word),
      score: 0
    }));
    
    // Calculate scores
    scoredWords.forEach(w => {
      w.score = calculateDifficultyScore(w.features);
    });
    
    // Find optimal thresholds using percentiles
    const beeScores = {
      'One Bee': scoredWords.filter(w => w.actual === 'One Bee').map(w => w.score).sort((a, b) => a - b),
      'Two Bee': scoredWords.filter(w => w.actual === 'Two Bee').map(w => w.score).sort((a, b) => a - b),
      'Three Bee': scoredWords.filter(w => w.actual === 'Three Bee').map(w => w.score).sort((a, b) => a - b)
    };
    
    // Calculate percentiles
    console.log('=== SCORE DISTRIBUTIONS ===\n');
    ['One Bee', 'Two Bee', 'Three Bee'].forEach(bee => {
      const scores = beeScores[bee];
      const percentiles = [10, 25, 50, 75, 90].map(p => ({
        p,
        value: scores[Math.floor(scores.length * p / 100)]
      }));
      
      console.log(`${bee}:`);
      percentiles.forEach(({ p, value }) => {
        console.log(`  ${p}th percentile: ${value.toFixed(1)}`);
      });
      console.log();
    });
    
    // Find optimal thresholds using ROC-like analysis
    const allScores = scoredWords.map(w => w.score).sort((a, b) => a - b);
    let bestThreshold1 = 0, bestThreshold2 = 0, bestAccuracy = 0;
    
    // Grid search for best thresholds
    for (let t1 = allScores[Math.floor(allScores.length * 0.2)]; 
         t1 < allScores[Math.floor(allScores.length * 0.5)]; 
         t1 += 0.5) {
      for (let t2 = allScores[Math.floor(allScores.length * 0.5)]; 
           t2 < allScores[Math.floor(allScores.length * 0.8)]; 
           t2 += 0.5) {
        
        if (t2 <= t1) continue;
        
        let correct = 0;
        scoredWords.forEach(w => {
          let predicted;
          if (w.score < t1) predicted = 'One Bee';
          else if (w.score < t2) predicted = 'Two Bee';
          else predicted = 'Three Bee';
          
          if (predicted === w.actual) correct++;
        });
        
        const accuracy = correct / scoredWords.length;
        if (accuracy > bestAccuracy) {
          bestAccuracy = accuracy;
          bestThreshold1 = t1;
          bestThreshold2 = t2;
        }
      }
    }
    
    console.log('=== OPTIMAL THRESHOLDS ===\n');
    console.log(`Threshold 1 (One/Two Bee): ${bestThreshold1.toFixed(1)}`);
    console.log(`Threshold 2 (Two/Three Bee): ${bestThreshold2.toFixed(1)}`);
    console.log(`Best accuracy: ${(bestAccuracy * 100).toFixed(1)}%\n`);
    
    // Test the model
    console.log('=== TESTING MODEL ===\n');
    
    const confusion = {
      'One Bee': { 'One Bee': 0, 'Two Bee': 0, 'Three Bee': 0 },
      'Two Bee': { 'One Bee': 0, 'Two Bee': 0, 'Three Bee': 0 },
      'Three Bee': { 'One Bee': 0, 'Two Bee': 0, 'Three Bee': 0 }
    };
    
    scoredWords.forEach(w => {
      let predicted;
      if (w.score < bestThreshold1) predicted = 'One Bee';
      else if (w.score < bestThreshold2) predicted = 'Two Bee';
      else predicted = 'Three Bee';
      
      confusion[w.actual][predicted]++;
    });
    
    console.log('Confusion Matrix:');
    console.log('            Predicted:');
    console.log('Actual:     One Bee  Two Bee  Three Bee');
    ['One Bee', 'Two Bee', 'Three Bee'].forEach(actual => {
      const row = `${actual.padEnd(10)} ${confusion[actual]['One Bee'].toString().padStart(7)} ${confusion[actual]['Two Bee'].toString().padStart(8)} ${confusion[actual]['Three Bee'].toString().padStart(10)}`;
      console.log(row);
    });
    
    // Calculate per-class accuracy
    console.log('\nPer-class accuracy:');
    ['One Bee', 'Two Bee', 'Three Bee'].forEach(bee => {
      const total = confusion[bee]['One Bee'] + confusion[bee]['Two Bee'] + confusion[bee]['Three Bee'];
      const correct = confusion[bee][bee];
      console.log(`  ${bee}: ${(correct / total * 100).toFixed(1)}%`);
    });
    
    // Save the model
    const model = {
      threshold1: bestThreshold1,
      threshold2: bestThreshold2,
      accuracy: bestAccuracy,
      algorithm: 'weighted_features_v1',
      features: Object.keys(extractFeatures('test')),
      mapping_to_5_scale: {
        description: 'Maps predicted bee ratings to 1-5 scale for adaptive learning',
        rules: [
          'Score < threshold1 * 0.5 → Level 1 (very easy)',
          'Score < threshold1 → Level 2 (easy/One Bee)',
          'Score < threshold2 → Level 3 (medium/Two Bee)',
          'Score < threshold2 * 1.5 → Level 4 (hard/Three Bee)',
          'Score >= threshold2 * 1.5 → Level 5 (very hard)'
        ]
      }
    };
    
    fs.writeFileSync('spelling_difficulty_model.json', JSON.stringify(model, null, 2));
    console.log('\n✓ Model saved to spelling_difficulty_model.json');
    
    // Generate implementation code
    const implementation = `
// Spelling Difficulty Predictor
// Accuracy: ${(bestAccuracy * 100).toFixed(1)}%

function predictSpellingDifficulty(word) {
  const features = extractFeatures(word);
  const score = calculateDifficultyScore(features);
  
  // Predict bee rating
  let beePrediction;
  if (score < ${bestThreshold1.toFixed(1)}) {
    beePrediction = 'One Bee';
  } else if (score < ${bestThreshold2.toFixed(1)}) {
    beePrediction = 'Two Bee';
  } else {
    beePrediction = 'Three Bee';
  }
  
  // Map to 1-5 scale for adaptive learning
  let difficultyLevel;
  if (score < ${(bestThreshold1 * 0.5).toFixed(1)}) {
    difficultyLevel = 1; // Very easy
  } else if (score < ${bestThreshold1.toFixed(1)}) {
    difficultyLevel = 2; // Easy (One Bee)
  } else if (score < ${bestThreshold2.toFixed(1)}) {
    difficultyLevel = 3; // Medium (Two Bee)
  } else if (score < ${(bestThreshold2 * 1.5).toFixed(1)}) {
    difficultyLevel = 4; // Hard (Three Bee)
  } else {
    difficultyLevel = 5; // Very hard
  }
  
  return {
    score: score,
    beePrediction: beePrediction,
    difficultyLevel: difficultyLevel
  };
}
`;
    
    fs.writeFileSync('spelling_difficulty_predictor.js', implementation);
    console.log('✓ Implementation saved to spelling_difficulty_predictor.js');
    
  } catch (error) {
    console.error('Error:', error);
  }
}

buildPredictor();
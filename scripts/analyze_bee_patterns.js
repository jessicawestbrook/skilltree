const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

// Phonetic patterns and complexity indicators
const PATTERNS = {
  // Silent letters
  silent_patterns: ['kn', 'gn', 'wr', 'mb', 'mn', 'ps', 'pn', 'rh', 'gh', 'wh'],
  
  // Complex vowel patterns
  vowel_digraphs: ['ai', 'ay', 'ea', 'ee', 'ei', 'ey', 'ie', 'oa', 'oe', 'oi', 'oy', 'oo', 'ou', 'ow', 'ue', 'ui'],
  vowel_trigraphs: ['eau', 'igh', 'eigh', 'ough'],
  
  // Complex consonant patterns
  consonant_clusters: ['tch', 'dge', 'ck', 'ph', 'ch', 'sh', 'th', 'wh', 'ng', 'nk'],
  consonant_blends: ['bl', 'br', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'pl', 'pr', 'sc', 'sk', 'sl', 'sm', 'sn', 'sp', 'st', 'sw', 'tr', 'tw', 'scr', 'spl', 'spr', 'str'],
  
  // Foreign origin indicators
  greek_patterns: ['ph', 'ch', 'ps', 'pn', 'rh', 'y'],
  latin_patterns: ['tion', 'sion', 'ture', 'ous', 'ious', 'eous', 'ium', 'ius'],
  french_patterns: ['eau', 'oux', 'eur', 'oir', 'ois', 'aille', 'eille', 'ogne', 'ique'],
  
  // Morphological complexity
  prefixes: ['un', 're', 'in', 'im', 'dis', 'en', 'em', 'non', 'over', 'mis', 'sub', 'pre', 'inter', 'fore', 'de', 'trans', 'super', 'semi', 'anti', 'mid', 'under'],
  suffixes: ['tion', 'sion', 'ment', 'ness', 'ity', 'ous', 'ful', 'less', 'able', 'ible', 'ance', 'ence', 'ive', 'ary', 'ory', 'ism', 'ist', 'ize', 'ise', 'fy'],
  
  // Phonetic irregularities
  irregular_patterns: ['ough', 'augh', 'eigh', 'tion', 'sion', 'cian', 'xion']
};

function analyzeWordFeatures(word) {
  const w = word.toLowerCase();
  const features = {
    length: w.length,
    syllables: countSyllables(w),
    
    // Basic metrics
    vowel_count: (w.match(/[aeiou]/g) || []).length,
    consonant_count: (w.match(/[bcdfghjklmnpqrstvwxyz]/g) || []).length,
    vowel_ratio: 0,
    
    // Pattern counts
    silent_letter_count: 0,
    vowel_digraph_count: 0,
    vowel_trigraph_count: 0,
    consonant_cluster_count: 0,
    consonant_blend_count: 0,
    
    // Origin indicators
    has_greek: false,
    has_latin: false,
    has_french: false,
    
    // Morphological
    prefix_count: 0,
    suffix_count: 0,
    
    // Irregularities
    irregular_count: 0,
    double_letter_count: (w.match(/(.)\1/g) || []).length,
    
    // Special characteristics
    has_apostrophe: w.includes("'") || w.includes("-"),
    starts_with_vowel: /^[aeiou]/.test(w),
    ends_with_e: w.endsWith('e'),
    has_y_as_vowel: /[^aeiou]y[^aeiou]/.test(w) || w.endsWith('y'),
    
    // Phonetic complexity score
    complexity_score: 0
  };
  
  // Calculate vowel ratio
  features.vowel_ratio = features.vowel_count / w.length;
  
  // Count pattern occurrences
  PATTERNS.silent_patterns.forEach(p => {
    if (w.includes(p)) features.silent_letter_count++;
  });
  
  PATTERNS.vowel_digraphs.forEach(p => {
    if (w.includes(p)) features.vowel_digraph_count++;
  });
  
  PATTERNS.vowel_trigraphs.forEach(p => {
    if (w.includes(p)) features.vowel_trigraph_count++;
  });
  
  PATTERNS.consonant_clusters.forEach(p => {
    if (w.includes(p)) features.consonant_cluster_count++;
  });
  
  PATTERNS.consonant_blends.forEach(p => {
    if (w.includes(p)) features.consonant_blend_count++;
  });
  
  // Check origin patterns
  PATTERNS.greek_patterns.forEach(p => {
    if (w.includes(p)) features.has_greek = true;
  });
  
  PATTERNS.latin_patterns.forEach(p => {
    if (w.includes(p)) features.has_latin = true;
  });
  
  PATTERNS.french_patterns.forEach(p => {
    if (w.includes(p)) features.has_french = true;
  });
  
  // Count morphological elements
  PATTERNS.prefixes.forEach(p => {
    if (w.startsWith(p)) features.prefix_count++;
  });
  
  PATTERNS.suffixes.forEach(p => {
    if (w.endsWith(p)) features.suffix_count++;
  });
  
  // Count irregularities
  PATTERNS.irregular_patterns.forEach(p => {
    if (w.includes(p)) features.irregular_count++;
  });
  
  // Calculate complexity score
  features.complexity_score = 
    features.length * 0.5 +
    features.syllables * 2 +
    features.silent_letter_count * 3 +
    features.vowel_trigraph_count * 4 +
    features.irregular_count * 5 +
    features.double_letter_count * 1.5 +
    (features.has_greek ? 3 : 0) +
    (features.has_latin ? 2 : 0) +
    (features.has_french ? 3 : 0) +
    features.prefix_count * 1.5 +
    features.suffix_count * 1.5;
  
  return features;
}

function countSyllables(word) {
  word = word.toLowerCase();
  let count = 0;
  let previousWasVowel = false;
  
  for (let i = 0; i < word.length; i++) {
    const isVowel = /[aeiou]/.test(word[i]);
    if (isVowel && !previousWasVowel) {
      count++;
    }
    previousWasVowel = isVowel;
  }
  
  // Adjust for silent e
  if (word.endsWith('e') && count > 1) {
    count--;
  }
  
  // Ensure at least one syllable
  return Math.max(1, count);
}

async function analyzeBeePatterns() {
  try {
    console.log('=== ANALYZING BEE RATING PATTERNS ===\n');
    
    // Get all words with bee ratings
    const { data: words, error } = await supabase
      .from('spelling_words')
      .select('word, source_difficulty')
      .in('source_difficulty', ['One Bee', 'Two Bee', 'Three Bee'])
      .order('word');
    
    if (error) throw error;
    
    console.log(`Analyzing ${words.length} words with bee ratings...\n`);
    
    // Analyze features by bee rating
    const featuresByBee = {
      'One Bee': [],
      'Two Bee': [],
      'Three Bee': []
    };
    
    words.forEach(w => {
      const features = analyzeWordFeatures(w.word);
      featuresByBee[w.source_difficulty].push(features);
    });
    
    // Calculate average features for each bee rating
    console.log('=== AVERAGE FEATURES BY BEE RATING ===\n');
    
    ['One Bee', 'Two Bee', 'Three Bee'].forEach(bee => {
      const features = featuresByBee[bee];
      const avgFeatures = {};
      
      // Calculate averages
      const featureKeys = Object.keys(features[0]);
      featureKeys.forEach(key => {
        if (typeof features[0][key] === 'number') {
          const sum = features.reduce((acc, f) => acc + f[key], 0);
          avgFeatures[key] = sum / features.length;
        } else if (typeof features[0][key] === 'boolean') {
          const count = features.filter(f => f[key]).length;
          avgFeatures[key] = (count / features.length * 100).toFixed(1) + '%';
        }
      });
      
      console.log(`${bee} (${features.length} words):`);
      console.log(`  Average length: ${avgFeatures.length.toFixed(1)} letters`);
      console.log(`  Average syllables: ${avgFeatures.syllables.toFixed(1)}`);
      console.log(`  Average complexity score: ${avgFeatures.complexity_score.toFixed(1)}`);
      console.log(`  Vowel ratio: ${avgFeatures.vowel_ratio.toFixed(2)}`);
      console.log(`  Silent letters: ${avgFeatures.silent_letter_count.toFixed(2)} per word`);
      console.log(`  Irregular patterns: ${avgFeatures.irregular_count.toFixed(2)} per word`);
      console.log(`  Has Greek origin: ${avgFeatures.has_greek}`);
      console.log(`  Has Latin origin: ${avgFeatures.has_latin}`);
      console.log(`  Has French origin: ${avgFeatures.has_french}`);
      console.log();
    });
    
    // Find discriminating thresholds
    console.log('=== DISCRIMINATING THRESHOLDS ===\n');
    
    // Complexity score distribution
    const complexityScores = {
      'One Bee': featuresByBee['One Bee'].map(f => f.complexity_score).sort((a, b) => a - b),
      'Two Bee': featuresByBee['Two Bee'].map(f => f.complexity_score).sort((a, b) => a - b),
      'Three Bee': featuresByBee['Three Bee'].map(f => f.complexity_score).sort((a, b) => a - b)
    };
    
    ['One Bee', 'Two Bee', 'Three Bee'].forEach(bee => {
      const scores = complexityScores[bee];
      const p25 = scores[Math.floor(scores.length * 0.25)];
      const p50 = scores[Math.floor(scores.length * 0.50)];
      const p75 = scores[Math.floor(scores.length * 0.75)];
      const p90 = scores[Math.floor(scores.length * 0.90)];
      
      console.log(`${bee} Complexity Score Percentiles:`);
      console.log(`  25th: ${p25.toFixed(1)}`);
      console.log(`  50th: ${p50.toFixed(1)} (median)`);
      console.log(`  75th: ${p75.toFixed(1)}`);
      console.log(`  90th: ${p90.toFixed(1)}`);
      console.log();
    });
    
    // Find optimal thresholds
    console.log('=== SUGGESTED THRESHOLDS ===\n');
    
    const oneBeeMedian = complexityScores['One Bee'][Math.floor(complexityScores['One Bee'].length * 0.50)];
    const twoBeeMedian = complexityScores['Two Bee'][Math.floor(complexityScores['Two Bee'].length * 0.50)];
    const threeBeeMedian = complexityScores['Three Bee'][Math.floor(complexityScores['Three Bee'].length * 0.50)];
    
    const threshold1 = (oneBeeMedian + twoBeeMedian) / 2;
    const threshold2 = (twoBeeMedian + threeBeeMedian) / 2;
    
    console.log(`Threshold between One and Two Bee: ${threshold1.toFixed(1)}`);
    console.log(`Threshold between Two and Three Bee: ${threshold2.toFixed(1)}`);
    
    console.log('\nSuggested algorithm:');
    console.log(`  if (complexity_score < ${threshold1.toFixed(1)}) → One Bee`);
    console.log(`  else if (complexity_score < ${threshold2.toFixed(1)}) → Two Bee`);
    console.log(`  else → Three Bee`);
    
    // Test accuracy
    console.log('\n=== TESTING ACCURACY ===\n');
    
    let correct = 0;
    let confusion = {
      'One Bee': { 'One Bee': 0, 'Two Bee': 0, 'Three Bee': 0 },
      'Two Bee': { 'One Bee': 0, 'Two Bee': 0, 'Three Bee': 0 },
      'Three Bee': { 'One Bee': 0, 'Two Bee': 0, 'Three Bee': 0 }
    };
    
    words.forEach(w => {
      const features = analyzeWordFeatures(w.word);
      let predicted;
      
      if (features.complexity_score < threshold1) {
        predicted = 'One Bee';
      } else if (features.complexity_score < threshold2) {
        predicted = 'Two Bee';
      } else {
        predicted = 'Three Bee';
      }
      
      confusion[w.source_difficulty][predicted]++;
      if (predicted === w.source_difficulty) correct++;
    });
    
    const accuracy = (correct / words.length * 100).toFixed(1);
    console.log(`Overall accuracy: ${accuracy}%\n`);
    
    console.log('Confusion Matrix:');
    console.log('            Predicted:');
    console.log('Actual:     One Bee  Two Bee  Three Bee');
    ['One Bee', 'Two Bee', 'Three Bee'].forEach(actual => {
      const row = `${actual.padEnd(10)} ${confusion[actual]['One Bee'].toString().padStart(7)} ${confusion[actual]['Two Bee'].toString().padStart(8)} ${confusion[actual]['Three Bee'].toString().padStart(10)}`;
      console.log(row);
    });
    
  } catch (error) {
    console.error('Error:', error);
  }
}

analyzeBeePatterns();
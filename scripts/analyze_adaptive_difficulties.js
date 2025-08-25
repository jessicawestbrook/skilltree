const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function analyzeAdaptiveDifficulties() {
  try {
    console.log('=== ADAPTIVE LEARNING DIFFICULTY ANALYSIS ===');
    console.log('Analyzing spelling_difficulty_level and vocabulary_difficulty_level (1-5 scales)\n');
    
    // Get all words with their difficulty levels
    const { data: words, error } = await supabase
      .from('spelling_words')
      .select('word, source_difficulty, spelling_difficulty_level, vocabulary_difficulty_level, definition')
      .order('word');
    
    if (error) throw error;
    
    // Analyze spelling_difficulty_level distribution
    console.log('=== SPELLING DIFFICULTY LEVEL (1-5) DISTRIBUTION ===');
    const spellingDist = {};
    const spellingByBee = {
      'One Bee': {},
      'Two Bee': {},
      'Three Bee': {}
    };
    
    words.forEach(w => {
      const level = w.spelling_difficulty_level || 'null';
      spellingDist[level] = (spellingDist[level] || 0) + 1;
      
      // Track by bee rating
      if (w.source_difficulty && !w.source_difficulty.includes(';')) {
        if (!spellingByBee[w.source_difficulty]) {
          spellingByBee[w.source_difficulty] = {};
        }
        spellingByBee[w.source_difficulty][level] = (spellingByBee[w.source_difficulty][level] || 0) + 1;
      }
    });
    
    console.log('\nOverall Spelling Difficulty Distribution:');
    Object.keys(spellingDist).sort().forEach(level => {
      const count = spellingDist[level];
      const pct = (count / words.length * 100).toFixed(1);
      console.log(`  Level ${level}: ${count} words (${pct}%)`);
    });
    
    console.log('\nSpelling Difficulty by Bee Rating:');
    ['One Bee', 'Two Bee', 'Three Bee'].forEach(bee => {
      console.log(`\n${bee}:`);
      const total = Object.values(spellingByBee[bee]).reduce((a, b) => a + b, 0);
      Object.keys(spellingByBee[bee]).sort().forEach(level => {
        const count = spellingByBee[bee][level];
        const pct = (count / total * 100).toFixed(1);
        console.log(`  Level ${level}: ${count} (${pct}%)`);
      });
    });
    
    // Analyze vocabulary_difficulty_level distribution
    console.log('\n=== VOCABULARY DIFFICULTY LEVEL (1-5) DISTRIBUTION ===');
    const vocabDist = {};
    const vocabByBee = {
      'One Bee': {},
      'Two Bee': {},
      'Three Bee': {}
    };
    
    words.forEach(w => {
      const level = w.vocabulary_difficulty_level || 'null';
      vocabDist[level] = (vocabDist[level] || 0) + 1;
      
      // Track by bee rating
      if (w.source_difficulty && !w.source_difficulty.includes(';')) {
        if (!vocabByBee[w.source_difficulty]) {
          vocabByBee[w.source_difficulty] = {};
        }
        vocabByBee[w.source_difficulty][level] = (vocabByBee[w.source_difficulty][level] || 0) + 1;
      }
    });
    
    console.log('\nOverall Vocabulary Difficulty Distribution:');
    Object.keys(vocabDist).sort().forEach(level => {
      const count = vocabDist[level];
      const pct = (count / words.length * 100).toFixed(1);
      console.log(`  Level ${level}: ${count} words (${pct}%)`);
    });
    
    console.log('\nVocabulary Difficulty by Bee Rating:');
    ['One Bee', 'Two Bee', 'Three Bee'].forEach(bee => {
      console.log(`\n${bee}:`);
      const total = Object.values(vocabByBee[bee]).reduce((a, b) => a + b, 0);
      Object.keys(vocabByBee[bee]).sort().forEach(level => {
        const count = vocabByBee[bee][level];
        const pct = (count / total * 100).toFixed(1);
        console.log(`  Level ${level}: ${count} (${pct}%)`);
      });
    });
    
    // Sample words at each level
    console.log('\n=== SAMPLE WORDS BY DIFFICULTY LEVEL ===');
    
    for (let level = 1; level <= 5; level++) {
      console.log(`\n--- SPELLING LEVEL ${level} ---`);
      const spellingSamples = words.filter(w => w.spelling_difficulty_level === level).slice(0, 10);
      
      if (spellingSamples.length === 0) {
        console.log('  No words at this level');
      } else {
        console.log(`  Total: ${words.filter(w => w.spelling_difficulty_level === level).length} words`);
        console.log('  Samples:');
        spellingSamples.forEach(w => {
          const def = w.definition ? w.definition.substring(0, 40) + '...' : 'no def';
          console.log(`    ${w.word.padEnd(15)} (${w.source_difficulty}) - ${def}`);
        });
      }
    }
    
    for (let level = 1; level <= 5; level++) {
      console.log(`\n--- VOCABULARY LEVEL ${level} ---`);
      const vocabSamples = words.filter(w => w.vocabulary_difficulty_level === level).slice(0, 10);
      
      if (vocabSamples.length === 0) {
        console.log('  No words at this level');
      } else {
        console.log(`  Total: ${words.filter(w => w.vocabulary_difficulty_level === level).length} words`);
        console.log('  Samples:');
        vocabSamples.forEach(w => {
          const def = w.definition ? w.definition.substring(0, 40) + '...' : 'no def';
          console.log(`    ${w.word.padEnd(15)} (${w.source_difficulty}) - ${def}`);
        });
      }
    }
    
    // Check for misalignments
    console.log('\n=== ALIGNMENT ANALYSIS ===');
    
    // Expected: One Bee should be levels 1-2, Two Bee 2-3, Three Bee 3-5
    const misaligned = words.filter(w => {
      if (!w.source_difficulty || !w.spelling_difficulty_level) return false;
      
      if (w.source_difficulty === 'One Bee' && w.spelling_difficulty_level > 3) return true;
      if (w.source_difficulty === 'Three Bee' && w.spelling_difficulty_level < 2) return true;
      return false;
    });
    
    console.log(`\nMisaligned words (spelling): ${misaligned.length}`);
    if (misaligned.length > 0) {
      console.log('Examples of misaligned words:');
      misaligned.slice(0, 10).forEach(w => {
        console.log(`  ${w.word}: ${w.source_difficulty} but Level ${w.spelling_difficulty_level}`);
      });
    }
    
    // Calculate average levels by bee rating
    console.log('\n=== AVERAGE DIFFICULTY LEVELS BY BEE RATING ===');
    ['One Bee', 'Two Bee', 'Three Bee'].forEach(bee => {
      const beeWords = words.filter(w => w.source_difficulty === bee);
      const avgSpelling = beeWords
        .filter(w => w.spelling_difficulty_level)
        .reduce((sum, w) => sum + w.spelling_difficulty_level, 0) / 
        beeWords.filter(w => w.spelling_difficulty_level).length;
      const avgVocab = beeWords
        .filter(w => w.vocabulary_difficulty_level)
        .reduce((sum, w) => sum + w.vocabulary_difficulty_level, 0) / 
        beeWords.filter(w => w.vocabulary_difficulty_level).length;
      
      console.log(`\n${bee}:`);
      console.log(`  Average Spelling Level: ${avgSpelling.toFixed(2)}`);
      console.log(`  Average Vocabulary Level: ${avgVocab.toFixed(2)}`);
    });
    
  } catch (error) {
    console.error('Error:', error);
  }
}

analyzeAdaptiveDifficulties();
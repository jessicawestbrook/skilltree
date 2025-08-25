const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function analyzeDifficultyQuality() {
  try {
    console.log('=== DIFFICULTY CATEGORIZATION QUALITY ANALYSIS ===\n');
    
    // Get words with all difficulty metrics
    const { data: words, error } = await supabase
      .from('spelling_words')
      .select('*')
      .order('word');
    
    if (error) throw error;
    
    // Analyze the 7 words at spelling level 2 (should be medium difficulty)
    console.log('=== DEEP DIVE: SPELLING LEVEL 2 WORDS ===');
    console.log('These 7 words are the ONLY ones categorized as Level 2:');
    const level2Words = words.filter(w => w.spelling_difficulty_level === 2);
    level2Words.forEach(w => {
      console.log(`\n${w.word} (${w.source_difficulty}):`);
      console.log(`  Definition: ${w.definition?.substring(0, 60)}...`);
      console.log(`  Length: ${w.word.length} letters`);
      console.log(`  AI Spelling Level: ${w.ai_spelling_difficulty_level}`);
      console.log(`  Vocabulary Level: ${w.vocabulary_difficulty_level}`);
      console.log(`  Grade: ${w.grade_level}`);
    });
    
    // Analyze spelling level 3 words (should be harder)
    console.log('\n=== SPELLING LEVEL 3 ANALYSIS ===');
    const level3Words = words.filter(w => w.spelling_difficulty_level === 3);
    console.log(`Total Level 3 words: ${level3Words.length}`);
    
    // Check bee rating distribution for level 3
    const level3ByBee = {};
    level3Words.forEach(w => {
      const bee = w.source_difficulty || 'null';
      level3ByBee[bee] = (level3ByBee[bee] || 0) + 1;
    });
    console.log('\nBee rating distribution for Level 3:');
    Object.entries(level3ByBee).forEach(([bee, count]) => {
      console.log(`  ${bee}: ${count} words`);
    });
    
    // Sample some level 3 words
    console.log('\nSample Level 3 words:');
    level3Words.slice(0, 10).forEach(w => {
      console.log(`  ${w.word.padEnd(30)} (${w.source_difficulty}) - Length: ${w.word.length}`);
    });
    
    // Find the longest and shortest words at each level
    console.log('\n=== WORD LENGTH ANALYSIS BY SPELLING LEVEL ===');
    for (let level = 1; level <= 3; level++) {
      const levelWords = words.filter(w => w.spelling_difficulty_level === level);
      if (levelWords.length > 0) {
        const lengths = levelWords.map(w => w.word.length);
        const avgLength = (lengths.reduce((a, b) => a + b, 0) / lengths.length).toFixed(1);
        const shortest = Math.min(...lengths);
        const longest = Math.max(...lengths);
        
        console.log(`\nLevel ${level}:`);
        console.log(`  Average length: ${avgLength} letters`);
        console.log(`  Range: ${shortest} - ${longest} letters`);
        
        const shortestWord = levelWords.find(w => w.word.length === shortest);
        const longestWord = levelWords.find(w => w.word.length === longest);
        console.log(`  Shortest: "${shortestWord.word}" (${shortestWord.source_difficulty})`);
        console.log(`  Longest: "${longestWord.word}" (${longestWord.source_difficulty})`);
      }
    }
    
    // Analyze vocabulary difficulty distribution quality
    console.log('\n=== VOCABULARY DIFFICULTY QUALITY CHECK ===');
    
    // Check Level 5 vocabulary words (should be most sophisticated)
    const level5Vocab = words.filter(w => w.vocabulary_difficulty_level === 5);
    console.log(`\nLevel 5 Vocabulary (Highest - ${level5Vocab.length} words):`);
    level5Vocab.forEach(w => {
      console.log(`  ${w.word.padEnd(20)} (${w.source_difficulty}) - ${w.definition?.substring(0, 40)}...`);
    });
    
    // Check for simple words at high vocabulary levels
    console.log('\n=== POTENTIAL MISCATEGORIZATIONS ===');
    
    // Simple words that shouldn't be at high vocabulary levels
    const simpleWords = ['set', 'idea', 'logs', 'ited', 'europe', 'search'];
    console.log('\nSimple words found at various levels:');
    simpleWords.forEach(word => {
      const w = words.find(item => item.word === word);
      if (w) {
        console.log(`  "${word}":`);
        console.log(`    Spelling Level: ${w.spelling_difficulty_level}`);
        console.log(`    Vocabulary Level: ${w.vocabulary_difficulty_level}`);
        console.log(`    Source: ${w.source_difficulty}`);
      }
    });
    
    // Complex words at low levels
    console.log('\nComplex words at Level 1 spelling:');
    const complexAtLevel1 = words.filter(w => 
      w.spelling_difficulty_level === 1 && 
      w.word.length > 15
    ).slice(0, 10);
    
    complexAtLevel1.forEach(w => {
      console.log(`  ${w.word.padEnd(30)} (${w.source_difficulty})`);
    });
    
    // Check correlation between AI and manual spelling difficulty
    console.log('\n=== AI VS MANUAL SPELLING DIFFICULTY CORRELATION ===');
    const correlationMatrix = {};
    words.forEach(w => {
      if (w.spelling_difficulty_level && w.ai_spelling_difficulty_level) {
        const key = `Manual ${w.spelling_difficulty_level} vs AI ${w.ai_spelling_difficulty_level}`;
        correlationMatrix[key] = (correlationMatrix[key] || 0) + 1;
      }
    });
    
    console.log('Correlation counts:');
    Object.entries(correlationMatrix)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .forEach(([combo, count]) => {
        console.log(`  ${combo}: ${count} words`);
      });
    
  } catch (error) {
    console.error('Error:', error);
  }
}

analyzeDifficultyQuality();
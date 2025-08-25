const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function verifyDifficultyFix() {
  try {
    console.log('=== VERIFYING DIFFICULTY LEVEL FIXES ===\n');
    
    // Get all words to analyze
    const { data: words, error } = await supabase
      .from('spelling_words')
      .select('source_difficulty, spelling_difficulty_level, vocabulary_difficulty_level')
      .order('word');
    
    if (error) throw error;
    
    console.log(`Analyzing ${words.length} words...\n`);
    
    // Analyze spelling difficulty distribution
    console.log('=== SPELLING DIFFICULTY LEVEL DISTRIBUTION ===');
    const spellingDist = {};
    let spellingNulls = 0;
    
    words.forEach(w => {
      if (w.spelling_difficulty_level === null) {
        spellingNulls++;
      } else {
        spellingDist[w.spelling_difficulty_level] = (spellingDist[w.spelling_difficulty_level] || 0) + 1;
      }
    });
    
    const totalSpelling = Object.values(spellingDist).reduce((a, b) => a + b, 0);
    
    for (let i = 1; i <= 5; i++) {
      const count = spellingDist[i] || 0;
      const pct = totalSpelling > 0 ? (count / totalSpelling * 100).toFixed(1) : '0.0';
      const bar = '█'.repeat(Math.round(count / 200));
      console.log(`Level ${i}: ${count.toString().padStart(5)} (${pct.padStart(5)}%) ${bar}`);
    }
    console.log(`NULL:     ${spellingNulls.toString().padStart(5)} (${((spellingNulls / words.length) * 100).toFixed(1).padStart(5)}%)`);
    
    // Analyze vocabulary difficulty distribution
    console.log('\n=== VOCABULARY DIFFICULTY LEVEL DISTRIBUTION ===');
    const vocabDist = {};
    let vocabNulls = 0;
    
    words.forEach(w => {
      if (w.vocabulary_difficulty_level === null) {
        vocabNulls++;
      } else {
        vocabDist[w.vocabulary_difficulty_level] = (vocabDist[w.vocabulary_difficulty_level] || 0) + 1;
      }
    });
    
    const totalVocab = Object.values(vocabDist).reduce((a, b) => a + b, 0);
    
    for (let i = 1; i <= 5; i++) {
      const count = vocabDist[i] || 0;
      const pct = totalVocab > 0 ? (count / totalVocab * 100).toFixed(1) : '0.0';
      const bar = '█'.repeat(Math.round(count / 200));
      console.log(`Level ${i}: ${count.toString().padStart(5)} (${pct.padStart(5)}%) ${bar}`);
    }
    console.log(`NULL:     ${vocabNulls.toString().padStart(5)} (${((vocabNulls / words.length) * 100).toFixed(1).padStart(5)}%)`);
    
    // Analyze alignment with bee ratings
    console.log('\n=== SPELLING LEVEL ALIGNMENT WITH BEE RATINGS ===');
    
    const beeRatings = ['One Bee', 'Two Bee', 'Three Bee'];
    beeRatings.forEach(bee => {
      const beeWords = words.filter(w => w.source_difficulty === bee);
      const distribution = {};
      
      beeWords.forEach(w => {
        const level = w.spelling_difficulty_level || 'null';
        distribution[level] = (distribution[level] || 0) + 1;
      });
      
      console.log(`\n${bee} (${beeWords.length} words):`);
      Object.keys(distribution).sort().forEach(level => {
        const count = distribution[level];
        const pct = (count / beeWords.length * 100).toFixed(1);
        const bar = '█'.repeat(Math.round(count / 50));
        console.log(`  Level ${level}: ${count.toString().padStart(5)} (${pct.padStart(5)}%) ${bar}`);
      });
      
      // Calculate average level
      const validWords = beeWords.filter(w => w.spelling_difficulty_level !== null);
      if (validWords.length > 0) {
        const avg = validWords.reduce((sum, w) => sum + w.spelling_difficulty_level, 0) / validWords.length;
        console.log(`  Average: ${avg.toFixed(2)}`);
      }
    });
    
    // Check for expected patterns
    console.log('\n=== QUALITY CHECKS ===');
    
    // Check if One Bee words are mostly in levels 1-2
    const oneBeeWords = words.filter(w => w.source_difficulty === 'One Bee' && w.spelling_difficulty_level !== null);
    const oneBeeInLowLevels = oneBeeWords.filter(w => w.spelling_difficulty_level <= 2).length;
    const oneBeePct = (oneBeeInLowLevels / oneBeeWords.length * 100).toFixed(1);
    console.log(`✓ One Bee words in Levels 1-2: ${oneBeePct}% (should be >60%)`);
    
    // Check if Three Bee words are mostly in levels 4-5
    const threeBeeWords = words.filter(w => w.source_difficulty === 'Three Bee' && w.spelling_difficulty_level !== null);
    const threeBeeInHighLevels = threeBeeWords.filter(w => w.spelling_difficulty_level >= 4).length;
    const threeBeePct = (threeBeeInHighLevels / threeBeeWords.length * 100).toFixed(1);
    console.log(`✓ Three Bee words in Levels 4-5: ${threeBeePct}% (should be >60%)`);
    
    // Check vocabulary distribution balance
    const vocabLevels = Object.values(vocabDist);
    const vocabMin = Math.min(...vocabLevels);
    const vocabMax = Math.max(...vocabLevels);
    const vocabRatio = vocabMax / vocabMin;
    console.log(`✓ Vocabulary level balance ratio: ${vocabRatio.toFixed(1)} (lower is better, <10 is good)`);
    
    // Summary
    console.log('\n=== SUMMARY ===');
    if (oneBeePct > 60 && threeBeePct > 60) {
      console.log('✅ Spelling difficulty alignment looks GOOD!');
    } else {
      console.log('⚠️  Spelling difficulty alignment needs improvement');
    }
    
    if (vocabRatio < 10 && vocabDist[1] > 0) {
      console.log('✅ Vocabulary difficulty distribution looks GOOD!');
    } else {
      console.log('⚠️  Vocabulary difficulty distribution needs improvement');
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
}

verifyDifficultyFix();
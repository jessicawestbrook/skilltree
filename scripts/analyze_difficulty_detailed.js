const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function analyzeDetailedDifficulty() {
  try {
    // Get sample words from each source difficulty level
    const sourceLevels = ['One Bee', 'Two Bee', 'Three Bee'];
    
    for (const level of sourceLevels) {
      console.log(`\n=== ${level.toUpperCase()} WORDS ===`);
      
      const { data: words, error } = await supabase
        .from('spelling_words')
        .select('word, definition, part_of_speech, difficulty, source_difficulty')
        .eq('source_difficulty', level)
        .limit(20);
      
      if (error) throw error;
      
      console.log(`Total ${level} words in database: ${words.length} (showing sample)`);
      console.log('\nSample words:');
      
      words.forEach(w => {
        const def = w.definition ? w.definition.substring(0, 50) + (w.definition.length > 50 ? '...' : '') : 'NO DEF';
        console.log(`  ${w.word.padEnd(20)} | Calc: ${(w.difficulty || 'null').padEnd(10)} | Def: ${def}`);
      });
      
      // Get word length statistics
      const { data: allWords, error: allError } = await supabase
        .from('spelling_words')
        .select('word')
        .eq('source_difficulty', level);
        
      if (!allError && allWords) {
        const lengths = allWords.map(w => w.word.length);
        const avgLength = (lengths.reduce((a,b) => a+b, 0) / lengths.length).toFixed(1);
        const minLength = Math.min(...lengths);
        const maxLength = Math.max(...lengths);
        
        console.log(`\nWord length stats for ${level}:`);
        console.log(`  Average: ${avgLength} letters`);
        console.log(`  Min: ${minLength} letters`);
        console.log(`  Max: ${maxLength} letters`);
      }
    }
    
    // Check for any words with non-null difficulty
    console.log('\n=== CHECKING FOR ANY CALCULATED DIFFICULTIES ===');
    const { data: withDiff, error: diffError } = await supabase
      .from('spelling_words')
      .select('word, difficulty, source_difficulty')
      .not('difficulty', 'is', null)
      .limit(10);
      
    if (diffError) throw diffError;
    
    if (withDiff && withDiff.length > 0) {
      console.log(`Found ${withDiff.length} words with calculated difficulty:`);
      withDiff.forEach(w => {
        console.log(`  ${w.word}: ${w.difficulty} (source: ${w.source_difficulty})`);
      });
    } else {
      console.log('No words have calculated difficulty values!');
      console.log('This means the difficulty field needs to be populated based on some criteria.');
    }
    
    // Check what other fields might be used for difficulty
    console.log('\n=== OTHER DIFFICULTY-RELATED FIELDS ===');
    const { data: sample, error: sampleError } = await supabase
      .from('spelling_words')
      .select('*')
      .limit(1);
      
    if (!sampleError && sample && sample.length > 0) {
      const fields = Object.keys(sample[0]);
      const diffFields = fields.filter(f => 
        f.includes('diff') || f.includes('level') || f.includes('grade') || f.includes('category')
      );
      console.log('Difficulty-related fields in table:');
      diffFields.forEach(f => {
        console.log(`  - ${f}: ${sample[0][f]}`);
      });
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
}

analyzeDetailedDifficulty();
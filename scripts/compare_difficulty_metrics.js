const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function compareDifficultyMetrics() {
  try {
    console.log('=== COMPARING DIFFICULTY METRICS ===\n');
    
    // Get all words with their difficulty metrics
    const { data: words, error } = await supabase
      .from('spelling_words')
      .select(`
        word,
        source_difficulty,
        spelling_difficulty_level,
        ai_spelling_difficulty_level,
        ai_spelling_difficulty_name,
        vocabulary_difficulty_level,
        grade_level
      `)
      .order('word');
    
    if (error) throw error;
    
    // Analyze correlations between source_difficulty and AI difficulty
    const correlations = {
      'One Bee': { spelling_levels: {}, ai_levels: {}, vocab_levels: {}, grades: {} },
      'Two Bee': { spelling_levels: {}, ai_levels: {}, vocab_levels: {}, grades: {} },
      'Three Bee': { spelling_levels: {}, ai_levels: {}, vocab_levels: {}, grades: {} }
    };
    
    words.forEach(w => {
      const source = w.source_difficulty;
      if (source && correlations[source]) {
        // Track spelling difficulty level distribution
        const spellLevel = w.spelling_difficulty_level || 'null';
        correlations[source].spelling_levels[spellLevel] = (correlations[source].spelling_levels[spellLevel] || 0) + 1;
        
        // Track AI spelling difficulty level distribution
        const aiLevel = w.ai_spelling_difficulty_level || 'null';
        correlations[source].ai_levels[aiLevel] = (correlations[source].ai_levels[aiLevel] || 0) + 1;
        
        // Track vocabulary difficulty level distribution
        const vocabLevel = w.vocabulary_difficulty_level || 'null';
        correlations[source].vocab_levels[vocabLevel] = (correlations[source].vocab_levels[vocabLevel] || 0) + 1;
        
        // Track grade level distribution
        const grade = w.grade_level || 'null';
        correlations[source].grades[grade] = (correlations[source].grades[grade] || 0) + 1;
      }
    });
    
    // Print correlation analysis
    ['One Bee', 'Two Bee', 'Three Bee'].forEach(source => {
      console.log(`\n=== ${source.toUpperCase()} CORRELATIONS ===`);
      
      console.log('\nSpelling Difficulty Levels:');
      Object.entries(correlations[source].spelling_levels)
        .sort((a, b) => b[1] - a[1])
        .forEach(([level, count]) => {
          const pct = ((count / Object.values(correlations[source].spelling_levels).reduce((a,b) => a+b, 0)) * 100).toFixed(1);
          console.log(`  Level ${level}: ${count} words (${pct}%)`);
        });
      
      console.log('\nAI Spelling Difficulty Levels:');
      Object.entries(correlations[source].ai_levels)
        .sort((a, b) => b[1] - a[1])
        .forEach(([level, count]) => {
          const pct = ((count / Object.values(correlations[source].ai_levels).reduce((a,b) => a+b, 0)) * 100).toFixed(1);
          console.log(`  Level ${level}: ${count} words (${pct}%)`);
        });
      
      console.log('\nVocabulary Difficulty Levels:');
      Object.entries(correlations[source].vocab_levels)
        .sort((a, b) => b[1] - a[1])
        .forEach(([level, count]) => {
          const pct = ((count / Object.values(correlations[source].vocab_levels).reduce((a,b) => a+b, 0)) * 100).toFixed(1);
          console.log(`  Level ${level}: ${count} words (${pct}%)`);
        });
      
      console.log('\nGrade Levels:');
      Object.entries(correlations[source].grades)
        .sort((a, b) => {
          if (a[0] === 'null') return 1;
          if (b[0] === 'null') return -1;
          return parseInt(a[0]) - parseInt(b[0]);
        })
        .forEach(([grade, count]) => {
          const pct = ((count / Object.values(correlations[source].grades).reduce((a,b) => a+b, 0)) * 100).toFixed(1);
          console.log(`  Grade ${grade}: ${count} words (${pct}%)`);
        });
    });
    
    // Find anomalies - words that don't match expected patterns
    console.log('\n=== POTENTIAL ANOMALIES ===');
    console.log('Words where AI difficulty seems misaligned with source difficulty:\n');
    
    const anomalies = words.filter(w => {
      if (!w.source_difficulty || !w.ai_spelling_difficulty_level) return false;
      
      // One Bee should generally be level 1-2
      if (w.source_difficulty === 'One Bee' && w.ai_spelling_difficulty_level > 3) return true;
      // Three Bee should generally be level 3-5
      if (w.source_difficulty === 'Three Bee' && w.ai_spelling_difficulty_level < 2) return true;
      
      return false;
    });
    
    console.log(`Found ${anomalies.length} potential anomalies:`);
    anomalies.slice(0, 20).forEach(w => {
      console.log(`  ${w.word}: ${w.source_difficulty} but AI Level ${w.ai_spelling_difficulty_level}`);
    });
    
    // Check for words with combined source difficulties
    const combined = words.filter(w => 
      w.source_difficulty && w.source_difficulty.includes(';')
    );
    
    console.log(`\n=== COMBINED SOURCE DIFFICULTIES ===`);
    console.log(`Found ${combined.length} words with multiple bee ratings:`);
    combined.slice(0, 10).forEach(w => {
      console.log(`  ${w.word}: ${w.source_difficulty}`);
    });
    
  } catch (error) {
    console.error('Error:', error);
  }
}

compareDifficultyMetrics();
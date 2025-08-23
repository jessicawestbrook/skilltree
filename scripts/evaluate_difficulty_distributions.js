const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

async function evaluateDifficultyDistributions() {
  console.log('=== DIFFICULTY DISTRIBUTION EVALUATION ===\n');

  try {
    // Get total word count
    const { count: totalWords } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true });
    
    console.log(`Total words in database: ${totalWords}\n`);

    // 1. SPELLING DIFFICULTY ANALYSIS
    console.log('=== SPELLING DIFFICULTY ANALYSIS ===\n');
    
    const spellingDistribution = {};
    const spellingStats = {};
    
    for (let level = 1; level <= 5; level++) {
      const { data: levelWords, error } = await supabase
        .from('spelling_words')
        .select('word, definition, spelling_difficulty_level, spelling_difficulty_name, phonetic_transparency_score, word_frequency_score, morphology_score, etymology_score, source_difficulties')
        .eq('spelling_difficulty_level', level)
        .order('word');

      if (error) {
        console.error(`Error fetching spelling level ${level}:`, error);
        continue;
      }

      const count = levelWords?.length || 0;
      const percentage = ((count / totalWords) * 100).toFixed(1);
      
      spellingDistribution[level] = {
        count,
        percentage,
        name: levelWords?.[0]?.spelling_difficulty_name || `Level ${level}`,
        words: levelWords || []
      };

      // Calculate statistics for this level
      const scores = levelWords?.filter(w => w.phonetic_transparency_score !== null) || [];
      if (scores.length > 0) {
        spellingStats[level] = {
          avgPhoneticTransparency: (scores.reduce((sum, w) => sum + (w.phonetic_transparency_score || 0), 0) / scores.length).toFixed(1),
          avgWordFrequency: (scores.reduce((sum, w) => sum + (w.word_frequency_score || 0), 0) / scores.length).toFixed(1),
          avgMorphology: (scores.reduce((sum, w) => sum + (w.morphology_score || 0), 0) / scores.length).toFixed(1),
          avgEtymology: (scores.reduce((sum, w) => sum + (w.etymology_score || 0), 0) / scores.length).toFixed(1)
        };
      }
    }

    // Print spelling distribution
    console.log('SPELLING DIFFICULTY DISTRIBUTION:');
    for (let level = 1; level <= 5; level++) {
      const data = spellingDistribution[level];
      console.log(`${level}. ${data.name}: ${data.count} words (${data.percentage}%)`);
    }

    // Print spelling statistics
    console.log('\nSPELLING COMPONENT SCORES BY LEVEL:');
    console.log('Level | Phonetic | Frequency | Morphology | Etymology');
    console.log('------|----------|-----------|------------|----------');
    for (let level = 1; level <= 5; level++) {
      const stats = spellingStats[level];
      if (stats) {
        const name = spellingDistribution[level].name.substring(0, 3);
        console.log(`${name}   |   ${stats.avgPhoneticTransparency.padStart(6)} |    ${stats.avgWordFrequency.padStart(6)} |     ${stats.avgMorphology.padStart(6)} |   ${stats.avgEtymology.padStart(6)}`);
      }
    }

    // Show sample words for each spelling level
    console.log('\nSPELLING SAMPLE WORDS BY LEVEL:');
    for (let level = 1; level <= 5; level++) {
      const data = spellingDistribution[level];
      console.log(`\n${level}. ${data.name} (${data.count} words):`);
      
      if (data.words.length > 0) {
        // Show first 10 words and a few random ones
        const samples = data.words.slice(0, 10);
        if (data.words.length > 10) {
          // Add some random samples
          const remaining = data.words.slice(10);
          const randomSamples = [];
          for (let i = 0; i < Math.min(5, remaining.length); i++) {
            const randomIndex = Math.floor(Math.random() * remaining.length);
            randomSamples.push(remaining[randomIndex]);
            remaining.splice(randomIndex, 1);
          }
          samples.push(...randomSamples);
        }
        
        samples.forEach(word => {
          const def = word.definition ? word.definition.substring(0, 60) + '...' : 'No definition';
          const source = word.source_difficulties ? `[${word.source_difficulties.join(', ')}]` : '';
          console.log(`  • ${word.word}: ${def} ${source}`);
        });
        
        if (data.words.length > 15) {
          console.log(`  ... and ${data.words.length - 15} more words`);
        }
      }
    }

    // 2. VOCABULARY DIFFICULTY ANALYSIS
    console.log('\n\n=== VOCABULARY DIFFICULTY ANALYSIS ===\n');
    
    const vocabularyDistribution = {};
    const vocabularyStats = {};
    
    for (let level = 1; level <= 5; level++) {
      const { data: levelWords, error } = await supabase
        .from('spelling_words')
        .select('word, definition, vocabulary_difficulty_level, vocabulary_difficulty_name, vocabulary_semantic_complexity_score, vocabulary_contextual_frequency_score, vocabulary_conceptual_sophistication_score, vocabulary_register_specificity_score')
        .eq('vocabulary_difficulty_level', level)
        .order('word');

      if (error) {
        console.error(`Error fetching vocabulary level ${level}:`, error);
        continue;
      }

      const count = levelWords?.length || 0;
      const percentage = ((count / totalWords) * 100).toFixed(1);
      
      vocabularyDistribution[level] = {
        count,
        percentage,
        name: levelWords?.[0]?.vocabulary_difficulty_name || `Level ${level}`,
        words: levelWords || []
      };

      // Calculate statistics for this level
      const scores = levelWords?.filter(w => w.vocabulary_semantic_complexity_score !== null) || [];
      if (scores.length > 0) {
        vocabularyStats[level] = {
          avgSemanticComplexity: (scores.reduce((sum, w) => sum + (w.vocabulary_semantic_complexity_score || 0), 0) / scores.length).toFixed(1),
          avgContextualFrequency: (scores.reduce((sum, w) => sum + (w.vocabulary_contextual_frequency_score || 0), 0) / scores.length).toFixed(1),
          avgConceptualSophistication: (scores.reduce((sum, w) => sum + (w.vocabulary_conceptual_sophistication_score || 0), 0) / scores.length).toFixed(1),
          avgRegisterSpecificity: (scores.reduce((sum, w) => sum + (w.vocabulary_register_specificity_score || 0), 0) / scores.length).toFixed(1)
        };
      }
    }

    // Print vocabulary distribution
    console.log('VOCABULARY DIFFICULTY DISTRIBUTION:');
    for (let level = 1; level <= 5; level++) {
      const data = vocabularyDistribution[level];
      console.log(`${level}. ${data.name}: ${data.count} words (${data.percentage}%)`);
    }

    // Print vocabulary statistics
    console.log('\nVOCABULARY COMPONENT SCORES BY LEVEL:');
    console.log('Level | Semantic | Frequency | Sophisticat | Register');
    console.log('------|----------|-----------|-------------|----------');
    for (let level = 1; level <= 5; level++) {
      const stats = vocabularyStats[level];
      if (stats) {
        const name = vocabularyDistribution[level].name.substring(0, 3);
        console.log(`${name}   |   ${stats.avgSemanticComplexity.padStart(6)} |    ${stats.avgContextualFrequency.padStart(6)} |      ${stats.avgConceptualSophistication.padStart(6)} |   ${stats.avgRegisterSpecificity.padStart(6)}`);
      }
    }

    // Show sample words for each vocabulary level
    console.log('\nVOCABULARY SAMPLE WORDS BY LEVEL:');
    for (let level = 1; level <= 5; level++) {
      const data = vocabularyDistribution[level];
      console.log(`\n${level}. ${data.name} (${data.count} words):`);
      
      if (data.words.length > 0) {
        // Show first 10 words and a few random ones
        const samples = data.words.slice(0, 10);
        if (data.words.length > 10) {
          // Add some random samples
          const remaining = data.words.slice(10);
          const randomSamples = [];
          for (let i = 0; i < Math.min(5, remaining.length); i++) {
            const randomIndex = Math.floor(Math.random() * remaining.length);
            randomSamples.push(remaining[randomIndex]);
            remaining.splice(randomIndex, 1);
          }
          samples.push(...randomSamples);
        }
        
        samples.forEach(word => {
          const def = word.definition ? word.definition.substring(0, 60) + '...' : 'No definition';
          console.log(`  • ${word.word}: ${def}`);
        });
        
        if (data.words.length > 15) {
          console.log(`  ... and ${data.words.length - 15} more words`);
        }
      }
    }

    // 3. CROSS-ANALYSIS: Words with mismatched spelling vs vocabulary difficulty
    console.log('\n\n=== CROSS-ANALYSIS: SPELLING vs VOCABULARY DIFFICULTY ===\n');

    const { data: allWords, error: allWordsError } = await supabase
      .from('spelling_words')
      .select('word, definition, spelling_difficulty_level, vocabulary_difficulty_level, spelling_difficulty_name, vocabulary_difficulty_name')
      .not('spelling_difficulty_level', 'is', null)
      .not('vocabulary_difficulty_level', 'is', null);

    if (allWordsError) {
      console.error('Error fetching all words:', allWordsError);
    } else {
      // Find words with big differences between spelling and vocabulary difficulty
      const mismatched = allWords.filter(word => 
        Math.abs(word.spelling_difficulty_level - word.vocabulary_difficulty_level) >= 3
      );

      console.log(`LARGE MISMATCHES (3+ level difference): ${mismatched.length} words`);
      
      // Show most extreme examples
      const sortedMismatches = mismatched.sort((a, b) => 
        Math.abs(b.spelling_difficulty_level - b.vocabulary_difficulty_level) - 
        Math.abs(a.spelling_difficulty_level - a.vocabulary_difficulty_level)
      );

      console.log('\nMost extreme examples:');
      sortedMismatches.slice(0, 15).forEach(word => {
        const diff = word.spelling_difficulty_level - word.vocabulary_difficulty_level;
        const diffStr = diff > 0 ? `+${diff}` : `${diff}`;
        console.log(`  • ${word.word}: Spelling(${word.spelling_difficulty_name}) vs Vocab(${word.vocabulary_difficulty_name}) [${diffStr}]`);
        if (word.definition) {
          console.log(`    ${word.definition.substring(0, 80)}...`);
        }
      });

      // Create distribution matrix
      console.log('\nSPELLING vs VOCABULARY DISTRIBUTION MATRIX:');
      console.log('     | Found | Acad  | Soph  | Spec  | Schol |');
      console.log('-----|-------|-------|-------|-------|-------|');
      
      const spellingLevels = ['Beginner', 'Elementary', 'Intermediate', 'Advanced', 'Expert'];
      
      for (let s = 1; s <= 5; s++) {
        const rowName = spellingLevels[s-1].substring(0, 4);
        let row = `${rowName} |`;
        
        for (let v = 1; v <= 5; v++) {
          const count = allWords.filter(w => 
            w.spelling_difficulty_level === s && w.vocabulary_difficulty_level === v
          ).length;
          row += ` ${count.toString().padStart(5)} |`;
        }
        
        console.log(row);
      }
    }

    // 4. ANALYSIS SUMMARY
    console.log('\n\n=== ANALYSIS SUMMARY ===\n');

    // Expected vs actual distributions
    console.log('DISTRIBUTION EXPECTATIONS vs REALITY:');
    console.log('Expected: Bell curve with most words in middle levels (2-4)');
    console.log('Reality:');
    console.log('  Spelling: Heavy concentration in lower levels, especially Beginner');
    console.log('  Vocabulary: Heavy concentration in Sophisticated level');

    // Identify potential issues
    const issues = [];
    
    if (spellingDistribution[1].percentage > 40) {
      issues.push('🔴 Too many words classified as Beginner spelling difficulty');
    }
    
    if (vocabularyDistribution[3].percentage > 60) {
      issues.push('🔴 Too many words classified as Sophisticated vocabulary');
    }
    
    if (spellingDistribution[5].count < 50) {
      issues.push('🟡 Very few Expert-level spelling words');
    }
    
    if (vocabularyDistribution[1].count < 100) {
      issues.push('🟡 Very few Foundation-level vocabulary words');
    }

    console.log('\nPOTENTIAL ISSUES IDENTIFIED:');
    if (issues.length === 0) {
      console.log('✅ No major distribution issues found');
    } else {
      issues.forEach(issue => console.log(issue));
    }

    console.log('\n✅ Analysis complete!');

  } catch (error) {
    console.error('Analysis failed:', error);
  }
}

if (require.main === module) {
  evaluateDifficultyDistributions();
}
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Vocabulary difficulty levels based on THEORETICAL_FOUNDATIONS.md
const VOCABULARY_LEVELS = {
  1: { name: 'Foundation', description: 'Basic everyday concepts' },
  2: { name: 'Academic', description: 'School-level vocabulary' },
  3: { name: 'Sophisticated', description: 'Advanced academic and professional' },
  4: { name: 'Specialized', description: 'Domain-specific terminology' },
  5: { name: 'Scholarly', description: 'Research and expert-level' }
};

// Vocabulary difficulty assessment based on the framework
function assessSemanticComplexity(word, definition) {
  let score = 50; // Base score
  
  if (!definition) return score;
  
  const def = definition.toLowerCase();
  const defLength = definition.length;
  
  // Definition length indicates complexity
  if (defLength < 50) score -= 20; // Simple, concrete concepts
  else if (defLength > 200) score += 30; // Complex, abstract concepts
  else if (defLength > 100) score += 15; // Moderate complexity
  
  // Abstract vs concrete indicators
  const abstractIndicators = [
    'concept', 'theory', 'principle', 'philosophy', 'ideology', 'paradigm',
    'methodology', 'framework', 'approach', 'perspective', 'viewpoint',
    'belief', 'idea', 'notion', 'understanding', 'interpretation'
  ];
  
  const concreteIndicators = [
    'object', 'thing', 'item', 'tool', 'device', 'building', 'place',
    'animal', 'plant', 'food', 'color', 'shape', 'size', 'made of',
    'physical', 'visible', 'tangible'
  ];
  
  const abstractCount = abstractIndicators.filter(indicator => def.includes(indicator)).length;
  const concreteCount = concreteIndicators.filter(indicator => def.includes(indicator)).length;
  
  score += abstractCount * 10;
  score -= concreteCount * 8;
  
  // Technical/professional language indicators
  const technicalIndicators = [
    'scientific', 'medical', 'legal', 'technical', 'professional',
    'specialized', 'academic', 'research', 'analysis', 'methodology'
  ];
  
  const technicalCount = technicalIndicators.filter(indicator => def.includes(indicator)).length;
  score += technicalCount * 15;
  
  return Math.max(0, Math.min(100, score));
}

function getContextualFrequency(word, definition, sourcedifficulty) {
  let score = 50; // Base score
  
  // Source difficulty provides frequency hints
  if (sourcedifficulty) {
    if (sourcedifficulty.includes('One Bee')) score += 25; // Common words
    else if (sourcedifficulty.includes('Two Bee')) score += 10; // Moderately common
    else if (sourcedifficulty.includes('Three Bee')) score -= 15; // Less common
  }
  
  // Word length as frequency indicator
  const wordLength = word.length;
  if (wordLength <= 4) score += 20; // Very common short words
  else if (wordLength <= 6) score += 10; // Common medium words
  else if (wordLength >= 10) score -= 15; // Uncommon long words
  else if (wordLength >= 13) score -= 25; // Rare very long words
  
  // Definition complexity as frequency indicator
  if (definition) {
    const defLength = definition.length;
    if (defLength < 50) score += 15; // Simple concepts are usually common
    else if (defLength > 150) score -= 20; // Complex definitions indicate rare words
    
    // Formal/academic language in definition
    const formalIndicators = [
      'refers to', 'characterized by', 'denotes', 'encompasses',
      'pertains to', 'constitutes', 'signifies', 'exemplifies'
    ];
    
    const formalCount = formalIndicators.filter(indicator => 
      definition.toLowerCase().includes(indicator)
    ).length;
    score -= formalCount * 10; // Formal definitions indicate less common words
  }
  
  return Math.max(0, Math.min(100, score));
}

function assessConceptualSophistication(word, definition) {
  let score = 30; // Base score
  
  if (!definition) return score;
  
  const def = definition.toLowerCase();
  
  // Cognitive complexity indicators
  const basicCognition = ['is a', 'simple', 'basic', 'common', 'everyday'];
  const analyticalThinking = ['analysis', 'compare', 'contrast', 'cause', 'effect', 'reason'];
  const synthesis = ['combination', 'synthesis', 'integration', 'relationship', 'connection'];
  const evaluation = ['evaluate', 'assess', 'judge', 'critique', 'analyze', 'determine'];
  const creation = ['theory', 'model', 'framework', 'hypothesis', 'innovation', 'creation'];
  
  const basicCount = basicCognition.filter(indicator => def.includes(indicator)).length;
  const analyticalCount = analyticalThinking.filter(indicator => def.includes(indicator)).length;
  const synthesisCount = synthesis.filter(indicator => def.includes(indicator)).length;
  const evaluationCount = evaluation.filter(indicator => def.includes(indicator)).length;
  const creationCount = creation.filter(indicator => def.includes(indicator)).length;
  
  score -= basicCount * 10;
  score += analyticalCount * 10;
  score += synthesisCount * 15;
  score += evaluationCount * 20;
  score += creationCount * 25;
  
  // Interdisciplinary indicators
  const interdisciplinaryIndicators = [
    'philosophy', 'psychology', 'sociology', 'anthropology', 'economics',
    'political', 'scientific', 'mathematical', 'linguistic', 'cultural'
  ];
  
  const interdisciplinaryCount = interdisciplinaryIndicators.filter(indicator => 
    def.includes(indicator)
  ).length;
  score += interdisciplinaryCount * 12;
  
  return Math.max(0, Math.min(100, score));
}

function assessRegisterSpecificity(word, definition) {
  let score = 30; // Base score
  
  if (!definition) return score;
  
  const def = definition.toLowerCase();
  
  // Domain-specific indicators
  const domains = {
    medical: ['medical', 'anatomy', 'disease', 'symptom', 'treatment', 'clinical', 'diagnostic'],
    legal: ['legal', 'law', 'court', 'justice', 'attorney', 'litigation', 'judicial'],
    scientific: ['scientific', 'research', 'experiment', 'hypothesis', 'theory', 'empirical'],
    technical: ['technical', 'engineering', 'computer', 'technology', 'digital', 'mechanical'],
    academic: ['academic', 'education', 'pedagogical', 'curriculum', 'scholarly', 'intellectual'],
    business: ['business', 'economic', 'financial', 'commercial', 'marketing', 'corporate'],
    artistic: ['artistic', 'aesthetic', 'creative', 'cultural', 'literary', 'musical']
  };
  
  let domainCount = 0;
  let totalMatches = 0;
  
  Object.values(domains).forEach(domainWords => {
    const matches = domainWords.filter(term => def.includes(term)).length;
    if (matches > 0) {
      domainCount++;
      totalMatches += matches;
    }
  });
  
  if (domainCount === 0) score -= 10; // Universal terms
  else if (domainCount === 1) score += totalMatches * 15; // Field-specific
  else if (domainCount === 2) score += totalMatches * 8; // Cross-disciplinary
  else score += totalMatches * 5; // Multiple domains (more general)
  
  // Technical jargon indicators
  const jargonIndicators = [
    'terminology', 'specialized', 'technical term', 'professional',
    'expert', 'advanced', 'complex', 'sophisticated'
  ];
  
  const jargonCount = jargonIndicators.filter(indicator => def.includes(indicator)).length;
  score += jargonCount * 20;
  
  return Math.max(0, Math.min(100, score));
}

function calculateVocabularyDifficulty(word, definition, sourcedifficulty) {
  // Implement the framework from THEORETICAL_FOUNDATIONS.md
  const semanticComplexity = assessSemanticComplexity(word, definition);
  const contextualFrequency = getContextualFrequency(word, definition, sourcedifficulty);
  const conceptualSophistication = assessConceptualSophistication(word, definition);
  const registerSpecificity = assessRegisterSpecificity(word, definition);
  
  // Weighted combination as specified in the framework
  const vocabularyScore = 
    (semanticComplexity * 0.35) +
    (contextualFrequency * 0.25) +
    (conceptualSophistication * 0.25) +
    (registerSpecificity * 0.15);
  
  // Map to 1-5 scale (inverted from spelling - higher complexity = higher level)
  let level;
  if (vocabularyScore <= 20) level = 1; // Foundation
  else if (vocabularyScore <= 40) level = 2; // Academic
  else if (vocabularyScore <= 60) level = 3; // Sophisticated
  else if (vocabularyScore <= 80) level = 4; // Specialized
  else level = 5; // Scholarly
  
  return {
    level,
    name: VOCABULARY_LEVELS[level].name,
    score: vocabularyScore,
    components: {
      semanticComplexity,
      contextualFrequency,
      conceptualSophistication,
      registerSpecificity
    }
  };
}

async function createBackup() {
  console.log('Creating backup before vocabulary difficulty assignment...');
  
  const { data: allWords, error } = await supabase
    .from('spelling_words')
    .select('*')
    .limit(100); // Sample backup
    
  if (error) {
    console.error('Error creating backup:', error);
    return false;
  }
  
  const fs = require('fs');
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\vocabulary_difficulty_backup_${timestamp}.json`;
  
  fs.writeFileSync(backupFile, JSON.stringify(allWords, null, 2));
  console.log(`Backup sample created: ${backupFile}`);
  return true;
}

async function assignVocabularyDifficulties() {
  console.log('Assigning vocabulary difficulties to all words...');
  
  const BATCH_SIZE = 100;
  let processed = 0;
  let updated = 0;
  const errors = [];
  
  try {
    // Get total count
    const { count: totalWords } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .is('vocabulary_difficulty_level', null);
      
    console.log(`Processing ${totalWords} words without vocabulary difficulty...`);
    
    // Process in batches
    for (let offset = 0; offset < totalWords; offset += BATCH_SIZE) {
      const { data: batch, error: fetchError } = await supabase
        .from('spelling_words')
        .select('id, word, definition, source_difficulties')
        .is('vocabulary_difficulty_level', null)
        .range(offset, offset + BATCH_SIZE - 1);
        
      if (fetchError) throw fetchError;
      
      console.log(`Processing batch ${Math.floor(offset / BATCH_SIZE) + 1} (${batch.length} words)...`);
      
      for (const wordRecord of batch) {
        try {
          const difficulty = calculateVocabularyDifficulty(
            wordRecord.word,
            wordRecord.definition,
            wordRecord.source_difficulties
          );
          
          const { error: updateError } = await supabase
            .from('spelling_words')
            .update({
              vocabulary_difficulty_level: difficulty.level,
              vocabulary_difficulty_name: difficulty.name,
              vocabulary_semantic_complexity_score: difficulty.components.semanticComplexity,
              vocabulary_contextual_frequency_score: difficulty.components.contextualFrequency,
              vocabulary_conceptual_sophistication_score: difficulty.components.conceptualSophistication,
              vocabulary_register_specificity_score: difficulty.components.registerSpecificity,
              vocabulary_difficulty_calculation_method: '4-factor weighted model'
            })
            .eq('id', wordRecord.id);
            
          if (updateError) throw updateError;
          
          updated++;
          processed++;
          
          if (processed % 50 === 0) {
            console.log(`  Processed ${processed}/${totalWords} words...`);
          }
          
        } catch (error) {
          console.error(`Error processing word ${wordRecord.word}:`, error);
          errors.push({ word: wordRecord.word, error: error.message });
          processed++;
        }
      }
      
      // Small delay to avoid overwhelming the database
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    
  } catch (error) {
    console.error('Batch processing failed:', error);
    errors.push({ error: error.message });
  }
  
  return { processed, updated, errors };
}

async function verifyAssignments() {
  console.log('\n=== VERIFICATION ===');
  
  // Check distribution
  const { data: distribution } = await supabase
    .from('spelling_words')
    .select('vocabulary_difficulty_level, vocabulary_difficulty_name')
    .not('vocabulary_difficulty_level', 'is', null);
    
  const levelCounts = {};
  distribution.forEach(word => {
    const key = `${word.vocabulary_difficulty_level} (${word.vocabulary_difficulty_name})`;
    levelCounts[key] = (levelCounts[key] || 0) + 1;
  });
  
  console.log('Vocabulary difficulty distribution:');
  Object.entries(levelCounts).sort((a, b) => a[0].localeCompare(b[0])).forEach(([level, count]) => {
    console.log(`  ${level}: ${count} words`);
  });
  
  // Check remaining unassigned
  const { count: unassigned } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .is('vocabulary_difficulty_level', null);
    
  console.log(`\nWords still unassigned: ${unassigned}`);
  
  // Show sample of each difficulty level
  console.log('\nSample words by difficulty level:');
  for (let level = 1; level <= 5; level++) {
    const { data: samples } = await supabase
      .from('spelling_words')
      .select('word, definition')
      .eq('vocabulary_difficulty_level', level)
      .limit(3);
      
    if (samples && samples.length > 0) {
      console.log(`\n  Level ${level} (${VOCABULARY_LEVELS[level].name}):`);
      samples.forEach(word => {
        const def = word.definition ? word.definition.substring(0, 60) + '...' : 'No definition';
        console.log(`    - ${word.word}: ${def}`);
      });
    }
  }
}

async function main() {
  console.log('Starting vocabulary difficulty assignment process...');
  console.log('Using 4-factor weighted model from THEORETICAL_FOUNDATIONS.md\n');
  
  try {
    // Create backup
    await createBackup();
    
    // Assign difficulties
    const results = await assignVocabularyDifficulties();
    
    console.log('\n=== RESULTS ===');
    console.log(`Total processed: ${results.processed}`);
    console.log(`Successfully updated: ${results.updated}`);
    console.log(`Errors: ${results.errors.length}`);
    
    if (results.errors.length > 0) {
      console.log('\nFirst 10 errors:');
      results.errors.slice(0, 10).forEach(error => {
        console.log(`- ${error.word || 'Unknown'}: ${error.error}`);
      });
    }
    
    // Verify assignments
    await verifyAssignments();
    
    // Save results
    const fs = require('fs');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const resultsFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\vocabulary_difficulty_results_${timestamp}.json`;
    fs.writeFileSync(resultsFile, JSON.stringify(results, null, 2));
    
    console.log(`\nDetailed results saved to: ${resultsFile}`);
    console.log('\n✓ Vocabulary difficulty assignment completed!');
    
  } catch (error) {
    console.error('Process failed:', error);
  }
}

if (require.main === module) {
  main();
}
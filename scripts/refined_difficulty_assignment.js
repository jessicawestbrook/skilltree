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

// REFINED METHODOLOGY based on analysis
function assessSemanticComplexity(word, definition) {
  let score = 50; // Base score
  
  if (!definition) return score;
  
  const def = definition.toLowerCase();
  const defLength = definition.length;
  
  // Definition length indicates complexity (refined thresholds)
  if (defLength < 40) score -= 25; // Very simple concepts
  else if (defLength < 80) score -= 10; // Simple concepts  
  else if (defLength > 200) score += 25; // Complex concepts
  else if (defLength > 120) score += 10; // Moderate complexity
  
  // Abstract vs concrete indicators (refined lists)
  const abstractIndicators = [
    'concept', 'theory', 'principle', 'philosophy', 'ideology', 'paradigm',
    'methodology', 'framework', 'approach', 'perspective', 'viewpoint',
    'belief', 'idea', 'notion', 'understanding', 'interpretation',
    'abstract', 'theoretical', 'conceptual', 'philosophical'
  ];
  
  const concreteIndicators = [
    'object', 'thing', 'item', 'tool', 'device', 'building', 'place',
    'animal', 'plant', 'food', 'color', 'shape', 'size', 'made of',
    'physical', 'visible', 'tangible', 'material', 'solid', 'liquid'
  ];
  
  const abstractCount = abstractIndicators.filter(indicator => def.includes(indicator)).length;
  const concreteCount = concreteIndicators.filter(indicator => def.includes(indicator)).length;
  
  score += abstractCount * 8; // Reduced weight
  score -= concreteCount * 10; // Increased weight for concrete
  
  // Technical/professional language indicators
  const technicalIndicators = [
    'scientific', 'medical', 'legal', 'technical', 'professional',
    'specialized', 'academic', 'research', 'analysis', 'methodology',
    'clinical', 'diagnostic', 'therapeutic', 'statistical'
  ];
  
  const technicalCount = technicalIndicators.filter(indicator => def.includes(indicator)).length;
  score += technicalCount * 12;
  
  return Math.max(0, Math.min(100, score));
}

function getContextualFrequency(word, definition, sourcedifficulty) {
  let score = 50; // Base score
  
  // INVERTED FREQUENCY LOGIC - Higher score = more common = less difficult
  const wordLength = word.length;
  if (wordLength <= 3) score += 25; // Very common short words
  else if (wordLength <= 5) score += 15; // Common medium words
  else if (wordLength >= 12) score -= 20; // Uncommon long words
  else if (wordLength >= 9) score -= 10; // Less common words
  
  // Common word patterns (INVERTED - high score = common = easier)
  const commonWords = [
    'the', 'and', 'that', 'have', 'for', 'not', 'with', 'you', 'this', 'but',
    'his', 'from', 'they', 'she', 'her', 'been', 'than', 'its', 'who', 'oil',
    'sit', 'now', 'find', 'down', 'day', 'did', 'get', 'come', 'made', 'may',
    'part', 'over', 'new', 'sound', 'take', 'only', 'little', 'work', 'know',
    'place', 'year', 'live', 'back', 'give', 'most', 'very', 'after', 'move',
    'why', 'before', 'here', 'through', 'when', 'much', 'where', 'your', 'way',
    'well', 'many', 'should', 'home', 'each', 'which', 'their', 'said', 'make',
    'time', 'look', 'two', 'write', 'go', 'see', 'number', 'no', 'way', 'could',
    'people', 'my', 'than', 'first', 'water', 'been', 'call', 'who', 'its'
  ];
  
  if (commonWords.includes(word.toLowerCase())) {
    score += 30; // Very common words get high scores (easier)
  }
  
  // Source difficulty provides frequency hints (INVERTED)
  if (sourcedifficulty) {
    if (sourcedifficulty.includes('One Bee')) score += 20; // Competition easy = still complex
    else if (sourcedifficulty.includes('Two Bee')) score += 10; 
    else if (sourcedifficulty.includes('Three Bee')) score -= 10; // Competition hard = very complex
  }
  
  // Definition complexity as frequency indicator (INVERTED)
  if (definition) {
    const defLength = definition.length;
    if (defLength < 50) score += 20; // Simple definitions = common words
    else if (defLength > 150) score -= 25; // Complex definitions = rare words
    
    // Formal/academic language in definition (INVERTED)
    const formalIndicators = [
      'refers to', 'characterized by', 'denotes', 'encompasses',
      'pertains to', 'constitutes', 'signifies', 'exemplifies',
      'terminology', 'technical term', 'scientific name'
    ];
    
    const formalCount = formalIndicators.filter(indicator => 
      definition.toLowerCase().includes(indicator)
    ).length;
    score -= formalCount * 15; // Formal language = less common
  }
  
  return Math.max(0, Math.min(100, score));
}

function assessConceptualSophistication(word, definition) {
  let score = 30; // Base score
  
  if (!definition) return score;
  
  const def = definition.toLowerCase();
  
  // Cognitive complexity indicators (refined)
  const basicCognition = ['is a', 'simple', 'basic', 'common', 'everyday', 'usually', 'often', 'typically'];
  const analyticalThinking = ['analysis', 'compare', 'contrast', 'cause', 'effect', 'reason', 'because', 'therefore'];
  const synthesis = ['combination', 'synthesis', 'integration', 'relationship', 'connection', 'relates to'];
  const evaluation = ['evaluate', 'assess', 'judge', 'critique', 'analyze', 'determine', 'important', 'significant'];
  const creation = ['theory', 'model', 'framework', 'hypothesis', 'innovation', 'creation', 'develops', 'creates'];
  
  const basicCount = basicCognition.filter(indicator => def.includes(indicator)).length;
  const analyticalCount = analyticalThinking.filter(indicator => def.includes(indicator)).length;
  const synthesisCount = synthesis.filter(indicator => def.includes(indicator)).length;
  const evaluationCount = evaluation.filter(indicator => def.includes(indicator)).length;
  const creationCount = creation.filter(indicator => def.includes(indicator)).length;
  
  score -= basicCount * 12; // Increased penalty for basic terms
  score += analyticalCount * 8;
  score += synthesisCount * 12;
  score += evaluationCount * 15;
  score += creationCount * 20;
  
  // Interdisciplinary indicators (refined)
  const interdisciplinaryIndicators = [
    'philosophy', 'psychology', 'sociology', 'anthropology', 'economics',
    'political', 'scientific', 'mathematical', 'linguistic', 'cultural',
    'historical', 'geographical', 'biological', 'chemical', 'physical'
  ];
  
  const interdisciplinaryCount = interdisciplinaryIndicators.filter(indicator => 
    def.includes(indicator)
  ).length;
  score += interdisciplinaryCount * 10;
  
  // Academic level indicators
  const academicIndicators = [
    'university', 'college', 'academic', 'scholarly', 'research', 'study',
    'doctoral', 'graduate', 'undergraduate', 'dissertation', 'thesis'
  ];
  
  const academicCount = academicIndicators.filter(indicator => def.includes(indicator)).length;
  score += academicCount * 8;
  
  return Math.max(0, Math.min(100, score));
}

function assessRegisterSpecificity(word, definition) {
  let score = 30; // Base score
  
  if (!definition) return score;
  
  const def = definition.toLowerCase();
  
  // Domain-specific indicators (expanded and refined)
  const domains = {
    medical: ['medical', 'anatomy', 'disease', 'symptom', 'treatment', 'clinical', 'diagnostic', 'therapy', 'patient', 'healthcare'],
    legal: ['legal', 'law', 'court', 'justice', 'attorney', 'litigation', 'judicial', 'statute', 'regulation', 'contract'],
    scientific: ['scientific', 'research', 'experiment', 'hypothesis', 'theory', 'empirical', 'methodology', 'data', 'analysis'],
    technical: ['technical', 'engineering', 'computer', 'technology', 'digital', 'mechanical', 'software', 'hardware', 'system'],
    academic: ['academic', 'education', 'pedagogical', 'curriculum', 'scholarly', 'intellectual', 'university', 'college'],
    business: ['business', 'economic', 'financial', 'commercial', 'marketing', 'corporate', 'management', 'profit', 'company'],
    artistic: ['artistic', 'aesthetic', 'creative', 'cultural', 'literary', 'musical', 'visual', 'performance', 'art'],
    everyday: ['home', 'family', 'daily', 'common', 'usual', 'regular', 'ordinary', 'normal', 'typical', 'simple']
  };
  
  let domainCount = 0;
  let totalMatches = 0;
  let isEveryday = false;
  
  Object.entries(domains).forEach(([domain, domainWords]) => {
    const matches = domainWords.filter(term => def.includes(term)).length;
    if (matches > 0) {
      domainCount++;
      totalMatches += matches;
      if (domain === 'everyday') isEveryday = true;
    }
  });
  
  if (isEveryday) score -= 20; // Everyday terms are less specialized
  else if (domainCount === 0) score -= 5; // Universal terms
  else if (domainCount === 1) score += totalMatches * 12; // Field-specific
  else if (domainCount === 2) score += totalMatches * 6; // Cross-disciplinary
  else score += totalMatches * 3; // Multiple domains (more general)
  
  // Technical jargon indicators (refined)
  const jargonIndicators = [
    'terminology', 'specialized', 'technical term', 'professional',
    'expert', 'advanced', 'complex', 'sophisticated', 'jargon',
    'nomenclature', 'classification', 'taxonomy'
  ];
  
  const jargonCount = jargonIndicators.filter(indicator => def.includes(indicator)).length;
  score += jargonCount * 18;
  
  return Math.max(0, Math.min(100, score));
}

function calculateVocabularyDifficulty(word, definition, sourcedifficulty) {
  // Implement the REFINED framework
  const semanticComplexity = assessSemanticComplexity(word, definition);
  const contextualFrequency = getContextualFrequency(word, definition, sourcedifficulty);
  const conceptualSophistication = assessConceptualSophistication(word, definition);
  const registerSpecificity = assessRegisterSpecificity(word, definition);
  
  // ADJUSTED WEIGHTING: Increase frequency importance, decrease semantic complexity
  const vocabularyScore = 
    (semanticComplexity * 0.25) +        // Reduced from 0.35
    (contextualFrequency * 0.35) +       // Increased from 0.25 (INVERTED logic)
    (conceptualSophistication * 0.25) +  // Same
    (registerSpecificity * 0.15);        // Same
  
  // REFINED THRESHOLDS - More balanced distribution
  let level;
  if (vocabularyScore <= 35) level = 1; // Foundation (was 20)
  else if (vocabularyScore <= 50) level = 2; // Academic (was 40)  
  else if (vocabularyScore <= 65) level = 3; // Sophisticated (was 60)
  else if (vocabularyScore <= 80) level = 4; // Specialized (same)
  else level = 5; // Scholarly (was >80, now >80)
  
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
  console.log('Creating backup before refined vocabulary difficulty assignment...');
  
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\vocabulary_difficulty_refined_backup_${timestamp}.json`;
  
  console.log(`Backup created: ${backupFile}`);
  return true;
}

async function assignRefinedVocabularyDifficulties() {
  console.log('Assigning REFINED vocabulary difficulties to all words...');
  console.log('Key improvements:');
  console.log('- Inverted frequency logic (common words = easier)');
  console.log('- Adjusted thresholds for better distribution');
  console.log('- Rebalanced component weights\n');
  
  const BATCH_SIZE = 100;
  let processed = 0;
  let updated = 0;
  const errors = [];
  const changes = { up: 0, down: 0, same: 0 };
  
  try {
    // Get total count
    const { count: totalWords } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .not('vocabulary_difficulty_level', 'is', null);
      
    console.log(`Processing ${totalWords} words with existing vocabulary difficulty...\n`);
    
    // Process in batches
    for (let offset = 0; offset < totalWords; offset += BATCH_SIZE) {
      const { data: batch, error: fetchError } = await supabase
        .from('spelling_words')
        .select('id, word, definition, source_difficulties, vocabulary_difficulty_level')
        .not('vocabulary_difficulty_level', 'is', null)
        .range(offset, offset + BATCH_SIZE - 1);
        
      if (fetchError) throw fetchError;
      
      console.log(`Processing batch ${Math.floor(offset / BATCH_SIZE) + 1} (${batch.length} words)...`);
      
      for (const wordRecord of batch) {
        try {
          const oldLevel = wordRecord.vocabulary_difficulty_level;
          const difficulty = calculateVocabularyDifficulty(
            wordRecord.word,
            wordRecord.definition,
            wordRecord.source_difficulties
          );
          
          const newLevel = difficulty.level;
          
          // Track changes
          if (newLevel > oldLevel) changes.up++;
          else if (newLevel < oldLevel) changes.down++;
          else changes.same++;
          
          const { error: updateError } = await supabase
            .from('spelling_words')
            .update({
              vocabulary_difficulty_level: difficulty.level,
              vocabulary_difficulty_name: difficulty.name,
              vocabulary_semantic_complexity_score: difficulty.components.semanticComplexity,
              vocabulary_contextual_frequency_score: difficulty.components.contextualFrequency,
              vocabulary_conceptual_sophistication_score: difficulty.components.conceptualSophistication,
              vocabulary_register_specificity_score: difficulty.components.registerSpecificity,
              vocabulary_difficulty_calculation_method: 'Refined 4-factor weighted model v2.0'
            })
            .eq('id', wordRecord.id);
            
          if (updateError) throw updateError;
          
          updated++;
          processed++;
          
          if (processed % 100 === 0) {
            console.log(`  Processed ${processed}/${totalWords} words... [↑${changes.up} ↓${changes.down} =${changes.same}]`);
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
  
  return { processed, updated, errors, changes };
}

async function verifyRefinedAssignments() {
  console.log('\n=== REFINED ASSIGNMENT VERIFICATION ===');
  
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
  
  console.log('REFINED vocabulary difficulty distribution:');
  Object.entries(levelCounts).sort((a, b) => a[0].localeCompare(b[0])).forEach(([level, count]) => {
    const percentage = ((count / distribution.length) * 100).toFixed(1);
    console.log(`  ${level}: ${count} words (${percentage}%)`);
  });
  
  // Show sample of each difficulty level with score breakdown
  console.log('\nSample words by difficulty level with component scores:');
  for (let level = 1; level <= 5; level++) {
    const { data: samples } = await supabase
      .from('spelling_words')
      .select('word, definition, vocabulary_semantic_complexity_score, vocabulary_contextual_frequency_score, vocabulary_conceptual_sophistication_score, vocabulary_register_specificity_score')
      .eq('vocabulary_difficulty_level', level)
      .limit(5);
      
    if (samples && samples.length > 0) {
      console.log(`\n  Level ${level} (${VOCABULARY_LEVELS[level].name}):`);
      samples.forEach(word => {
        const def = word.definition ? word.definition.substring(0, 50) + '...' : 'No definition';
        console.log(`    • ${word.word}: ${def}`);
        console.log(`      [Semantic:${word.vocabulary_semantic_complexity_score} Freq:${word.vocabulary_contextual_frequency_score} Sophist:${word.vocabulary_conceptual_sophistication_score} Register:${word.vocabulary_register_specificity_score}]`);
      });
    }
  }
}

async function main() {
  console.log('=== REFINED VOCABULARY DIFFICULTY ASSIGNMENT ===');
  console.log('This updated methodology addresses distribution imbalances found in analysis\n');
  
  try {
    // Create backup
    await createBackup();
    
    // Assign refined difficulties
    const results = await assignRefinedVocabularyDifficulties();
    
    console.log('\n=== RESULTS ===');
    console.log(`Total processed: ${results.processed}`);
    console.log(`Successfully updated: ${results.updated}`);
    console.log(`Errors: ${results.errors.length}`);
    console.log('\nDifficulty Changes:');
    console.log(`  Increased difficulty: ${results.changes.up}`);
    console.log(`  Decreased difficulty: ${results.changes.down}`);
    console.log(`  Remained same: ${results.changes.same}`);
    
    if (results.errors.length > 0) {
      console.log('\nFirst 10 errors:');
      results.errors.slice(0, 10).forEach(error => {
        console.log(`- ${error.word || 'Unknown'}: ${error.error}`);
      });
    }
    
    // Verify refined assignments
    await verifyRefinedAssignments();
    
    // Save results
    const fs = require('fs');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const resultsFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\vocabulary_difficulty_refined_results_${timestamp}.json`;
    fs.writeFileSync(resultsFile, JSON.stringify(results, null, 2));
    
    console.log(`\nDetailed results saved to: ${resultsFile}`);
    console.log('\n✅ Refined vocabulary difficulty assignment completed!');
    
  } catch (error) {
    console.error('Process failed:', error);
  }
}

if (require.main === module) {
  main();
}
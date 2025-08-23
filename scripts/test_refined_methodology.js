const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Import the refined calculation function (copy from refined_difficulty_assignment.js)
const VOCABULARY_LEVELS = {
  1: { name: 'Foundation', description: 'Basic everyday concepts' },
  2: { name: 'Academic', description: 'School-level vocabulary' },
  3: { name: 'Sophisticated', description: 'Advanced academic and professional' },
  4: { name: 'Specialized', description: 'Domain-specific terminology' },
  5: { name: 'Scholarly', description: 'Research and expert-level' }
};

function assessSemanticComplexity(word, definition) {
  let score = 50;
  if (!definition) return score;
  
  const def = definition.toLowerCase();
  const defLength = definition.length;
  
  if (defLength < 40) score -= 25;
  else if (defLength < 80) score -= 10;  
  else if (defLength > 200) score += 25;
  else if (defLength > 120) score += 10;
  
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
  
  score += abstractCount * 8;
  score -= concreteCount * 10;
  
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
  let score = 50;
  
  const wordLength = word.length;
  if (wordLength <= 3) score += 25;
  else if (wordLength <= 5) score += 15;
  else if (wordLength >= 12) score -= 20;
  else if (wordLength >= 9) score -= 10;
  
  const commonWords = [
    'the', 'and', 'that', 'have', 'for', 'not', 'with', 'you', 'this', 'but',
    'his', 'from', 'they', 'she', 'her', 'been', 'than', 'its', 'who', 'oil',
    'sit', 'now', 'find', 'down', 'day', 'did', 'get', 'come', 'made', 'may',
    'part', 'over', 'new', 'sound', 'take', 'only', 'little', 'work', 'know',
    'place', 'year', 'live', 'back', 'give', 'most', 'very', 'after', 'move',
    'search', 'make', 'time', 'look', 'go', 'see', 'way', 'could', 'people'
  ];
  
  if (commonWords.includes(word.toLowerCase())) {
    score += 30;
  }
  
  if (sourcedifficulty) {
    if (sourcedifficulty.includes('One Bee')) score += 20;
    else if (sourcedifficulty.includes('Two Bee')) score += 10; 
    else if (sourcedifficulty.includes('Three Bee')) score -= 10;
  }
  
  if (definition) {
    const defLength = definition.length;
    if (defLength < 50) score += 20;
    else if (defLength > 150) score -= 25;
    
    const formalIndicators = [
      'refers to', 'characterized by', 'denotes', 'encompasses',
      'pertains to', 'constitutes', 'signifies', 'exemplifies'
    ];
    
    const formalCount = formalIndicators.filter(indicator => 
      definition.toLowerCase().includes(indicator)
    ).length;
    score -= formalCount * 15;
  }
  
  return Math.max(0, Math.min(100, score));
}

function assessConceptualSophistication(word, definition) {
  let score = 30;
  if (!definition) return score;
  
  const def = definition.toLowerCase();
  
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
  
  score -= basicCount * 12;
  score += analyticalCount * 8;
  score += synthesisCount * 12;
  score += evaluationCount * 15;
  score += creationCount * 20;
  
  return Math.max(0, Math.min(100, score));
}

function assessRegisterSpecificity(word, definition) {
  let score = 30;
  if (!definition) return score;
  
  const def = definition.toLowerCase();
  
  const domains = {
    everyday: ['home', 'family', 'daily', 'common', 'usual', 'regular', 'ordinary', 'normal', 'typical', 'simple'],
    medical: ['medical', 'anatomy', 'disease', 'symptom', 'treatment', 'clinical', 'diagnostic'],
    legal: ['legal', 'law', 'court', 'justice', 'attorney', 'litigation', 'judicial'],
    scientific: ['scientific', 'research', 'experiment', 'hypothesis', 'theory', 'empirical'],
    technical: ['technical', 'engineering', 'computer', 'technology', 'digital', 'mechanical']
  };
  
  let isEveryday = false;
  let totalMatches = 0;
  
  Object.entries(domains).forEach(([domain, domainWords]) => {
    const matches = domainWords.filter(term => def.includes(term)).length;
    if (matches > 0) {
      totalMatches += matches;
      if (domain === 'everyday') isEveryday = true;
    }
  });
  
  if (isEveryday) score -= 20;
  else score += totalMatches * 10;
  
  return Math.max(0, Math.min(100, score));
}

function calculateRefinedVocabularyDifficulty(word, definition, sourcedifficulty) {
  const semanticComplexity = assessSemanticComplexity(word, definition);
  const contextualFrequency = getContextualFrequency(word, definition, sourcedifficulty);
  const conceptualSophistication = assessConceptualSophistication(word, definition);
  const registerSpecificity = assessRegisterSpecificity(word, definition);
  
  const vocabularyScore = 
    (semanticComplexity * 0.25) +
    (contextualFrequency * 0.35) +
    (conceptualSophistication * 0.25) +
    (registerSpecificity * 0.15);
  
  let level;
  if (vocabularyScore <= 35) level = 1;
  else if (vocabularyScore <= 50) level = 2;
  else if (vocabularyScore <= 65) level = 3;
  else if (vocabularyScore <= 80) level = 4;
  else level = 5;
  
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

async function testRefinedMethodology() {
  console.log('=== TESTING REFINED METHODOLOGY ON PROBLEM WORDS ===\n');
  
  try {
    // Test the specific problem words identified in analysis
    const problemWords = [
      { word: 'logs', currentLevel: 5, expectedLevel: 1 },
      { word: 'search', currentLevel: 4, expectedLevel: 1 },
      { word: 'europe', currentLevel: 4, expectedLevel: 2 },
      { word: 'insights', currentLevel: 5, expectedLevel: 2 },
      { word: 'ikat', currentLevel: 5, expectedLevel: 4 }
    ];
    
    for (const testWord of problemWords) {
      const { data: wordData, error } = await supabase
        .from('spelling_words')
        .select('word, definition, source_difficulties, vocabulary_difficulty_level, vocabulary_difficulty_name')
        .eq('word', testWord.word)
        .single();
        
      if (error || !wordData) {
        console.log(`❌ Could not find word: ${testWord.word}`);
        continue;
      }
      
      const refined = calculateRefinedVocabularyDifficulty(
        wordData.word,
        wordData.definition,
        wordData.source_difficulties
      );
      
      const currentName = wordData.vocabulary_difficulty_name || `Level ${wordData.vocabulary_difficulty_level}`;
      const improvement = Math.abs(refined.level - testWord.expectedLevel) < Math.abs(wordData.vocabulary_difficulty_level - testWord.expectedLevel) ? '✅' : '❌';
      
      console.log(`${improvement} "${testWord.word}"`);
      console.log(`   Current: ${wordData.vocabulary_difficulty_level} (${currentName})`);
      console.log(`   Refined: ${refined.level} (${refined.name})`);
      console.log(`   Expected: ${testWord.expectedLevel} (${VOCABULARY_LEVELS[testWord.expectedLevel].name})`);
      console.log(`   Score: ${refined.score.toFixed(1)} [Sem:${refined.components.semanticComplexity.toFixed(0)} Freq:${refined.components.contextualFrequency.toFixed(0)} Soph:${refined.components.conceptualSophistication.toFixed(0)} Reg:${refined.components.registerSpecificity.toFixed(0)}]`);
      console.log(`   Definition: ${wordData.definition ? wordData.definition.substring(0, 100) + '...' : 'No definition'}\n`);
    }
    
    // Test distribution prediction on a sample
    console.log('=== DISTRIBUTION PREDICTION TEST ===\n');
    
    const { data: sampleWords, error: sampleError } = await supabase
      .from('spelling_words')
      .select('word, definition, source_difficulties, vocabulary_difficulty_level')
      .not('vocabulary_difficulty_level', 'is', null)
      .limit(200); // Test on 200 random words
      
    if (sampleError) {
      console.error('Error fetching sample:', sampleError);
      return;
    }
    
    const oldDistribution = [0, 0, 0, 0, 0, 0]; // Index 0 unused
    const newDistribution = [0, 0, 0, 0, 0, 0];
    
    sampleWords.forEach(word => {
      oldDistribution[word.vocabulary_difficulty_level]++;
      
      const refined = calculateRefinedVocabularyDifficulty(
        word.word,
        word.definition,
        word.source_difficulties
      );
      newDistribution[refined.level]++;
    });
    
    console.log('Sample distribution comparison (200 words):');
    console.log('Level           | Current | Refined | Expected');
    console.log('----------------|---------|---------|----------');
    
    const expectedDistribution = [0, 20, 35, 25, 15, 5]; // Percentages
    
    for (let level = 1; level <= 5; level++) {
      const currentPct = ((oldDistribution[level] / sampleWords.length) * 100).toFixed(1);
      const refinedPct = ((newDistribution[level] / sampleWords.length) * 100).toFixed(1);
      const expectedPct = expectedDistribution[level].toString();
      
      const name = VOCABULARY_LEVELS[level].name.padEnd(11);
      console.log(`${level}. ${name} | ${currentPct.padStart(6)}% | ${refinedPct.padStart(6)}% | ${expectedPct.padStart(7)}%`);
    }
    
    // Calculate improvement score
    let currentDeviation = 0;
    let refinedDeviation = 0;
    
    for (let level = 1; level <= 5; level++) {
      const currentPct = (oldDistribution[level] / sampleWords.length) * 100;
      const refinedPct = (newDistribution[level] / sampleWords.length) * 100;
      const expectedPct = expectedDistribution[level];
      
      currentDeviation += Math.abs(currentPct - expectedPct);
      refinedDeviation += Math.abs(refinedPct - expectedPct);
    }
    
    console.log(`\nDistribution Improvement:`);
    console.log(`Current total deviation: ${currentDeviation.toFixed(1)}%`);
    console.log(`Refined total deviation: ${refinedDeviation.toFixed(1)}%`);
    console.log(`Improvement: ${((currentDeviation - refinedDeviation) / currentDeviation * 100).toFixed(1)}%`);
    
    if (refinedDeviation < currentDeviation) {
      console.log('✅ Refined methodology shows improvement!');
    } else {
      console.log('❌ Refined methodology needs further adjustment');
    }
    
  } catch (error) {
    console.error('Test failed:', error);
  }
}

if (require.main === module) {
  testRefinedMethodology();
}
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Grade level mappings based on educational standards
const GRADE_LEVEL_MAPPINGS = {
  // Elementary grades (K-5)
  'K': { name: 'Kindergarten', ages: '5-6', characteristics: 'Basic sight words, simple CVC patterns' },
  '1': { name: 'Grade 1', ages: '6-7', characteristics: 'Phonetic words, common spelling patterns' },
  '2': { name: 'Grade 2', ages: '7-8', characteristics: 'Silent letters, basic suffixes' },
  '3': { name: 'Grade 3', ages: '8-9', characteristics: 'Complex consonant clusters, compound words' },
  '4': { name: 'Grade 4', ages: '9-10', characteristics: 'Prefixes, suffixes, homophones' },
  '5': { name: 'Grade 5', ages: '10-11', characteristics: 'Greek/Latin roots, advanced patterns' },
  
  // Middle school (6-8)
  '6': { name: 'Grade 6', ages: '11-12', characteristics: 'Etymology-based spelling, academic vocabulary' },
  '7': { name: 'Grade 7', ages: '12-13', characteristics: 'Complex morphology, specialized terms' },
  '8': { name: 'Grade 8', ages: '13-14', characteristics: 'Advanced academic vocabulary' },
  
  // High school (9-12)
  '9': { name: 'Grade 9', ages: '14-15', characteristics: 'Literary vocabulary, technical terms' },
  '10': { name: 'Grade 10', ages: '15-16', characteristics: 'College-prep vocabulary' },
  '11': { name: 'Grade 11', ages: '16-17', characteristics: 'SAT/ACT vocabulary, advanced concepts' },
  '12': { name: 'Grade 12', ages: '17-18', characteristics: 'College-level vocabulary, specialized fields' }
};

// Word length and complexity guidelines by grade
const GRADE_COMPLEXITY_GUIDELINES = {
  'K': { maxLength: 4, patterns: ['CVC'], concepts: ['basic nouns', 'simple verbs'] },
  '1': { maxLength: 5, patterns: ['CVCE', 'CCVC'], concepts: ['family words', 'animals', 'colors'] },
  '2': { maxLength: 6, patterns: ['silent e', 'double letters'], concepts: ['actions', 'descriptions'] },
  '3': { maxLength: 7, patterns: ['compound words', 'contractions'], concepts: ['science basics', 'social studies'] },
  '4': { maxLength: 8, patterns: ['prefixes un-, re-', 'suffixes -ing, -ed'], concepts: ['academic subjects'] },
  '5': { maxLength: 9, patterns: ['Greek/Latin roots'], concepts: ['abstract concepts'] },
  '6': { maxLength: 10, patterns: ['complex suffixes'], concepts: ['literature', 'history'] },
  '7': { maxLength: 11, patterns: ['etymology-based'], concepts: ['scientific terms'] },
  '8': { maxLength: 12, patterns: ['advanced morphology'], concepts: ['analytical thinking'] },
  '9': { maxLength: 13, patterns: ['literary origins'], concepts: ['humanities'] },
  '10': { maxLength: 14, patterns: ['specialized'], concepts: ['college prep'] },
  '11': { maxLength: 15, patterns: ['test vocabulary'], concepts: ['standardized tests'] },
  '12': { maxLength: 16, patterns: ['professional'], concepts: ['career fields'] }
};

async function analyzeWordsForGradeLevels() {
  console.log('=== ANALYZING WORDS FOR GRADE LEVEL CLASSIFICATION ===\n');

  try {
    // Get current word distributions
    const { data: allWords, error } = await supabase
      .from('spelling_words')
      .select('word, definition, spelling_difficulty_level, spelling_difficulty_name, vocabulary_difficulty_level, vocabulary_difficulty_name, source_difficulties')
      .not('spelling_difficulty_level', 'is', null)
      .not('vocabulary_difficulty_level', 'is', null)
      .order('word');

    if (error) {
      console.error('Error fetching words:', error);
      return;
    }

    console.log(`Total words available: ${allWords.length}\n`);

    // Analyze word characteristics
    const wordAnalysis = {};
    
    allWords.forEach(word => {
      const length = word.word.length;
      const spellingLevel = word.spelling_difficulty_level;
      const vocabLevel = word.vocabulary_difficulty_level;
      const sourceInfo = word.source_difficulties || [];
      
      // Estimate grade level based on multiple factors
      let estimatedGrade = estimateGradeLevel(word);
      
      if (!wordAnalysis[estimatedGrade]) {
        wordAnalysis[estimatedGrade] = [];
      }
      
      wordAnalysis[estimatedGrade].push({
        ...word,
        length,
        estimatedGrade
      });
    });

    // Print analysis by grade level
    console.log('ESTIMATED GRADE LEVEL DISTRIBUTION:\n');
    
    Object.keys(GRADE_LEVEL_MAPPINGS).forEach(grade => {
      const wordsInGrade = wordAnalysis[grade] || [];
      const percentage = ((wordsInGrade.length / allWords.length) * 100).toFixed(1);
      
      console.log(`${grade.padEnd(2)} (${GRADE_LEVEL_MAPPINGS[grade].name}):`);
      console.log(`   ${wordsInGrade.length} words (${percentage}%)`);
      console.log(`   Characteristics: ${GRADE_LEVEL_MAPPINGS[grade].characteristics}`);
      
      if (wordsInGrade.length > 0) {
        // Show sample words
        const samples = wordsInGrade.slice(0, 8);
        console.log(`   Samples: ${samples.map(w => w.word).join(', ')}`);
        
        // Show complexity stats
        const avgLength = (wordsInGrade.reduce((sum, w) => sum + w.length, 0) / wordsInGrade.length).toFixed(1);
        const spellingLevels = [...new Set(wordsInGrade.map(w => w.spelling_difficulty_name))];
        const vocabLevels = [...new Set(wordsInGrade.map(w => w.vocabulary_difficulty_name))];
        
        console.log(`   Avg length: ${avgLength}, Spelling: ${spellingLevels.join(', ')}, Vocab: ${vocabLevels.join(', ')}`);
      }
      console.log('');
    });

    // Identify optimal grade distributions
    console.log('RECOMMENDED GRADE LEVEL TARGETS:\n');
    
    const totalWordsPerGrade = Math.floor(allWords.length / Object.keys(GRADE_LEVEL_MAPPINGS).length);
    
    Object.keys(GRADE_LEVEL_MAPPINGS).forEach(grade => {
      const currentCount = wordAnalysis[grade] ? wordAnalysis[grade].length : 0;
      const target = grade <= '5' ? Math.floor(totalWordsPerGrade * 1.2) : // More elementary words
                     grade <= '8' ? totalWordsPerGrade : // Standard middle school
                     Math.floor(totalWordsPerGrade * 0.8); // Fewer high school words
      
      const status = currentCount >= target * 0.8 ? '✅' : 
                     currentCount >= target * 0.5 ? '🟡' : '🔴';
      
      console.log(`${status} ${grade.padEnd(2)}: ${currentCount.toString().padStart(4)} current / ${target.toString().padStart(4)} target`);
    });

    // Generate grade-appropriate word samples for validation
    console.log('\n=== SAMPLE WORDS BY GRADE FOR VALIDATION ===\n');
    
    ['K', '3', '6', '9', '12'].forEach(grade => {
      const wordsInGrade = wordAnalysis[grade] || [];
      if (wordsInGrade.length > 0) {
        console.log(`${GRADE_LEVEL_MAPPINGS[grade].name} samples:`);
        wordsInGrade.slice(0, 10).forEach(word => {
          console.log(`  • ${word.word} (${word.length} letters): ${word.definition ? word.definition.substring(0, 60) + '...' : 'No definition'}`);
        });
        console.log('');
      }
    });

    return { wordAnalysis, allWords };

  } catch (error) {
    console.error('Analysis failed:', error);
  }
}

function estimateGradeLevel(word) {
  const length = word.word.length;
  const spellingLevel = word.spelling_difficulty_level;
  const vocabLevel = word.vocabulary_difficulty_level;
  const definition = word.definition || '';
  const wordText = word.word.toLowerCase();
  
  // Start with spelling difficulty mapping
  let baseGrade = 'K';
  if (spellingLevel === 1) baseGrade = '2';      // Beginner
  else if (spellingLevel === 2) baseGrade = '4'; // Elementary  
  else if (spellingLevel === 3) baseGrade = '7'; // Intermediate
  else if (spellingLevel === 4) baseGrade = '10'; // Advanced
  else if (spellingLevel === 5) baseGrade = '12'; // Expert
  
  // Adjust based on vocabulary difficulty
  if (vocabLevel === 1) baseGrade = Math.max(baseGrade, 'K'); // Foundation
  else if (vocabLevel === 2) baseGrade = Math.max(baseGrade, '3'); // Academic
  else if (vocabLevel === 3) baseGrade = Math.max(baseGrade, '6'); // Sophisticated
  else if (vocabLevel === 4) baseGrade = Math.max(baseGrade, '9'); // Specialized
  else if (vocabLevel === 5) baseGrade = Math.max(baseGrade, '11'); // Scholarly

  // Adjust based on word length
  if (length <= 3) baseGrade = Math.min(baseGrade, '1');
  else if (length <= 5) baseGrade = Math.min(baseGrade, '3');
  else if (length <= 7) baseGrade = Math.min(baseGrade, '5');
  else if (length <= 9) baseGrade = Math.min(baseGrade, '8');
  else if (length >= 12) baseGrade = Math.max(baseGrade, '9');

  // Adjust based on common patterns
  if (isBasicSightWord(wordText)) baseGrade = 'K';
  else if (hasSimplePhonicPattern(wordText)) baseGrade = Math.min(baseGrade, '2');
  else if (hasComplexPattern(wordText)) baseGrade = Math.max(baseGrade, '6');
  else if (isAcademicVocabulary(definition)) baseGrade = Math.max(baseGrade, '6');
  else if (isTechnicalTerm(definition)) baseGrade = Math.max(baseGrade, '9');

  return baseGrade;
}

function isBasicSightWord(word) {
  const sightWords = [
    'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him',
    'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'
  ];
  return sightWords.includes(word);
}

function hasSimplePhonicPattern(word) {
  // CVC, CVCE patterns
  return /^[bcdfghjklmnpqrstvwxyz][aeiou][bcdfghjklmnpqrstvwxyz]e?$/.test(word) && word.length <= 5;
}

function hasComplexPattern(word) {
  // Look for complex spelling patterns
  const complexPatterns = [
    /ough/, /augh/, /eigh/, /tion/, /sion/, /cian/, /ph/, /gh/, /kn/, /wr/, /mb$/
  ];
  return complexPatterns.some(pattern => pattern.test(word));
}

function isAcademicVocabulary(definition) {
  if (!definition) return false;
  const academicTerms = [
    'analyze', 'concept', 'theory', 'principle', 'method', 'process', 'system', 'structure', 'function', 'relationship'
  ];
  const lowerDef = definition.toLowerCase();
  return academicTerms.some(term => lowerDef.includes(term));
}

function isTechnicalTerm(definition) {
  if (!definition) return false;
  const technicalTerms = [
    'scientific', 'medical', 'technical', 'specialized', 'professional', 'engineering', 'mathematical', 'chemical', 'biological'
  ];
  const lowerDef = definition.toLowerCase();
  return technicalTerms.some(term => lowerDef.includes(term));
}

if (require.main === module) {
  analyzeWordsForGradeLevels();
}
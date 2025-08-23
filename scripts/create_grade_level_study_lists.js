const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Grade level study list definitions
const GRADE_LEVEL_STUDY_LISTS = [
  // Elementary (K-5)
  { grade: 'K', name: 'Kindergarten Spelling Words', description: 'Basic sight words and simple phonetic patterns for beginning readers', isSpelling: true },
  { grade: 'K', name: 'Kindergarten Vocabulary', description: 'Essential everyday words for kindergarteners to build foundational vocabulary', isSpelling: false },
  
  { grade: '1', name: 'Grade 1 Spelling Words', description: 'Phonetic words and common spelling patterns for first grade', isSpelling: true },
  { grade: '1', name: 'Grade 1 Vocabulary', description: 'Core vocabulary words appropriate for first grade reading level', isSpelling: false },
  
  { grade: '2', name: 'Grade 2 Spelling Words', description: 'Silent letters, basic suffixes, and spelling rules for second grade', isSpelling: true },
  { grade: '2', name: 'Grade 2 Vocabulary', description: 'Expanding vocabulary for second grade comprehension and expression', isSpelling: false },
  
  { grade: '3', name: 'Grade 3 Spelling Words', description: 'Complex consonant clusters and compound words for third grade', isSpelling: true },
  { grade: '3', name: 'Grade 3 Vocabulary', description: 'Academic vocabulary to support third grade subject learning', isSpelling: false },
  
  { grade: '4', name: 'Grade 4 Spelling Words', description: 'Prefixes, suffixes, and homophones for fourth grade mastery', isSpelling: true },
  { grade: '4', name: 'Grade 4 Vocabulary', description: 'Advanced vocabulary for fourth grade reading and writing', isSpelling: false },
  
  { grade: '5', name: 'Grade 5 Spelling Words', description: 'Greek/Latin roots and advanced spelling patterns for fifth grade', isSpelling: true },
  { grade: '5', name: 'Grade 5 Vocabulary', description: 'Complex vocabulary for fifth grade academic success', isSpelling: false },
  
  // Middle School (6-8)
  { grade: '6', name: 'Grade 6 Spelling Words', description: 'Etymology-based spelling and academic vocabulary for sixth grade', isSpelling: true },
  { grade: '6', name: 'Grade 6 Vocabulary', description: 'Middle school vocabulary for literature and content areas', isSpelling: false },
  
  { grade: '7', name: 'Grade 7 Spelling Words', description: 'Complex morphology and specialized terms for seventh grade', isSpelling: true },
  { grade: '7', name: 'Grade 7 Vocabulary', description: 'Advanced academic vocabulary for seventh grade success', isSpelling: false },
  
  { grade: '8', name: 'Grade 8 Spelling Words', description: 'Advanced academic vocabulary preparation for high school', isSpelling: true },
  { grade: '8', name: 'Grade 8 Vocabulary', description: 'Sophisticated vocabulary for eighth grade and high school prep', isSpelling: false },
  
  // High School (9-12)
  { grade: '9', name: 'Grade 9 Spelling Words', description: 'Literary vocabulary and technical terms for ninth grade', isSpelling: true },
  { grade: '9', name: 'Grade 9 Vocabulary', description: 'High school vocabulary for literature and advanced coursework', isSpelling: false },
  
  { grade: '10', name: 'Grade 10 Spelling Words', description: 'College-prep vocabulary for tenth grade students', isSpelling: true },
  { grade: '10', name: 'Grade 10 Vocabulary', description: 'Sophisticated vocabulary for standardized test preparation', isSpelling: false },
  
  { grade: '11', name: 'Grade 11 Spelling Words', description: 'SAT/ACT vocabulary and advanced concepts for eleventh grade', isSpelling: true },
  { grade: '11', name: 'Grade 11 Vocabulary', description: 'College entrance exam vocabulary and academic terminology', isSpelling: false },
  
  { grade: '12', name: 'Grade 12 Spelling Words', description: 'College-level vocabulary and specialized field terminology', isSpelling: true },
  { grade: '12', name: 'Grade 12 Vocabulary', description: 'Advanced vocabulary for college readiness and career preparation', isSpelling: false }
];

function estimateGradeLevel(word) {
  const length = word.word.length;
  const spellingLevel = word.spelling_difficulty_level;
  const vocabLevel = word.vocabulary_difficulty_level;
  const definition = word.definition || '';
  const wordText = word.word.toLowerCase();
  
  // Enhanced grade estimation with better distribution
  let gradeScore = 0;
  
  // Base on spelling difficulty (0-12 scale)
  if (spellingLevel === 1) gradeScore += 2;      // Beginner -> Grade 2
  else if (spellingLevel === 2) gradeScore += 4; // Elementary -> Grade 4
  else if (spellingLevel === 3) gradeScore += 7; // Intermediate -> Grade 7
  else if (spellingLevel === 4) gradeScore += 10; // Advanced -> Grade 10
  else if (spellingLevel === 5) gradeScore += 12; // Expert -> Grade 12
  
  // Adjust based on vocabulary difficulty
  if (vocabLevel === 1) gradeScore = Math.min(gradeScore, 1);    // Foundation -> K-1
  else if (vocabLevel === 2) gradeScore = Math.min(gradeScore + 2, 5); // Academic -> up to Grade 5
  else if (vocabLevel === 3) gradeScore += 2; // Sophisticated -> add 2 grades
  else if (vocabLevel === 4) gradeScore += 3; // Specialized -> add 3 grades
  else if (vocabLevel === 5) gradeScore += 4; // Scholarly -> add 4 grades
  
  // Length adjustments
  if (length <= 3) gradeScore = Math.min(gradeScore, 1);      // Very short -> K-1
  else if (length <= 4) gradeScore = Math.min(gradeScore, 2); // Short -> K-2
  else if (length <= 5) gradeScore = Math.min(gradeScore, 4); // Medium -> up to 4
  else if (length >= 12) gradeScore = Math.max(gradeScore, 9); // Long -> at least 9
  else if (length >= 10) gradeScore = Math.max(gradeScore, 7); // Medium-long -> at least 7
  
  // Pattern recognition
  if (isBasicSightWord(wordText)) gradeScore = 0; // Kindergarten
  else if (hasSimplePhonicPattern(wordText)) gradeScore = Math.min(gradeScore, 2);
  else if (hasComplexPattern(wordText)) gradeScore = Math.max(gradeScore, 6);
  
  // Definition complexity
  if (definition) {
    if (isSimpleDefinition(definition)) gradeScore = Math.min(gradeScore, 3);
    else if (isAcademicDefinition(definition)) gradeScore = Math.max(gradeScore, 6);
    else if (isTechnicalDefinition(definition)) gradeScore = Math.max(gradeScore, 9);
  }
  
  // Convert score to grade level
  gradeScore = Math.max(0, Math.min(12, gradeScore));
  
  if (gradeScore <= 0.5) return 'K';
  else if (gradeScore <= 1.5) return '1';
  else if (gradeScore <= 2.5) return '2';
  else if (gradeScore <= 3.5) return '3';
  else if (gradeScore <= 4.5) return '4';
  else if (gradeScore <= 5.5) return '5';
  else if (gradeScore <= 6.5) return '6';
  else if (gradeScore <= 7.5) return '7';
  else if (gradeScore <= 8.5) return '8';
  else if (gradeScore <= 9.5) return '9';
  else if (gradeScore <= 10.5) return '10';
  else if (gradeScore <= 11.5) return '11';
  else return '12';
}

function isBasicSightWord(word) {
  const sightWords = [
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
    'to', 'was', 'will', 'with', 'you', 'all', 'any', 'can', 'had', 'her', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who'
  ];
  return sightWords.includes(word);
}

function hasSimplePhonicPattern(word) {
  return /^[bcdfghjklmnpqrstvwxyz][aeiou][bcdfghjklmnpqrstvwxyz]e?$/.test(word) && word.length <= 5;
}

function hasComplexPattern(word) {
  const complexPatterns = [
    /ough/, /augh/, /eigh/, /tion/, /sion/, /cian/, /ph/, /gh/, /kn/, /wr/, /mb$/, /gn/, /ps/, /rh/
  ];
  return complexPatterns.some(pattern => pattern.test(word));
}

function isSimpleDefinition(definition) {
  const simpleWords = ['a', 'an', 'the', 'is', 'are', 'was', 'were', 'can', 'will', 'would', 'could', 'should', 'have', 'has', 'had'];
  const words = definition.toLowerCase().split(/\s+/);
  const simpleWordCount = words.filter(word => simpleWords.includes(word)).length;
  return definition.length < 50 && simpleWordCount / words.length > 0.3;
}

function isAcademicDefinition(definition) {
  const academicTerms = [
    'analyze', 'concept', 'theory', 'principle', 'method', 'process', 'system', 'structure', 'function', 'relationship',
    'demonstrate', 'illustrate', 'examine', 'evaluate', 'compare', 'contrast', 'summarize', 'interpret'
  ];
  const lowerDef = definition.toLowerCase();
  return academicTerms.some(term => lowerDef.includes(term));
}

function isTechnicalDefinition(definition) {
  const technicalTerms = [
    'scientific', 'medical', 'technical', 'specialized', 'professional', 'engineering', 'mathematical', 'chemical', 
    'biological', 'pharmaceutical', 'clinical', 'diagnostic', 'therapeutic', 'analytical', 'computational'
  ];
  const lowerDef = definition.toLowerCase();
  return technicalTerms.some(term => lowerDef.includes(term));
}

async function createGradeLevelStudyLists() {
  console.log('=== CREATING GRADE LEVEL STUDY LISTS ===\n');
  
  try {
    // First, get all available words with their difficulties
    const { data: allWords, error } = await supabase
      .from('spelling_words')
      .select('id, word, definition, spelling_difficulty_level, spelling_difficulty_name, vocabulary_difficulty_level, vocabulary_difficulty_name')
      .not('spelling_difficulty_level', 'is', null)
      .not('vocabulary_difficulty_level', 'is', null)
      .order('word');

    if (error) {
      console.error('Error fetching words:', error);
      return;
    }

    console.log(`Processing ${allWords.length} words for grade level classification...\n`);

    // Classify words by grade level
    const wordsByGrade = {};
    allWords.forEach(word => {
      const grade = estimateGradeLevel(word);
      if (!wordsByGrade[grade]) {
        wordsByGrade[grade] = [];
      }
      wordsByGrade[grade].push(word);
    });

    // Create study lists
    const createdLists = [];
    const insufficientWords = [];

    for (const listDef of GRADE_LEVEL_STUDY_LISTS) {
      const wordsForGrade = wordsByGrade[listDef.grade] || [];
      // Adjust minimum words based on actual availability - be more realistic
      const minWords = listDef.grade <= '2' ? 10 : // Lower for early grades where we have fewer words
                       listDef.grade <= '5' ? 20 : // Elementary 
                       listDef.grade <= '8' ? 30 : // Middle school
                       15; // High school - lower since we have gaps
      
      console.log(`Creating ${listDef.name}...`);
      console.log(`  Available words: ${wordsForGrade.length}, Minimum needed: ${minWords}`);

      if (wordsForGrade.length < minWords) {
        console.log(`  ⚠️  Insufficient words for ${listDef.name} (need ${minWords}, have ${wordsForGrade.length})`);
        insufficientWords.push({ 
          ...listDef, 
          available: wordsForGrade.length, 
          needed: minWords,
          words: wordsForGrade.slice(0, Math.min(10, wordsForGrade.length)).map(w => w.word)
        });
        continue;
      }

      // Create study list in database
      // Use existing user ID (first user found - for system lists)
      const systemUserId = '2eaf6609-b02d-4d15-8b6d-197056945e31';
      
      const { data: studyList, error: listError } = await supabase
        .from('study_lists')
        .insert({
          name: listDef.name,
          description: listDef.description,
          is_public: true,
          user_id: systemUserId // System-created list
        })
        .select()
        .single();

      if (listError) {
        console.error(`  ❌ Error creating study list: ${listError.message}`);
        continue;
      }

      // Add words to the study list (limit to reasonable number)
      const wordsToAdd = wordsForGrade.slice(0, Math.min(wordsForGrade.length, minWords * 2));
      const studyListItems = wordsToAdd.map(word => ({
        study_list_id: studyList.id,
        item_type: 'spelling_word',
        item_id: word.id.toString(), // Ensure string format
        item_data: {
          word: word.word,
          definition: word.definition,
          spelling_difficulty: word.spelling_difficulty_name,
          vocabulary_difficulty: word.vocabulary_difficulty_name,
          grade_level: listDef.grade,
          order: wordsToAdd.indexOf(word)
        }
      }));

      const { error: itemsError } = await supabase
        .from('study_list_items')
        .insert(studyListItems);

      if (itemsError) {
        console.error(`  ❌ Error adding items to study list: ${itemsError.message}`);
        // Clean up the study list if items couldn't be added
        await supabase.from('study_lists').delete().eq('id', studyList.id);
        continue;
      }

      console.log(`  ✅ Created "${listDef.name}" with ${wordsToAdd.length} words`);
      
      // Show sample words
      const samples = wordsToAdd.slice(0, 5).map(w => w.word);
      console.log(`  Sample words: ${samples.join(', ')}`);
      
      createdLists.push({
        ...listDef,
        id: studyList.id,
        wordCount: wordsToAdd.length,
        sampleWords: samples
      });
      
      // Small delay to avoid overwhelming the database
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    // Summary
    console.log('\n=== SUMMARY ===\n');
    console.log(`Successfully created: ${createdLists.length} study lists`);
    console.log(`Insufficient data for: ${insufficientWords.length} study lists\n`);

    if (createdLists.length > 0) {
      console.log('CREATED STUDY LISTS:');
      createdLists.forEach(list => {
        console.log(`✅ ${list.name}: ${list.wordCount} words`);
      });
    }

    if (insufficientWords.length > 0) {
      console.log('\nINSUFFICIENT DATA FOR:');
      insufficientWords.forEach(list => {
        console.log(`❌ ${list.name}: ${list.available}/${list.needed} words`);
        if (list.words.length > 0) {
          console.log(`   Available words: ${list.words.join(', ')}`);
        }
      });
      
      console.log('\nRECOMMENDATIONS:');
      console.log('1. Add more basic sight words and phonetic words for grades K-2');
      console.log('2. Include more subject-specific vocabulary for grades 4, 8, 10-12');
      console.log('3. Consider sourcing words from grade-level reading lists');
      console.log('4. Add words from state educational standards by grade');
    }

    // Save results for review
    const fs = require('fs');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const resultsFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\grade_level_study_lists_results_${timestamp}.json`;
    
    const results = {
      created: createdLists,
      insufficient: insufficientWords,
      wordDistribution: Object.keys(wordsByGrade).map(grade => ({
        grade,
        count: wordsByGrade[grade].length,
        sampleWords: wordsByGrade[grade].slice(0, 10).map(w => w.word)
      }))
    };
    
    fs.writeFileSync(resultsFile, JSON.stringify(results, null, 2));
    console.log(`\nDetailed results saved to: ${resultsFile}`);

    return results;

  } catch (error) {
    console.error('Failed to create grade level study lists:', error);
  }
}

if (require.main === module) {
  createGradeLevelStudyLists();
}
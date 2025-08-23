const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

async function populateDifficultyLevels() {
  console.log('Populating difficulty level lookup tables...');
  
  try {
    // Check if tables exist first
    console.log('Checking if difficulty level tables exist...');
    
    const { data: spellingCheck, error: spellingCheckError } = await supabase
      .from('spelling_difficulty_levels')
      .select('id')
      .limit(1);
    
    const { data: vocabCheck, error: vocabCheckError } = await supabase
      .from('vocabulary_difficulty_levels')
      .select('id')
      .limit(1);
    
    if (spellingCheckError) {
      console.log('❌ spelling_difficulty_levels table does not exist');
      console.log('Please run the SQL migration script first');
      return;
    }
    
    if (vocabCheckError) {
      console.log('❌ vocabulary_difficulty_levels table does not exist');
      console.log('Please run the SQL migration script first');
      return;
    }
    
    console.log('✓ Both difficulty level tables exist');

    // Populate spelling difficulty levels
    console.log('Populating spelling difficulty levels...');
    const spellingLevels = [
      {
        id: 1,
        name: 'Beginner',
        description: 'Common everyday vocabulary, phonetic spelling, basic patterns',
        grade_equivalent: 'Grades 1-3',
        characteristics: 'friend, because, special'
      },
      {
        id: 2,
        name: 'Elementary',
        description: 'Standard school vocabulary, introduction to silent letters, common prefixes/suffixes',
        grade_equivalent: 'Grades 4-5',
        characteristics: 'beautiful, knowledge, necessary'
      },
      {
        id: 3,
        name: 'Intermediate',
        description: 'Complex patterns, foreign borrowings, multiple syllables, irregular spellings',
        grade_equivalent: 'Grades 6-8',
        characteristics: 'rhythm, conscience, restaurant'
      },
      {
        id: 4,
        name: 'Advanced',
        description: 'Etymology-based spelling, uncommon letter combinations, technical vocabulary',
        grade_equivalent: 'Grades 9-12 (Regional)',
        characteristics: 'pharaoh, silhouette, entrepreneur'
      },
      {
        id: 5,
        name: 'Expert',
        description: 'Championship words, rare etymology, complex linguistic origins',
        grade_equivalent: 'Competition Level',
        characteristics: 'pneumonia, onomatopoeia, schadenfreude'
      }
    ];

    const { error: spellingInsertError } = await supabase
      .from('spelling_difficulty_levels')
      .upsert(spellingLevels, { onConflict: 'id' });
    if (spellingInsertError) throw spellingInsertError;
    console.log('✓ Spelling difficulty levels populated');

    // Populate vocabulary difficulty levels
    console.log('Populating vocabulary difficulty levels...');
    const vocabularyLevels = [
      {
        id: 1,
        name: 'Foundation',
        description: 'Basic everyday concepts',
        characteristics: 'Concrete nouns, simple actions, common adjectives - happy, run, big, house, dog'
      },
      {
        id: 2,
        name: 'Academic',
        description: 'School-level vocabulary',
        characteristics: 'Abstract concepts, academic subjects, formal language - analyze, democracy, ecosystem, literature'
      },
      {
        id: 3,
        name: 'Sophisticated',
        description: 'Advanced academic and professional',
        characteristics: 'Complex abstractions, technical concepts, nuanced meanings - paradigm, synthesize, empirical, rhetoric'
      },
      {
        id: 4,
        name: 'Specialized',
        description: 'Domain-specific terminology',
        characteristics: 'Professional jargon, scientific terms, specialized fields - cytoplasm, jurisprudence, thermodynamics, epistemology'
      },
      {
        id: 5,
        name: 'Scholarly',
        description: 'Research and expert-level',
        characteristics: 'Highly specialized, theoretical concepts, academic discourse - phenomenology, hermeneutics, ontological, epistemic'
      }
    ];

    const { error: vocabInsertError } = await supabase
      .from('vocabulary_difficulty_levels')
      .upsert(vocabularyLevels, { onConflict: 'id' });
    if (vocabInsertError) throw vocabInsertError;
    console.log('✓ Vocabulary difficulty levels populated');

    // Verification
    console.log('\n=== VERIFICATION ===');
    
    const { data: spellingLevelsData } = await supabase
      .from('spelling_difficulty_levels')
      .select('id, name, description')
      .order('id');
      
    const { data: vocabLevelsData } = await supabase
      .from('vocabulary_difficulty_levels')
      .select('id, name, description')
      .order('id');

    console.log('\nSpelling Difficulty Levels:');
    spellingLevelsData?.forEach(level => {
      console.log(`  ${level.id}. ${level.name}: ${level.description}`);
    });

    console.log('\nVocabulary Difficulty Levels:');
    vocabLevelsData?.forEach(level => {
      console.log(`  ${level.id}. ${level.name}: ${level.description}`);
    });

    console.log('\n✓ Difficulty levels population completed successfully!');
    console.log('\nNext steps:');
    console.log('1. Run the SQL script to add foreign key columns to spelling_words');
    console.log('2. Update React components to use the new tables');

  } catch (error) {
    console.error('Population failed:', error);
    throw error;
  }
}

if (require.main === module) {
  populateDifficultyLevels();
}
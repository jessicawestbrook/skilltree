const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

async function runMigration() {
  console.log('Starting difficulty levels normalization migration...');
  console.log('Note: Table creation will be done manually. Focusing on data population...');
  
  try {
    // Skip table creation steps - will need to be done manually via SQL
    console.log('Step 1-3: Skipping table creation (do manually via SQL)...');

    // Step 4: Populate spelling difficulty levels
    console.log('Step 4: Populating spelling difficulty levels...');
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
      .upsert(spellingLevels);
    if (spellingInsertError) throw spellingInsertError;
    console.log('✓ Spelling difficulty levels populated');

    // Step 5: Populate vocabulary difficulty levels
    console.log('Step 5: Populating vocabulary difficulty levels...');
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
      .upsert(vocabularyLevels);
    if (vocabInsertError) throw vocabInsertError;
    console.log('✓ Vocabulary difficulty levels populated');

    console.log('Step 6-8: Skipping schema changes (do manually via SQL)...');

    // Step 9: Verification
    console.log('\n=== VERIFICATION ===');
    
    const { data: spellingCount } = await supabase
      .from('spelling_difficulty_levels')
      .select('*', { count: 'exact', head: true });
    console.log(`Spelling difficulty levels: ${spellingCount}`);

    const { data: vocabCount } = await supabase
      .from('vocabulary_difficulty_levels')
      .select('*', { count: 'exact', head: true });
    console.log(`Vocabulary difficulty levels: ${vocabCount}`);

    const { data: wordsWithSpelling } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .not('spelling_difficulty_id', 'is', null);
    console.log(`Words with spelling difficulty FK: ${wordsWithSpelling}`);

    const { data: wordsWithVocab } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .not('vocabulary_difficulty_id', 'is', null);
    console.log(`Words with vocabulary difficulty FK: ${wordsWithVocab}`);

    // Show sample data
    console.log('\nSpelling Difficulty Levels:');
    const { data: spellingLevelsData } = await supabase
      .from('spelling_difficulty_levels')
      .select('id, name, description')
      .order('id');
    spellingLevelsData?.forEach(level => {
      console.log(`  ${level.id}. ${level.name}: ${level.description}`);
    });

    console.log('\nVocabulary Difficulty Levels:');
    const { data: vocabLevelsData } = await supabase
      .from('vocabulary_difficulty_levels')
      .select('id, name, description')
      .order('id');
    vocabLevelsData?.forEach(level => {
      console.log(`  ${level.id}. ${level.name}: ${level.description}`);
    });

    console.log('\n✓ Difficulty levels normalization completed successfully!');

  } catch (error) {
    console.error('Migration failed:', error);
    throw error;
  }
}

if (require.main === module) {
  runMigration();
}
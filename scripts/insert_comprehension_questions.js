#!/usr/bin/env node

const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: '.env.local' });

// Use service role key to bypass RLS
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
);

async function insertComprehensionQuestions() {
  try {
    // Read the generated questions
    const questionsPath = path.join(__dirname, 'spanish_comprehension_questions.json');
    const questions = JSON.parse(fs.readFileSync(questionsPath, 'utf-8'));
    
    console.log(`Loading ${questions.length} comprehension questions...`);
    
    // First, we need to get the Spanish language ID from the database
    const { data: languages, error: langError } = await supabase
      .from('languages')
      .select('id, name, code')
      .eq('code', 'es')
      .single();
    
    if (langError) {
      console.error('Error fetching Spanish language:', langError);
      return;
    }
    
    console.log(`Found Spanish language with ID: ${languages.id}`);
    
    // Get the Reading & Listening Comprehension category
    const { data: comprehensionCategory, error: catError } = await supabase
      .from('language_categories')
      .select('id')
      .eq('language_id', languages.id)
      .eq('name', 'Reading & Listening Comprehension')
      .single();
    
    if (catError) {
      console.error('Error fetching comprehension category:', catError);
      return;
    }
    
    console.log(`Found comprehension category with ID: ${comprehensionCategory.id}`);
    
    // Transform questions to match database schema
    const dbQuestions = questions.map(q => ({
      language_id: languages.id, // Use actual UUID from database
      category_id: comprehensionCategory.id, // Use the comprehension category ID
      category: q.category,
      question_type: q.question_type || 'multiple_choice',
      difficulty_level: q.difficulty_level,
      question_text: q.question_text,
      options: q.options,
      correct_answer_index: q.correct_answer_index,
      explanation: q.explanation
      // Note: metadata field doesn't exist in the table
    }));
    
    // Insert questions
    console.log('Inserting questions into database...');
    const { data: insertedData, error: insertError } = await supabase
      .from('language_questions')
      .insert(dbQuestions)
      .select();
    
    if (insertError) {
      console.error('Error inserting questions:', insertError);
      return;
    }
    
    console.log(`✓ Successfully inserted ${insertedData.length} comprehension questions`);
    
    // Verify the insertion
    const { data: grammarCount } = await supabase
      .from('language_questions')
      .select('id', { count: 'exact' })
      .eq('language_id', languages.id)
      .eq('category', 'grammar');
    
    const { data: comprehensionCount } = await supabase
      .from('language_questions')
      .select('id', { count: 'exact' })
      .eq('language_id', languages.id)
      .eq('category', 'reading/listening');
    
    console.log('\nSpanish questions distribution:');
    console.log(`- Grammar: ${grammarCount?.length || 0}`);
    console.log(`- Reading/Listening: ${comprehensionCount?.length || 0}`);
    
  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

// Run the insertion
insertComprehensionQuestions();
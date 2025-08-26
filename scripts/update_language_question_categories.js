#!/usr/bin/env node

const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function updateCategories() {
  try {
    console.log('Fetching all language questions...');
    
    // Get all questions
    const { data: questions, error } = await supabase
      .from('language_questions')
      .select('id, language_id, question_text, question_type');
    
    if (error) {
      console.error('Error fetching questions:', error);
      return;
    }
    
    console.log(`Found ${questions.length} questions to categorize`);
    
    // Categorize questions
    const grammarQuestions = [];
    const comprehensionQuestions = []; // For both reading and listening
    
    questions.forEach(q => {
      const text = q.question_text.toLowerCase();
      
      // Reading/listening comprehension indicators
      if (text.includes('read') || 
          text.includes('listen') ||
          text.includes('passage') || 
          text.includes('text') ||
          text.includes('story') ||
          text.includes('article') ||
          text.includes('according to') ||
          text.includes('comprehension') ||
          text.includes('hear') || 
          text.includes('audio') ||
          text.includes('sound')) {
        comprehensionQuestions.push(q.id);
      }
      // Grammar indicators (including basic vocabulary)
      else {
        grammarQuestions.push(q.id);
      }
    });
    
    console.log(`\nCategorization results:`);
    console.log(`- Grammar questions: ${grammarQuestions.length}`);
    console.log(`- Reading/Listening questions: ${comprehensionQuestions.length}`);
    
    // Update in batches
    console.log('\nUpdating categories in database...');
    
    if (grammarQuestions.length > 0) {
      const { error: grammarError } = await supabase
        .from('language_questions')
        .update({ category: 'grammar' })
        .in('id', grammarQuestions);
      
      if (grammarError) {
        console.error('Error updating grammar questions:', grammarError);
      } else {
        console.log(`✓ Updated ${grammarQuestions.length} grammar questions`);
      }
    }
    
    if (comprehensionQuestions.length > 0) {
      const { error: comprehensionError } = await supabase
        .from('language_questions')
        .update({ category: 'reading/listening' })
        .in('id', comprehensionQuestions);
      
      if (comprehensionError) {
        console.error('Error updating reading/listening questions:', comprehensionError);
      } else {
        console.log(`✓ Updated ${comprehensionQuestions.length} reading/listening questions`);
      }
    }
    
    // Verify the update
    console.log('\nVerifying update...');
    const { data: categoryCounts, error: countError } = await supabase
      .from('language_questions')
      .select('category');
    
    if (!countError && categoryCounts) {
      const counts = categoryCounts.reduce((acc, item) => {
        acc[item.category] = (acc[item.category] || 0) + 1;
        return acc;
      }, {});
      
      console.log('\nFinal category distribution:');
      Object.entries(counts).forEach(([category, count]) => {
        console.log(`- ${category}: ${count}`);
      });
    }
    
  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

// Run the update
updateCategories();
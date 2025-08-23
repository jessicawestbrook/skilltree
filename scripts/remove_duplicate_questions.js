const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
);

async function removeDuplicates() {
  try {
    // Find all questions, ordered by creation date
    const { data: allQuestions, error } = await supabase
      .from('questions')
      .select('id, question_text, difficulty, created_at')
      .or('question_text.ilike.%$1.75%,question_text.ilike.%$3.25%')
      .order('created_at', { ascending: true });
    
    if (error) throw error;
    
    console.log('=== DUPLICATE QUESTION ANALYSIS ===\n');
    
    // Group by question text
    const questionGroups = {};
    allQuestions.forEach(q => {
      const text = q.question_text;
      if (!questionGroups[text]) {
        questionGroups[text] = [];
      }
      questionGroups[text].push(q);
    });
    
    // Find duplicates
    const duplicatesToRemove = [];
    Object.entries(questionGroups).forEach(([text, questions]) => {
      if (questions.length > 1) {
        console.log(`Found ${questions.length} copies of: "${text.substring(0, 50)}..."`);
        questions.forEach((q, i) => {
          console.log(`  ${i + 1}. ID: ${q.id}, Difficulty: ${q.difficulty}, Created: ${q.created_at}`);
        });
        
        // Keep the first one (oldest), remove the rest
        for (let i = 1; i < questions.length; i++) {
          duplicatesToRemove.push(questions[i].id);
        }
        console.log(`  Keeping the first one, removing ${questions.length - 1} duplicate(s)\n`);
      }
    });
    
    if (duplicatesToRemove.length > 0) {
      console.log(`\nRemoving ${duplicatesToRemove.length} duplicate questions...`);
      
      for (const id of duplicatesToRemove) {
        const { error: deleteError } = await supabase
          .from('questions')
          .delete()
          .eq('id', id);
        
        if (deleteError) {
          console.error(`Error deleting question ${id}:`, deleteError.message);
        } else {
          console.log(`✅ Deleted duplicate question ID: ${id}`);
        }
      }
    } else {
      console.log('No duplicates found!');
    }
    
    // Final count
    const { count, error: countError } = await supabase
      .from('questions')
      .select('*', { count: 'exact', head: true })
      .or('question_text.ilike.%penny%,question_text.ilike.%nickel%,question_text.ilike.%dime%,question_text.ilike.%quarter%,question_text.ilike.%dollar%,question_text.ilike.%cents%,question_text.ilike.%coins%,question_text.ilike.%$1.75%,question_text.ilike.%$3.25%,question_text.ilike.%$5 bill%');
    
    if (!countError) {
      console.log(`\n=== FINAL COUNT ===`);
      console.log(`Total money counting questions after cleanup: ${count}`);
    }
    
  } catch (error) {
    console.error('Error:', error.message);
  }
  
  process.exit(0);
}

removeDuplicates();
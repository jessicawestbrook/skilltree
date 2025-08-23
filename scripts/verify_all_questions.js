const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
);

async function verifyAllQuestions() {
  try {
    // Get all money-related questions
    const { data: questions, error } = await supabase
      .from('questions')
      .select('question_text, difficulty')
      .or('question_text.ilike.%penny%,question_text.ilike.%nickel%,question_text.ilike.%dime%,question_text.ilike.%quarter%,question_text.ilike.%dollar%,question_text.ilike.%cents%,question_text.ilike.%coins%,question_text.ilike.%$1.75%,question_text.ilike.%$3.25%,question_text.ilike.%$5 bill%')
      .order('created_at', { ascending: true });
    
    if (error) throw error;
    
    console.log('=== ALL MONEY COUNTING QUESTIONS IN DATABASE ===\n');
    console.log(`Total count: ${questions.length}\n`);
    
    // Group by difficulty
    const byDifficulty = {};
    questions.forEach(q => {
      if (!byDifficulty[q.difficulty]) {
        byDifficulty[q.difficulty] = [];
      }
      byDifficulty[q.difficulty].push(q.question_text);
    });
    
    Object.entries(byDifficulty).forEach(([difficulty, qs]) => {
      console.log(`${difficulty.toUpperCase()} (${qs.length} questions):`);
      qs.forEach((q, i) => {
        console.log(`  ${i + 1}. ${q.substring(0, 70)}${q.length > 70 ? '...' : ''}`);
      });
      console.log();
    });
    
    // Check for the specific questions that were failing
    const specificQuestions = [
      'You have $1.75',
      'You buy a toy for $3.25'
    ];
    
    console.log('=== VERIFICATION OF PREVIOUSLY FAILED QUESTIONS ===');
    specificQuestions.forEach(searchText => {
      const found = questions.find(q => q.question_text.includes(searchText));
      if (found) {
        console.log(`✅ "${searchText}..." - FOUND (difficulty: ${found.difficulty})`);
      } else {
        console.log(`❌ "${searchText}..." - NOT FOUND`);
      }
    });
    
  } catch (error) {
    console.error('Error:', error.message);
  }
  
  process.exit(0);
}

verifyAllQuestions();
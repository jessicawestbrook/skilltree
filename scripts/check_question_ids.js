const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
);

async function checkQuestionIds() {
  try {
    // Check Money Counting learning content
    const { data: content, error } = await supabase
      .from('learning_content')
      .select('id, title, question_ids')
      .eq('id', 1991)
      .single();
    
    if (error) throw error;
    
    console.log('=== MONEY COUNTING LEARNING CONTENT ===');
    console.log('ID:', content.id);
    console.log('Title:', content.title);
    console.log('question_ids field:', content.question_ids);
    console.log('Has question_ids:', content.question_ids !== null && content.question_ids !== undefined);
    console.log('Question IDs count:', content.question_ids?.length || 0);
    
    if (!content.question_ids || content.question_ids.length === 0) {
      console.log('\n⚠️  NO QUESTION IDS LINKED TO LEARNING CONTENT!');
      console.log('This is why the site cannot find questions for this content.');
      
      // Get all money counting questions to link
      const { data: questions, error: qError } = await supabase
        .from('questions')
        .select('id')
        .or('question_text.ilike.%penny%,question_text.ilike.%nickel%,question_text.ilike.%dime%,question_text.ilike.%quarter%,question_text.ilike.%dollar%,question_text.ilike.%cents%,question_text.ilike.%coins%,question_text.ilike.%money%');
      
      if (!qError && questions) {
        console.log(`\nFound ${questions.length} money counting questions that need to be linked.`);
        console.log('Question IDs to link:', questions.map(q => q.id));
      }
    }
    
  } catch (error) {
    console.error('Error:', error.message);
  }
  
  process.exit(0);
}

checkQuestionIds();
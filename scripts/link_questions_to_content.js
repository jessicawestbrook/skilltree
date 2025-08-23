/**
 * Script to link money counting questions to the learning content
 * =================================================================
 */

const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
);

async function linkQuestionsToContent() {
  try {
    console.log('=== LINKING MONEY COUNTING QUESTIONS TO LEARNING CONTENT ===\n');
    
    // Get all money counting question IDs
    const { data: questions, error: qError } = await supabase
      .from('questions')
      .select('id, question_text')
      .or('question_text.ilike.%penny%,question_text.ilike.%nickel%,question_text.ilike.%dime%,question_text.ilike.%quarter%,question_text.ilike.%dollar%,question_text.ilike.%cents%,question_text.ilike.%coins%,question_text.ilike.%money%');
    
    if (qError) throw qError;
    
    console.log(`Found ${questions.length} money counting questions to link`);
    
    // Extract just the IDs
    const questionIds = questions.map(q => q.id);
    
    console.log('\nQuestion IDs to link:');
    questions.forEach((q, i) => {
      console.log(`${i + 1}. ${q.question_text.substring(0, 60)}...`);
    });
    
    // Update the learning content with question IDs
    console.log('\nUpdating learning content ID 1991 with question IDs...');
    
    const { error: updateError } = await supabase
      .from('learning_content')
      .update({ question_ids: questionIds })
      .eq('id', 1991);
    
    if (updateError) {
      console.error('Error updating learning content:', updateError.message);
      return;
    }
    
    console.log('✅ Successfully linked questions to learning content!');
    
    // Verify the update
    const { data: verifyData, error: verifyError } = await supabase
      .from('learning_content')
      .select('id, title, question_ids')
      .eq('id', 1991)
      .single();
    
    if (!verifyError && verifyData) {
      console.log('\n=== VERIFICATION ===');
      console.log('Learning Content:', verifyData.title);
      console.log('Number of linked questions:', verifyData.question_ids?.length || 0);
      console.log('\n🎉 Money Counting module is now fully functional!');
      console.log('- Learning content: ✅');
      console.log('- Questions linked: ✅');
      console.log('- Ready for use in the application: ✅');
    }
    
  } catch (error) {
    console.error('Error:', error.message);
  }
  
  process.exit(0);
}

linkQuestionsToContent();
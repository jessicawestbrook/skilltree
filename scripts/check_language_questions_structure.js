const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkStructure() {
  try {
    // Check a sample of language questions
    const { data, error } = await supabase
      .from('language_questions')
      .select('id, language_id, category_id, question_type, question_text')
      .limit(10);
    
    if (error) {
      console.error('Error fetching questions:', error);
      return;
    }
    
    console.log('Sample language questions:');
    data.forEach(q => {
      console.log(`- Language: ${q.language_id}, Category: ${q.category_id}, Type: ${q.question_type}`);
      console.log(`  Text: ${q.question_text.substring(0, 50)}...`);
    });
    
    // Check distinct categories
    const { data: categories, error: catError } = await supabase
      .from('language_questions')
      .select('category_id')
      .not('category_id', 'is', null);
    
    if (!catError && categories) {
      const uniqueCategories = [...new Set(categories.map(c => c.category_id))];
      console.log('\nUnique category_ids in use:', uniqueCategories);
    }
    
    // Count nulls
    const { count: totalCount } = await supabase
      .from('language_questions')
      .select('*', { count: 'exact', head: true });
      
    const { count: nullCount } = await supabase
      .from('language_questions')
      .select('*', { count: 'exact', head: true })
      .is('category_id', null);
    
    console.log(`\nTotal questions: ${totalCount}`);
    console.log(`Questions with null category_id: ${nullCount}`);
    
  } catch (error) {
    console.error('Error:', error);
  }
}

checkStructure();

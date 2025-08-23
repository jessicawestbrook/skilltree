const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function testStarredItemsDisplay() {
  console.log('Testing Starred Items Display Functionality\n');
  console.log('=' .repeat(50));

  try {
    // Test 1: Check if starred_items table is accessible
    console.log('\n1. Testing starred_items table access...');
    const { data: starredItems, error: starredError } = await supabase
      .from('starred_items')
      .select('*')
      .limit(5);

    if (starredError) {
      console.error('❌ Error accessing starred_items:', starredError);
    } else {
      console.log('✅ Successfully accessed starred_items table');
      console.log(`   Found ${starredItems?.length || 0} starred items`);
    }

    // Test 2: Check if skill_tree_nodes has required columns
    console.log('\n2. Testing skill_tree_nodes columns...');
    const { data: nodeData, error: nodeError } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, learning_area, type, path')
      .limit(1);

    if (nodeError) {
      console.error('❌ Error accessing skill_tree_nodes:', nodeError);
    } else {
      console.log('✅ Successfully accessed skill_tree_nodes with all columns');
      if (nodeData && nodeData[0]) {
        console.log('   Sample node:', {
          name: nodeData[0].name,
          learning_area: nodeData[0].learning_area || 'NOT SET',
          type: nodeData[0].type || 'NOT SET',
          path: nodeData[0].path || 'NOT SET'
        });
      }
    }

    // Test 3: Check if spelling_words table has RLS enabled
    console.log('\n3. Testing spelling_words table access...');
    const { data: spellingData, error: spellingError } = await supabase
      .from('spelling_words')
      .select('id, word, definition, difficulty')
      .limit(1);

    if (spellingError) {
      console.error('❌ Error accessing spelling_words:', spellingError);
    } else {
      console.log('✅ Successfully accessed spelling_words table');
      if (spellingData && spellingData[0]) {
        console.log('   Sample word:', spellingData[0].word);
      }
    }

    // Test 4: Check if language_questions table has RLS enabled
    console.log('\n4. Testing language_questions table access...');
    const { data: langData, error: langError } = await supabase
      .from('language_questions')
      .select('id, question, language, category')
      .limit(1);

    if (langError) {
      console.error('❌ Error accessing language_questions:', langError);
    } else {
      console.log('✅ Successfully accessed language_questions table');
      if (langData && langData[0]) {
        console.log('   Sample question language:', langData[0].language);
      }
    }

    // Test 5: Check user_progress with foreign key join
    console.log('\n5. Testing user_progress with node details...');
    const { data: progressData, error: progressError } = await supabase
      .from('user_progress')
      .select(`
        *,
        skill_tree_nodes:node_id (
          id,
          name,
          learning_area,
          description
        )
      `)
      .limit(1);

    if (progressError) {
      console.error('❌ Error accessing user_progress with joins:', progressError);
    } else {
      console.log('✅ Successfully accessed user_progress with node details');
      if (progressData && progressData[0] && progressData[0].skill_tree_nodes) {
        console.log('   Node name in progress:', progressData[0].skill_tree_nodes.name);
      }
    }

    console.log('\n' + '=' .repeat(50));
    console.log('Testing complete!');
    console.log('\nNext steps:');
    console.log('1. If you see errors above, run the SQL scripts in Supabase:');
    console.log('   - scripts/fix_database_tables.sql');
    console.log('   - scripts/fix_table_columns_and_rls.sql');
    console.log('2. Visit http://localhost:3000 and log in');
    console.log('3. Navigate to your profile page');
    console.log('4. Check if starred items are displayed correctly');

  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

testStarredItemsDisplay();
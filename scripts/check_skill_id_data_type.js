const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error('Missing Supabase credentials');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function checkSkillIdDataType() {
  console.log('Checking skill_id data types...\n');

  // Check column information
  const { data: columnInfo, error: columnError } = await supabase
    .rpc('get_column_info', { 
      p_table_name: 'user_progress',
      p_column_name: 'skill_id'
    })
    .single();

  if (columnError) {
    // Try a direct query approach
    console.log('Checking user_progress table structure...');
    
    // Get sample data
    const { data: sampleData, error: sampleError } = await supabase
      .from('user_progress')
      .select('skill_id, user_id')
      .limit(5);

    if (sampleError) {
      console.error('Error fetching sample data:', sampleError);
    } else {
      console.log('Sample skill_id values from user_progress:');
      sampleData.forEach(row => {
        console.log(`  skill_id: ${row.skill_id} (type: ${typeof row.skill_id})`);
      });
    }

    // Check if skill_id values look like UUIDs
    const { data: allData, error: allError } = await supabase
      .from('user_progress')
      .select('skill_id')
      .not('skill_id', 'is', null)
      .limit(100);

    if (!allError && allData) {
      const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
      const validUuids = allData.filter(row => uuidPattern.test(row.skill_id));
      
      console.log(`\nUUID format check:`);
      console.log(`  Total rows checked: ${allData.length}`);
      console.log(`  Valid UUID format: ${validUuids.length}`);
      console.log(`  Invalid format: ${allData.length - validUuids.length}`);
      
      if (allData.length > validUuids.length) {
        console.log('\nSample invalid values:');
        allData.filter(row => !uuidPattern.test(row.skill_id))
          .slice(0, 5)
          .forEach(row => console.log(`  ${row.skill_id}`));
      }
    }
  } else {
    console.log('Column info:', columnInfo);
  }

  // Check starred_categories table
  console.log('\n\nChecking starred_categories table...');
  const { data: starredSample, error: starredError } = await supabase
    .from('starred_categories')
    .select('skill_id, user_id')
    .limit(5);

  if (!starredError && starredSample) {
    console.log('Sample skill_id values from starred_categories:');
    starredSample.forEach(row => {
      console.log(`  skill_id: ${row.skill_id} (type: ${typeof row.skill_id})`);
    });
  }

  // Check assessment_sessions table
  console.log('\n\nChecking assessment_sessions table (category_id column)...');
  const { data: assessmentSample, error: assessmentError } = await supabase
    .from('assessment_sessions')
    .select('category_id, user_id')
    .limit(5);

  if (!assessmentError && assessmentSample) {
    console.log('Sample category_id values from assessment_sessions:');
    assessmentSample.forEach(row => {
      console.log(`  category_id: ${row.category_id} (type: ${typeof row.category_id})`);
    });
  }

  process.exit(0);
}

checkSkillIdDataType().catch(console.error);
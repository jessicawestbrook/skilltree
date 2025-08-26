const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkCourseChildren() {
  console.log('Checking Henle Latin: First Year for children/modules...\n');
  
  const courseId = 'cebb7f42-e51b-4ac4-8464-29fee0894024';
  
  // Check for children nodes (modules/lessons)
  const { data: children, error } = await supabase
    .from('skill_tree_nodes')
    .select('*')
    .eq('parent_id', courseId)
    .order('display_order');
  
  if (error) {
    console.log('Error:', error);
    return;
  }
  
  console.log(`Found ${children?.length || 0} children for Henle Latin: First Year`);
  
  if (children && children.length > 0) {
    console.log('\nChildren (modules/lessons):');
    children.forEach(child => {
      console.log(`  - ${child.name} (order: ${child.display_order})`);
      console.log(`    Has content: ${child.learning_content_ids?.length > 0}`);
    });
  } else {
    console.log('\n⚠️  No children found - course has no modules/lessons yet');
  }
  
  // Check if course_modules table exists
  console.log('\n\nChecking course_modules table...');
  const { data: modules, error: modError } = await supabase
    .from('course_modules')
    .select('*')
    .eq('course_id', courseId)
    .limit(5);
  
  if (modError) {
    console.log('❌ course_modules table error:', modError.message);
  } else {
    console.log(`✅ course_modules table exists, found ${modules?.length || 0} modules`);
  }
  
  process.exit(0);
}

checkCourseChildren();
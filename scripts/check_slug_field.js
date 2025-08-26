const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkSlugField() {
  console.log('Checking for slug field in skill_tree_nodes...\n');
  
  // Get a sample node to check its structure
  const { data: sample, error } = await supabase
    .from('skill_tree_nodes')
    .select('*')
    .eq('name', 'Henle Latin: First Year')
    .single();
  
  if (error) {
    console.log('Error:', error);
    return;
  }
  
  console.log('Sample node (Henle Latin: First Year):');
  console.log('Fields available:', Object.keys(sample));
  console.log('\nFull record:');
  console.log(JSON.stringify(sample, null, 2));
  
  // Check if slug field exists
  if ('slug' in sample) {
    console.log('\n✅ Slug field exists! Value:', sample.slug);
  } else {
    console.log('\n❌ No slug field found');
  }
  
  // Check other Latin courses
  const { data: latinCourses } = await supabase
    .from('skill_tree_nodes')
    .select('id, name, slug')
    .eq('parent_id', 'b91a46fa-6e1e-48e0-acdd-4360393058b8') // Latin under Languages
    .ilike('name', 'Henle Latin%');
  
  console.log('\n📚 Latin courses with slug field:');
  latinCourses?.forEach(course => {
    console.log(`  ${course.name}: slug = ${course.slug || 'NOT SET'}`);
  });
  
  process.exit(0);
}

checkSlugField();
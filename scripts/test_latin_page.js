const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function testLatinPageLogic() {
  console.log('Testing Latin Language page course detection logic...\n');
  
  const latinSkillId = 'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8';
  
  // 1. Fetch the Latin Language node (as CategoryPage does)
  const { data: categoryData, error: catError } = await supabase
    .from('skill_tree_nodes')
    .select('*')
    .eq('id', latinSkillId)
    .single();
  
  if (catError) {
    console.log('❌ Error fetching Latin Language node:', catError);
    return;
  }
  
  console.log('✅ Latin Language Node:');
  console.log('   Name:', categoryData.name);
  console.log('   ID:', categoryData.id);
  console.log('   Parent ID:', categoryData.parent_id);
  
  // 2. Fetch children (as CategoryPage does)
  const { data: subcategoriesData, error: subError } = await supabase
    .from('skill_tree_nodes')
    .select('*')
    .eq('parent_id', latinSkillId)
    .eq('is_hidden', false)
    .order('display_order', { nullsFirst: false })
    .order('name');
  
  if (subError) {
    console.log('❌ Error fetching children:', subError);
    return;
  }
  
  console.log('\n📚 Children of Latin Language:');
  console.log('   Total found:', subcategoriesData?.length || 0);
  
  if (subcategoriesData && subcategoriesData.length > 0) {
    subcategoriesData.forEach(node => {
      console.log(`\n   Child: ${node.name}`);
      console.log(`   - ID: ${node.id}`);
      console.log(`   - Display Order: ${node.display_order}`);
      console.log(`   - Metadata:`, JSON.stringify(node.metadata));
      console.log(`   - Has textbook metadata:`, !!node.metadata?.textbook);
      console.log(`   - Has year metadata:`, !!node.metadata?.year);
      console.log(`   - Name includes 'Year':`, node.name.includes('Year'));
      console.log(`   - Name includes 'Henle':`, node.name.includes('Henle'));
    });
  }
  
  // 3. Test the detection logic
  console.log('\n🔍 Testing Course Detection Logic:');
  
  const isSkillWithCourses = 
    // Check by skill name patterns
    (categoryData.name.includes('Language') || 
     categoryData.name.includes('Programming') || 
     categoryData.name.includes('Mathematics')) ||
    // Or check if all/most children are courses
    (subcategoriesData.length > 0 && subcategoriesData.every(node => 
      node.metadata?.textbook || 
      node.metadata?.year || 
      node.metadata?.course_type ||
      node.metadata?.chapters ||
      node.name.match(/Year|Course|Level|Module|Part|Chapter|Unit|Lesson|Henle/i)
    ));
  
  console.log('   Is skill with courses?', isSkillWithCourses);
  console.log('   Name includes "Language"?', categoryData.name.includes('Language'));
  console.log('   All children look like courses?', 
    subcategoriesData.every(node => 
      node.metadata?.textbook || 
      node.metadata?.year || 
      node.name.match(/Year|Course|Level|Module|Part|Chapter|Unit|Lesson|Henle/i)
    )
  );
  
  if (isSkillWithCourses && subcategoriesData.length > 0) {
    console.log('\n✅ COURSES SHOULD BE DISPLAYED:');
    subcategoriesData.forEach(course => {
      console.log(`   - ${course.name}`);
    });
  } else {
    console.log('\n❌ Courses would NOT be displayed');
    console.log('   Reason: Detection logic failed');
  }
  
  process.exit(0);
}

testLatinPageLogic();
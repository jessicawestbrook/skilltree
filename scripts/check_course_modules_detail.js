const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkCourseModulesDetail() {
  console.log('Checking course_modules table in detail...\n');
  
  // Get all course modules
  const { data: modules, error } = await supabase
    .from('course_modules')
    .select('*')
    .order('course_id')
    .limit(20);
  
  if (error) {
    console.log('Error:', error);
    return;
  }
  
  console.log(`Found ${modules?.length || 0} total modules\n`);
  
  // Group by course_id
  const courseGroups = {};
  modules?.forEach(mod => {
    if (!courseGroups[mod.course_id]) {
      courseGroups[mod.course_id] = [];
    }
    courseGroups[mod.course_id].push(mod);
  });
  
  // Display grouped modules
  for (const [courseId, courseMods] of Object.entries(courseGroups)) {
    console.log(`\n📚 Course ID: ${courseId}`);
    console.log(`   Modules (${courseMods.length}):`);
    courseMods.forEach(mod => {
      console.log(`   - Chapter ${mod.chapter_number}: ${mod.title}`);
      console.log(`     Type: ${mod.module_type}, Order: ${mod.display_order}`);
    });
    
    // Try to find the course name
    const { data: course } = await supabase
      .from('courses')
      .select('name')
      .eq('id', courseId)
      .single();
    
    if (course) {
      console.log(`   Course name in courses table: ${course.name}`);
    }
    
    // Also check if this ID exists in skill_tree_nodes
    const { data: node } = await supabase
      .from('skill_tree_nodes')
      .select('name')
      .eq('id', courseId)
      .single();
    
    if (node) {
      console.log(`   ✅ Also exists in skill_tree_nodes as: ${node.name}`);
    }
  }
  
  process.exit(0);
}

checkCourseModulesDetail();
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkLatinCourses() {
  try {
    console.log('Checking Latin Language skill and its courses...\n');
    
    // 1. Find Latin Language skill node
    const { data: latinSkill, error: skillError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .eq('id', 'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8')
      .single();
    
    if (skillError || !latinSkill) {
      console.log('❌ Latin Language skill not found');
      return;
    }
    
    console.log('✅ Latin Language Skill:');
    console.log('   ID:', latinSkill.id);
    console.log('   Name:', latinSkill.name);
    console.log('   Parent ID:', latinSkill.parent_id);
    
    // 2. Find courses under Latin Language skill
    console.log('\n📚 Fetching courses under Latin Language...');
    const { data: courses, error: coursesError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .eq('parent_id', 'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8')
      .order('display_order');
    
    if (coursesError) {
      console.log('❌ Error fetching courses:', coursesError);
      return;
    }
    
    if (!courses || courses.length === 0) {
      console.log('❌ No courses found under Latin Language skill');
      console.log('\n⚠️  This is the problem - the course nodes were not created!');
      console.log('Need to run: scripts/fix_latin_courses_as_nodes.sql');
    } else {
      console.log(`✅ Found ${courses.length} courses:`);
      courses.forEach(course => {
        console.log(`\n   Course: ${course.name}`);
        console.log(`   ID: ${course.id}`);
        console.log(`   Display Order: ${course.display_order}`);
        console.log(`   Metadata:`, course.metadata);
      });
    }
    
    // 3. Check learning_path_courses references
    console.log('\n🔗 Checking learning_path_courses references...');
    const courseIds = [
      'cebb7f42-e51b-4ac4-8464-29fee0894024',
      'b1661d5c-7e1f-44a9-bbb4-17265e521670',
      'b72b43fa-c306-40da-b7a1-bfd46990cb80'
    ];
    
    for (const id of courseIds) {
      const { data: node } = await supabase
        .from('skill_tree_nodes')
        .select('name')
        .eq('id', id)
        .single();
      
      if (node) {
        console.log(`   ✅ ${id.substring(0, 8)}... exists as: ${node.name}`);
      } else {
        console.log(`   ❌ ${id.substring(0, 8)}... NOT FOUND`);
      }
    }
    
    // 4. Check the parent of Latin Language (to verify it's a skill under a category)
    if (latinSkill.parent_id) {
      const { data: parent } = await supabase
        .from('skill_tree_nodes')
        .select('name, parent_id')
        .eq('id', latinSkill.parent_id)
        .single();
      
      if (parent) {
        console.log('\n📂 Latin Language Parent:');
        console.log('   Name:', parent.name);
        console.log('   Is Category:', parent.parent_id ? 'No (has parent)' : 'Maybe (no parent)');
      }
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
  
  process.exit(0);
}

checkLatinCourses();
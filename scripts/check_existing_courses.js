const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkExistingCourses() {
  try {
    console.log('Investigating existing course structure...\n');
    
    // Get the course IDs from learning_path_courses
    const courseIds = [
      'cebb7f42-e51b-4ac4-8464-29fee0894024',
      'b1661d5c-7e1f-44a9-bbb4-17265e521670',
      'b72b43fa-c306-40da-b7a1-bfd46990cb80'
    ];
    
    console.log('Course IDs found in learning_path_courses table:');
    courseIds.forEach(id => console.log('  -', id));
    
    // Check if these exist in skill_tree_nodes (maybe courses are stored there?)
    console.log('\n1. Checking if course IDs are in skill_tree_nodes...');
    const { data: nodes, error: nodesError } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, description, parent_id')
      .in('id', courseIds);
    
    if (!nodesError && nodes && nodes.length > 0) {
      console.log('✅ Found courses in skill_tree_nodes table!');
      nodes.forEach(node => {
        console.log(`\n   Course/Node: ${node.name}`);
        console.log(`   ID: ${node.id}`);
        console.log(`   Parent ID: ${node.parent_id || 'None'}`);
        console.log(`   Description: ${node.description?.substring(0, 100)}...`);
      });
      
      // Check if these have a common parent (which would be the skill)
      if (nodes[0].parent_id) {
        console.log('\n2. Checking parent node (skill)...');
        const { data: parent, error: parentError } = await supabase
          .from('skill_tree_nodes')
          .select('id, name, description, parent_id')
          .eq('id', nodes[0].parent_id)
          .single();
        
        if (!parentError && parent) {
          console.log('   Parent (Skill):', parent.name);
          console.log('   Parent ID:', parent.id);
          console.log('   Parent\'s Parent:', parent.parent_id || 'Root');
        }
      }
    } else {
      console.log('❌ Course IDs not found in skill_tree_nodes');
    }
    
    // Check learning_content table
    console.log('\n3. Checking if courses have learning_content...');
    const { data: content, error: contentError } = await supabase
      .from('learning_content')
      .select('id, title, content')
      .in('id', courseIds)
      .limit(3);
    
    if (!contentError && content && content.length > 0) {
      console.log('✅ Found learning content with course IDs');
      content.forEach(c => {
        console.log(`   - ${c.title}`);
      });
    } else {
      console.log('❌ No learning content found with these IDs');
    }
    
    // Check latin_learning_modules table
    console.log('\n4. Checking for latin_learning_modules table...');
    const { data: latinModules, error: latinError } = await supabase
      .from('latin_learning_modules')
      .select('*')
      .limit(3);
    
    if (!latinError) {
      console.log('✅ latin_learning_modules table exists');
      if (latinModules && latinModules.length > 0) {
        console.log('   Columns:', Object.keys(latinModules[0]));
        console.log('   Sample module:', {
          id: latinModules[0].id,
          title: latinModules[0].title || latinModules[0].name,
          course_id: latinModules[0].course_id || 'N/A'
        });
      }
    } else {
      console.log('❌ latin_learning_modules not found');
    }
    
    // Check latin_course_modules table
    console.log('\n5. Checking for latin_course_modules table...');
    const { data: courseModules, error: cmError } = await supabase
      .from('latin_course_modules')
      .select('*')
      .limit(3);
    
    if (!cmError) {
      console.log('✅ latin_course_modules table exists');
      if (courseModules && courseModules.length > 0) {
        console.log('   Columns:', Object.keys(courseModules[0]));
      }
    } else {
      console.log('❌ latin_course_modules not found');
    }
    
    console.log('\n' + '='.repeat(60));
    console.log('CURRENT STRUCTURE ANALYSIS:');
    console.log('='.repeat(60));
    
    if (!nodesError && nodes && nodes.length > 0) {
      console.log('\n📊 CURRENT IMPLEMENTATION:');
      console.log('   - Courses are stored as skill_tree_nodes');
      console.log('   - learning_path_courses links to these nodes');
      console.log('   - Each "course" node has a parent (the skill)');
      console.log('\n⚠️  This means courses ARE already tied to skills!');
      console.log('   They\'re just stored in skill_tree_nodes table');
      console.log('   with their parent_id pointing to the skill node');
      
      console.log('\n✅ NO NEED for separate courses table!');
      console.log('   The structure already supports:');
      console.log('   - Courses tied to skills (via parent_id)');
      console.log('   - Learning paths with multiple courses');
      console.log('   - Courses from different skills in one path');
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
  
  process.exit(0);
}

checkExistingCourses();
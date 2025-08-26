const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function verifyCourseStructure() {
  try {
    console.log('Verifying Course Structure Implementation\n');
    console.log('=' .repeat(50));
    
    // Check if courses table exists
    console.log('\n1. Checking for courses table...');
    const { data: coursesCheck, error: coursesError } = await supabase
      .from('courses')
      .select('id, name, skill_node_id')
      .limit(1);
    
    if (coursesError) {
      console.log('❌ Courses table does not exist yet');
      console.log('   Need to run: scripts/create_courses_structure.sql');
    } else {
      console.log('✅ Courses table exists');
      if (coursesCheck && coursesCheck.length > 0) {
        console.log('   Sample course:', coursesCheck[0]);
      }
    }
    
    // Check if learning_path_courses table exists
    console.log('\n2. Checking for learning_path_courses junction table...');
    const { data: junctionCheck, error: junctionError } = await supabase
      .from('learning_path_courses')
      .select('*')
      .limit(1);
    
    if (junctionError) {
      console.log('❌ Junction table does not exist yet');
    } else {
      console.log('✅ Junction table exists');
    }
    
    // Check if user_course_progress table exists
    console.log('\n3. Checking for user_course_progress table...');
    const { data: progressCheck, error: progressError } = await supabase
      .from('user_course_progress')
      .select('*')
      .limit(1);
    
    if (progressError) {
      console.log('❌ User course progress table does not exist yet');
    } else {
      console.log('✅ User course progress table exists');
    }
    
    // Show the new data model
    console.log('\n' + '=' .repeat(50));
    console.log('NEW DATA MODEL STRUCTURE');
    console.log('=' .repeat(50));
    
    console.log('\n📚 COURSES');
    console.log('   - Each course is tied to ONE skill_node_id');
    console.log('   - Courses contain the actual learning content');
    console.log('   - Example: "Henle Latin Year 1" → Latin Language skill');
    
    console.log('\n🛤️ LEARNING PATHS');
    console.log('   - Learning paths are collections of courses');
    console.log('   - Can contain courses from DIFFERENT skill nodes');
    console.log('   - Example: "Complete Language Learning Path" could include:');
    console.log('     • Latin Grammar (Latin skill)');
    console.log('     • Spanish Vocabulary (Spanish skill)');
    console.log('     • Language History (Linguistics skill)');
    
    console.log('\n🔗 RELATIONSHIPS');
    console.log('   learning_paths ←→ learning_path_courses ←→ courses → skill_tree_nodes');
    console.log('   - Many-to-many between learning_paths and courses');
    console.log('   - One-to-many between skill_nodes and courses');
    
    console.log('\n' + '=' .repeat(50));
    console.log('SQL TO EXECUTE');
    console.log('=' .repeat(50));
    
    const sqlFile = path.join(__dirname, 'create_courses_structure.sql');
    if (fs.existsSync(sqlFile)) {
      console.log('\n📄 File: scripts/create_courses_structure.sql');
      console.log('\nThis SQL will:');
      console.log('1. Create the courses table (each course tied to a skill)');
      console.log('2. Create learning_path_courses junction table');
      console.log('3. Create user_course_progress tracking table');
      console.log('4. Set up proper indexes and RLS policies');
      console.log('5. Migrate existing Latin course data');
      console.log('6. Create helpful views for querying');
      
      console.log('\n🚀 TO EXECUTE:');
      console.log('1. Go to Supabase Dashboard → SQL Editor');
      console.log('2. Copy contents of scripts/create_courses_structure.sql');
      console.log('3. Paste and click "Run"');
    }
    
    console.log('\n' + '=' .repeat(50));
    console.log('BENEFITS OF THIS STRUCTURE');
    console.log('=' .repeat(50));
    console.log('\n✅ Flexibility: Learning paths can combine courses from any skills');
    console.log('✅ Clarity: Each course clearly belongs to one skill area');
    console.log('✅ Reusability: Same course can be in multiple learning paths');
    console.log('✅ Progress Tracking: Track progress per course, not just per path');
    console.log('✅ Scalability: Easy to add new courses and paths independently');
    
  } catch (error) {
    console.error('Error:', error);
  }
  
  process.exit(0);
}

verifyCourseStructure();
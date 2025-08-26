const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkCoursesTables() {
  console.log('Checking courses table structure and data...\n');
  
  // Check if courses table exists and has data
  const { data: courses, error: coursesError } = await supabase
    .from('courses')
    .select('id, name, skill_node_id')
    .limit(5);
  
  if (coursesError) {
    console.log('❌ courses table error:', coursesError.message);
  } else {
    console.log('✅ courses table exists');
    console.log('   Sample courses:', courses?.length || 0, 'found');
    if (courses && courses.length > 0) {
      courses.forEach(c => {
        console.log('   -', c.name, '(skill_node_id:', c.skill_node_id, ')');
      });
    }
  }
  
  // Check courses for Latin Language skill specifically
  if (!coursesError) {
    const latinSkillId = 'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8';
    const { data: latinCourses, error: latinError } = await supabase
      .from('courses')
      .select('*')
      .eq('skill_node_id', latinSkillId);
    
    console.log('\n📚 Courses for Latin Language skill:');
    if (latinError) {
      console.log('   Error:', latinError.message);
    } else {
      console.log('   Found', latinCourses?.length || 0, 'courses');
      latinCourses?.forEach(c => {
        console.log('   -', c.name);
      });
    }
  }
  
  process.exit(0);
}

checkCoursesTables();
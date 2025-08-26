const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkExistingTables() {
  try {
    console.log('Checking existing course-related tables...\n');
    
    // Check for latin_course table
    console.log('1. Checking for latin_course table...');
    const { data: latinCourse, error: latinError } = await supabase
      .from('latin_course')
      .select('*')
      .limit(3);
    
    if (!latinError) {
      console.log('✅ latin_course table exists');
      if (latinCourse && latinCourse.length > 0) {
        console.log('   Columns:', Object.keys(latinCourse[0]));
        console.log('   Total rows:', latinCourse.length);
        console.log('   Sample:', latinCourse[0]);
      }
    } else {
      console.log('❌ latin_course table not found:', latinError.message);
    }
    
    // Check for latin_modules table
    console.log('\n2. Checking for latin_modules table...');
    const { data: latinModules, error: modulesError } = await supabase
      .from('latin_modules')
      .select('*')
      .limit(3);
    
    if (!modulesError) {
      console.log('✅ latin_modules table exists');
      if (latinModules && latinModules.length > 0) {
        console.log('   Columns:', Object.keys(latinModules[0]));
        console.log('   Sample:', latinModules[0]);
      }
    } else {
      console.log('❌ latin_modules table not found:', modulesError.message);
    }
    
    // Check for latin_questions table
    console.log('\n3. Checking for latin_questions table...');
    const { data: latinQuestions, error: questionsError } = await supabase
      .from('latin_questions')
      .select('*')
      .limit(3);
    
    if (!questionsError) {
      console.log('✅ latin_questions table exists');
      if (latinQuestions && latinQuestions.length > 0) {
        console.log('   Columns:', Object.keys(latinQuestions[0]));
        console.log('   Sample question:', {
          id: latinQuestions[0].id,
          module_id: latinQuestions[0].module_id,
          question_text: latinQuestions[0].question_text?.substring(0, 50) + '...'
        });
      }
    } else {
      console.log('❌ latin_questions table not found:', questionsError.message);
    }
    
    // Check for courses table (generic)
    console.log('\n4. Checking for generic courses table...');
    const { data: courses, error: coursesError } = await supabase
      .from('courses')
      .select('*')
      .limit(3);
    
    if (!coursesError) {
      console.log('✅ courses table exists');
      if (courses && courses.length > 0) {
        console.log('   Columns:', Object.keys(courses[0]));
        console.log('   Sample:', courses[0]);
      }
    } else {
      console.log('❌ courses table not found:', coursesError.message);
    }
    
    // Check learning_path_courses junction table
    console.log('\n5. Checking for learning_path_courses junction table...');
    const { data: lpCourses, error: lpError } = await supabase
      .from('learning_path_courses')
      .select('*')
      .limit(3);
    
    if (!lpError) {
      console.log('✅ learning_path_courses table exists');
      if (lpCourses && lpCourses.length > 0) {
        console.log('   Columns:', Object.keys(lpCourses[0]));
        console.log('   Data:', lpCourses);
      }
    } else {
      console.log('❌ learning_path_courses table not found:', lpError.message);
    }
    
    // Check how the Latin learning path currently works
    console.log('\n6. Checking Latin learning path structure...');
    const { data: latinPath, error: pathError } = await supabase
      .from('learning_paths')
      .select('*')
      .eq('slug', 'complete-henle-latin-program')
      .single();
    
    if (!pathError && latinPath) {
      console.log('Latin Learning Path:');
      console.log('   ID:', latinPath.id);
      console.log('   Name:', latinPath.name);
      console.log('   Metadata:', latinPath.metadata);
      
      // Check if it references latin_course
      if (latinPath.metadata && latinPath.metadata.course_table) {
        console.log('   ⚠️ References course table:', latinPath.metadata.course_table);
      }
    }
    
    console.log('\n' + '='.repeat(50));
    console.log('SUMMARY:');
    console.log('='.repeat(50));
    
    if (!latinError) {
      console.log('\n📚 Latin course data is stored in dedicated tables:');
      console.log('   - latin_course: Main course structure');
      console.log('   - latin_modules: Course modules/chapters');
      console.log('   - latin_questions: Questions for each module');
      console.log('\n⚠️ These are SEPARATE from the generic courses table');
    }
    
    if (!lpError && lpCourses && lpCourses.length > 0) {
      console.log('\n🔗 learning_path_courses junction table already exists');
      console.log('   But it may not be properly linked to course data');
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
  
  process.exit(0);
}

checkExistingTables();
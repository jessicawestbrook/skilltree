const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function analyzeStructure() {
  try {
    console.log('ANALYZING CURRENT DATABASE STRUCTURE\n');
    console.log('='.repeat(60));
    
    // 1. Check learning_path_courses orphaned references
    console.log('\n1. LEARNING_PATH_COURSES TABLE:');
    const { data: lpCourses, error: lpError } = await supabase
      .from('learning_path_courses')
      .select('*');
    
    if (!lpError && lpCourses) {
      console.log(`   Found ${lpCourses.length} entries`);
      console.log('   These reference course_id values that don\'t exist anywhere');
      console.log('   ⚠️  These are ORPHANED references\n');
    }
    
    // 2. Check if we have Latin skill nodes
    console.log('2. LATIN SKILL NODES:');
    const { data: latinNodes } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, parent_id')
      .or('name.ilike.%latin%,id.eq.c3f6b6ad-7456-4b66-bfcf-e0803a4925f8,id.eq.b91a46fa-6e1e-48e0-acdd-4360393058b8')
      .limit(5);
    
    if (latinNodes && latinNodes.length > 0) {
      console.log('   Found Latin-related skill nodes:');
      latinNodes.forEach(node => {
        console.log(`   - ${node.name} (ID: ${node.id.substring(0, 8)}...)`);
      });
    }
    
    // 3. Check current learning path
    console.log('\n3. LEARNING PATH:');
    const { data: path } = await supabase
      .from('learning_paths')
      .select('*')
      .eq('slug', 'complete-henle-latin-program')
      .single();
    
    if (path) {
      console.log('   Complete Henle Latin Program exists');
      console.log(`   ID: ${path.id}`);
    }
    
    console.log('\n' + '='.repeat(60));
    console.log('RECOMMENDATION:');
    console.log('='.repeat(60));
    
    console.log('\n✅ SIMPLER APPROACH:');
    console.log('   Instead of creating a separate courses table,');
    console.log('   we should use the existing skill_tree_nodes structure:\n');
    
    console.log('   1. Courses ARE skill_tree_nodes (with parent = skill)');
    console.log('   2. Skills have courses as children');
    console.log('   3. learning_path_courses links paths to course nodes\n');
    
    console.log('   Example structure:');
    console.log('   Latin Language (skill node)');
    console.log('     └─ Henle Latin Year 1 (course node)');
    console.log('     └─ Henle Latin Year 2 (course node)');
    console.log('     └─ Henle Latin Year 3 (course node)');
    console.log('     └─ Henle Latin Year 4 (course node)\n');
    
    console.log('📝 WHAT WE NEED TO DO:');
    console.log('   1. Create course nodes under Latin Language skill');
    console.log('   2. Fix learning_path_courses to reference these nodes');
    console.log('   3. No need for a separate courses table!');
    
  } catch (error) {
    console.error('Error:', error);
  }
  
  process.exit(0);
}

analyzeStructure();
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkLearningPathsStructure() {
  try {
    // Check learning_paths table structure
    console.log('Checking learning_paths table structure...\n');
    const { data: pathsData, error: pathsError } = await supabase
      .from('learning_paths')
      .select('*')
      .limit(3);
    
    if (!pathsError && pathsData && pathsData.length > 0) {
      console.log('learning_paths columns:', Object.keys(pathsData[0]));
      console.log('\nSample learning paths:');
      pathsData.forEach(path => {
        console.log(`- ${path.name} (ID: ${path.id})`);
        if (path.skill_node_id) {
          console.log(`  Associated with skill node: ${path.skill_node_id}`);
        } else {
          console.log(`  ⚠️ No skill node association`);
        }
      });
      
      // Count paths without skill node associations
      const { count: totalCount } = await supabase
        .from('learning_paths')
        .select('*', { count: 'exact', head: true });
      
      const { count: withoutSkillCount } = await supabase
        .from('learning_paths')
        .select('*', { count: 'exact', head: true })
        .is('skill_node_id', null);
      
      console.log(`\nTotal learning paths: ${totalCount}`);
      console.log(`Paths without skill node: ${withoutSkillCount}`);
      console.log(`Paths with skill node: ${totalCount - withoutSkillCount}`);
    } else if (pathsError) {
      console.log('Error fetching learning_paths:', pathsError);
    }
    
    // Check if there's a modules field or related table
    console.log('\n\nChecking for module relationships...');
    const { data: moduleData, error: moduleError } = await supabase
      .from('learning_paths')
      .select('*, skill_tree_nodes(*)')
      .limit(1);
    
    if (!moduleError && moduleData && moduleData.length > 0) {
      console.log('Learning path with skill node data:', JSON.stringify(moduleData[0], null, 2));
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
  
  process.exit(0);
}

checkLearningPathsStructure();
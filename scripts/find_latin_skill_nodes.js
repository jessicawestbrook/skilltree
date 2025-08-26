const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function findLatinSkillNodes() {
  try {
    console.log('Searching for Latin-related skill nodes...\n');
    
    // Search for Latin nodes
    const { data: latinNodes, error: latinError } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, parent_id, description')
      .or('name.ilike.%latin%,description.ilike.%latin%')
      .limit(20);
    
    if (!latinError && latinNodes) {
      console.log(`Found ${latinNodes.length} Latin-related nodes:\n`);
      latinNodes.forEach(node => {
        console.log(`ID: ${node.id}`);
        console.log(`Name: ${node.name}`);
        console.log(`Description: ${node.description || 'No description'}`);
        console.log(`Parent ID: ${node.parent_id || 'Root node'}`);
        console.log('---');
      });
      
      // Check for Language Learning or Foreign Language category
      console.log('\n\nSearching for Language Learning category nodes...\n');
      const { data: langNodes, error: langError } = await supabase
        .from('skill_tree_nodes')
        .select('id, name, parent_id, description')
        .or('name.ilike.%language%,name.ilike.%foreign%')
        .is('parent_id', null) // Look for root level categories
        .limit(10);
      
      if (!langError && langNodes) {
        console.log(`Found ${langNodes.length} language category nodes:\n`);
        langNodes.forEach(node => {
          console.log(`ID: ${node.id}`);
          console.log(`Name: ${node.name}`);
          console.log('---');
        });
      }
    }
    
    // Get the existing Latin learning path details
    console.log('\n\nExisting Latin Learning Path:\n');
    const { data: latinPath, error: pathError } = await supabase
      .from('learning_paths')
      .select('*')
      .eq('slug', 'complete-henle-latin-program')
      .single();
    
    if (!pathError && latinPath) {
      console.log('Name:', latinPath.name);
      console.log('ID:', latinPath.id);
      console.log('Category:', latinPath.category);
      console.log('Language ID:', latinPath.language_id);
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
  
  process.exit(0);
}

findLatinSkillNodes();
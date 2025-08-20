const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(process.env.REACT_APP_SUPABASE_URL, process.env.REACT_APP_SUPABASE_ANON_KEY);

async function queryHierarchy() {
  try {
    // First find Formal Sciences
    const { data: formalSciences, error: fsError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .eq('name', 'Formal Sciences')
      .single();
    
    if (fsError) {
      console.log('Error finding Formal Sciences:', fsError);
      return;
    }
    
    console.log('Formal Sciences:', formalSciences);
    
    if (formalSciences) {
      // Find its parent
      const { data: parent } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .eq('id', formalSciences.parent_id)
        .single();
      
      console.log('Parent of Formal Sciences:', parent);
      
      // Find its children
      const { data: children } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .eq('parent_id', formalSciences.id)
        .order('name');
      
      console.log('Children of Formal Sciences:', children);
      
      // Find grandchildren (descendants of Mathematics and Computer Science)
      for (const child of children || []) {
        const { data: grandchildren } = await supabase
          .from('skill_tree_nodes')
          .select('*')
          .eq('parent_id', child.id)
          .order('name');
        
        console.log(`Descendants of ${child.name}:`, grandchildren);
      }
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

queryHierarchy();
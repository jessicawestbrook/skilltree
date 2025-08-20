const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(process.env.REACT_APP_SUPABASE_URL, process.env.REACT_APP_SUPABASE_ANON_KEY);

async function reorganizeHierarchy() {
  try {
    console.log('Starting hierarchy reorganization...');
    
    // Step 1: Get the current structure
    const { data: formalSciences } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .eq('name', 'Formal Sciences')
      .single();
    
    console.log('Found Formal Sciences:', formalSciences.id);
    
    // Step 2: Get Mathematics and Computer Science
    const { data: mathAndCS } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .eq('parent_id', formalSciences.id)
      .in('name', ['Mathematics', 'Computer Science']);
    
    console.log('Found Math and CS:', mathAndCS.map(node => ({ id: node.id, name: node.name })));
    
    // Step 3: Update Mathematics and Computer Science to have Academic Disciplines as parent
    const academicDisciplinesId = formalSciences.parent_id; // Academic Disciplines ID
    
    for (const category of mathAndCS) {
      console.log(`Updating ${category.name} parent from ${category.parent_id} to ${academicDisciplinesId}`);
      
      const { error: updateError } = await supabase
        .from('skill_tree_nodes')
        .update({ 
          parent_id: academicDisciplinesId,
          learning_area: 'Academic Disciplines',
          updated_at: new Date().toISOString()
        })
        .eq('id', category.id);
      
      if (updateError) {
        console.error(`Error updating ${category.name}:`, updateError);
        return;
      }
      
      console.log(`✓ Successfully updated ${category.name}`);
    }
    
    // Step 4: Update all descendants to have appropriate learning_area
    for (const category of mathAndCS) {
      console.log(`Updating descendants of ${category.name}...`);
      
      // Get all descendants recursively
      const descendants = await getAllDescendants(category.id);
      console.log(`Found ${descendants.length} descendants for ${category.name}`);
      
      // Update learning_area for all descendants
      for (const descendant of descendants) {
        const { error: updateError } = await supabase
          .from('skill_tree_nodes')
          .update({ 
            learning_area: category.name, // Mathematics or Computer Science
            updated_at: new Date().toISOString()
          })
          .eq('id', descendant.id);
        
        if (updateError) {
          console.error(`Error updating descendant ${descendant.name}:`, updateError);
        } else {
          console.log(`  ✓ Updated ${descendant.name} learning_area to ${category.name}`);
        }
      }
    }
    
    // Step 5: Check if Formal Sciences has any remaining children
    const { data: remainingChildren } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .eq('parent_id', formalSciences.id);
    
    if (remainingChildren && remainingChildren.length > 0) {
      console.log('Warning: Formal Sciences still has children:', remainingChildren.map(c => c.name));
      console.log('Please review before deleting Formal Sciences node.');
    } else {
      // Step 6: Delete the Formal Sciences node
      console.log('Deleting Formal Sciences node...');
      
      const { error: deleteError } = await supabase
        .from('skill_tree_nodes')
        .delete()
        .eq('id', formalSciences.id);
      
      if (deleteError) {
        console.error('Error deleting Formal Sciences:', deleteError);
      } else {
        console.log('✓ Successfully deleted Formal Sciences node');
      }
    }
    
    console.log('Hierarchy reorganization completed!');
    
    // Verification step
    console.log('\nVerification:');
    const { data: updatedMathAndCS } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .in('name', ['Mathematics', 'Computer Science']);
    
    for (const category of updatedMathAndCS) {
      console.log(`${category.name}: parent_id=${category.parent_id}, learning_area=${category.learning_area}`);
    }
    
  } catch (error) {
    console.error('Error during reorganization:', error);
  }
}

async function getAllDescendants(parentId, allDescendants = []) {
  const { data: children } = await supabase
    .from('skill_tree_nodes')
    .select('*')
    .eq('parent_id', parentId);
  
  if (children) {
    for (const child of children) {
      allDescendants.push(child);
      await getAllDescendants(child.id, allDescendants);
    }
  }
  
  return allDescendants;
}

// Ask for confirmation before running
console.log('This script will:');
console.log('1. Move Mathematics and Computer Science up one level (under Academic Disciplines)');
console.log('2. Update learning_area for all descendants');
console.log('3. Delete the Formal Sciences category');
console.log('\nPress Ctrl+C to cancel, or press Enter to continue...');

process.stdin.once('data', () => {
  reorganizeHierarchy();
});
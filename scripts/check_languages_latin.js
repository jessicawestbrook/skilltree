const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkLanguagesLatin() {
  try {
    console.log('Checking /languages/latin structure...\n');
    
    const latinId = 'b91a46fa-6e1e-48e0-acdd-4360393058b8';
    
    // Get the Latin node
    const { data: latinNode } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .eq('id', latinId)
      .single();
    
    console.log('📂 Latin node under Languages:');
    console.log('   Name:', latinNode.name);
    console.log('   ID:', latinNode.id);
    console.log('   Parent ID:', latinNode.parent_id);
    
    // Get current children
    const { data: children } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .eq('parent_id', latinId)
      .order('display_order', { nullsFirst: false })
      .order('name');
    
    console.log('\n📚 Current children of /languages/latin:');
    if (children && children.length > 0) {
      children.forEach(child => {
        console.log(`\n   ${child.name}`);
        console.log(`   - ID: ${child.id}`);
        console.log(`   - Display Order: ${child.display_order}`);
        console.log(`   - Has metadata: ${child.metadata ? 'Yes' : 'No'}`);
        if (child.metadata) {
          console.log(`   - Metadata:`, JSON.stringify(child.metadata));
        }
      });
    } else {
      console.log('   No children found');
    }
    
    // Check if these look like courses
    const courseChildren = children?.filter(c => 
      c.metadata?.textbook || 
      c.metadata?.year || 
      c.name.includes('Year') ||
      c.name.includes('Henle')
    ) || [];
    
    console.log('\n🎓 Course-like children:', courseChildren.length);
    if (courseChildren.length > 0) {
      console.log('   Courses detected:');
      courseChildren.forEach(c => console.log(`   - ${c.name}`));
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
  
  process.exit(0);
}

checkLanguagesLatin();
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

async function debugChevrons() {
  try {
    console.log('Checking which categories have subcategories...\n');
    
    // Get top-level categories
    const { data: rootNodes, error: rootError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .is('parent_id', null)
      .or('learning_content_ids.is.null,learning_content_ids.eq.{}')
      .order('display_order', { nullsFirst: false })
      .order('name')
      .limit(10);
    
    if (rootError) throw rootError;
    
    console.log(`Found ${rootNodes?.length || 0} top-level categories\n`);
    
    // Check each category for subcategories
    for (const category of rootNodes || []) {
      const { data: childNodes } = await supabase
        .from('skill_tree_nodes')
        .select('id, name')
        .eq('parent_id', category.id)
        .order('name');
      
      console.log(`${category.name}:`);
      if (childNodes && childNodes.length > 0) {
        console.log(`  ✓ Has ${childNodes.length} subcategories (should show chevron)`);
        console.log(`  First few: ${childNodes.slice(0, 3).map(n => n.name).join(', ')}`);
      } else {
        console.log(`  ✗ No subcategories (no chevron)`);
      }
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
}

debugChevrons();
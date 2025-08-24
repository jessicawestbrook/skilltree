// Script to verify all nodes now have display_order values
require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Missing Supabase environment variables!');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function verifyDisplayOrder() {
  console.log('Verifying display_order update...\n');
  
  // Get counts
  const { count: totalCount } = await supabase
    .from('skill_tree_nodes')
    .select('*', { count: 'exact', head: true });
  
  const { count: withOrderCount } = await supabase
    .from('skill_tree_nodes')
    .select('*', { count: 'exact', head: true })
    .not('display_order', 'is', null);
  
  const { count: withoutOrderCount } = await supabase
    .from('skill_tree_nodes')
    .select('*', { count: 'exact', head: true })
    .is('display_order', null);
  
  console.log('📊 Final Statistics:');
  console.log(`Total nodes: ${totalCount}`);
  console.log(`Nodes WITH display_order: ${withOrderCount}`);
  console.log(`Nodes WITHOUT display_order: ${withoutOrderCount}`);
  
  if (withoutOrderCount === 0) {
    console.log('\n✅ SUCCESS! All nodes now have display_order values!');
  } else {
    console.log(`\n⚠️  Still ${withoutOrderCount} nodes without display_order`);
    
    // Show which ones
    const { data: missing } = await supabase
      .from('skill_tree_nodes')
      .select('name, parent_id')
      .is('display_order', null)
      .limit(10);
    
    if (missing && missing.length > 0) {
      console.log('\nExamples of nodes still missing display_order:');
      missing.forEach(node => {
        console.log(`  - ${node.name}`);
      });
    }
  }
  
  // Show some examples of the ordering
  console.log('\n📋 Sample of ordered nodes:');
  
  // Get a few different parent groups
  const { data: samples } = await supabase
    .from('skill_tree_nodes')
    .select('name, parent_id, display_order')
    .not('display_order', 'is', null)
    .in('parent_id', [
      '040e07a0-8a46-49b2-adc3-ed442448ae72', // Sciences
      'be15d09c-ba13-498f-9994-808b84e17244', // Early Math
      '29807bca-a157-46e1-aaca-05c889147d1d'  // Ancient Greece
    ])
    .order('parent_id')
    .order('display_order')
    .limit(20);
  
  if (samples && samples.length > 0) {
    let currentParent = null;
    samples.forEach(node => {
      if (node.parent_id !== currentParent) {
        currentParent = node.parent_id;
        console.log(`\n  Parent: ${currentParent ? currentParent.substring(0, 8) + '...' : 'root'}`);
      }
      console.log(`    ${node.display_order}. ${node.name}`);
    });
  }
  
  console.log('\n✅ Verification complete!');
}

verifyDisplayOrder().catch(console.error);
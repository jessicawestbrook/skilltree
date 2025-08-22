require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function checkDescriptions() {
  try {
    console.log('🔍 CHECKING DESCRIPTION STATUS\n');
    
    // Get all nodes
    const { data: nodes, error } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, parent_id, description')
      .order('name');
      
    if (error) {
      console.error('Error:', error);
      return;
    }
    
    const withDesc = nodes.filter(n => n.description && n.description.trim() !== '');
    const withoutDesc = nodes.filter(n => !n.description || n.description.trim() === '');
    
    console.log('📊 DESCRIPTION STATUS:');
    console.log('============================');
    console.log(`Total nodes: ${nodes.length}`);
    console.log(`With descriptions: ${withDesc.length}`);
    console.log(`Missing descriptions: ${withoutDesc.length}`);
    console.log(`Progress: ${Math.round((withDesc.length / nodes.length) * 100)}%`);
    
    if (withoutDesc.length > 0) {
      console.log('\n🔍 FIRST 20 NODES MISSING DESCRIPTIONS:');
      withoutDesc.slice(0, 20).forEach((node, i) => {
        console.log(`${i + 1}. ${node.name} (ID: ${node.id})`);
      });
      
      if (withoutDesc.length > 20) {
        console.log(`\n... and ${withoutDesc.length - 20} more nodes without descriptions`);
      }
    }
    
    if (withDesc.length > 0) {
      console.log('\n✅ EXAMPLE NODES WITH DESCRIPTIONS:');
      withDesc.slice(0, 3).forEach(node => {
        console.log(`• ${node.name}: "${node.description.substring(0, 100)}..."`);
      });
    }
    
  } catch (error) {
    console.error('Error in analysis:', error);
  }
}

checkDescriptions();
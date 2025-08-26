const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

function nameToSlug(name) {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

async function buildPath(nodeId) {
  const segments = [];
  let currentId = nodeId;
  
  while (currentId) {
    const { data: node } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, parent_id')
      .eq('id', currentId)
      .single();
    
    if (!node) break;
    
    // Don't include root "Knowledge" node
    if (node.name !== 'Knowledge') {
      segments.unshift(nameToSlug(node.name));
    }
    
    currentId = node.parent_id;
  }
  
  return segments.join('/');
}

async function findLatinPath() {
  try {
    console.log('Finding path to Latin Language page...\n');
    
    const latinSkillId = 'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8';
    
    // Build the path
    const path = await buildPath(latinSkillId);
    
    console.log('✅ Latin Language page URL:');
    console.log(`   /${path}`);
    console.log('\n📋 Full URL for your app:');
    console.log(`   http://localhost:3000/${path}`);
    
    // Also check parent path
    const { data: latinSkill } = await supabase
      .from('skill_tree_nodes')
      .select('parent_id')
      .eq('id', latinSkillId)
      .single();
    
    if (latinSkill?.parent_id) {
      const parentPath = await buildPath(latinSkill.parent_id);
      console.log('\n📂 Parent category URL:');
      console.log(`   http://localhost:3000/${parentPath}`);
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
  
  process.exit(0);
}

findLatinPath();
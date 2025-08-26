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

async function findLanguagesLatinPaths() {
  try {
    console.log('Searching for Latin under Languages category...\n');
    
    // First, find the Languages category
    const { data: languagesNodes } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .ilike('name', '%languages%')
      .limit(10);
    
    if (languagesNodes && languagesNodes.length > 0) {
      console.log('Found nodes with "Languages" in name:');
      for (const node of languagesNodes) {
        const path = await buildPath(node.id);
        console.log(`\n📂 ${node.name}`);
        console.log(`   ID: ${node.id}`);
        console.log(`   Path: /${path}`);
        console.log(`   URL: http://localhost:3000/${path}`);
      }
    }
    
    // Now search for Latin nodes
    console.log('\n\nSearching for Latin nodes...');
    const { data: latinNodes } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .ilike('name', '%latin%')
      .limit(10);
    
    if (latinNodes && latinNodes.length > 0) {
      console.log('\nFound nodes with "Latin" in name:');
      for (const node of latinNodes) {
        const path = await buildPath(node.id);
        console.log(`\n📚 ${node.name}`);
        console.log(`   ID: ${node.id}`);
        console.log(`   Path: /${path}`);
        console.log(`   URL: http://localhost:3000/${path}`);
        
        // Check if this node has courses (children)
        const { data: children } = await supabase
          .from('skill_tree_nodes')
          .select('name')
          .eq('parent_id', node.id)
          .limit(5);
        
        if (children && children.length > 0) {
          console.log(`   Has ${children.length} children:`, children.map(c => c.name).join(', '));
        }
      }
    }
    
    // Check if there's a Latin node directly under a Languages category
    console.log('\n\nLooking for the expected /languages/latin path...');
    
    // Find Languages category first
    const { data: langCategory } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .eq('name', 'Languages')
      .single();
    
    if (langCategory) {
      console.log(`\n✅ Found Languages category: ${langCategory.id}`);
      
      // Check for Latin directly under Languages
      const { data: latinUnderLang } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .eq('parent_id', langCategory.id)
        .ilike('name', '%latin%');
      
      if (latinUnderLang && latinUnderLang.length > 0) {
        console.log('Found Latin under Languages:');
        for (const latin of latinUnderLang) {
          const path = await buildPath(latin.id);
          console.log(`   - ${latin.name}: http://localhost:3000/${path}`);
        }
      } else {
        console.log('   No Latin node found directly under Languages');
        
        // Check all children of Languages
        const { data: allLangChildren } = await supabase
          .from('skill_tree_nodes')
          .select('id, name')
          .eq('parent_id', langCategory.id);
        
        console.log('\n   All children of Languages:');
        if (allLangChildren) {
          for (const child of allLangChildren) {
            console.log(`     - ${child.name}`);
          }
        }
      }
    } else {
      console.log('❌ No "Languages" category found');
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
  
  process.exit(0);
}

findLanguagesLatinPaths();
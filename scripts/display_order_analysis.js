const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

async function analyzeDisplayOrder() {
  console.log('=== DISPLAY ORDER FIELD ANALYSIS ===\n');

  try {
    // 1. Get nodes with display_order values by parent
    console.log('1. DISPLAY ORDER USAGE BY PARENT:');
    
    const { data: orderedNodes, error } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, parent_id, display_order, type')
      .not('display_order', 'is', null)
      .order('parent_id')
      .order('display_order');

    if (error) {
      console.error('Error:', error);
      return;
    }

    // Group by parent_id
    const byParent = {};
    orderedNodes.forEach(node => {
      const parentId = node.parent_id || 'root';
      if (!byParent[parentId]) {
        byParent[parentId] = [];
      }
      byParent[parentId].push(node);
    });

    console.log(`Found ${Object.keys(byParent).length} parents with ordered children:`);
    
    // Show a few examples
    let count = 0;
    for (const [parentId, children] of Object.entries(byParent)) {
      if (count >= 5) break; // Show first 5 examples
      
      console.log(`\nParent ID ${parentId.substring(0, 8)}... has ${children.length} ordered children:`);
      children.slice(0, 8).forEach(child => {
        console.log(`  ${child.display_order}: ${child.name}`);
      });
      if (children.length > 8) {
        console.log(`  ... and ${children.length - 8} more`);
      }
      count++;
    }

    // 2. Check if top-level categories have display_order
    console.log('\n2. TOP-LEVEL CATEGORIES DISPLAY ORDER:');
    const { data: topLevel, error: topError } = await supabase
      .from('skill_tree_nodes')
      .select('name, display_order')
      .is('parent_id', null)
      .order('name');

    if (topError) {
      console.error('Error:', topError);
      return;
    }

    console.log('Top-level categories and their display_order values:');
    topLevel.forEach(cat => {
      console.log(`- ${cat.name}: ${cat.display_order || 'null'}`);
    });

    // 3. Look for academic progression patterns in ordered children
    console.log('\n3. ACADEMIC PROGRESSION PATTERNS:');
    
    // Check Mathematics children
    const { data: mathNode, error: mathError } = await supabase
      .from('skill_tree_nodes')
      .select('id')
      .eq('name', 'Mathematics')
      .single();

    if (mathError) {
      console.error('Error finding Math node:', mathError);
    } else {
      const mathChildren = byParent[mathNode.id] || [];
      if (mathChildren.length > 0) {
        console.log('\nMathematics children ordering:');
        mathChildren.forEach(child => {
          console.log(`  ${child.display_order}: ${child.name}`);
        });
        
        // Check if this follows academic progression
        const progression = analyzeAcademicProgression(mathChildren, 'mathematics');
        if (progression.issues.length > 0) {
          console.log('  Issues found:');
          progression.issues.forEach(issue => console.log(`    ⚠️  ${issue}`));
        }
      } else {
        console.log('\nMathematics children are not using display_order field.');
      }
    }

    // Check Languages children
    const { data: langNode, error: langError } = await supabase
      .from('skill_tree_nodes')
      .select('id')
      .eq('name', 'Languages')
      .single();

    if (langError) {
      console.error('Error finding Languages node:', langError);
    } else {
      const langChildren = byParent[langNode.id] || [];
      if (langChildren.length > 0) {
        console.log('\nLanguages children ordering:');
        langChildren.forEach(child => {
          console.log(`  ${child.display_order}: ${child.name}`);
        });
        
        const progression = analyzeAcademicProgression(langChildren, 'languages');
        if (progression.issues.length > 0) {
          console.log('  Issues found:');
          progression.issues.forEach(issue => console.log(`    ⚠️  ${issue}`));
        }
      } else {
        console.log('\nLanguages children are not using display_order field.');
      }
    }

    // 4. Summary of ordering system
    console.log('\n4. ORDERING SYSTEM SUMMARY:');
    const totalNodes = await getTotalNodeCount();
    const orderedCount = orderedNodes.length;
    const unorderedCount = totalNodes - orderedCount;
    
    console.log(`Total nodes: ${totalNodes}`);
    console.log(`Nodes with display_order: ${orderedCount} (${((orderedCount/totalNodes)*100).toFixed(1)}%)`);
    console.log(`Nodes without display_order: ${unorderedCount} (${((unorderedCount/totalNodes)*100).toFixed(1)}%)`);
    
    if (orderedCount < totalNodes * 0.5) {
      console.log('\n⚠️  MAJOR FINDING: Less than 50% of nodes use display_order field.');
      console.log('   This means most of the tree relies on default ordering (likely by ID or name).');
      console.log('   A comprehensive reordering system needs to be implemented.');
    }

  } catch (error) {
    console.error('Error in analysis:', error);
  }
}

function analyzeAcademicProgression(orderedNodes, subject) {
  const issues = [];
  
  if (subject === 'mathematics') {
    // Look for specific math progression issues
    const nodeNames = orderedNodes.map(n => n.name.toLowerCase());
    
    // Check if advanced topics come before basics
    const advancedBeforeBasic = [
      { advanced: 'calculus', basic: 'arithmetic' },
      { advanced: 'abstract algebra', basic: 'elementary algebra' },
      { advanced: 'differential equations', basic: 'algebra' },
      { advanced: 'topology', basic: 'geometry' }
    ];
    
    advancedBeforeBasic.forEach(pair => {
      const advancedIndex = nodeNames.findIndex(name => name.includes(pair.advanced));
      const basicIndex = nodeNames.findIndex(name => name.includes(pair.basic));
      
      if (advancedIndex !== -1 && basicIndex !== -1 && advancedIndex < basicIndex) {
        const advancedNode = orderedNodes[advancedIndex];
        const basicNode = orderedNodes[basicIndex];
        issues.push(`${advancedNode.name} (order ${advancedNode.display_order}) comes before ${basicNode.name} (order ${basicNode.display_order})`);
      }
    });
  }
  
  if (subject === 'languages') {
    // Look for ancient languages before modern ones
    const ancient = ['latin', 'ancient greek', 'classical'];
    const modern = ['spanish', 'french', 'german', 'italian', 'portuguese'];
    
    orderedNodes.forEach((node, index) => {
      const name = node.name.toLowerCase();
      const isAncient = ancient.some(a => name.includes(a));
      const modernAfter = orderedNodes.slice(index + 1).some(laterNode => 
        modern.some(m => laterNode.name.toLowerCase().includes(m))
      );
      
      if (isAncient && modernAfter) {
        issues.push(`${node.name} (ancient language) comes before modern languages`);
      }
    });
  }
  
  return { issues };
}

async function getTotalNodeCount() {
  const { count, error } = await supabase
    .from('skill_tree_nodes')
    .select('*', { count: 'exact', head: true });
  
  return error ? 0 : count;
}

// Run the analysis
analyzeDisplayOrder().then(() => {
  console.log('\n=== DISPLAY ORDER ANALYSIS COMPLETE ===');
  process.exit(0);
}).catch(error => {
  console.error('Analysis failed:', error);
  process.exit(1);
});
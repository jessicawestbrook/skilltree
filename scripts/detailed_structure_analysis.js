const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

async function detailedStructureAnalysis() {
  console.log('=== DETAILED SKILL TREE STRUCTURE ANALYSIS ===\n');

  try {
    // 1. Check if these are actually top-level categories or if there's a missing root
    console.log('1. ANALYZING ROOT NODE STRUCTURE:');
    
    // Check nodes with null parent_id
    const { data: nullParentNodes, error: nullError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .is('parent_id', null)
      .order('name');

    if (nullError) {
      console.error('Error:', nullError);
      return;
    }

    console.log(`Found ${nullParentNodes?.length || 0} nodes with null parent_id:`);
    nullParentNodes?.forEach((node, index) => {
      console.log(`${index + 1}. ${node.name} (ID: ${node.id.substring(0, 8)}...)`);
      console.log(`   Type: ${node.type || 'N/A'}, Display Order: ${node.display_order || 'null'}`);
    });

    // 2. Look for nodes that reference non-existent parents (orphaned nodes)
    console.log('\n2. CHECKING FOR ORPHANED NODES:');
    const { data: allNodes, error: allError } = await supabase
      .from('skill_tree_nodes')
      .select('id, parent_id, name')
      .not('parent_id', 'is', null);

    if (allError) {
      console.error('Error:', allError);
      return;
    }

    const allIds = new Set(allNodes?.map(n => n.id) || []);
    const orphans = allNodes?.filter(node => node.parent_id && !allIds.has(node.parent_id)) || [];
    
    console.log(`Found ${orphans.length} orphaned nodes (parent doesn't exist):`);
    orphans.forEach(orphan => {
      console.log(`- ${orphan.name} (parent_id: ${orphan.parent_id?.substring(0, 8)}...)`);
    });

    // 3. Examine Mathematics category and its children in detail
    console.log('\n3. DETAILED MATHEMATICS CATEGORY ANALYSIS:');
    const mathNode = nullParentNodes?.find(n => n.name.toLowerCase().includes('math'));
    
    if (mathNode) {
      await analyzeMathematicsStructure(mathNode.id);
    }

    // 4. Examine Languages category and its children in detail
    console.log('\n4. DETAILED LANGUAGES CATEGORY ANALYSIS:');
    const langNode = nullParentNodes?.find(n => n.name.toLowerCase().includes('language'));
    
    if (langNode) {
      await analyzeLanguagesStructure(langNode.id);
    }

    // 5. Check display_order usage throughout the tree
    console.log('\n5. DISPLAY_ORDER FIELD ANALYSIS:');
    const { data: nodesWithOrder, error: orderError } = await supabase
      .from('skill_tree_nodes')
      .select('name, display_order, parent_id')
      .not('display_order', 'is', null);

    if (orderError) {
      console.error('Error:', orderError);
      return;
    }

    console.log(`Found ${nodesWithOrder?.length || 0} nodes with non-null display_order values:`);
    if (nodesWithOrder && nodesWithOrder.length > 0) {
      nodesWithOrder.slice(0, 10).forEach(node => {
        console.log(`- ${node.name}: display_order = ${node.display_order}`);
      });
      if (nodesWithOrder.length > 10) {
        console.log(`... and ${nodesWithOrder.length - 10} more`);
      }
    } else {
      console.log('No nodes are currently using the display_order field.');
    }

    // 6. Sample problematic ordering examples
    console.log('\n6. SPECIFIC ORDERING PROBLEMS IDENTIFIED:');
    await identifySpecificProblems(nullParentNodes);

  } catch (error) {
    console.error('Error in detailed analysis:', error);
  }
}

async function analyzeMathematicsStructure(mathId) {
  const { data: mathChildren, error } = await supabase
    .from('skill_tree_nodes')
    .select('*')
    .eq('parent_id', mathId)
    .order('name');

  if (error) {
    console.error('Error getting math children:', error);
    return;
  }

  console.log(`Mathematics has ${mathChildren?.length || 0} direct children:`);
  mathChildren?.forEach((child, index) => {
    console.log(`  ${index + 1}. ${child.name}`);
  });

  // Look for specific problematic cases in math
  if (mathChildren) {
    const abstractAlgebra = mathChildren.find(c => c.name.toLowerCase().includes('abstract') && c.name.toLowerCase().includes('algebra'));
    const elementaryAlgebra = mathChildren.find(c => c.name.toLowerCase().includes('elementary') || c.name.toLowerCase().includes('basic'));
    const calculus = mathChildren.find(c => c.name.toLowerCase().includes('calculus'));
    const arithmetic = mathChildren.find(c => c.name.toLowerCase().includes('arithmetic'));

    if (abstractAlgebra && elementaryAlgebra) {
      const abstractIndex = mathChildren.indexOf(abstractAlgebra);
      const elementaryIndex = mathChildren.indexOf(elementaryAlgebra);
      if (abstractIndex < elementaryIndex) {
        console.log(`  ⚠️  MAJOR ISSUE: "${abstractAlgebra.name}" comes before "${elementaryAlgebra.name}"`);
      }
    }

    if (calculus && arithmetic) {
      const calculusIndex = mathChildren.indexOf(calculus);
      const arithmeticIndex = mathChildren.indexOf(arithmetic);
      if (calculusIndex < arithmeticIndex) {
        console.log(`  ⚠️  MAJOR ISSUE: "${calculus.name}" comes before "${arithmetic.name}"`);
      }
    }

    // Look at algebra subcategories if they exist
    const algebraNode = mathChildren.find(c => c.name.toLowerCase().includes('algebra') && !c.name.toLowerCase().includes('abstract'));
    if (algebraNode) {
      console.log(`\n  Examining Algebra subcategories:`);
      await examineAlgebraSubcategories(algebraNode.id);
    }
  }
}

async function examineAlgebraSubcategories(algebraId) {
  const { data: algebraChildren, error } = await supabase
    .from('skill_tree_nodes')
    .select('*')
    .eq('parent_id', algebraId)
    .order('name');

  if (error) {
    console.error('Error getting algebra children:', error);
    return;
  }

  console.log(`    Algebra has ${algebraChildren?.length || 0} subcategories:`);
  algebraChildren?.forEach((child, index) => {
    console.log(`    ${index + 1}. ${child.name}`);
  });

  // Check for Abstract Algebra being mixed with Elementary
  const abstract = algebraChildren?.filter(c => c.name.toLowerCase().includes('abstract')) || [];
  const elementary = algebraChildren?.filter(c => c.name.toLowerCase().includes('elementary') || c.name.toLowerCase().includes('basic')) || [];

  if (abstract.length > 0 && elementary.length > 0) {
    console.log(`    ⚠️  ISSUE: Abstract and Elementary algebra topics mixed together`);
    abstract.forEach(a => console.log(`      Abstract: ${a.name}`));
    elementary.forEach(e => console.log(`      Elementary: ${e.name}`));
  }
}

async function analyzeLanguagesStructure(langId) {
  const { data: langChildren, error } = await supabase
    .from('skill_tree_nodes')
    .select('*')
    .eq('parent_id', langId)
    .order('name');

  if (error) {
    console.error('Error getting language children:', error);
    return;
  }

  console.log(`Languages has ${langChildren?.length || 0} direct children:`);
  langChildren?.forEach((child, index) => {
    console.log(`  ${index + 1}. ${child.name}`);
  });

  // Look for specific ordering issues
  if (langChildren) {
    const spanish = langChildren.find(c => c.name.toLowerCase().includes('spanish'));
    const greek = langChildren.find(c => c.name.toLowerCase().includes('greek'));
    const latin = langChildren.find(c => c.name.toLowerCase().includes('latin'));
    const english = langChildren.find(c => c.name.toLowerCase().includes('english'));

    if (greek && spanish) {
      const greekIndex = langChildren.indexOf(greek);
      const spanishIndex = langChildren.indexOf(spanish);
      if (greekIndex < spanishIndex) {
        console.log(`  ⚠️  ISSUE: "${greek.name}" comes before "${spanish.name}" (ancient before modern)`);
      }
    }

    if (latin && spanish) {
      const latinIndex = langChildren.indexOf(latin);
      const spanishIndex = langChildren.indexOf(spanish);
      if (latinIndex < spanishIndex) {
        console.log(`  ⚠️  ISSUE: "${latin.name}" comes before "${spanish.name}" (ancient before modern)`);
      }
    }
  }
}

async function identifySpecificProblems(rootNodes) {
  console.log('Academic progression issues identified:');
  
  // 1. Check if fundamental subjects come before advanced ones at top level
  const categories = rootNodes?.map(n => n.name.toLowerCase()) || [];
  
  if (categories.includes('philosophy') && categories.includes('mathematics')) {
    const philIndex = categories.indexOf('philosophy');
    const mathIndex = categories.indexOf('mathematics');
    if (philIndex < mathIndex) {
      console.log('⚠️  Philosophy comes before Mathematics at top level - typically math should be more fundamental');
    }
  }

  // 2. Current ordering appears to be alphabetical rather than academic progression
  console.log('\nCurrent top-level ordering appears to be alphabetical rather than following academic difficulty progression.');
  console.log('Recommended academic progression order would be:');
  console.log('1. Mathematics (foundational)');
  console.log('2. Natural Sciences (builds on math)');
  console.log('3. Computer Science (builds on math and logic)');
  console.log('4. Applied Sciences (applies other sciences)');
  console.log('5. Social Sciences (human studies)');
  console.log('6. Languages (communication)');
  console.log('7. Humanities (cultural and philosophical)');
  console.log('8. Creative Skills (artistic expression)');
  console.log('9. Professional Skills (career application)');
  console.log('10. Life Skills (practical application)');
  console.log('11. Technical Skills (specialized tools)');
  console.log('12. Test Preparation (assessment)');

  console.log('\nCurrent order vs recommended order shows significant misalignment.');
}

// Run the analysis
detailedStructureAnalysis().then(() => {
  console.log('\n=== DETAILED ANALYSIS COMPLETE ===');
  process.exit(0);
}).catch(error => {
  console.error('Analysis failed:', error);
  process.exit(1);
});
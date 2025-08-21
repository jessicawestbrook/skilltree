const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseKey);

async function checkAcademicOrdering() {
  console.log('=== Academic Ordering Verification ===\n');
  
  try {
    // 1. Query top-level categories (parent_id IS NULL)
    console.log('1. TOP-LEVEL CATEGORIES:');
    const { data: topLevel, error: topError } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, display_order, parent_id')
      .is('parent_id', null)
      .order('display_order', { ascending: true, nullsFirst: false });

    if (topError) {
      console.error('Error fetching top-level categories:', topError);
      return;
    }

    topLevel.forEach((node, index) => {
      console.log(`${index + 1}. ${node.name} (ID: ${node.id}, display_order: ${node.display_order})`);
    });

    // 2. Check Mathematics children
    console.log('\n2. MATHEMATICS CHILDREN:');
    const mathNode = topLevel.find(node => node.name === 'Mathematics');
    if (mathNode) {
      const { data: mathChildren, error: mathError } = await supabase
        .from('skill_tree_nodes')
        .select('id, name, display_order, parent_id')
        .eq('parent_id', mathNode.id)
        .order('display_order', { ascending: true, nullsFirst: false });

      if (mathError) {
        console.error('Error fetching Mathematics children:', mathError);
      } else {
        mathChildren.forEach((node, index) => {
          console.log(`   ${index + 1}. ${node.name} (ID: ${node.id}, display_order: ${node.display_order})`);
        });
      }
    } else {
      console.log('   Mathematics node not found!');
    }

    // 3. Check Languages children
    console.log('\n3. LANGUAGES CHILDREN:');
    const languagesNode = topLevel.find(node => node.name === 'Languages');
    if (languagesNode) {
      const { data: langChildren, error: langError } = await supabase
        .from('skill_tree_nodes')
        .select('id, name, display_order, parent_id')
        .eq('parent_id', languagesNode.id)
        .order('display_order', { ascending: true, nullsFirst: false });

      if (langError) {
        console.error('Error fetching Languages children:', langError);
      } else {
        langChildren.forEach((node, index) => {
          console.log(`   ${index + 1}. ${node.name} (ID: ${node.id}, display_order: ${node.display_order})`);
        });
      }
    } else {
      console.log('   Languages node not found!');
    }

    // 4. Count nodes with and without display_order (accurate counts)
    console.log('\n4. DISPLAY_ORDER STATISTICS:');
    
    // Get total count
    const { count: totalCount, error: countError } = await supabase
      .from('skill_tree_nodes')
      .select('*', { count: 'exact', head: true });

    // Get count with display_order
    const { count: withOrderCount, error: withOrderError } = await supabase
      .from('skill_tree_nodes')
      .select('*', { count: 'exact', head: true })
      .not('display_order', 'is', null);

    // Get count without display_order  
    const { count: withoutOrderCount, error: withoutOrderError } = await supabase
      .from('skill_tree_nodes')
      .select('*', { count: 'exact', head: true })
      .is('display_order', null);

    if (countError || withOrderError || withoutOrderError) {
      console.error('Error getting counts:', { countError, withOrderError, withoutOrderError });
    } else {
      console.log(`   Total nodes in database: ${totalCount}`);
      console.log(`   Nodes with display_order: ${withOrderCount}`);
      console.log(`   Nodes without display_order: ${withoutOrderCount}`);
      
      if (withOrderCount + withoutOrderCount !== totalCount) {
        console.log(`   ⚠️  Count mismatch detected: ${withOrderCount} + ${withoutOrderCount} ≠ ${totalCount}`);
      }
    }

    // 5. Sample of academic ordered nodes
    console.log('\n5. ACADEMIC ORDERED NODES (Top-level + Major Subcategories):');
    const { data: academicNodes, error: academicError } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, parent_id, display_order')
      .in('display_order', [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110])
      .order('display_order', { ascending: true });

    if (academicError) {
      console.error('Error fetching academic nodes:', academicError);
    } else {
      academicNodes.forEach((node, index) => {
        const nodeType = node.parent_id === null ? 'TOP-LEVEL' : 'SUBCATEGORY';
        console.log(`   ${index + 1}. ${node.name} (${nodeType}, display_order: ${node.display_order})`);
      });
    }

    // 6. Sample of nodes without display_order
    console.log('\n6. SAMPLE NODES WITHOUT DISPLAY_ORDER:');
    const { data: nullOrderNodes, error: nullError } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, parent_id, display_order')
      .is('display_order', null)
      .limit(5);

    if (nullError) {
      console.error('Error fetching null display_order nodes:', nullError);
    } else {
      nullOrderNodes.forEach((node, index) => {
        console.log(`   ${index + 1}. ${node.name} (ID: ${node.id}, parent_id: ${node.parent_id})`);
      });
    }

  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

checkAcademicOrdering();
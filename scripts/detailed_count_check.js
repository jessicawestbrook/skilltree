const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseKey);

async function detailedCountCheck() {
  console.log('=== Detailed Count Analysis ===\n');
  
  try {
    // Get total count from both databases/sources
    const { count: totalCount1, error: countError1 } = await supabase
      .from('skill_tree_nodes')
      .select('*', { count: 'exact', head: true });

    console.log(`Total nodes (count query): ${totalCount1}`);

    // Get actual data count
    const { data: allNodes, error: fetchError } = await supabase
      .from('skill_tree_nodes')
      .select('id, display_order');

    if (fetchError) {
      console.error('Error fetching all nodes:', fetchError);
      return;
    }

    console.log(`Total nodes (data fetch): ${allNodes.length}`);

    // Count nodes with and without display_order
    const withOrder = allNodes.filter(n => n.display_order !== null);
    const withoutOrder = allNodes.filter(n => n.display_order === null);

    console.log(`\nNodes with display_order: ${withOrder.length}`);
    console.log(`Nodes without display_order: ${withoutOrder.length}`);

    // Show distribution of display_order values
    const orderValues = withOrder.map(n => n.display_order).sort((a, b) => a - b);
    const uniqueOrders = [...new Set(orderValues)];
    
    console.log(`\nUnique display_order values: ${uniqueOrders.join(', ')}`);
    
    // Count nodes by display_order value
    console.log('\nCount by display_order value:');
    uniqueOrders.forEach(order => {
      const count = orderValues.filter(v => v === order).length;
      console.log(`  ${order}: ${count} nodes`);
    });

    // Check if there are nodes beyond the 1000 we saw earlier
    if (allNodes.length > 1000) {
      console.log(`\nNote: Database contains ${allNodes.length} total nodes, not 1000 as shown in previous query.`);
      console.log('This suggests the verification script had a limit or filtering issue.');
    }

  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

detailedCountCheck();
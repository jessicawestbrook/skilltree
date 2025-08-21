const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = 'https://ozujqlucqdyszxmzhigf.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im96dWpxbHVjcWR5c3p4bXpoaWdmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUyNDEzMzUsImV4cCI6MjA3MDgxNzMzNX0.k21_FmGqGsojgPMKN97-dZI-y5kwrbxKGZcGpDnikG4';

const supabase = createClient(supabaseUrl, supabaseKey);

async function analyzeDisplayOrderUsage() {
    console.log('=== ANALYZING DISPLAY_ORDER FIELD USAGE ===\n');
    
    try {
        // Get all nodes with display_order values
        console.log('1. Getting all nodes with display_order values...');
        const { data: orderedNodes, error: orderedError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id, type, path, display_order')
            .not('display_order', 'is', null)
            .order('display_order');

        if (orderedError) {
            console.error('Error getting ordered nodes:', orderedError);
            return;
        }

        console.log(`Found ${orderedNodes.length} nodes with display_order values`);

        // Group by parent_id to see ordering within categories
        console.log('\n2. Grouping nodes by parent_id to analyze ordering patterns...');
        const nodesByParent = {};
        orderedNodes.forEach(node => {
            const parentKey = node.parent_id || 'ROOT';
            if (!nodesByParent[parentKey]) {
                nodesByParent[parentKey] = [];
            }
            nodesByParent[parentKey].push(node);
        });

        console.log(`Nodes with display_order are grouped under ${Object.keys(nodesByParent).length} different parents`);

        // Show ordering examples for different parent categories
        console.log('\n3. Examples of current ordering patterns:');
        let exampleCount = 0;
        for (const [parentId, children] of Object.entries(nodesByParent)) {
            if (exampleCount >= 5) break; // Limit to 5 examples
            
            const parentName = parentId === 'ROOT' ? 'ROOT LEVEL' : 
                orderedNodes.find(n => n.id === parentId)?.name || 'Unknown Parent';
            
            console.log(`\nParent: ${parentName} (${parentId})`);
            children.forEach(child => {
                console.log(`  Order ${child.display_order}: ${child.name} (${child.type})`);
            });
            exampleCount++;
        }

        // Check for duplicate display_order values within same parent
        console.log('\n4. Checking for ordering conflicts...');
        let conflictsFound = 0;
        for (const [parentId, children] of Object.entries(nodesByParent)) {
            const orderValues = children.map(c => c.display_order);
            const uniqueOrders = new Set(orderValues);
            
            if (orderValues.length !== uniqueOrders.size) {
                conflictsFound++;
                const parentName = parentId === 'ROOT' ? 'ROOT LEVEL' : 
                    orderedNodes.find(n => n.id === parentId)?.name || 'Unknown Parent';
                console.log(`  Conflict in ${parentName}: ${orderValues.length} children but only ${uniqueOrders.size} unique order values`);
            }
        }
        
        if (conflictsFound === 0) {
            console.log('  No ordering conflicts found - each child has unique display_order within its parent');
        }

        // Show distribution of display_order values
        console.log('\n5. Distribution of display_order values:');
        const orderDistribution = {};
        orderedNodes.forEach(node => {
            orderDistribution[node.display_order] = (orderDistribution[node.display_order] || 0) + 1;
        });
        
        Object.keys(orderDistribution).sort((a, b) => parseInt(a) - parseInt(b)).forEach(order => {
            console.log(`  Order ${order}: ${orderDistribution[order]} nodes`);
        });

        // Check nodes without display_order
        console.log('\n6. Checking nodes without display_order...');
        const { count: totalCount } = await supabase
            .from('skill_tree_nodes')
            .select('*', { count: 'exact', head: true });

        const nodesWithoutOrder = totalCount - orderedNodes.length;
        console.log(`  ${nodesWithoutOrder} nodes (${((nodesWithoutOrder/totalCount) * 100).toFixed(1)}%) do not have display_order values`);

        // Sample some nodes without display_order to understand pattern
        const { data: unorderedSample } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id, type, path')
            .is('display_order', null)
            .limit(10);

        if (unorderedSample && unorderedSample.length > 0) {
            console.log('\n  Sample nodes without display_order:');
            unorderedSample.forEach(node => {
                console.log(`    ${node.name} (${node.type}) - Path: ${node.path ? node.path.join(' > ') : 'No path'}`);
            });
        }

    } catch (error) {
        console.error('Error analyzing display_order usage:', error);
    }
}

// Run the analysis
analyzeDisplayOrderUsage().then(() => {
    console.log('\n=== ANALYSIS COMPLETE ===');
    process.exit(0);
});
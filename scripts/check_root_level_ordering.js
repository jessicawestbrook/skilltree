const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = 'https://ozujqlucqdyszxmzhigf.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im96dWpxbHVjcWR5c3p4bXpoaWdmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUyNDEzMzUsImV4cCI6MjA3MDgxNzMzNX0.k21_FmGqGsojgPMKN97-dZI-y5kwrbxKGZcGpDnikG4';

const supabase = createClient(supabaseUrl, supabaseKey);

async function checkRootLevelOrdering() {
    console.log('=== CHECKING ROOT LEVEL CATEGORY ORDERING ===\n');
    
    try {
        // Get all root nodes (no parent_id)
        const { data: rootNodes, error: rootError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, display_order, path')
            .is('parent_id', null)
            .order('display_order', { nullsLast: true });

        if (rootError) {
            console.error('Error getting root nodes:', rootError);
            return;
        }

        console.log('Root-level categories:');
        rootNodes.forEach(node => {
            const orderText = node.display_order !== null ? `Order ${node.display_order}` : 'No order';
            console.log(`  ${orderText}: ${node.name} (${node.type})`);
        });

        // Separate those with and without display_order
        const withOrder = rootNodes.filter(n => n.display_order !== null);
        const withoutOrder = rootNodes.filter(n => n.display_order === null);

        console.log(`\nSummary:`);
        console.log(`  ${withOrder.length} root categories have display_order`);
        console.log(`  ${withoutOrder.length} root categories do NOT have display_order`);

        if (withOrder.length > 0) {
            console.log('\nOrdered root categories:');
            withOrder.forEach(node => {
                console.log(`  ${node.display_order}: ${node.name}`);
            });
        }

        if (withoutOrder.length > 0) {
            console.log('\nUnordered root categories:');
            withoutOrder.forEach(node => {
                console.log(`  - ${node.name}`);
            });
        }

    } catch (error) {
        console.error('Error checking root level ordering:', error);
    }
}

// Run the analysis
checkRootLevelOrdering().then(() => {
    console.log('\n=== ANALYSIS COMPLETE ===');
    process.exit(0);
});
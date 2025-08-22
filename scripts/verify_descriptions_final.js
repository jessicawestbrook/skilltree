const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

async function verifyDescriptions() {
    const supabase = createClient(
        process.env.REACT_APP_SUPABASE_URL,
        process.env.SUPABASE_SERVICE_ROLE_KEY
    );

    try {
        // Get all nodes
        const { data: allNodes, error: allError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, description')
            .order('name');

        if (allError) throw allError;

        // Count nodes with valid descriptions
        const withDesc = allNodes.filter(node => 
            node.description && 
            node.description.trim() !== '' && 
            node.description !== null
        );

        // Count nodes without descriptions
        const withoutDesc = allNodes.filter(node => 
            !node.description || 
            node.description.trim() === '' || 
            node.description === null
        );

        console.log('\n=== FINAL DESCRIPTION VERIFICATION ===');
        console.log(`Total nodes in database: ${allNodes.length}`);
        console.log(`Nodes with valid descriptions: ${withDesc.length}`);
        console.log(`Nodes without descriptions: ${withoutDesc.length}`);
        console.log(`Completion rate: ${((withDesc.length / allNodes.length) * 100).toFixed(2)}%`);

        if (withoutDesc.length > 0) {
            console.log('\nRemaining nodes without descriptions:');
            withoutDesc.slice(0, 20).forEach((node, i) => {
                console.log(`${i + 1}. ${node.name} (ID: ${node.id}) - desc: "${node.description}"`);
            });
        } else {
            console.log('\n✅ ALL NODES HAVE DESCRIPTIONS!');
        }

        // Show sample of recent descriptions
        console.log('\nSample of nodes with descriptions:');
        withDesc.slice(0, 5).forEach((node, i) => {
            const desc = node.description.substring(0, 100);
            console.log(`${i + 1}. ${node.name}: ${desc}...`);
        });

    } catch (error) {
        console.error('Error:', error.message);
    }
}

verifyDescriptions();
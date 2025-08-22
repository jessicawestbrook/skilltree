const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

async function checkDescriptionStatus() {
    const supabase = createClient(
        process.env.REACT_APP_SUPABASE_URL,
        process.env.SUPABASE_SERVICE_ROLE_KEY
    );

    try {
        // Get total nodes
        const { data: allNodes, error: allError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .order('name');

        if (allError) throw allError;

        // Get nodes with descriptions
        const { data: withDesc, error: withError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .not('description', 'is', null)
            .neq('description', '');

        if (withError) throw withError;

        // Get nodes without descriptions
        const { data: withoutDesc, error: withoutError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id')
            .or('description.is.null,description.eq.')
            .limit(10);

        if (withoutError) throw withoutError;

        console.log('\n=== DESCRIPTION STATUS ===');
        console.log(`Total nodes: ${allNodes.length}`);
        console.log(`Nodes with descriptions: ${withDesc.length}`);
        console.log(`Nodes without descriptions: ${allNodes.length - withDesc.length}`);
        console.log(`Completion: ${((withDesc.length / allNodes.length) * 100).toFixed(1)}%`);

        if (withoutDesc.length > 0) {
            console.log('\nFirst 10 nodes without descriptions:');
            withoutDesc.forEach((node, i) => {
                console.log(`${i + 1}. ${node.name} (ID: ${node.id})`);
            });
        }

    } catch (error) {
        console.error('Error:', error.message);
    }
}

checkDescriptionStatus();
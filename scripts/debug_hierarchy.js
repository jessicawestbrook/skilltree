require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function debugHierarchy() {
    try {
        console.log('🔍 DEBUG: Understanding the hierarchy issue...\n');
        
        // Get a sample of nodes that point to specific missing parent IDs
        const missingParentIds = [
            'c868330e-6677-471c-a046-fbd2c934f1c5', // Humanities
            '4a18b634-28a1-455e-8dc2-cce93dfbff84', // Languages  
            '30cdbf72-74e7-4420-8717-4842541c66a3', // Mathematics
            'dbb32dc0-550a-4475-9494-c53dc69045db', // Natural Sciences
            'e5806548-bb90-47ba-b6f8-62a87b80552e'  // Social Sciences
        ];
        
        console.log('=== CHECKING IF THESE PARENT IDs EXIST ===');
        for (const parentId of missingParentIds) {
            const { data: parent, error } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, type, parent_id')
                .eq('id', parentId)
                .single();
                
            if (error) {
                console.log(`❌ ${parentId}: NOT FOUND (${error.code})`);
            } else {
                console.log(`✅ ${parentId}: ${parent.name} (${parent.type}, parent: ${parent.parent_id})`);
            }
        }
        
        console.log('\n=== CHECKING NODES THAT CLAIM TO POINT TO MISSING PARENTS ===');
        
        const { data: sampleNodes, error: sampleError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, parent_id')
            .eq('parent_id', missingParentIds[0])
            .limit(5);
            
        if (sampleError) throw sampleError;
        
        console.log(`Nodes claiming to have parent ${missingParentIds[0]}:`);
        sampleNodes.forEach(node => {
            console.log(`  - ${node.name} (${node.type})`);
        });
        
        console.log('\n=== ACTUAL ROOT NODE CHECK ===');
        const { data: actualRoots, error: rootError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, parent_id')
            .is('parent_id', null);
            
        if (rootError) throw rootError;
        
        console.log(`Actual root nodes (parent_id IS NULL): ${actualRoots.length}`);
        actualRoots.forEach(node => {
            console.log(`  - ${node.name} (${node.type})`);
        });
        
        console.log('\n=== TOTAL NODE COUNT CHECK ===');
        const { count, error: countError } = await supabase
            .from('skill_tree_nodes')
            .select('*', { count: 'exact', head: true });
            
        if (countError) throw countError;
        console.log(`Total nodes in database: ${count}`);
        
    } catch (error) {
        console.error('Error in debug:', error);
    }
}

debugHierarchy();
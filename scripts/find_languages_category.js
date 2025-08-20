require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function findLanguagesCategory() {
    try {
        console.log('Searching for Languages category...\n');
        
        // Find Languages nodes
        const { data: languagesNodes, error: findError } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .ilike('name', '%language%')
            .order('name');
            
        if (findError) {
            console.error('Error finding Languages nodes:', findError);
            return;
        }
        
        console.log('Found nodes with "language" in name:');
        for (const node of languagesNodes) {
            console.log(`- ${node.name} (${node.type}) - ID: ${node.id} - Parent: ${node.parent_id} - Learning Area: ${node.learning_area}`);
        }
        
        // Also search for potential variations
        const { data: linguisticsNodes, error: linguisticsError } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .or('name.ilike.%linguistic%,name.ilike.%foreign%')
            .order('name');
            
        if (!linguisticsError && linguisticsNodes.length > 0) {
            console.log('\nFound nodes with linguistics/foreign:');
            for (const node of linguisticsNodes) {
                console.log(`- ${node.name} (${node.type}) - ID: ${node.id} - Parent: ${node.parent_id} - Learning Area: ${node.learning_area}`);
            }
        }
        
        // Find Humanities node to understand the hierarchy
        const { data: humanitiesNode, error: humanitiesError } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .eq('name', 'Humanities')
            .single();
            
        if (humanitiesError) {
            console.error('Error finding Humanities node:', humanitiesError);
            return;
        }
        
        console.log('\nHumanities node:');
        console.log(`- ${humanitiesNode.name} (${humanitiesNode.type}) - ID: ${humanitiesNode.id} - Parent: ${humanitiesNode.parent_id} - Learning Area: ${humanitiesNode.learning_area}`);
        
        // Get children of Humanities to see current structure
        const { data: humanitiesChildren, error: childrenError } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .eq('parent_id', humanitiesNode.id)
            .order('name');
            
        if (childrenError) {
            console.error('Error getting Humanities children:', childrenError);
            return;
        }
        
        console.log('\nChildren of Humanities:');
        for (const child of humanitiesChildren) {
            console.log(`- ${child.name} (${child.type}) - ID: ${child.id} - Learning Area: ${child.learning_area}`);
        }
        
        // Find Academic Disciplines node
        const { data: academicNode, error: academicError } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .eq('name', 'Academic Disciplines')
            .single();
            
        if (academicError) {
            console.error('Error finding Academic Disciplines node:', academicError);
            return;
        }
        
        console.log('\nAcademic Disciplines node:');
        console.log(`- ${academicNode.name} (${academicNode.type}) - ID: ${academicNode.id} - Parent: ${academicNode.parent_id} - Learning Area: ${academicNode.learning_area}`);
        
    } catch (error) {
        console.error('Unexpected error:', error);
    }
}

findLanguagesCategory();
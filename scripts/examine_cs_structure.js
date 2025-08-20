require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function examineCSStructure() {
    try {
        console.log('Examining Computer Science structure for comparison...\n');
        
        // Find Computer Science node
        const { data: csNode, error: findError } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .eq('name', 'Computer Science')
            .single();
            
        if (findError) {
            console.error('Error finding Computer Science node:', findError);
            return;
        }
        
        console.log('Computer Science root node:', {
            id: csNode.id,
            name: csNode.name,
            learning_area: csNode.learning_area
        });
        
        // Get all descendants recursively (limited depth for overview)
        await getDescendants(csNode.id, 'Computer Science', 0, 2); // Only go 2 levels deep for comparison
        
    } catch (error) {
        console.error('Unexpected error:', error);
    }
}

async function getDescendants(parentId, parentName, depth, maxDepth) {
    try {
        if (depth >= maxDepth) return;
        
        const { data: children, error } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type')
            .eq('parent_id', parentId)
            .order('name', { ascending: true });
            
        if (error) {
            console.error(`Error getting children of ${parentName}:`, error);
            return;
        }
        
        if (children && children.length > 0) {
            const indent = '  '.repeat(depth + 1);
            console.log(`\n${indent}Children of ${parentName}:`);
            
            for (const child of children) {
                console.log(`${indent}- ${child.name} (${child.type})`);
                
                // Recursively get this child's descendants
                await getDescendants(child.id, child.name, depth + 1, maxDepth);
            }
        }
    } catch (error) {
        console.error(`Error in getDescendants for ${parentName}:`, error);
    }
}

examineCSStructure();
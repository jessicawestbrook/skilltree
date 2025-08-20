require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function removeKnowledgeRoot() {
    try {
        console.log('🧹 REMOVING EXTRA KNOWLEDGE ROOT NODE...\n');
        
        // Find the Knowledge root node
        const { data: knowledgeNodes, error: findError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id')
            .eq('name', 'Knowledge')
            .is('parent_id', null);
            
        if (findError) throw findError;
        
        if (knowledgeNodes.length === 0) {
            console.log('No Knowledge root node found - nothing to remove');
            return;
        }
        
        console.log(`Found ${knowledgeNodes.length} Knowledge root node(s)`);
        
        for (const knowledgeNode of knowledgeNodes) {
            console.log(`Processing Knowledge node: ${knowledgeNode.id}`);
            
            // Check if it has any children
            const { count: childCount, error: countError } = await supabase
                .from('skill_tree_nodes')
                .select('*', { count: 'exact', head: true })
                .eq('parent_id', knowledgeNode.id);
                
            if (countError) throw countError;
            
            if (childCount > 0) {
                console.log(`  ⚠️ Knowledge node has ${childCount} children - need to handle them first`);
                
                // Get the children
                const { data: children, error: childError } = await supabase
                    .from('skill_tree_nodes')
                    .select('id, name, type')
                    .eq('parent_id', knowledgeNode.id);
                    
                if (childError) throw childError;
                
                console.log('  Children found:');
                children.forEach(child => {
                    console.log(`    - ${child.name} (${child.type})`);
                });
                
                // For now, let's delete the children too since they're the extra nested structure
                for (const child of children) {
                    // Check if child has grandchildren
                    const { count: grandchildCount } = await supabase
                        .from('skill_tree_nodes')
                        .select('*', { count: 'exact', head: true })
                        .eq('parent_id', child.id);
                        
                    if (grandchildCount > 0) {
                        console.log(`    ${child.name} has ${grandchildCount} children - this is the nested structure we created`);
                    }
                    
                    // Delete the child and all its descendants recursively
                    await deleteNodeAndDescendants(child.id, `    `);
                }
            }
            
            // Now delete the Knowledge root node itself
            const { error: deleteError } = await supabase
                .from('skill_tree_nodes')
                .delete()
                .eq('id', knowledgeNode.id);
                
            if (deleteError) {
                console.log(`  ❌ Failed to delete Knowledge node: ${deleteError.message}`);
            } else {
                console.log(`  ✅ Deleted Knowledge root node`);
            }
        }
        
        console.log('\n✅ Cleanup complete!');
        
    } catch (error) {
        console.error('Error removing Knowledge root:', error);
    }
}

async function deleteNodeAndDescendants(nodeId, indent = '') {
    // Get all children first
    const { data: children, error: childError } = await supabase
        .from('skill_tree_nodes')
        .select('id, name')
        .eq('parent_id', nodeId);
        
    if (childError) {
        console.log(`${indent}❌ Error getting children: ${childError.message}`);
        return;
    }
    
    // Recursively delete all descendants first
    for (const child of children) {
        await deleteNodeAndDescendants(child.id, indent + '  ');
    }
    
    // Then delete this node
    const { error: deleteError } = await supabase
        .from('skill_tree_nodes')
        .delete()
        .eq('id', nodeId);
        
    if (deleteError) {
        console.log(`${indent}❌ Failed to delete node ${nodeId}: ${deleteError.message}`);
    } else {
        console.log(`${indent}🗑️ Deleted node and its descendants`);
    }
}

removeKnowledgeRoot();
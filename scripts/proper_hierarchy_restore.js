require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function properHierarchyRestore() {
    try {
        console.log('🔧 PROPER HIERARCHY RESTORE: Rebuilding skill tree correctly...\n');
        
        // The 12 categories that should be at the root level
        const targetTopLevelCategories = [
            'Mathematics', 'Languages', 'Natural Sciences', 'Computer Science',
            'Social Sciences', 'Humanities', 'Applied Sciences', 'Creative Skills',
            'Professional Skills', 'Technical Skills', 'Life Skills', 'Test Preparation and Assessment'
        ];
        
        console.log('=== STEP 1: Find the target top-level categories ===');
        
        const topLevelNodes = {};
        for (const categoryName of targetTopLevelCategories) {
            const { data: nodes, error } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, type')
                .eq('name', categoryName)
                .eq('type', 'category');
                
            if (error) throw error;
            
            if (nodes.length > 0) {
                topLevelNodes[categoryName] = nodes[0];
                console.log(`✅ Found ${categoryName} (id: ${nodes[0].id})`);
                
                // Make sure this category is at root level
                const { error: updateError } = await supabase
                    .from('skill_tree_nodes')
                    .update({ 
                        parent_id: null,
                        updated_at: new Date().toISOString()
                    })
                    .eq('id', nodes[0].id);
                    
                if (updateError) {
                    console.error(`Error setting ${categoryName} as root:`, updateError);
                }
            } else {
                console.log(`❌ Missing ${categoryName}`);
            }
        }
        
        console.log('\\n=== STEP 2: Rebuild hierarchy for all other nodes ===');
        
        // Get all nodes that are NOT our target top-level categories
        const { data: allNodes, error: allNodesError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, learning_area, parent_id')
            .not('name', 'in', `(${targetTopLevelCategories.map(n => `"${n}"`).join(',')})`);
            
        if (allNodesError) throw allNodesError;
        
        console.log(`Processing ${allNodes.length} nodes to assign correct parents...`);
        
        let reassignCount = 0;
        let errorCount = 0;
        
        for (const node of allNodes) {
            // Skip nodes that already have appropriate parents
            if (node.parent_id && topLevelNodes[Object.keys(topLevelNodes).find(key => topLevelNodes[key].id === node.parent_id)]) {
                continue;
            }
            
            // Find the appropriate top-level parent based on learning_area
            let parentNode = null;
            const learningArea = node.learning_area;
            
            // Direct mapping first
            if (topLevelNodes[learningArea]) {
                parentNode = topLevelNodes[learningArea];
            } else {
                // Fallback mappings for nodes with learning areas that don't match exactly
                const fallbackMappings = {
                    'Applied Knowledge': 'Technical Skills',
                    'root': null, // Special case - delete these
                    'Academic Disciplines': null // Delete these too
                };
                
                if (fallbackMappings.hasOwnProperty(learningArea)) {
                    const fallbackArea = fallbackMappings[learningArea];
                    if (fallbackArea) {
                        parentNode = topLevelNodes[fallbackArea];
                    } else {
                        // Delete nodes with 'root' or 'Academic Disciplines' learning area
                        console.log(`🗑️ Deleting obsolete node: ${node.name}`);
                        const { error: deleteError } = await supabase
                            .from('skill_tree_nodes')
                            .delete()
                            .eq('id', node.id);
                            
                        if (deleteError) {
                            console.error(`Error deleting ${node.name}:`, deleteError);
                            errorCount++;
                        }
                        continue;
                    }
                }
            }
            
            if (parentNode) {
                const { error: updateError } = await supabase
                    .from('skill_tree_nodes')
                    .update({ 
                        parent_id: parentNode.id,
                        updated_at: new Date().toISOString()
                    })
                    .eq('id', node.id);
                    
                if (updateError) {
                    console.error(`Error reassigning ${node.name}:`, updateError);
                    errorCount++;
                } else {
                    reassignCount++;
                    if (reassignCount % 100 === 0) {
                        console.log(`  Processed ${reassignCount} nodes...`);
                    }
                }
            } else {
                console.log(`⚠️ Could not find parent for "${node.name}" (learning_area: ${learningArea})`);
                errorCount++;
            }
        }
        
        console.log('\\n=== STEP 3: Verification ===');
        
        // Check final structure
        const { data: finalRootNodes, error: finalError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type')
            .is('parent_id', null)
            .order('name');
            
        if (finalError) throw finalError;
        
        console.log('\\nFinal root-level nodes:');
        finalRootNodes.forEach(node => {
            console.log(`- ${node.name} (${node.type})`);
        });
        
        const skillsAtRoot = finalRootNodes.filter(n => n.type === 'skill').length;
        const categoriesAtRoot = finalRootNodes.filter(n => n.type === 'category').length;
        
        console.log(`\\n📊 FINAL SUMMARY:`);
        console.log(`- Categories at root level: ${categoriesAtRoot}`);
        console.log(`- Skills at root level: ${skillsAtRoot}`);
        console.log(`- Nodes reassigned: ${reassignCount}`);
        console.log(`- Errors encountered: ${errorCount}`);
        
        if (skillsAtRoot === 0 && categoriesAtRoot === targetTopLevelCategories.length) {
            console.log('\\n🎉 HIERARCHY SUCCESSFULLY RESTORED!');
            console.log('The skill tree now has the correct structure with 12 top-level categories.');
        } else {
            console.log('\\n⚠️ HIERARCHY NEEDS ADDITIONAL WORK');
            if (skillsAtRoot > 0) {
                console.log(`- ${skillsAtRoot} individual skills are still at root level`);
            }
            if (categoriesAtRoot !== targetTopLevelCategories.length) {
                console.log(`- Expected ${targetTopLevelCategories.length} categories at root, found ${categoriesAtRoot}`);
            }
        }
        
    } catch (error) {
        console.error('Error during proper hierarchy restore:', error);
    }
}

properHierarchyRestore();
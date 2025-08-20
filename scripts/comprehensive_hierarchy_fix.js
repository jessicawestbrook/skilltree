require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function comprehensiveHierarchyFix() {
    try {
        console.log('🚨 COMPREHENSIVE HIERARCHY FIX: Starting complete restoration...\n');
        
        // Step 1: Create the 12 expected top-level categories if they don't exist
        const expectedTopLevel = [
            'Mathematics', 'Languages', 'Natural Sciences', 'Computer Science',
            'Social Sciences', 'Humanities', 'Applied Sciences', 'Creative Skills',
            'Professional Skills', 'Technical Skills', 'Life Skills', 'Test Preparation and Assessment'
        ];
        
        console.log('=== STEP 1: Ensure top-level categories exist ===');
        
        const topLevelNodes = {};
        for (const categoryName of expectedTopLevel) {
            // Try to find existing node
            const { data: existing, error: findError } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, learning_area')
                .eq('name', categoryName)
                .eq('type', 'category');
                
            if (findError) throw findError;
            
            if (existing.length > 0) {
                // Make sure it's at root level
                const node = existing[0];
                const { error: updateError } = await supabase
                    .from('skill_tree_nodes')
                    .update({ 
                        parent_id: null,
                        learning_area: categoryName,
                        updated_at: new Date().toISOString()
                    })
                    .eq('id', node.id);
                    
                if (updateError) throw updateError;
                topLevelNodes[categoryName] = node;
                console.log(`✅ Found and fixed: ${categoryName}`);
            } else {
                // Create missing category
                console.log(`❌ Missing category: ${categoryName} - would need to be recreated`);
            }
        }
        
        console.log(`\nFound ${Object.keys(topLevelNodes).length} existing top-level categories`);
        
        // Step 2: Fix all orphaned nodes
        console.log('\n=== STEP 2: Fix orphaned nodes ===');
        
        // Get all nodes
        const { data: allNodes, error: allError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, parent_id, learning_area');
            
        if (allError) throw allError;
        
        // Find orphaned nodes
        const nodeIds = new Set(allNodes.map(n => n.id));
        const orphanedNodes = allNodes.filter(n => 
            n.parent_id !== null && !nodeIds.has(n.parent_id)
        );
        
        console.log(`Found ${orphanedNodes.length} orphaned nodes to fix...`);
        
        let fixedCount = 0;
        const batchSize = 100;
        
        for (let i = 0; i < orphanedNodes.length; i += batchSize) {
            const batch = orphanedNodes.slice(i, i + batchSize);
            console.log(`Processing batch ${Math.floor(i/batchSize) + 1}/${Math.ceil(orphanedNodes.length/batchSize)}`);
            
            for (const node of batch) {
                let targetParent = null;
                
                // Try to find appropriate parent based on learning_area
                if (topLevelNodes[node.learning_area]) {
                    targetParent = topLevelNodes[node.learning_area];
                } else {
                    // Fallback mapping for difficult cases
                    const mappings = {
                        'Applied Knowledge': topLevelNodes['Technical Skills'],
                        'Academic Disciplines': topLevelNodes['Humanities'], // Default fallback
                        'root': null // Delete these
                    };
                    
                    if (mappings.hasOwnProperty(node.learning_area)) {
                        targetParent = mappings[node.learning_area];
                    } else {
                        // Try to map based on content type
                        const contentMappings = {
                            'Mathematics': topLevelNodes['Mathematics'],
                            'Languages': topLevelNodes['Languages'],
                            'Natural Sciences': topLevelNodes['Natural Sciences'],
                            'Computer Science': topLevelNodes['Computer Science'],
                            'Social Sciences': topLevelNodes['Social Sciences'],
                            'Humanities': topLevelNodes['Humanities'],
                            'Applied Sciences': topLevelNodes['Applied Sciences']
                        };
                        
                        // Try to guess from node name
                        const nodeName = node.name.toLowerCase();
                        if (nodeName.includes('math') || nodeName.includes('algebra') || nodeName.includes('calculus')) {
                            targetParent = topLevelNodes['Mathematics'];
                        } else if (nodeName.includes('language') || nodeName.includes('french') || nodeName.includes('spanish') || nodeName.includes('latin')) {
                            targetParent = topLevelNodes['Languages'];
                        } else if (nodeName.includes('science') || nodeName.includes('chemistry') || nodeName.includes('physics') || nodeName.includes('biology')) {
                            targetParent = topLevelNodes['Natural Sciences'];
                        } else if (nodeName.includes('computer') || nodeName.includes('programming') || nodeName.includes('algorithm')) {
                            targetParent = topLevelNodes['Computer Science'];
                        } else if (nodeName.includes('history') || nodeName.includes('literature') || nodeName.includes('philosophy')) {
                            targetParent = topLevelNodes['Humanities'];
                        } else if (nodeName.includes('psychology') || nodeName.includes('sociology') || nodeName.includes('politics')) {
                            targetParent = topLevelNodes['Social Sciences'];
                        } else {
                            // Default to Humanities if we can't determine
                            targetParent = topLevelNodes['Humanities'];
                        }
                    }
                }
                
                if (targetParent === null) {
                    // Delete node with null learning area
                    console.log(`🗑️ Deleting: ${node.name}`);
                    const { error: deleteError } = await supabase
                        .from('skill_tree_nodes')
                        .delete()
                        .eq('id', node.id);
                        
                    if (!deleteError) fixedCount++;
                } else if (targetParent) {
                    // Reassign to appropriate parent
                    const { error: updateError } = await supabase
                        .from('skill_tree_nodes')
                        .update({ 
                            parent_id: targetParent.id,
                            learning_area: targetParent.name,
                            updated_at: new Date().toISOString()
                        })
                        .eq('id', node.id);
                        
                    if (!updateError) fixedCount++;
                }
            }
        }
        
        console.log(`Fixed ${fixedCount} orphaned nodes`);
        
        // Step 3: Final verification
        console.log('\n=== STEP 3: Final verification ===');
        
        // Check final root structure
        const { data: finalRootNodes, error: finalError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type')
            .is('parent_id', null)
            .order('name');
            
        if (finalError) throw finalError;
        
        console.log('\nFinal root-level structure:');
        const finalCategories = finalRootNodes.filter(n => n.type === 'category');
        const finalSkills = finalRootNodes.filter(n => n.type === 'skill');
        
        finalCategories.forEach(cat => {
            console.log(`✅ ${cat.name}`);
        });
        
        if (finalSkills.length > 0) {
            console.log(`\n❌ ${finalSkills.length} skills still at root level`);
        }
        
        // Check for remaining orphans
        const { data: allNodesAfter, error: allAfterError } = await supabase
            .from('skill_tree_nodes')
            .select('id, parent_id');
            
        if (allAfterError) throw allAfterError;
        
        const nodeIdsAfter = new Set(allNodesAfter.map(n => n.id));
        const remainingOrphans = allNodesAfter.filter(n => 
            n.parent_id !== null && !nodeIdsAfter.has(n.parent_id)
        );
        
        console.log(`\n📊 FINAL RESULTS:`);
        console.log(`- Root categories: ${finalCategories.length} (target: 12)`);
        console.log(`- Root skills: ${finalSkills.length} (target: 0)`);
        console.log(`- Remaining orphaned nodes: ${remainingOrphans.length} (target: 0)`);
        console.log(`- Total nodes fixed: ${fixedCount}`);
        
        if (finalCategories.length === 12 && finalSkills.length === 0 && remainingOrphans.length === 0) {
            console.log('\n🎉 HIERARCHY FULLY RESTORED!');
        } else {
            console.log('\n⚠️ HIERARCHY STILL NEEDS WORK');
        }
        
    } catch (error) {
        console.error('Error in comprehensive hierarchy fix:', error);
    }
}

comprehensiveHierarchyFix();
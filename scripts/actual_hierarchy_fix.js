require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function actualHierarchyFix() {
    try {
        console.log('🔧 ACTUAL HIERARCHY FIX: Fixing the real issues...\n');
        
        // Step 1: Get the current UUIDs of our target top-level categories
        const expectedCategories = [
            'Mathematics', 'Languages', 'Natural Sciences', 'Computer Science',
            'Social Sciences', 'Humanities', 'Applied Sciences', 'Creative Skills',
            'Professional Skills', 'Technical Skills', 'Life Skills', 'Test Preparation and Assessment'
        ];
        
        const { data: existingTopLevel, error: topError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, learning_area')
            .in('name', expectedCategories)
            .eq('type', 'category');
            
        if (topError) throw topError;
        
        const topLevelMap = {};
        existingTopLevel.forEach(cat => {
            topLevelMap[cat.name] = cat;
        });
        
        console.log(`Found ${existingTopLevel.length} existing top-level categories with these IDs:`);
        existingTopLevel.forEach(cat => {
            console.log(`  ${cat.name}: ${cat.id}`);
        });
        
        // Step 2: Get all orphaned nodes that point to non-existent parents
        const { data: allNodes, error: allError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, parent_id, learning_area');
            
        if (allError) throw allError;
        
        const allNodeIds = new Set(allNodes.map(n => n.id));
        const orphanedNodes = allNodes.filter(n => 
            n.parent_id !== null && !allNodeIds.has(n.parent_id)
        );
        
        console.log(`\nFound ${orphanedNodes.length} orphaned nodes to fix`);
        
        // Step 3: Fix orphaned nodes in smaller batches
        let fixedCount = 0;
        const batchSize = 50;
        
        for (let i = 0; i < orphanedNodes.length; i += batchSize) {
            const batch = orphanedNodes.slice(i, i + batchSize);
            console.log(`\nProcessing batch ${Math.floor(i/batchSize) + 1} of ${Math.ceil(orphanedNodes.length/batchSize)}`);
            
            for (const node of batch) {
                let newParent = null;
                
                // Match by learning_area first
                if (topLevelMap[node.learning_area]) {
                    newParent = topLevelMap[node.learning_area];
                } else {
                    // Smart fallback based on node name and type
                    const name = node.name.toLowerCase();
                    
                    if (name.includes('math') || name.includes('algebra') || name.includes('calculus') || name.includes('arithmetic') || name.includes('geometry')) {
                        newParent = topLevelMap['Mathematics'];
                    } else if (name.includes('language') || name.includes('spanish') || name.includes('french') || name.includes('latin') || name.includes('arabic') || name.includes('chinese') || name.includes('japanese') || name.includes('german') || name.includes('italian')) {
                        newParent = topLevelMap['Languages'];
                    } else if (name.includes('science') || name.includes('chemistry') || name.includes('physics') || name.includes('biology') || name.includes('astronomy') || name.includes('biochemistry')) {
                        newParent = topLevelMap['Natural Sciences'];
                    } else if (name.includes('computer') || name.includes('programming') || name.includes('algorithm') || name.includes('data structure') || name.includes('database') || name.includes('javascript') || name.includes('python')) {
                        newParent = topLevelMap['Computer Science'];
                    } else if (name.includes('history') || name.includes('literature') || name.includes('philosophy') || name.includes('ancient') || name.includes('medieval') || name.includes('renaissance')) {
                        newParent = topLevelMap['Humanities'];
                    } else if (name.includes('psychology') || name.includes('sociology') || name.includes('politics') || name.includes('economics') || name.includes('government')) {
                        newParent = topLevelMap['Social Sciences'];
                    } else if (name.includes('engineering') || name.includes('medicine') || name.includes('business') || name.includes('applied')) {
                        newParent = topLevelMap['Applied Sciences'];
                    } else if (name.includes('art') || name.includes('design') || name.includes('music') || name.includes('creative') || name.includes('writing') || name.includes('media')) {
                        newParent = topLevelMap['Creative Skills'];
                    } else if (name.includes('professional') || name.includes('management') || name.includes('leadership') || name.includes('sales') || name.includes('marketing')) {
                        newParent = topLevelMap['Professional Skills'];
                    } else if (name.includes('technical') || name.includes('technology') || name.includes('digital') || name.includes('cyber') || name.includes('cloud')) {
                        newParent = topLevelMap['Technical Skills'];
                    } else if (name.includes('life') || name.includes('communication') || name.includes('critical thinking') || name.includes('financial')) {
                        newParent = topLevelMap['Life Skills'];
                    } else if (name.includes('test') || name.includes('exam') || name.includes('act') || name.includes('sat') || name.includes('gre')) {
                        newParent = topLevelMap['Test Preparation and Assessment'];
                    } else {
                        // Default fallback based on type
                        if (node.type === 'category') {
                            newParent = topLevelMap['Humanities']; // Default for uncategorized categories
                        } else {
                            newParent = topLevelMap['Technical Skills']; // Default for uncategorized skills
                        }
                    }
                }
                
                if (newParent) {
                    try {
                        const { error: updateError } = await supabase
                            .from('skill_tree_nodes')
                            .update({
                                parent_id: newParent.id,
                                learning_area: newParent.name,
                                updated_at: new Date().toISOString()
                            })
                            .eq('id', node.id);
                            
                        if (updateError) {
                            console.error(`  ❌ Failed to update ${node.name}: ${updateError.message}`);
                        } else {
                            fixedCount++;
                            console.log(`  ✅ ${node.name} → ${newParent.name}`);
                        }
                    } catch (err) {
                        console.error(`  ❌ Error updating ${node.name}:`, err.message);
                    }
                } else {
                    console.log(`  ⚠️ No suitable parent found for: ${node.name}`);
                }
                
                // Small delay to prevent overwhelming the database
                if (fixedCount % 10 === 0) {
                    await new Promise(resolve => setTimeout(resolve, 100));
                }
            }
        }
        
        console.log(`\n📊 RESULTS:`);
        console.log(`- Total orphaned nodes processed: ${orphanedNodes.length}`);
        console.log(`- Successfully fixed: ${fixedCount}`);
        console.log(`- Failed to fix: ${orphanedNodes.length - fixedCount}`);
        
        // Final verification
        console.log('\n=== FINAL VERIFICATION ===');
        
        const { data: finalCheck, error: finalError } = await supabase
            .from('skill_tree_nodes')
            .select('id, parent_id');
            
        if (finalError) throw finalError;
        
        const finalNodeIds = new Set(finalCheck.map(n => n.id));
        const remainingOrphans = finalCheck.filter(n => 
            n.parent_id !== null && !finalNodeIds.has(n.parent_id)
        );
        
        console.log(`Remaining orphaned nodes: ${remainingOrphans.length}`);
        
        if (remainingOrphans.length === 0) {
            console.log('🎉 ALL ORPHANED NODES FIXED!');
        } else {
            console.log(`⚠️ ${remainingOrphans.length} nodes still need fixing`);
        }
        
    } catch (error) {
        console.error('Error in actual hierarchy fix:', error);
    }
}

actualHierarchyFix();
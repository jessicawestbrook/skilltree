require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function moveCivicEducationToHumanities() {
    try {
        console.log('🔄 MOVING CIVIC EDUCATION & GOVERNMENT TO HUMANITIES\n');
        
        // Step 1: Find the Humanities category
        console.log('🔍 Finding Humanities category...');
        const { data: humanities, error: humanitiesError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, display_order')
            .eq('name', 'Humanities')
            .is('parent_id', null)
            .single();
            
        if (humanitiesError || !humanities) {
            console.error('❌ Error finding Humanities category:', humanitiesError);
            return;
        }
        
        console.log(`✅ Found Humanities: ${humanities.id}`);
        
        // Step 2: Find the Civic Education & Government category
        console.log('\n🔍 Finding Civic Education & Government category...');
        const { data: civicEducation, error: civicError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id, display_order')
            .eq('name', 'Civic Education & Government')
            .single();
            
        if (civicError || !civicEducation) {
            console.error('❌ Error finding Civic Education category:', civicError);
            return;
        }
        
        console.log(`✅ Found Civic Education & Government: ${civicEducation.id}`);
        console.log(`   Current parent_id: ${civicEducation.parent_id || 'null (top-level)'}`);
        
        // Step 3: Check current Humanities subcategories to determine appropriate display_order
        console.log('\n🔍 Checking existing Humanities subcategories...');
        const { data: humanitiesChildren, error: childrenError } = await supabase
            .from('skill_tree_nodes')
            .select('name, display_order')
            .eq('parent_id', humanities.id)
            .order('display_order', { nullsFirst: false })
            .order('name');
            
        if (childrenError) {
            console.error('❌ Error fetching Humanities children:', childrenError);
            return;
        }
        
        console.log(`Found ${humanitiesChildren.length} existing subcategories under Humanities:`);
        humanitiesChildren.forEach(child => {
            console.log(`   • ${child.name} (order: ${child.display_order || 'null'})`);
        });
        
        // Determine appropriate display order (place it after existing categories)
        const maxOrder = Math.max(...humanitiesChildren.map(c => c.display_order || 0));
        const newDisplayOrder = maxOrder + 10;
        console.log(`\n📝 Will assign display_order: ${newDisplayOrder} to Civic Education`);
        
        // Step 4: Update the Civic Education category to move it under Humanities
        console.log('\n🔄 Moving Civic Education & Government under Humanities...');
        const { error: updateError } = await supabase
            .from('skill_tree_nodes')
            .update({
                parent_id: humanities.id,
                display_order: newDisplayOrder
            })
            .eq('id', civicEducation.id);
            
        if (updateError) {
            console.error('❌ Error updating Civic Education parent:', updateError);
            return;
        }
        
        console.log('✅ Successfully moved Civic Education & Government under Humanities');
        
        // Step 5: Update path for Civic Education and all its descendants
        console.log('\n🔄 Updating path hierarchy for all affected nodes...');
        
        // Get all descendants of Civic Education
        const { data: allCivicNodes, error: descendantsError } = await supabase
            .rpc('get_node_descendants', { node_id: civicEducation.id });
            
        if (descendantsError) {
            // If RPC doesn't exist, get them manually
            console.log('Using manual method to get descendants...');
            
            // Get direct children first
            const { data: directChildren, error: directError } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, type')
                .eq('parent_id', civicEducation.id);
                
            if (directError) {
                console.error('❌ Error getting direct children:', directError);
                return;
            }
            
            // Update Civic Education itself
            await supabase
                .from('skill_tree_nodes')
                .update({
                    path: ['Humanities']
                })
                .eq('id', civicEducation.id);
            console.log('   ✅ Updated Civic Education & Government path');
            
            // Update all direct children
            for (const child of directChildren) {
                await supabase
                    .from('skill_tree_nodes')
                    .update({
                        path: ['Humanities', 'Civic Education & Government']
                    })
                    .eq('id', child.id);
                console.log(`   ✅ Updated path for ${child.name}`);
                
                // Update grandchildren (skills under subcategories)
                const { data: grandchildren, error: grandError } = await supabase
                    .from('skill_tree_nodes')
                    .select('id, name')
                    .eq('parent_id', child.id);
                    
                if (!grandError && grandchildren) {
                    for (const grandchild of grandchildren) {
                        await supabase
                            .from('skill_tree_nodes')
                            .update({
                                path: ['Humanities', 'Civic Education & Government', child.name]
                            })
                            .eq('id', grandchild.id);
                        console.log(`   ✅ Updated path for ${grandchild.name}`);
                    }
                }
            }
        } else {
            // Use RPC result
            for (const node of allCivicNodes) {
                const newPath = ['Humanities', ...node.path.slice(1)];
                await supabase
                    .from('skill_tree_nodes')
                    .update({ path: newPath })
                    .eq('id', node.id);
                console.log(`   ✅ Updated path for ${node.name}`);
            }
        }
        
        // Step 6: Verify the changes
        console.log('\n✅ VERIFICATION\n');
        
        // Check updated Civic Education
        const { data: updatedCivic, error: verifyError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id, display_order, path')
            .eq('id', civicEducation.id)
            .single();
            
        if (verifyError) {
            console.error('❌ Error verifying update:', verifyError);
        } else {
            console.log('Updated Civic Education & Government:');
            console.log(`   Parent ID: ${updatedCivic.parent_id} (should be ${humanities.id})`);
            console.log(`   Display Order: ${updatedCivic.display_order}`);
            console.log(`   Path: ${JSON.stringify(updatedCivic.path)}`);
        }
        
        // Check Humanities subcategories
        const { data: updatedHumanities, error: updatedError } = await supabase
            .from('skill_tree_nodes')
            .select('name, display_order')
            .eq('parent_id', humanities.id)
            .order('display_order', { nullsFirst: false })
            .order('name');
            
        if (!updatedError) {
            console.log(`\nUpdated Humanities subcategories (${updatedHumanities.length}):`);
            updatedHumanities.forEach(child => {
                const marker = child.name === 'Civic Education & Government' ? '🆕' : '  ';
                console.log(`${marker} • ${child.name} (order: ${child.display_order || 'null'})`);
            });
        }
        
        // Check top-level categories
        const { data: topLevel, error: topError } = await supabase
            .from('skill_tree_nodes')
            .select('name, display_order')
            .is('parent_id', null)
            .order('display_order', { nullsFirst: false })
            .order('name');
            
        if (!topError) {
            console.log(`\nTop-level categories (${topLevel.length}):`);
            topLevel.forEach((cat, index) => {
                console.log(`   ${index + 1}. ${cat.name} (order: ${cat.display_order || 'null'})`);
            });
        }
        
        console.log('\n🎉 Successfully moved Civic Education & Government under Humanities!');
        console.log('✅ Hierarchy updated');
        console.log('✅ Paths updated for all descendant nodes');
        console.log('✅ Academic ordering maintained');
        
    } catch (error) {
        console.error('❌ Migration failed:', error);
    }
}

moveCivicEducationToHumanities();
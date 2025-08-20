require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function promoteCategoriesToTopLevel() {
    try {
        console.log('📈 PROMOTING CATEGORIES TO TOP-LEVEL...\n');
        
        // Categories to promote to top-level
        const categoriesToPromote = [
            { name: 'Mathematics', newLearningArea: 'Mathematics' },
            { name: 'Computer Science', newLearningArea: 'Computer Science' },
            { name: 'Languages', newLearningArea: 'Languages' }
        ];
        
        for (const category of categoriesToPromote) {
            console.log(`Processing ${category.name}...`);
            
            // Find the category
            const { data: categoryNode, error: findError } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, parent_id, learning_area')
                .eq('name', category.name)
                .eq('type', 'category')
                .single();
                
            if (findError) {
                console.log(`  ❌ Could not find ${category.name}: ${findError.message}`);
                continue;
            }
            
            if (categoryNode.parent_id === null) {
                console.log(`  ✅ ${category.name} is already top-level`);
                continue;
            }
            
            console.log(`  📤 Promoting ${category.name} to top-level...`);
            console.log(`     Current parent: ${categoryNode.parent_id}`);
            console.log(`     Current learning area: ${categoryNode.learning_area}`);
            
            // Update to make it top-level
            const { error: updateError } = await supabase
                .from('skill_tree_nodes')
                .update({
                    parent_id: null,
                    learning_area: category.newLearningArea,
                    path: [],
                    updated_at: new Date().toISOString()
                })
                .eq('id', categoryNode.id);
                
            if (updateError) {
                console.log(`  ❌ Failed to promote ${category.name}: ${updateError.message}`);
                continue;
            }
            
            console.log(`  ✅ Successfully promoted ${category.name} to top-level`);
            
            // Update all descendant nodes to have the new learning area
            console.log(`  🔄 Updating descendants to use learning area: ${category.newLearningArea}`);
            
            const { error: descendantsError } = await supabase
                .rpc('update_descendants_learning_area', {
                    root_node_id: categoryNode.id,
                    new_learning_area: category.newLearningArea
                });
                
            if (descendantsError) {
                // If the RPC doesn't exist, do it manually with recursive query
                console.log(`  📝 Updating descendants manually...`);
                
                // Get all descendants recursively  
                let nodesToUpdate = [categoryNode.id];
                let allDescendants = [];
                
                while (nodesToUpdate.length > 0) {
                    const { data: children, error: childrenError } = await supabase
                        .from('skill_tree_nodes')
                        .select('id')
                        .in('parent_id', nodesToUpdate);
                        
                    if (childrenError) throw childrenError;
                    
                    if (children.length === 0) break;
                    
                    const childIds = children.map(c => c.id);
                    allDescendants.push(...childIds);
                    nodesToUpdate = childIds;
                }
                
                if (allDescendants.length > 0) {
                    const { error: updateDescendantsError } = await supabase
                        .from('skill_tree_nodes')
                        .update({
                            learning_area: category.newLearningArea,
                            updated_at: new Date().toISOString()
                        })
                        .in('id', allDescendants);
                        
                    if (updateDescendantsError) {
                        console.log(`  ⚠️ Warning: Could not update all descendants: ${updateDescendantsError.message}`);
                    } else {
                        console.log(`  ✅ Updated ${allDescendants.length} descendant nodes`);
                    }
                }
            } else {
                console.log(`  ✅ Updated descendants using RPC`);
            }
        }
        
        // Verify final structure
        console.log('\n=== FINAL VERIFICATION ===');
        
        const { data: rootCategories, error: rootError } = await supabase
            .from('skill_tree_nodes')
            .select('name, learning_area')
            .is('parent_id', null)
            .eq('type', 'category')
            .order('name');
            
        if (rootError) throw rootError;
        
        console.log(`\nTop-level categories (${rootCategories.length}):`);
        rootCategories.forEach((cat, i) => {
            console.log(`  ${i+1}. ${cat.name} (${cat.learning_area})`);
        });
        
        // Check if we have the expected 12 categories
        const expectedTopLevel = [
            'Mathematics', 'Languages', 'Computer Science', 'Natural Sciences',
            'Social Sciences', 'Humanities', 'Applied Sciences', 'Creative Skills',
            'Professional Skills', 'Technical Skills', 'Life Skills', 
            'Test Preparation and Assessment'
        ];
        
        const currentTopLevel = rootCategories.map(c => c.name);
        const missing = expectedTopLevel.filter(name => !currentTopLevel.includes(name));
        const extra = currentTopLevel.filter(name => !expectedTopLevel.includes(name));
        
        if (missing.length === 0 && extra.length === 0) {
            console.log('\n🎉 SUCCESS! All 12 expected top-level categories are present!');
        } else {
            console.log('\n📊 Summary:');
            if (missing.length > 0) {
                console.log(`Missing: ${missing.join(', ')}`);
            }
            if (extra.length > 0) {
                console.log(`Extra: ${extra.join(', ')}`);
            }
        }
        
        // Final count
        const { count, error: countError } = await supabase
            .from('skill_tree_nodes')
            .select('*', { count: 'exact', head: true });
            
        if (countError) throw countError;
        
        console.log(`\n📈 PROMOTION COMPLETE!`);
        console.log(`Total nodes: ${count}`);
        console.log(`Top-level categories: ${rootCategories.length}`);
        
    } catch (error) {
        console.error('Error promoting categories:', error);
    }
}

promoteCategoriesToTopLevel();
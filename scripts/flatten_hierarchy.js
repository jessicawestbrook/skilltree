require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function flattenHierarchy() {
    try {
        console.log('Starting hierarchy flattening process...\n');
        
        // Step 1: Get the nodes we'll be working with
        const { data: level1, error: level1Error } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .is('parent_id', null);
            
        if (level1Error) throw level1Error;
        
        const { data: level2, error: level2Error } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .in('parent_id', level1.map(n => n.id));
            
        if (level2Error) throw level2Error;
        
        const { data: level3, error: level3Error } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, learning_area, display_order')
            .in('parent_id', level2.map(n => n.id))
            .order('display_order', { nullsLast: true })
            .order('name');
            
        if (level3Error) throw level3Error;
        
        console.log(`Found ${level1.length} level 1 nodes, ${level2.length} level 2 nodes, ${level3.length} level 3 nodes to promote`);
        
        // Step 2: Update level 3 nodes to have no parent (make them top-level)
        console.log('\n=== STEP 2: Promoting level 3 nodes to top level ===');
        
        let promotionCount = 0;
        for (const node of level3) {
            const { error: updateError } = await supabase
                .from('skill_tree_nodes')
                .update({ 
                    parent_id: null,
                    updated_at: new Date().toISOString()
                })
                .eq('id', node.id);
                
            if (updateError) {
                console.error(`Error promoting ${node.name}:`, updateError);
            } else {
                console.log(`✅ Promoted "${node.name}" to top level`);
                promotionCount++;
            }
        }
        
        console.log(`Successfully promoted ${promotionCount} categories to top level`);
        
        // Step 3: Check for dependencies excluding the level 2 nodes themselves
        console.log('\n=== STEP 3: Checking for remaining dependencies ===');
        
        const level2Ids = level2.map(n => n.id);
        const level1Ids = level1.map(n => n.id);
        
        // Check for any nodes that depend on level 1 nodes (excluding level 2 nodes)
        const { data: level1Dependents, error: dep1Error } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id')
            .in('parent_id', level1Ids)
            .not('id', 'in', `(${level2Ids.join(',')})`);
            
        if (dep1Error) throw dep1Error;
        
        // Check for any nodes that depend on level 2 nodes (should be none since we promoted level 3)
        const { data: level2Dependents, error: dep2Error } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id')
            .in('parent_id', level2Ids);
            
        if (dep2Error) throw dep2Error;
        
        const totalDependents = level1Dependents.length + level2Dependents.length;
        
        if (totalDependents > 0) {
            console.log(`⚠️ WARNING: Found unexpected dependencies:`);
            if (level1Dependents.length > 0) {
                console.log('Dependencies on level 1 nodes (excluding level 2):');
                level1Dependents.forEach(node => console.log(`  - ${node.name}`));
            }
            if (level2Dependents.length > 0) {
                console.log('Dependencies on level 2 nodes:');
                level2Dependents.forEach(node => console.log(`  - ${node.name}`));
            }
            console.log('\nAborting removal until dependencies are resolved.');
            return;
        } else {
            console.log('✅ No unexpected dependencies found. Safe to remove level 1 and 2 nodes.');
        }
        
        // Step 4: Remove level 2 nodes first (children before parents)
        console.log('\n=== STEP 4: Removing level 2 nodes ===');
        
        let level2RemovalCount = 0;
        for (const node of level2) {
            const { error: deleteError } = await supabase
                .from('skill_tree_nodes')
                .delete()
                .eq('id', node.id);
                
            if (deleteError) {
                console.error(`Error removing level 2 node ${node.name}:`, deleteError);
            } else {
                console.log(`✅ Removed "${node.name}"`);
                level2RemovalCount++;
            }
        }
        
        // Step 5: Remove level 1 nodes
        console.log('\n=== STEP 5: Removing level 1 nodes ===');
        
        let level1RemovalCount = 0;
        for (const node of level1) {
            const { error: deleteError } = await supabase
                .from('skill_tree_nodes')
                .delete()
                .eq('id', node.id);
                
            if (deleteError) {
                console.error(`Error removing level 1 node ${node.name}:`, deleteError);
            } else {
                console.log(`✅ Removed "${node.name}"`);
                level1RemovalCount++;
            }
        }
        
        console.log('\n🎉 HIERARCHY FLATTENING COMPLETE!');
        console.log(`Summary:`);
        console.log(`- Promoted ${promotionCount} categories to top level`);
        console.log(`- Removed ${level2RemovalCount} level 2 nodes`);
        console.log(`- Removed ${level1RemovalCount} level 1 nodes`);
        
        // Step 6: Verify final structure
        console.log('\n=== VERIFICATION: New top-level structure ===');
        
        const { data: newTopLevel, error: verifyError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, display_order, learning_area')
            .is('parent_id', null)
            .eq('type', 'category')
            .order('display_order', { nullsLast: true })
            .order('name');
            
        if (verifyError) throw verifyError;
        
        console.log('\nNew top-level categories:');
        newTopLevel.forEach((node, i) => {
            console.log(`${i + 1}. ${node.name} (display_order: ${node.display_order || 'null'}, learning_area: ${node.learning_area})`);
        });
        
    } catch (error) {
        console.error('Error flattening hierarchy:', error);
    }
}

flattenHierarchy();
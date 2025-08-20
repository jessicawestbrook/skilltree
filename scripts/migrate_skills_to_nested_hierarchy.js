require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function migrateSkillsToNestedHierarchy() {
    try {
        console.log('🔄 MIGRATING SKILLS TO PROPER NESTED HIERARCHY...\n');
        
        // Step 1: Get all current nodes
        const { data: allNodes, error: allError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, parent_id, learning_area');
            
        if (allError) throw allError;
        
        const nodeMap = {};
        allNodes.forEach(node => {
            nodeMap[node.id] = node;
        });
        
        console.log(`Total nodes in database: ${allNodes.length}`);
        
        // Step 2: Identify the old flat structure vs new nested structure
        const oldFlatCategories = allNodes.filter(node => 
            node.type === 'category' && 
            node.parent_id === null &&
            node.name !== 'Knowledge' && // This is our new root
            [
                'Mathematics', 'Languages', 'Natural Sciences', 'Computer Science', 
                'Social Sciences', 'Humanities', 'Applied Sciences', 'Creative Skills',
                'Professional Skills', 'Technical Skills', 'Life Skills', 
                'Test Preparation and Assessment'
            ].includes(node.name)
        );
        
        console.log(`Found ${oldFlatCategories.length} old flat categories to migrate from:`);
        oldFlatCategories.forEach(cat => console.log(`  - ${cat.name}`));
        
        // Step 3: Find the new nested structure under Knowledge
        const knowledgeRoot = allNodes.find(n => n.name === 'Knowledge' && n.parent_id === null);
        if (!knowledgeRoot) {
            throw new Error('Knowledge root node not found');
        }
        
        // Map old categories to new nested locations
        const categoryMappings = {
            // These should go under Academic Disciplines → Humanities
            'Humanities': 'Knowledge → Academic Disciplines → Humanities',
            'Languages': 'Knowledge → Academic Disciplines → Humanities → Languages',
            
            // These should go under Academic Disciplines → Natural Sciences  
            'Mathematics': 'Knowledge → Academic Disciplines → Natural Sciences → Mathematics',
            'Natural Sciences': 'Knowledge → Academic Disciplines → Natural Sciences',
            
            // These should go under Academic Disciplines → Computer Science
            'Computer Science': 'Knowledge → Academic Disciplines → Computer Science',
            
            // These should go under Academic Disciplines → Social Sciences
            'Social Sciences': 'Knowledge → Academic Disciplines → Social Sciences',
            
            // These should go under Applied Knowledge
            'Professional Skills': 'Knowledge → Applied Knowledge → Professional Skills',
            'Technical Skills': 'Knowledge → Applied Knowledge → Technical Skills', 
            'Life Skills': 'Knowledge → Applied Knowledge → Life Skills',
            
            // These need new categories created
            'Applied Sciences': 'Knowledge → Academic Disciplines → Applied Sciences',
            'Creative Skills': 'Knowledge → Applied Knowledge → Creative Skills',
            'Test Preparation and Assessment': 'Knowledge → Applied Knowledge → Test Preparation and Assessment'
        };
        
        // Step 4: Find target locations in new hierarchy
        function findNodeByPath(path) {
            const pathParts = path.split(' → ');
            let current = knowledgeRoot;
            
            for (let i = 1; i < pathParts.length; i++) { // Skip 'Knowledge' 
                const children = allNodes.filter(n => n.parent_id === current.id);
                current = children.find(child => child.name === pathParts[i]);
                if (!current) {
                    console.log(`  ⚠️ Could not find '${pathParts[i]}' under '${pathParts[i-1]}'`);
                    return null;
                }
            }
            return current;
        }
        
        let migratedSkills = 0;
        let migratedCategories = 0;
        let errors = 0;
        
        // Step 5: Migrate each old category's content
        for (const oldCategory of oldFlatCategories) {
            console.log(`\nProcessing ${oldCategory.name}...`);
            
            const targetPath = categoryMappings[oldCategory.name];
            if (!targetPath) {
                console.log(`  ⚠️ No mapping defined for ${oldCategory.name}`);
                continue;
            }
            
            const targetLocation = findNodeByPath(targetPath);
            if (!targetLocation) {
                console.log(`  ❌ Target location not found: ${targetPath}`);
                continue;
            }
            
            console.log(`  Target: ${targetLocation.name} (${targetLocation.id})`);
            
            // Get all direct children of the old category
            const children = allNodes.filter(n => n.parent_id === oldCategory.id);
            console.log(`  Found ${children.length} children to migrate`);
            
            // Migrate each child
            for (const child of children) {
                try {
                    const { error: updateError } = await supabase
                        .from('skill_tree_nodes')
                        .update({ 
                            parent_id: targetLocation.id,
                            learning_area: targetLocation.learning_area || targetLocation.name,
                            updated_at: new Date().toISOString()
                        })
                        .eq('id', child.id);
                        
                    if (updateError) {
                        console.log(`    ❌ Failed to migrate ${child.name}: ${updateError.message}`);
                        errors++;
                    } else {
                        if (child.type === 'skill') {
                            migratedSkills++;
                        } else {
                            migratedCategories++;
                        }
                        console.log(`    ✅ Migrated ${child.name} (${child.type})`);
                    }
                } catch (err) {
                    console.log(`    ❌ Error migrating ${child.name}: ${err.message}`);
                    errors++;
                }
            }
        }
        
        // Step 6: Remove the now-empty old flat categories
        console.log(`\n=== Cleaning up empty old categories ===`);
        let removedCategories = 0;
        
        for (const oldCategory of oldFlatCategories) {
            // Double-check it has no children
            const { count, error: countError } = await supabase
                .from('skill_tree_nodes')
                .select('*', { count: 'exact', head: true })
                .eq('parent_id', oldCategory.id);
                
            if (countError) {
                console.log(`  ❌ Error checking ${oldCategory.name}: ${countError.message}`);
                continue;
            }
            
            if (count === 0) {
                const { error: deleteError } = await supabase
                    .from('skill_tree_nodes')
                    .delete()
                    .eq('id', oldCategory.id);
                    
                if (!deleteError) {
                    removedCategories++;
                    console.log(`  🗑️ Removed empty category: ${oldCategory.name}`);
                } else {
                    console.log(`  ❌ Failed to remove ${oldCategory.name}: ${deleteError.message}`);
                }
            } else {
                console.log(`  ⚠️ ${oldCategory.name} still has ${count} children, not removing`);
            }
        }
        
        // Step 7: Final summary
        console.log(`\n📊 MIGRATION RESULTS:`);
        console.log(`- Skills migrated: ${migratedSkills}`);
        console.log(`- Categories migrated: ${migratedCategories}`);
        console.log(`- Empty old categories removed: ${removedCategories}`);
        console.log(`- Errors: ${errors}`);
        
        // Step 8: Final verification
        console.log('\n=== FINAL VERIFICATION ===');
        
        const { data: finalNodes, error: finalError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, parent_id');
            
        if (finalError) throw finalError;
        
        const rootNodes = finalNodes.filter(n => n.parent_id === null);
        console.log(`Root nodes after migration: ${rootNodes.length}`);
        rootNodes.forEach(node => {
            console.log(`  - ${node.name}`);
        });
        
        if (rootNodes.length === 1 && rootNodes[0].name === 'Knowledge') {
            console.log('\n🎉 SUCCESS! Hierarchy now has single Knowledge root with proper nesting!');
        } else {
            console.log('\n⚠️ Migration partially successful, but multiple root nodes still exist');
        }
        
    } catch (error) {
        console.error('Error during migration:', error);
    }
}

migrateSkillsToNestedHierarchy();
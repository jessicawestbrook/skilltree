require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function emergencyRestore() {
    try {
        console.log('🚨 EMERGENCY RESTORE: Fixing broken hierarchy...\n');
        
        // First, let's see what we have
        const { data: rootNodes, error: rootError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, learning_area')
            .is('parent_id', null)
            .eq('type', 'category')
            .order('name')
            .limit(20);
            
        if (rootError) throw rootError;
        
        console.log('Current top-level categories:');
        rootNodes.forEach(node => {
            console.log(`- ${node.name} (learning_area: ${node.learning_area})`);
        });
        
        // These are the categories that should remain at the top level
        const correctTopLevelCategories = [
            'Mathematics',
            'Languages', 
            'Natural Sciences',
            'Computer Science',
            'Social Sciences',
            'Humanities',
            'Applied Sciences',
            'Creative Skills',
            'Professional Skills',
            'Technical Skills',
            'Life Skills',
            'Test Preparation and Assessment'
        ];
        
        console.log('\n=== STEP 1: Finding correct top-level categories ===');
        
        const topLevelNodes = {};
        for (const categoryName of correctTopLevelCategories) {
            const { data: nodes, error } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, type, learning_area')
                .eq('name', categoryName)
                .eq('type', 'category')
                .is('parent_id', null);
                
            if (error) throw error;
            
            if (nodes.length > 0) {
                topLevelNodes[categoryName] = nodes[0];
                console.log(`✅ Found ${categoryName}`);
            } else {
                console.log(`❌ Missing ${categoryName}`);
            }
        }
        
        console.log('\n=== STEP 2: Finding misplaced categories ===');
        
        // Find all category nodes that are currently at root level but shouldn't be
        const { data: allRootCategories, error: allRootError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, learning_area')
            .is('parent_id', null)
            .eq('type', 'category');
            
        if (allRootError) throw allRootError;
        
        const misplacedCategories = allRootCategories.filter(node => 
            !correctTopLevelCategories.includes(node.name)
        );
        
        console.log(`Found ${misplacedCategories.length} misplaced categories that need to be moved`);
        
        console.log('\n=== STEP 3: Reassigning parent relationships ===');
        
        let reassignCount = 0;
        for (const category of misplacedCategories) {
            // Try to determine the correct parent based on learning_area
            const parentName = category.learning_area;
            const parentNode = topLevelNodes[parentName];
            
            if (parentNode) {
                const { error: updateError } = await supabase
                    .from('skill_tree_nodes')
                    .update({ 
                        parent_id: parentNode.id,
                        updated_at: new Date().toISOString()
                    })
                    .eq('id', category.id);
                    
                if (updateError) {
                    console.error(`Error reassigning ${category.name}:`, updateError);
                } else {
                    console.log(`✅ Reassigned "${category.name}" under "${parentName}"`);
                    reassignCount++;
                }
            } else {
                console.log(`⚠️ Could not find parent for "${category.name}" (learning_area: ${category.learning_area})`);
            }
        }
        
        console.log('\n=== STEP 4: Fixing skill nodes ===');
        
        // Find all skill nodes that are currently at root level (they should all have parents)
        const { data: rootSkills, error: skillError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, learning_area')
            .is('parent_id', null)
            .eq('type', 'skill')
            .limit(1000); // Process in batches
            
        if (skillError) throw skillError;
        
        console.log(`Found ${rootSkills.length} skill nodes at root level that need parents`);
        
        // This will be complex to fix automatically. For now, let's just report the scale of the problem
        if (rootSkills.length > 0) {
            console.log('\n❌ CRITICAL: There are individual skill nodes at the root level!');
            console.log('This requires manual intervention or a more sophisticated restore strategy.');
            console.log('First few examples:');
            rootSkills.slice(0, 10).forEach(skill => {
                console.log(`  - ${skill.name} (learning_area: ${skill.learning_area})`);
            });
        }
        
        console.log(`\n📊 SUMMARY:`);
        console.log(`- Correct top-level categories: ${Object.keys(topLevelNodes).length}`);
        console.log(`- Categories reassigned: ${reassignCount}`);
        console.log(`- Skill nodes at root (should be 0): ${rootSkills.length}`);
        
        if (rootSkills.length === 0 && reassignCount === misplacedCategories.length) {
            console.log('\n🎉 HIERARCHY RESTORED SUCCESSFULLY!');
        } else {
            console.log('\n⚠️ PARTIAL RESTORATION - Manual intervention may be needed');
        }
        
    } catch (error) {
        console.error('Error during emergency restore:', error);
    }
}

emergencyRestore();
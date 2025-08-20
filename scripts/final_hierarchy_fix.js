require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function finalHierarchyFix() {
    try {
        console.log('🔧 FINAL HIERARCHY FIX: Completing the restoration...\n');
        
        // The exact 12 categories that should be at the root level
        const targetTopLevelCategories = [
            'Mathematics', 'Languages', 'Natural Sciences', 'Computer Science',
            'Social Sciences', 'Humanities', 'Applied Sciences', 'Creative Skills',
            'Professional Skills', 'Technical Skills', 'Life Skills', 'Test Preparation and Assessment'
        ];
        
        console.log('=== STEP 1: Identify and fix extra categories at root ===');
        
        const { data: rootCategories, error: rootError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, learning_area')
            .is('parent_id', null)
            .eq('type', 'category')
            .order('name');
            
        if (rootError) throw rootError;
        
        console.log('Current root categories:');
        rootCategories.forEach(cat => {
            const isTarget = targetTopLevelCategories.includes(cat.name);
            console.log(`${isTarget ? '✅' : '❌'} ${cat.name} (learning_area: ${cat.learning_area})`);
        });
        
        // Find the target categories to use as parents
        const targetNodes = {};
        for (const categoryName of targetTopLevelCategories) {
            const node = rootCategories.find(c => c.name === categoryName);
            if (node) {
                targetNodes[categoryName] = node;
            }
        }
        
        // Handle extra categories
        const extraCategories = rootCategories.filter(cat => !targetTopLevelCategories.includes(cat.name));
        console.log(`\\nFound ${extraCategories.length} extra categories to reassign:`);
        
        for (const extraCat of extraCategories) {
            let newParent = null;
            
            // Handle specific cases
            if (extraCat.name === 'AI Ethics') {
                newParent = targetNodes['Computer Science'];
            } else if (extraCat.name === 'C++ Programming') {
                newParent = targetNodes['Computer Science'];
            }
            
            if (newParent) {
                console.log(`  Reassigning "${extraCat.name}" under "${newParent.name}"`);
                
                const { error: updateError } = await supabase
                    .from('skill_tree_nodes')
                    .update({ 
                        parent_id: newParent.id,
                        updated_at: new Date().toISOString()
                    })
                    .eq('id', extraCat.id);
                    
                if (updateError) {
                    console.error(`Error reassigning ${extraCat.name}:`, updateError);
                }
            }
        }
        
        console.log('\\n=== STEP 2: Fix remaining individual skills at root ===');
        
        // Get all skills at root level
        const { data: rootSkills, error: skillError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, learning_area')
            .is('parent_id', null)
            .eq('type', 'skill');
            
        if (skillError) throw skillError;
        
        console.log(`Found ${rootSkills.length} individual skills to reassign...`);
        
        let skillsFixed = 0;
        const batchSize = 50;
        
        for (let i = 0; i < rootSkills.length; i += batchSize) {
            const batch = rootSkills.slice(i, i + batchSize);
            
            for (const skill of batch) {
                let parentNode = null;
                
                // Try to find parent by learning area
                if (targetNodes[skill.learning_area]) {
                    parentNode = targetNodes[skill.learning_area];
                } else {
                    // Fallback mapping for skills with unclear learning areas
                    const fallbackMap = {
                        'Applied Knowledge': 'Technical Skills',
                        'Politics': 'Social Sciences',
                        'root': 'Technical Skills' // Default fallback
                    };
                    
                    const fallback = fallbackMap[skill.learning_area] || 'Technical Skills';
                    parentNode = targetNodes[fallback];
                }
                
                if (parentNode) {
                    const { error: updateError } = await supabase
                        .from('skill_tree_nodes')
                        .update({ 
                            parent_id: parentNode.id,
                            learning_area: parentNode.name, // Update learning area to match parent
                            updated_at: new Date().toISOString()
                        })
                        .eq('id', skill.id);
                        
                    if (!updateError) {
                        skillsFixed++;
                    } else {
                        console.error(`Error fixing skill ${skill.name}:`, updateError);
                    }
                }
            }
            
            console.log(`  Fixed ${Math.min(i + batchSize, rootSkills.length)} / ${rootSkills.length} skills...`);
        }
        
        console.log('\\n=== STEP 3: Final verification ===');
        
        // Check final structure
        const { data: finalRootNodes, error: finalError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type')
            .is('parent_id', null)
            .order('name');
            
        if (finalError) throw finalError;
        
        const finalCategories = finalRootNodes.filter(n => n.type === 'category');
        const finalSkills = finalRootNodes.filter(n => n.type === 'skill');
        
        console.log('\\nFinal root-level structure:');
        console.log('CATEGORIES:');
        finalCategories.forEach(cat => {
            console.log(`  ✅ ${cat.name}`);
        });
        
        if (finalSkills.length > 0) {
            console.log('\\nREMAINING SKILLS AT ROOT (should be 0):');
            finalSkills.slice(0, 10).forEach(skill => {
                console.log(`  ❌ ${skill.name}`);
            });
            if (finalSkills.length > 10) {
                console.log(`  ... and ${finalSkills.length - 10} more`);
            }
        }
        
        console.log(`\\n📊 FINAL RESULTS:`);
        console.log(`- Categories at root level: ${finalCategories.length} (target: 12)`);
        console.log(`- Skills at root level: ${finalSkills.length} (target: 0)`);
        console.log(`- Skills reassigned: ${skillsFixed}`);
        
        if (finalSkills.length === 0 && finalCategories.length === 12) {
            console.log('\\n🎉 HIERARCHY RESTORATION COMPLETE!');
            console.log('The skill tree now has the perfect structure with exactly 12 top-level categories and no orphaned skills.');
        } else {
            console.log('\\n⚠️ HIERARCHY STILL NEEDS WORK');
        }
        
    } catch (error) {
        console.error('Error during final hierarchy fix:', error);
    }
}

finalHierarchyFix();
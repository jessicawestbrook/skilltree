require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function removeEmptyFormalSciences() {
    try {
        console.log('🧹 REMOVING EMPTY FORMAL SCIENCES CATEGORY...\n');
        
        // Find the Formal Sciences category
        const { data: formalSciencesNode, error: findError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id')
            .eq('name', 'Formal Sciences')
            .eq('type', 'category')
            .is('parent_id', null)
            .single();
            
        if (findError) {
            if (findError.code === 'PGRST116') {
                console.log('✅ Formal Sciences category not found (already removed)');
                return;
            }
            throw findError;
        }
        
        console.log(`Found Formal Sciences: ${formalSciencesNode.id}`);
        
        // Check if it has any children left
        const { count: childCount, error: countError } = await supabase
            .from('skill_tree_nodes')
            .select('*', { count: 'exact', head: true })
            .eq('parent_id', formalSciencesNode.id);
            
        if (countError) throw countError;
        
        console.log(`Formal Sciences has ${childCount} children`);
        
        if (childCount > 0) {
            console.log('⚠️ Formal Sciences still has children, cannot remove safely');
            
            // List the children
            const { data: children, error: childrenError } = await supabase
                .from('skill_tree_nodes')
                .select('name, type')
                .eq('parent_id', formalSciencesNode.id);
                
            if (childrenError) throw childrenError;
            
            console.log('Remaining children:');
            children.forEach(child => {
                console.log(`  - ${child.name} (${child.type})`);
            });
            
            return;
        }
        
        // Safe to remove since it has no children
        console.log('🗑️ Removing empty Formal Sciences category...');
        
        const { error: deleteError } = await supabase
            .from('skill_tree_nodes')
            .delete()
            .eq('id', formalSciencesNode.id);
            
        if (deleteError) throw deleteError;
        
        console.log('✅ Successfully removed Formal Sciences category');
        
        // Final verification
        const { data: rootCategories, error: rootError } = await supabase
            .from('skill_tree_nodes')
            .select('name, learning_area')
            .is('parent_id', null)
            .eq('type', 'category')
            .order('name');
            
        if (rootError) throw rootError;
        
        console.log(`\n📊 FINAL RESULT:`);
        console.log(`Top-level categories: ${rootCategories.length}`);
        
        if (rootCategories.length === 12) {
            console.log('🎉 Perfect! Now we have exactly 12 top-level categories!');
        }
        
        console.log('\nFinal top-level categories:');
        rootCategories.forEach((cat, i) => {
            console.log(`  ${i+1}. ${cat.name}`);
        });
        
    } catch (error) {
        console.error('Error removing Formal Sciences:', error);
    }
}

removeEmptyFormalSciences();
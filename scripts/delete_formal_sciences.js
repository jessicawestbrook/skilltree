require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseServiceKey) {
    console.error('Missing environment variables. Make sure REACT_APP_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are set.');
    process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function deleteFormalSciencesCategory() {
    try {
        console.log('Starting deletion of empty Formal Sciences category...');
        
        // First, find the Formal Sciences node
        const { data: formalSciencesNode, error: findError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id')
            .eq('name', 'Formal Sciences')
            .single();
            
        if (findError) {
            console.error('Error finding Formal Sciences node:', findError);
            return;
        }
        
        console.log('Found Formal Sciences node:', formalSciencesNode);
        
        // Verify it has no children before deleting
        const { data: children, error: childrenError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .eq('parent_id', formalSciencesNode.id);
            
        if (childrenError) {
            console.error('Error checking for children:', childrenError);
            return;
        }
        
        if (children && children.length > 0) {
            console.error('❌ SAFETY CHECK FAILED: Formal Sciences still has children. Cannot delete.');
            console.log('Children found:');
            children.forEach(child => {
                console.log(`  - ${child.name} (${child.id})`);
            });
            return;
        }
        
        console.log('✅ SAFETY CHECK PASSED: Formal Sciences has no children. Safe to delete.');
        
        // Delete the Formal Sciences node
        const { error: deleteError } = await supabase
            .from('skill_tree_nodes')
            .delete()
            .eq('id', formalSciencesNode.id);
            
        if (deleteError) {
            console.error('Error deleting Formal Sciences node:', deleteError);
            return;
        }
        
        console.log('✅ Successfully deleted Formal Sciences category');
        
        // Verify deletion by trying to find it again
        const { data: verifyNode, error: verifyError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .eq('name', 'Formal Sciences')
            .single();
            
        if (verifyError && verifyError.code === 'PGRST116') {
            // This is expected - no rows found
            console.log('✅ VERIFICATION PASSED: Formal Sciences category no longer exists in database');
        } else if (verifyNode) {
            console.error('❌ VERIFICATION FAILED: Formal Sciences still exists in database');
        } else {
            console.error('Unexpected error during verification:', verifyError);
        }
        
        console.log('🎉 Formal Sciences category deletion complete!');
        
    } catch (error) {
        console.error('Unexpected error:', error);
    }
}

// Run the deletion
deleteFormalSciencesCategory();
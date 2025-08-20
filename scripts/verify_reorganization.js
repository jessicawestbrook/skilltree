require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function verifyReorganization() {
    try {
        console.log('Verifying reorganization results...\n');
        
        // Get Academic Disciplines node
        const { data: academicNode, error: academicError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .eq('name', 'Academic Disciplines')
            .single();
            
        if (academicError) {
            console.error('Error finding Academic Disciplines:', academicError);
            return;
        }
        
        // Get children of Academic Disciplines
        const { data: academicChildren, error: childrenError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, learning_area')
            .eq('parent_id', academicNode.id)
            .order('name');
            
        if (childrenError) {
            console.error('Error getting Academic Disciplines children:', childrenError);
            return;
        }
        
        console.log('Children of Academic Disciplines:');
        academicChildren.forEach(child => {
            console.log(`  - ${child.name} (learning_area: ${child.learning_area})`);
        });
        
        // Check if CS and Math are there
        const csChild = academicChildren.find(child => child.name === 'Computer Science');
        const mathChild = academicChildren.find(child => child.name === 'Mathematics');
        
        if (csChild && mathChild) {
            console.log('\n✅ SUCCESS: Both Computer Science and Mathematics are now direct children of Academic Disciplines');
            console.log(`✅ Computer Science learning area: ${csChild.learning_area}`);
            console.log(`✅ Mathematics learning area: ${mathChild.learning_area}`);
        } else {
            console.log('\n❌ ERROR: One or both subjects are missing from Academic Disciplines');
        }
        
        // Check Formal Sciences is empty
        const { data: formalSciencesNode, error: formalError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .eq('name', 'Formal Sciences')
            .single();
            
        if (!formalError && formalSciencesNode) {
            const { data: formalChildren, error: formalChildrenError } = await supabase
                .from('skill_tree_nodes')
                .select('name')
                .eq('parent_id', formalSciencesNode.id);
                
            if (!formalChildrenError) {
                console.log(`\n✅ Formal Sciences now has ${formalChildren.length} children (should be 0)`);
                if (formalChildren.length > 0) {
                    console.log('Remaining children in Formal Sciences:');
                    formalChildren.forEach(child => {
                        console.log(`  - ${child.name}`);
                    });
                }
            }
        }
        
    } catch (error) {
        console.error('Error during verification:', error);
    }
}

verifyReorganization();
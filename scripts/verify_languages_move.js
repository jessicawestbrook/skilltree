require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function verifyLanguagesMove() {
    try {
        console.log('Verifying Languages reorganization...\n');
        
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
        
        // Check if Languages is there
        const languagesChild = academicChildren.find(child => child.name === 'Languages');
        const humanitiesChild = academicChildren.find(child => child.name === 'Humanities');
        
        if (languagesChild && humanitiesChild) {
            console.log('\n✅ SUCCESS: Languages and Humanities are both direct children of Academic Disciplines');
            console.log(`✅ Languages learning area: ${languagesChild.learning_area}`);
            console.log(`✅ Humanities learning area: ${humanitiesChild.learning_area}`);
        } else {
            console.log('\n❌ ERROR: Languages or Humanities missing from Academic Disciplines');
        }
        
        // Check current state of Languages node specifically
        const { data: languagesNode, error: languagesNodeError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id, learning_area')
            .eq('name', 'Languages')
            .eq('learning_area', 'Languages')
            .single();
            
        if (!languagesNodeError && languagesNode) {
            console.log(`\n✅ Languages node details:`);
            console.log(`   - ID: ${languagesNode.id}`);
            console.log(`   - Parent ID: ${languagesNode.parent_id}`);
            console.log(`   - Learning Area: ${languagesNode.learning_area}`);
            console.log(`   - Parent matches Academic Disciplines: ${languagesNode.parent_id === academicNode.id ? 'YES' : 'NO'}`);
        }
        
        // Check if Humanities no longer has Languages as child
        const { data: humanitiesNode, error: humanitiesError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .eq('name', 'Humanities')
            .single();
            
        if (!humanitiesError && humanitiesNode) {
            const { data: humanitiesChildren, error: humanitiesChildrenError } = await supabase
                .from('skill_tree_nodes')
                .select('name')
                .eq('parent_id', humanitiesNode.id)
                .order('name');
                
            if (!humanitiesChildrenError) {
                console.log(`\n✅ Current children of Humanities:`);
                humanitiesChildren.forEach(child => {
                    console.log(`   - ${child.name}`);
                });
                
                const hasLanguages = humanitiesChildren.some(child => child.name === 'Languages');
                console.log(`\n✅ Humanities still contains Languages: ${hasLanguages ? 'NO - Good!' : 'YES - Issue!'}`);
            }
        }
        
    } catch (error) {
        console.error('Error during verification:', error);
    }
}

verifyLanguagesMove();
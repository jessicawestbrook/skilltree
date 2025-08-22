require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function addDescriptionColumn() {
    try {
        console.log('🔧 ADDING DESCRIPTION COLUMN TO SKILL_TREE_NODES TABLE\n');
        
        // Use RPC to add the column safely
        const { data, error } = await supabase.rpc('add_description_column');
        
        if (error) {
            // If RPC doesn't exist, we'll use direct SQL
            console.log('RPC method not available, using direct approach...');
            
            // First, let's check if the column already exists
            const { data: testData, error: testError } = await supabase
                .from('skill_tree_nodes')
                .select('description')
                .limit(1);
                
            if (testError && testError.message.includes('column "description" does not exist')) {
                console.log('Description column does not exist, needs to be added manually.');
                console.log('\nTo add the description column, please run this SQL command in your Supabase dashboard:');
                console.log('\nALTER TABLE skill_tree_nodes ADD COLUMN description TEXT;');
                console.log('\nAfter adding the column, run this script again to verify.');
                return;
            } else if (!testError) {
                console.log('✅ Description column already exists!');
                return;
            } else {
                throw testError;
            }
        }
        
        console.log('✅ Description column added successfully!');
        
        // Verify the column was added
        const { data: verifyData, error: verifyError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, description')
            .limit(5);
            
        if (!verifyError) {
            console.log('\n✅ Verification successful - description column is available');
            console.log('Sample data:');
            verifyData.forEach(node => {
                console.log(`  - ${node.name}: ${node.description || '(null)'}`);
            });
        }
        
    } catch (error) {
        console.error('❌ Error adding description column:', error);
    }
}

addDescriptionColumn();
require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function executeDescriptionMigration() {
    try {
        console.log('🔧 EXECUTING DESCRIPTION COLUMN MIGRATION\n');
        
        // First check if column already exists
        console.log('Checking if description column already exists...');
        
        try {
            const { data: testData, error: testError } = await supabase
                .from('skill_tree_nodes')
                .select('description')
                .limit(1);
                
            if (!testError) {
                console.log('✅ Description column already exists!');
                
                // Show sample data
                const { data: sampleData } = await supabase
                    .from('skill_tree_nodes')
                    .select('name, description')
                    .limit(5);
                    
                console.log('\nSample nodes with description column:');
                sampleData.forEach(node => {
                    console.log(`  - ${node.name}: ${node.description || '(null)'}`);
                });
                return;
            }
        } catch (error) {
            // Column doesn't exist, proceed with migration
        }
        
        console.log('Description column does not exist, adding it...');
        
        // Execute the SQL to add the description column
        const { data, error } = await supabase.rpc('exec_sql', {
            sql: 'ALTER TABLE skill_tree_nodes ADD COLUMN description TEXT;'
        });
        
        if (error) {
            // Try alternative approach using edge functions or direct query
            console.log('Direct SQL execution not available.');
            console.log('\nPlease execute this SQL command manually in your Supabase dashboard:');
            console.log('\nALTER TABLE skill_tree_nodes ADD COLUMN description TEXT;');
            console.log('\nAlternatively, go to Database > SQL Editor and run the SQL file:');
            console.log('scripts/add_description_column.sql');
            return;
        }
        
        console.log('✅ Description column added successfully!');
        
        // Verify the column was added
        const { data: verifyData, error: verifyError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, description')
            .limit(3);
            
        if (!verifyError) {
            console.log('\n✅ Verification successful - description column is available');
            console.log('Sample data with new column:');
            verifyData.forEach(node => {
                console.log(`  - ${node.name}: ${node.description || '(null)'}`);
            });
        } else {
            console.log('\n⚠️  Column may have been added but verification failed:', verifyError.message);
        }
        
    } catch (error) {
        console.error('❌ Migration failed:', error);
        console.log('\nPlease add the description column manually using the Supabase dashboard.');
        console.log('Go to Database > Tables > skill_tree_nodes > Add Column');
        console.log('Column name: description');
        console.log('Data type: text');
        console.log('Nullable: Yes');
    }
}

executeDescriptionMigration();
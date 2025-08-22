require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function removeTypeColumn() {
    try {
        console.log('🗑️  REMOVING TYPE COLUMN FROM SKILL_TREE_NODES TABLE\n');
        
        // Step 1: Check current schema
        console.log('Step 1: Checking current schema...');
        const { data: currentData, error: currentError } = await supabase
            .from('skill_tree_nodes')
            .select('id, type')
            .limit(5);
            
        if (currentError) {
            console.error('❌ Error accessing table:', currentError);
            return;
        }
        
        const hasTypeColumn = currentData.length > 0 && 'type' in currentData[0];
        
        if (!hasTypeColumn) {
            console.log('✅ Type column already removed!');
            return;
        }
        
        console.log('✅ Type column exists, proceeding with removal...');
        
        // Step 2: Count records by type for verification
        console.log('\nStep 2: Analyzing type column data...');
        const { data: allData, error: countError } = await supabase
            .from('skill_tree_nodes')
            .select('type');
            
        if (countError) {
            console.error('❌ Error counting types:', countError);
            return;
        }
        
        const typeCounts = {};
        allData.forEach(row => {
            const type = row.type || 'null';
            typeCounts[type] = (typeCounts[type] || 0) + 1;
        });
        
        console.log('Type distribution:');
        Object.entries(typeCounts).forEach(([type, count]) => {
            console.log(`   ${type}: ${count} records`);
        });
        
        console.log(`   Total records: ${allData.length}`);
        
        // Step 3: Inform about manual SQL execution
        console.log('\n⚠️  IMPORTANT: Column removal requires manual SQL execution');
        console.log('\nTo remove the type column, please execute this SQL in your Supabase dashboard:');
        console.log('\n--- Copy and paste this into SQL Editor ---');
        console.log('-- Create backup first');
        console.log('CREATE TABLE skill_tree_nodes_type_backup AS');
        console.log('SELECT id, type FROM skill_tree_nodes;');
        console.log('');
        console.log('-- Remove the type column');
        console.log('ALTER TABLE skill_tree_nodes DROP COLUMN type;');
        console.log('--- End of SQL commands ---');
        
        console.log('\nAfter executing the SQL, run this script again to verify removal.');
        
    } catch (error) {
        console.error('❌ Error in type column removal:', error);
    }
}

removeTypeColumn();
require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function checkSchema() {
    try {
        console.log('🔍 CHECKING SKILL_TREE_NODES SCHEMA\n');
        
        // Get a sample record to understand the structure
        const { data, error } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .limit(1);
            
        if (error) {
            console.error('Error:', error);
            return;
        }
        
        if (data && data.length > 0) {
            console.log('Available columns:');
            Object.keys(data[0]).forEach(column => {
                console.log(`  • ${column}: ${typeof data[0][column]} (${data[0][column]})`);
            });
            
            console.log('\nSample record:');
            console.log(JSON.stringify(data[0], null, 2));
        }
        
    } catch (error) {
        console.error('Error checking schema:', error);
    }
}

checkSchema();
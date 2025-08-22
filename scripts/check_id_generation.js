require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');
const { v4: uuidv4 } = require('uuid');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function checkIdGeneration() {
    try {
        console.log('🔍 Checking ID generation strategy\n');
        
        // Check existing IDs to understand format
        const { data: sampleData, error: sampleError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .limit(3);
            
        if (sampleError) {
            console.error('Error fetching samples:', sampleError);
            return;
        }
        
        console.log('Sample existing IDs:');
        sampleData.forEach(node => {
            console.log(`  ${node.id} -> ${node.name}`);
        });
        
        // Try inserting with UUID
        const testId = uuidv4();
        console.log(`\n🧪 Testing with generated UUID: ${testId}`);
        
        const { data, error } = await supabase
            .from('skill_tree_nodes')
            .insert({
                id: testId,
                name: 'Test Category with UUID',
                type: 'category',
                learning_area: 'Test Area',
                metadata: { description: 'Test description' },
                path: [],
                has_learning_content: false,
                is_menu_leaf: false
            })
            .select()
            .single();
            
        if (error) {
            console.error('❌ Insert with UUID failed:', error);
        } else {
            console.log('✅ Insert with UUID succeeded!');
            console.log(`   Created: ${data.id} -> ${data.name}`);
            
            // Clean up test
            await supabase.from('skill_tree_nodes').delete().eq('id', data.id);
            console.log('🧹 Test record cleaned up');
            
            console.log('\n💡 Strategy: Generate UUIDs manually for new records');
        }
        
    } catch (error) {
        console.error('Test failed:', error);
    }
}

checkIdGeneration();
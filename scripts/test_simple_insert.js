require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function testSimpleInsert() {
    try {
        console.log('🧪 Testing simple insert to understand schema requirements\n');
        
        // Test with minimal data to see what's required
        const { data, error } = await supabase
            .from('skill_tree_nodes')
            .insert({
                name: 'Test Category',
                type: 'category',
                learning_area: 'Test Area',
                metadata: { description: 'Test description' },
                has_learning_content: false,
                is_menu_leaf: false
            })
            .select()
            .single();
            
        if (error) {
            console.error('❌ Insert failed:', error);
            
            // Try with path field
            console.log('\n🔄 Trying with path field...');
            const { data: data2, error: error2 } = await supabase
                .from('skill_tree_nodes')
                .insert({
                    name: 'Test Category 2',
                    type: 'category',
                    learning_area: 'Test Area',
                    metadata: { description: 'Test description' },
                    path: [],
                    has_learning_content: false,
                    is_menu_leaf: false
                })
                .select()
                .single();
                
            if (error2) {
                console.error('❌ Second insert failed:', error2);
            } else {
                console.log('✅ Second insert succeeded:', data2.id);
                
                // Clean up test
                await supabase.from('skill_tree_nodes').delete().eq('id', data2.id);
                console.log('🧹 Test record cleaned up');
            }
        } else {
            console.log('✅ Insert succeeded:', data.id);
            
            // Clean up test
            await supabase.from('skill_tree_nodes').delete().eq('id', data.id);
            console.log('🧹 Test record cleaned up');
        }
        
    } catch (error) {
        console.error('Test failed:', error);
    }
}

testSimpleInsert();
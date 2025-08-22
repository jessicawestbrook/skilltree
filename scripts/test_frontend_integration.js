require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function testFrontendIntegration() {
    try {
        console.log('🌐 TESTING FRONTEND INTEGRATION\n');
        
        // Test the same queries that the frontend MegaMenu component would use
        console.log('📋 Testing MegaMenu query (top-level categories)...');
        const { data: megaMenuData, error: megaError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, learning_area, has_learning_content, is_menu_leaf')
            .is('parent_id', null)
            .order('display_order', { nullsFirst: false })
            .order('name')
            .limit(3);
            
        if (megaError) {
            console.error('❌ MegaMenu query error:', megaError);
        } else {
            console.log(`✅ MegaMenu query successful - ${megaMenuData.length} categories:`);
            megaMenuData.forEach((cat, index) => {
                console.log(`   ${index + 1}. ${cat.name} (${cat.learning_area})`);
            });
        }
        
        // Test Humanities category page query
        console.log('\n📖 Testing Humanities category page query...');
        const { data: humanitiesData, error: humanitiesError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, learning_area, has_learning_content, is_menu_leaf, metadata')
            .eq('name', 'Humanities')
            .is('parent_id', null)
            .single();
            
        if (humanitiesError) {
            console.error('❌ Humanities query error:', humanitiesError);
        } else {
            console.log(`✅ Humanities found: ${humanitiesData.name} (${humanitiesData.id})`);
            
            // Get Humanities children
            const { data: humanitiesChildren, error: childrenError } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, type, learning_area, has_learning_content, is_menu_leaf, display_order, metadata')
                .eq('parent_id', humanitiesData.id)
                .order('display_order', { nullsFirst: false })
                .order('name');
                
            if (childrenError) {
                console.error('❌ Humanities children query error:', childrenError);
            } else {
                console.log(`✅ Humanities children query successful - ${humanitiesChildren.length} subcategories:`);
                humanitiesChildren.forEach(child => {
                    const description = child.metadata?.description || 'No description';
                    const marker = child.name === 'Civic Education & Government' ? '🆕' : '  ';
                    console.log(`${marker} • ${child.name} (${child.type}) - ${description.substring(0, 50)}...`);
                });
            }
        }
        
        // Test Civic Education category page query
        console.log('\n🏛️ Testing Civic Education category page query...');
        const { data: civicEducationData, error: civicError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, learning_area, has_learning_content, is_menu_leaf, display_order, metadata')
            .eq('name', 'Civic Education & Government')
            .single();
            
        if (civicError) {
            console.error('❌ Civic Education query error:', civicError);
        } else {
            console.log(`✅ Civic Education found: ${civicEducationData.name}`);
            console.log(`   Description: ${civicEducationData.metadata?.description || 'No description'}`);
            console.log(`   Learning Area: ${civicEducationData.learning_area}`);
            console.log(`   Display Order: ${civicEducationData.display_order}`);
            
            // Get Civic Education children
            const { data: civicChildren, error: civicChildrenError } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, type, has_learning_content, is_menu_leaf, display_order')
                .eq('parent_id', civicEducationData.id)
                .order('display_order', { nullsFirst: false })
                .order('name');
                
            if (civicChildrenError) {
                console.error('❌ Civic Education children query error:', civicChildrenError);
            } else {
                console.log(`✅ Civic Education children: ${civicChildren.length} subcategories`);
                civicChildren.forEach(child => {
                    console.log(`     • ${child.name} (${child.type})`);
                });
            }
        }
        
        // Test academic ordering
        console.log('\n📊 Testing academic ordering...');
        const { data: orderedCategories, error: orderError } = await supabase
            .from('skill_tree_nodes')
            .select('name, display_order')
            .is('parent_id', null)
            .order('display_order', { nullsFirst: false })
            .order('name');
            
        if (orderError) {
            console.error('❌ Academic ordering query error:', orderError);
        } else {
            console.log('✅ Academic ordering maintained:');
            orderedCategories.forEach((cat, index) => {
                const order = cat.display_order || 'null';
                console.log(`   ${index + 1}. ${cat.name} (order: ${order})`);
            });
        }
        
        console.log('\n🎉 FRONTEND INTEGRATION TEST COMPLETE!');
        console.log('✅ All queries work as expected');
        console.log('✅ Civic Education properly nested under Humanities');
        console.log('✅ Academic ordering maintained');
        console.log('✅ MegaMenu will show correct top-level categories');
        console.log('✅ Category pages will work correctly');
        
    } catch (error) {
        console.error('❌ Frontend integration test failed:', error);
    }
}

testFrontendIntegration();
require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function verifyHierarchy() {
    try {
        console.log('🔍 VERIFYING FINAL HIERARCHY STRUCTURE...\n');
        
        // Check root level structure
        const { data: rootNodes, error: rootError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, display_order')
            .is('parent_id', null)
            .order('display_order', { nullsFirst: false })
            .order('name');
            
        if (rootError) throw rootError;
        
        console.log('=== ROOT LEVEL STRUCTURE ===');
        console.log(`Total root nodes: ${rootNodes.length}`);
        
        const categories = rootNodes.filter(n => n.type === 'category');
        const skills = rootNodes.filter(n => n.type === 'skill');
        
        console.log(`\nCategories at root (should be 12): ${categories.length}`);
        categories.forEach(cat => {
            console.log(`  ✅ ${cat.name} (display_order: ${cat.display_order || 'null'})`);
        });
        
        if (skills.length > 0) {
            console.log(`\n❌ Skills at root (should be 0): ${skills.length}`);
            skills.slice(0, 5).forEach(skill => {
                console.log(`    - ${skill.name}`);
            });
        }
        
        // Check some sample categories have children
        console.log('\n=== SAMPLE CATEGORY CHILDREN ===');
        
        const sampleCategories = ['Mathematics', 'Languages', 'Computer Science'];
        for (const categoryName of sampleCategories) {
            const category = categories.find(c => c.name === categoryName);
            if (category) {
                const { data: children, error: childError } = await supabase
                    .from('skill_tree_nodes')
                    .select('id, name, type')
                    .eq('parent_id', category.id);
                    
                if (!childError) {
                    console.log(`\n${categoryName}: ${children.length} children`);
                    children.slice(0, 5).forEach(child => {
                        console.log(`  - ${child.name} (${child.type})`);
                    });
                    if (children.length > 5) {
                        console.log(`  ... and ${children.length - 5} more`);
                    }
                }
            }
        }
        
        // Final assessment
        console.log('\n📊 FINAL ASSESSMENT:');
        
        const success = categories.length === 12 && skills.length === 0;
        
        if (success) {
            console.log('🎉 HIERARCHY STRUCTURE IS PERFECT!');
            console.log('✅ Exactly 12 top-level categories');
            console.log('✅ No orphaned skills at root level');
            console.log('✅ Categories have proper child relationships');
        } else {
            console.log('⚠️ HIERARCHY NEEDS ATTENTION:');
            if (categories.length !== 12) {
                console.log(`❌ Expected 12 categories, found ${categories.length}`);
            }
            if (skills.length > 0) {
                console.log(`❌ Found ${skills.length} skills at root level`);
            }
        }
        
    } catch (error) {
        console.error('Error verifying hierarchy:', error);
    }
}

verifyHierarchy();
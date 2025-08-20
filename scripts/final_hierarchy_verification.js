require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function finalHierarchyVerification() {
    try {
        console.log('✅ FINAL HIERARCHY VERIFICATION: Confirming structure is correct...\n');
        
        // Check 1: Root level structure
        const { data: rootNodes, error: rootError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, display_order')
            .is('parent_id', null)
            .order('display_order', { nullsFirst: false })
            .order('name');
            
        if (rootError) throw rootError;
        
        const categories = rootNodes.filter(n => n.type === 'category');
        const skills = rootNodes.filter(n => n.type === 'skill');
        
        console.log('=== ROOT LEVEL STRUCTURE ===');
        console.log(`✅ Root categories: ${categories.length} (expected: 12)`);
        console.log(`✅ Root skills: ${skills.length} (expected: 0)`);
        
        categories.forEach((cat, i) => {
            console.log(`  ${i+1}. ${cat.name} (display_order: ${cat.display_order || 'null'})`);
        });
        
        if (skills.length > 0) {
            console.log('\n❌ Unexpected skills at root level:');
            skills.forEach(skill => console.log(`  - ${skill.name}`));
        }
        
        // Check 2: Sample category children
        console.log('\n=== SAMPLE CATEGORY CHILDREN ===');
        const sampleCategories = ['Mathematics', 'Languages', 'Computer Science', 'Humanities'];
        
        for (const categoryName of sampleCategories) {
            const category = categories.find(c => c.name === categoryName);
            if (category) {
                const { data: children, error: childError } = await supabase
                    .from('skill_tree_nodes')
                    .select('id, name, type')
                    .eq('parent_id', category.id)
                    .order('name')
                    .limit(10);
                    
                if (!childError) {
                    console.log(`\n${categoryName}: ${children.length} children (showing first 10)`);
                    children.forEach(child => {
                        console.log(`  - ${child.name} (${child.type})`);
                    });
                }
            }
        }
        
        // Check 3: Total database stats
        console.log('\n=== DATABASE STATISTICS ===');
        
        const { count: totalCount, error: totalError } = await supabase
            .from('skill_tree_nodes')
            .select('*', { count: 'exact', head: true });
            
        if (!totalError) {
            console.log(`Total nodes: ${totalCount}`);
        }
        
        const { count: categoryCount, error: catError } = await supabase
            .from('skill_tree_nodes')
            .select('*', { count: 'exact', head: true })
            .eq('type', 'category');
            
        if (!catError) {
            console.log(`Total categories: ${categoryCount}`);
        }
        
        const { count: skillCount, error: skillError } = await supabase
            .from('skill_tree_nodes')
            .select('*', { count: 'exact', head: true })
            .eq('type', 'skill');
            
        if (!skillError) {
            console.log(`Total skills: ${skillCount}`);
        }
        
        // Check 4: Verify no actual orphans
        console.log('\n=== ORPHAN CHECK ===');
        
        // Get all unique parent_ids that are not null
        const { data: parentIds, error: parentError } = await supabase
            .from('skill_tree_nodes')
            .select('parent_id')
            .not('parent_id', 'is', null);
            
        if (parentError) throw parentError;
        
        const uniqueParentIds = [...new Set(parentIds.map(n => n.parent_id))];
        console.log(`Unique parent IDs referenced: ${uniqueParentIds.length}`);
        
        // Check if all these parent IDs exist as actual nodes
        const { data: existingParents, error: existingError } = await supabase
            .from('skill_tree_nodes')
            .select('id')
            .in('id', uniqueParentIds);
            
        if (existingError) throw existingError;
        
        const existingParentIds = new Set(existingParents.map(p => p.id));
        const missingParents = uniqueParentIds.filter(pid => !existingParentIds.has(pid));
        
        if (missingParents.length === 0) {
            console.log('✅ No orphaned nodes found - all parent references are valid!');
        } else {
            console.log(`❌ Found ${missingParents.length} missing parent references:`);
            missingParents.forEach(pid => console.log(`  - ${pid}`));
        }
        
        // Final assessment
        console.log('\n📊 FINAL ASSESSMENT:');
        
        const isValid = 
            categories.length === 12 && 
            skills.length === 0 && 
            missingParents.length === 0;
            
        if (isValid) {
            console.log('🎉 HIERARCHY IS PERFECTLY STRUCTURED!');
            console.log('✅ Exactly 12 top-level categories');
            console.log('✅ No skills at root level');
            console.log('✅ No orphaned nodes');
            console.log('✅ All parent references are valid');
        } else {
            console.log('⚠️ HIERARCHY ISSUES DETECTED:');
            if (categories.length !== 12) console.log(`❌ Expected 12 root categories, found ${categories.length}`);
            if (skills.length > 0) console.log(`❌ Found ${skills.length} skills at root level`);
            if (missingParents.length > 0) console.log(`❌ Found ${missingParents.length} orphaned nodes`);
        }
        
    } catch (error) {
        console.error('Error in final verification:', error);
    }
}

finalHierarchyVerification();
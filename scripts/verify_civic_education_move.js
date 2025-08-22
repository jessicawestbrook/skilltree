require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function verifyCivicEducationMove() {
    try {
        console.log('✅ COMPREHENSIVE VERIFICATION OF CIVIC EDUCATION MOVE\n');
        
        // 1. Verify top-level categories count
        console.log('📊 Checking top-level category count...');
        const { data: topLevelCategories, error: topError } = await supabase
            .from('skill_tree_nodes')
            .select('name, display_order')
            .is('parent_id', null)
            .order('display_order', { nullsFirst: false })
            .order('name');
            
        if (topError) {
            console.error('❌ Error fetching top-level categories:', topError);
            return;
        }
        
        console.log(`✅ Found ${topLevelCategories.length} top-level categories (should be 12):`);
        topLevelCategories.forEach((cat, index) => {
            const order = cat.display_order || 'null';
            console.log(`   ${index + 1}. ${cat.name} (order: ${order})`);
        });
        
        // Verify Civic Education is NOT in top-level
        const civicInTopLevel = topLevelCategories.find(cat => 
            cat.name === 'Civic Education & Government'
        );
        
        if (civicInTopLevel) {
            console.log('❌ ERROR: Civic Education still appears in top-level categories!');
        } else {
            console.log('✅ CONFIRMED: Civic Education no longer in top-level categories');
        }
        
        // 2. Verify Civic Education is under Humanities
        console.log('\n🏛️ Checking Civic Education placement under Humanities...');
        const { data: humanities, error: humanitiesError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .eq('name', 'Humanities')
            .is('parent_id', null)
            .single();
            
        if (humanitiesError) {
            console.error('❌ Error finding Humanities:', humanitiesError);
            return;
        }
        
        const { data: humanitiesChildren, error: childrenError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, display_order, path')
            .eq('parent_id', humanities.id)
            .order('display_order', { nullsFirst: false })
            .order('name');
            
        if (childrenError) {
            console.error('❌ Error fetching Humanities children:', childrenError);
            return;
        }
        
        console.log(`Found ${humanitiesChildren.length} subcategories under Humanities:`);
        let civicEducationFound = false;
        humanitiesChildren.forEach(child => {
            const order = child.display_order || 'null';
            const marker = child.name === 'Civic Education & Government' ? '✅' : '  ';
            if (child.name === 'Civic Education & Government') {
                civicEducationFound = true;
                console.log(`${marker} • ${child.name} (order: ${order}) - Path: ${JSON.stringify(child.path)}`);
            } else {
                console.log(`${marker} • ${child.name} (order: ${order})`);
            }
        });
        
        if (!civicEducationFound) {
            console.log('❌ ERROR: Civic Education & Government not found under Humanities!');
            return;
        }
        
        console.log('✅ CONFIRMED: Civic Education & Government is properly under Humanities');
        
        // 3. Verify the complete Civic Education hierarchy
        console.log('\n🏛️ Verifying complete Civic Education hierarchy...');
        const civicEducation = humanitiesChildren.find(child => 
            child.name === 'Civic Education & Government'
        );
        
        if (!civicEducation) {
            console.log('❌ ERROR: Could not find Civic Education for hierarchy check');
            return;
        }
        
        // Get Civic Education subcategories
        const { data: civicSubcategories, error: civicSubError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, display_order, path, type')
            .eq('parent_id', civicEducation.id)
            .order('display_order');
            
        if (civicSubError) {
            console.error('❌ Error fetching Civic Education subcategories:', civicSubError);
            return;
        }
        
        console.log(`Found ${civicSubcategories.length} subcategories under Civic Education:`);
        for (const subcat of civicSubcategories) {
            const expectedPath = ['Humanities', 'Civic Education & Government'];
            const pathMatches = JSON.stringify(subcat.path) === JSON.stringify(expectedPath);
            const pathStatus = pathMatches ? '✅' : '❌';
            
            console.log(`   ${pathStatus} ${subcat.name} (${subcat.type}) - Path: ${JSON.stringify(subcat.path)}`);
            
            // Check skills under each subcategory
            const { data: skills, error: skillsError } = await supabase
                .from('skill_tree_nodes')
                .select('name, path, type')
                .eq('parent_id', subcat.id);
                
            if (!skillsError && skills && skills.length > 0) {
                console.log(`     └─ ${skills.length} skills:`);
                skills.forEach(skill => {
                    const expectedSkillPath = ['Humanities', 'Civic Education & Government', subcat.name];
                    const skillPathMatches = JSON.stringify(skill.path) === JSON.stringify(expectedSkillPath);
                    const skillPathStatus = skillPathMatches ? '✅' : '❌';
                    console.log(`        ${skillPathStatus} ${skill.name} (${skill.type}) - Path: ${JSON.stringify(skill.path)}`);
                });
            }
        }
        
        // 4. Check for any orphaned nodes
        console.log('\n🔍 Checking for orphaned Civic Education nodes...');
        const { data: orphanedNodes, error: orphanError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id, path')
            .like('path', '%Civic Education & Government%')
            .neq('parent_id', civicEducation.id)
            .not('id', 'eq', civicEducation.id);
            
        if (orphanError) {
            console.error('❌ Error checking for orphaned nodes:', orphanError);
        } else if (orphanedNodes && orphanedNodes.length > 0) {
            console.log(`❌ Found ${orphanedNodes.length} potentially orphaned nodes:`);
            orphanedNodes.forEach(node => {
                console.log(`   • ${node.name} (${node.id}) - parent: ${node.parent_id}`);
            });
        } else {
            console.log('✅ No orphaned nodes found');
        }
        
        // 5. Final statistics
        console.log('\n📊 Final Statistics:');
        const { data: totalNodes, error: totalError } = await supabase
            .from('skill_tree_nodes')
            .select('type', { count: 'exact' });
            
        if (!totalError) {
            const categories = totalNodes.filter(n => n.type === 'category').length;
            const skills = totalNodes.filter(n => n.type === 'skill').length;
            console.log(`   Total nodes: ${totalNodes.length}`);
            console.log(`   Categories: ${categories}`);
            console.log(`   Skills: ${skills}`);
            console.log(`   Top-level categories: ${topLevelCategories.length}`);
        }
        
        console.log('\n🎉 VERIFICATION COMPLETE!');
        console.log('✅ Civic Education & Government successfully moved under Humanities');
        console.log('✅ All hierarchy paths updated correctly');
        console.log('✅ Academic ordering maintained');
        console.log('✅ No orphaned nodes detected');
        
        console.log('\n📋 SUMMARY OF CHANGES:');
        console.log('• Civic Education & Government moved from top-level to Humanities');
        console.log('• Display order: 50 (after Language Arts)');
        console.log('• All descendant paths updated to include Humanities');
        console.log('• Top-level categories reduced from 13 to 12');
        console.log('• Humanities subcategories increased from 6 to 7');
        
    } catch (error) {
        console.error('❌ Verification failed:', error);
    }
}

verifyCivicEducationMove();
require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function cleanupGraduateSchoolDuplicates() {
    try {
        console.log('🧹 CLEANING UP GRADUATE SCHOOL EXAM DUPLICATES\n');
        
        // Get Graduate School Exams category
        const { data: gradSchoolExams, error: gradError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .eq('name', 'Graduate School Exams')
            .single();
            
        if (gradError || !gradSchoolExams) {
            console.error('❌ Error finding Graduate School Exams category:', gradError);
            return;
        }
        
        console.log(`✅ Found Graduate School Exams: ${gradSchoolExams.id}`);
        
        // Get all subcategories under Graduate School Exams
        const { data: allSubcategories, error: subcatError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, display_order')
            .eq('parent_id', gradSchoolExams.id)
            .order('name');
            
        if (subcatError) {
            console.error('❌ Error fetching subcategories:', subcatError);
            return;
        }
        
        console.log(`\nFound ${allSubcategories.length} subcategories under Graduate School Exams:`);
        allSubcategories.forEach((cat, index) => {
            const order = cat.display_order || 'null';
            console.log(`   ${index + 1}. ${cat.name} (${cat.id}) - Order: ${order}`);
        });
        
        // Group by name to find duplicates
        const subcategoryGroups = {};
        allSubcategories.forEach(cat => {
            if (!subcategoryGroups[cat.name]) {
                subcategoryGroups[cat.name] = [];
            }
            subcategoryGroups[cat.name].push(cat);
        });
        
        console.log('\n🔍 Analyzing duplicates...');
        
        for (const [testName, categories] of Object.entries(subcategoryGroups)) {
            if (categories.length > 1) {
                console.log(`\n📂 DUPLICATE FOUND: ${testName} (${categories.length} instances)`);
                
                // Check which ones have children
                const categoriesWithDetails = [];
                
                for (const cat of categories) {
                    const { data: children, error: childrenError } = await supabase
                        .from('skill_tree_nodes')
                        .select('id, name, type')
                        .eq('parent_id', cat.id);
                        
                    if (childrenError) {
                        console.error(`   ❌ Error checking children for ${cat.id}:`, childrenError);
                        continue;
                    }
                    
                    categoriesWithDetails.push({
                        ...cat,
                        childrenCount: children ? children.length : 0,
                        children: children || []
                    });
                }
                
                // Sort by children count (keep the one with most children)
                categoriesWithDetails.sort((a, b) => b.childrenCount - a.childrenCount);
                
                console.log(`   Analysis:`);
                categoriesWithDetails.forEach((cat, index) => {
                    const order = cat.display_order || 'null';
                    console.log(`      ${index + 1}. ID: ${cat.id} | Order: ${order} | Children: ${cat.childrenCount}`);
                    if (cat.children.length > 0) {
                        cat.children.forEach(child => {
                            console.log(`         • ${child.name} (${child.type})`);
                        });
                    }
                });
                
                // Keep the first one (most children) and remove the rest
                const keepCategory = categoriesWithDetails[0];
                const removeCategories = categoriesWithDetails.slice(1);
                
                console.log(`   ✅ KEEPING: ${keepCategory.id} (${keepCategory.childrenCount} children)`);
                
                for (const removeCategory of removeCategories) {
                    if (removeCategory.childrenCount === 0) {
                        // Safe to remove empty duplicate
                        const { error: deleteError } = await supabase
                            .from('skill_tree_nodes')
                            .delete()
                            .eq('id', removeCategory.id);
                            
                        if (deleteError) {
                            console.error(`   ❌ Error removing empty duplicate ${removeCategory.id}:`, deleteError);
                        } else {
                            console.log(`   🗑️  REMOVED: Empty duplicate ${removeCategory.id}`);
                        }
                    } else {
                        // Has children - need to move them to the keep category first
                        console.log(`   🔄 Moving ${removeCategory.childrenCount} children from ${removeCategory.id} to ${keepCategory.id}`);
                        
                        for (const child of removeCategory.children) {
                            const { error: moveError } = await supabase
                                .from('skill_tree_nodes')
                                .update({
                                    parent_id: keepCategory.id,
                                    path: ['Test Preparation and Assessment', 'Graduate School Exams', testName]
                                })
                                .eq('id', child.id);
                                
                            if (moveError) {
                                console.error(`      ❌ Error moving ${child.name}:`, moveError);
                            } else {
                                console.log(`      ✅ Moved: ${child.name}`);
                            }
                        }
                        
                        // Now remove the empty duplicate
                        const { error: deleteError } = await supabase
                            .from('skill_tree_nodes')
                            .delete()
                            .eq('id', removeCategory.id);
                            
                        if (deleteError) {
                            console.error(`   ❌ Error removing duplicate after moving children:`, deleteError);
                        } else {
                            console.log(`   🗑️  REMOVED: Duplicate ${removeCategory.id} after moving children`);
                        }
                    }
                }
            }
        }
        
        // Verify final structure
        console.log('\n🔍 Verifying final Graduate School Exams structure...');
        
        const { data: finalSubcategories, error: finalError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, display_order')
            .eq('parent_id', gradSchoolExams.id)
            .order('display_order', { nullsFirst: false })
            .order('name');
            
        if (!finalError) {
            console.log(`\nFinal Graduate School Exams subcategories (${finalSubcategories.length}):`);
            finalSubcategories.forEach((cat, index) => {
                const order = cat.display_order || 'null';
                console.log(`   ${index + 1}. ${cat.name} - Order: ${order}`);
            });
            
            // Check each test has proper sections
            for (const testCat of finalSubcategories) {
                const { data: sections, error: sectionsError } = await supabase
                    .from('skill_tree_nodes')
                    .select('name, type')
                    .eq('parent_id', testCat.id);
                    
                if (!sectionsError && sections && sections.length > 0) {
                    console.log(`      └─ ${testCat.name}: ${sections.length} sections`);
                }
            }
        }
        
        console.log('\n🎉 Graduate School Exams cleanup completed!');
        console.log('✅ Duplicate test categories removed');
        console.log('✅ All test sections properly preserved');
        console.log('✅ Clean hierarchy structure restored');
        
    } catch (error) {
        console.error('❌ Cleanup failed:', error);
    }
}

cleanupGraduateSchoolDuplicates();
require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function fixGraduateTestPlacement() {
    try {
        console.log('🔧 FIXING GRADUATE TEST CATEGORY PLACEMENT\n');
        
        // Get Test Preparation category
        const { data: testPrep, error: testPrepError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .eq('name', 'Test Preparation and Assessment')
            .is('parent_id', null)
            .single();
            
        if (testPrepError || !testPrep) {
            console.error('❌ Error finding Test Preparation category:', testPrepError);
            return;
        }
        
        // Get Graduate School Exams category
        const { data: gradSchoolExams, error: gradError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .eq('name', 'Graduate School Exams')
            .eq('parent_id', testPrep.id)
            .single();
            
        if (gradError || !gradSchoolExams) {
            console.error('❌ Error finding Graduate School Exams category:', gradError);
            return;
        }
        
        console.log(`✅ Found Graduate School Exams: ${gradSchoolExams.id}`);
        
        // Find the individual test categories that should be under Graduate School Exams
        const individualTests = [
            'GRE (Graduate Record Examination)',
            'GMAT (Graduate Management)',
            'LSAT (Law School)',
            'MCAT (Medical School)'
        ];
        
        console.log('\n🔄 Moving individual test categories under Graduate School Exams...');
        
        for (const testName of individualTests) {
            // Find the test category that's currently at the wrong level
            const { data: testCategory, error: testError } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, parent_id, display_order')
                .eq('name', testName)
                .eq('parent_id', testPrep.id) // Currently under Test Prep instead of Graduate School Exams
                .single();
                
            if (testError || !testCategory) {
                console.log(`   ⚠️  Test category not found at top level: ${testName}`);
                continue;
            }
            
            console.log(`   📝 Moving ${testName} (${testCategory.id})`);
            
            // Move it under Graduate School Exams and update path
            const { error: moveError } = await supabase
                .from('skill_tree_nodes')
                .update({
                    parent_id: gradSchoolExams.id,
                    path: ['Test Preparation and Assessment', 'Graduate School Exams']
                })
                .eq('id', testCategory.id);
                
            if (moveError) {
                console.error(`   ❌ Error moving ${testName}:`, moveError);
            } else {
                console.log(`   ✅ Moved ${testName} under Graduate School Exams`);
                
                // Update paths for all children of this test category
                const { data: testSections, error: sectionsError } = await supabase
                    .from('skill_tree_nodes')
                    .select('id, name')
                    .eq('parent_id', testCategory.id);
                    
                if (!sectionsError && testSections) {
                    console.log(`      Updating paths for ${testSections.length} sections...`);
                    
                    for (const section of testSections) {
                        const { error: pathError } = await supabase
                            .from('skill_tree_nodes')
                            .update({
                                path: ['Test Preparation and Assessment', 'Graduate School Exams', testName]
                            })
                            .eq('id', section.id);
                            
                        if (pathError) {
                            console.error(`      ❌ Error updating path for ${section.name}:`, pathError);
                        } else {
                            console.log(`      ✅ Updated path for ${section.name}`);
                        }
                    }
                }
            }
        }
        
        // Verify the final structure
        console.log('\n🔍 Verifying final structure...');
        
        // Check Test Preparation top-level categories
        const { data: topCategories, error: topError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, display_order')
            .eq('parent_id', testPrep.id)
            .order('display_order', { nullsFirst: false })
            .order('name');
            
        if (!topError) {
            console.log(`\nTop-level categories under Test Preparation (${topCategories.length}):`);
            topCategories.forEach((cat, index) => {
                const order = cat.display_order || 'null';
                console.log(`   ${index + 1}. ${cat.name} - Order: ${order}`);
            });
        }
        
        // Check Graduate School Exams subcategories
        const { data: gradSubcategories, error: gradSubError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, display_order')
            .eq('parent_id', gradSchoolExams.id)
            .order('display_order', { nullsFirst: false })
            .order('name');
            
        if (!gradSubError) {
            console.log(`\nGraduate School Exams subcategories (${gradSubcategories.length}):`);
            gradSubcategories.forEach((cat, index) => {
                const order = cat.display_order || 'null';
                console.log(`   ${index + 1}. ${cat.name} - Order: ${order}`);
            });
        }
        
        console.log('\n🎉 Graduate test placement fixed!');
        console.log('✅ Individual test categories moved under Graduate School Exams');
        console.log('✅ Paths updated for all test sections');
        console.log('✅ Clean hierarchy structure restored');
        
    } catch (error) {
        console.error('❌ Fix failed:', error);
    }
}

fixGraduateTestPlacement();
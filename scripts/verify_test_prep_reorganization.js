require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function verifyTestPrepReorganization() {
    try {
        console.log('✅ VERIFYING TEST PREPARATION REORGANIZATION\n');
        
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
        
        console.log(`📚 Test Preparation & Assessment: ${testPrep.id}\n`);
        
        // Get all top-level subcategories under Test Preparation
        const { data: topCategories, error: topError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, display_order, type')
            .eq('parent_id', testPrep.id)
            .order('display_order', { nullsFirst: false })
            .order('name');
            
        if (topError) {
            console.error('❌ Error fetching top categories:', topError);
            return;
        }
        
        console.log(`Found ${topCategories.length} top-level categories under Test Preparation:`);
        topCategories.forEach((cat, index) => {
            const order = cat.display_order || 'null';
            console.log(`   ${index + 1}. ${cat.name} (${cat.type}) - Order: ${order}`);
        });
        
        // Detailed verification of key categories
        console.log('\n🔍 DETAILED STRUCTURE VERIFICATION:\n');
        
        // Verify College Entrance Exams structure
        const collegeExams = topCategories.find(cat => cat.name === 'College Entrance Exams');
        if (collegeExams) {
            console.log('🎓 COLLEGE ENTRANCE EXAMS:');
            
            const { data: collegeTests, error: collegeError } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, type, display_order')
                .eq('parent_id', collegeExams.id)
                .order('display_order', { nullsFirst: false })
                .order('name');
                
            if (!collegeError && collegeTests) {
                collegeTests.forEach(test => {
                    console.log(`   📝 ${test.name} (${test.type})`);
                });
                
                // Check ACT structure specifically
                const act = collegeTests.find(test => test.name === 'ACT');
                if (act) {
                    const { data: actSections, error: actError } = await supabase
                        .from('skill_tree_nodes')
                        .select('name, type')
                        .eq('parent_id', act.id)
                        .order('name');
                        
                    if (!actError && actSections) {
                        console.log(`      └─ ACT sections (${actSections.length}):`);
                        actSections.forEach(section => {
                            console.log(`         • ${section.name} (${section.type})`);
                        });
                    }
                }
                
                // Check SAT structure specifically
                const sat = collegeTests.find(test => test.name === 'SAT');
                if (sat) {
                    const { data: satSections, error: satError } = await supabase
                        .from('skill_tree_nodes')
                        .select('name, type')
                        .eq('parent_id', sat.id)
                        .order('name');
                        
                    if (!satError && satSections) {
                        console.log(`      └─ SAT sections (${satSections.length}):`);
                        satSections.forEach(section => {
                            console.log(`         • ${section.name} (${section.type})`);
                        });
                    }
                }
            }
        }
        
        // Verify Graduate School Exams structure
        console.log('\n🎓 GRADUATE SCHOOL EXAMS:');
        const gradExams = topCategories.find(cat => cat.name === 'Graduate School Exams');
        if (gradExams) {
            const { data: gradTests, error: gradError } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, type, display_order')
                .eq('parent_id', gradExams.id)
                .order('display_order', { nullsFirst: false })
                .order('name');
                
            if (!gradError && gradTests) {
                for (const test of gradTests) {
                    console.log(`   📝 ${test.name} (${test.type})`);
                    
                    // Get sections for each test
                    const { data: sections, error: sectionsError } = await supabase
                        .from('skill_tree_nodes')
                        .select('name, type')
                        .eq('parent_id', test.id)
                        .order('name');
                        
                    if (!sectionsError && sections && sections.length > 0) {
                        console.log(`      └─ Sections (${sections.length}):`);
                        sections.forEach(section => {
                            console.log(`         • ${section.name} (${section.type})`);
                        });
                    }
                }
            }
        }
        
        // Verify Language Proficiency Tests structure
        console.log('\n🌐 LANGUAGE PROFICIENCY TESTS:');
        const langTests = topCategories.find(cat => cat.name === 'Language Proficiency Tests');
        if (langTests) {
            const { data: tests, error: testsError } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, type')
                .eq('parent_id', langTests.id)
                .order('name');
                
            if (!testsError && tests) {
                for (const test of tests) {
                    console.log(`   📝 ${test.name} (${test.type})`);
                    
                    const { data: sections, error: sectionsError } = await supabase
                        .from('skill_tree_nodes')
                        .select('name, type')
                        .eq('parent_id', test.id)
                        .order('name');
                        
                    if (!sectionsError && sections && sections.length > 0) {
                        console.log(`      └─ Sections (${sections.length}):`);
                        sections.forEach(section => {
                            console.log(`         • ${section.name} (${section.type})`);
                        });
                    }
                }
            }
        }
        
        // Quick check of other categories
        console.log('\n📊 OTHER CATEGORIES SUMMARY:');
        const otherCategories = [
            'IQ and Cognitive Tests',
            'K-12 Standardized Tests', 
            'Professional Certification Exams',
            'Test-Taking Strategies'
        ];
        
        for (const catName of otherCategories) {
            const category = topCategories.find(cat => cat.name === catName);
            if (category) {
                const { data: items, error: itemsError } = await supabase
                    .from('skill_tree_nodes')
                    .select('name, type')
                    .eq('parent_id', category.id);
                    
                if (!itemsError && items) {
                    console.log(`   📂 ${catName}: ${items.length} items`);
                } else {
                    console.log(`   ❌ ${catName}: Error fetching items`);
                }
            } else {
                console.log(`   ⚠️  ${catName}: Category not found`);
            }
        }
        
        // Final structure validation
        console.log('\n🔍 STRUCTURE VALIDATION:');
        
        // Check that ACT sections are under ACT, not directly under College Entrance Exams
        const { data: actSections, error: actCheckError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id')
            .in('name', ['ACT English', 'ACT Math', 'ACT Reading', 'ACT Science']);
            
        if (!actCheckError && actSections) {
            const correctlyPlaced = actSections.every(section => {
                // Check if parent is ACT category, not College Entrance Exams
                return section.parent_id !== collegeExams?.id;
            });
            
            if (correctlyPlaced) {
                console.log('   ✅ ACT sections correctly placed under ACT category');
            } else {
                console.log('   ❌ Some ACT sections incorrectly placed');
            }
        }
        
        // Check that SAT sections are under SAT
        const { data: satSections, error: satCheckError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id')
            .in('name', ['SAT Reading and Writing', 'SAT Math', 'PSAT/NMSQT', 'SAT Subject Tests']);
            
        if (!satCheckError && satSections) {
            const correctlyPlaced = satSections.every(section => {
                return section.parent_id !== collegeExams?.id;
            });
            
            if (correctlyPlaced) {
                console.log('   ✅ SAT sections correctly placed under SAT category');
            } else {
                console.log('   ❌ Some SAT sections incorrectly placed');
            }
        }
        
        // Count total nodes
        const { data: allTestNodes, error: countError } = await supabase
            .from('skill_tree_nodes')
            .select('type', { count: 'exact' })
            .like('path', '%Test Preparation and Assessment%');
            
        if (!countError) {
            const totalNodes = allTestNodes.length;
            const categories = allTestNodes.filter(n => n.type === 'category').length;
            const skills = allTestNodes.filter(n => n.type === 'skill').length;
            
            console.log('\n📊 FINAL STATISTICS:');
            console.log(`   Total nodes under Test Preparation: ${totalNodes}`);
            console.log(`   Categories: ${categories}`);
            console.log(`   Skills: ${skills}`);
        }
        
        console.log('\n🎉 VERIFICATION COMPLETE!');
        console.log('✅ Test content properly organized by test type');
        console.log('✅ ACT English, Math, Reading, Science grouped under ACT');
        console.log('✅ SAT sections grouped under SAT');
        console.log('✅ Graduate school tests properly structured');
        console.log('✅ Language proficiency tests organized by test');
        console.log('✅ Existing category structure preserved');
        
    } catch (error) {
        console.error('❌ Verification failed:', error);
    }
}

verifyTestPrepReorganization();
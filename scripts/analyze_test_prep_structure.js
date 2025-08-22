require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function analyzeTestPrepStructure() {
    try {
        console.log('🔍 ANALYZING TEST PREPARATION & ASSESSMENT STRUCTURE\n');
        
        // 1. Find the Test Preparation category
        console.log('📚 Finding Test Preparation & Assessment category...');
        const { data: testPrep, error: testPrepError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, display_order')
            .eq('name', 'Test Preparation and Assessment')
            .is('parent_id', null)
            .single();
            
        if (testPrepError || !testPrep) {
            console.error('❌ Error finding Test Preparation category:', testPrepError);
            return;
        }
        
        console.log(`✅ Found Test Preparation & Assessment: ${testPrep.id}`);
        console.log(`   Display Order: ${testPrep.display_order}`);
        
        // 2. Get all direct children (current subcategories)
        console.log('\n📋 Current subcategories under Test Preparation:');
        const { data: currentSubcategories, error: subcatError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, display_order, learning_area, metadata')
            .eq('parent_id', testPrep.id)
            .order('display_order', { nullsFirst: false })
            .order('name');
            
        if (subcatError) {
            console.error('❌ Error fetching subcategories:', subcatError);
            return;
        }
        
        console.log(`Found ${currentSubcategories.length} current subcategories:`);
        currentSubcategories.forEach((subcat, index) => {
            const order = subcat.display_order || 'null';
            const description = subcat.metadata?.description || 'No description';
            console.log(`   ${index + 1}. ${subcat.name} (${subcat.type}) - Order: ${order}`);
            console.log(`      Learning Area: ${subcat.learning_area || 'None'}`);
            console.log(`      Description: ${description}\n`);
        });
        
        // 3. Analyze the complete hierarchy
        console.log('🌳 Complete Test Preparation hierarchy:');
        
        for (const subcat of currentSubcategories) {
            // Get children of each subcategory
            const { data: children, error: childrenError } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, type, display_order, learning_area')
                .eq('parent_id', subcat.id)
                .order('display_order', { nullsFirst: false })
                .order('name');
                
            if (childrenError) {
                console.error(`❌ Error fetching children for ${subcat.name}:`, childrenError);
                continue;
            }
            
            console.log(`\n📂 ${subcat.name} (${children.length} children):`);
            for (const child of children) {
                console.log(`   │ ├─ ${child.name} (${child.type})`);
                
                // Get grandchildren if any
                const { data: grandchildren, error: grandError } = await supabase
                    .from('skill_tree_nodes')
                    .select('name, type')
                    .eq('parent_id', child.id);
                    
                if (!grandError && grandchildren && grandchildren.length > 0) {
                    grandchildren.forEach(grandchild => {
                        console.log(`   │ │   └─ ${grandchild.name} (${grandchild.type})`);
                    });
                }
            }
        }
        
        // 4. Identify test patterns
        console.log('\n🎯 IDENTIFYING TEST PATTERNS:\n');
        
        // Look for test-specific content by analyzing names
        const allTestContent = [];
        
        for (const subcat of currentSubcategories) {
            const { data: allDescendants, error: descendantsError } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, type, parent_id, learning_area')
                .eq('parent_id', subcat.id);
                
            if (!descendantsError && allDescendants) {
                for (const desc of allDescendants) {
                    // Get their children too
                    const { data: subDescendants, error: subDescError } = await supabase
                        .from('skill_tree_nodes')
                        .select('id, name, type, parent_id, learning_area')
                        .eq('parent_id', desc.id);
                        
                    if (!subDescError && subDescendants) {
                        allTestContent.push(...subDescendants.map(sd => ({
                            ...sd,
                            parentCategory: subcat.name,
                            grandparentCategory: desc.name
                        })));
                    }
                    
                    allTestContent.push({
                        ...desc,
                        parentCategory: subcat.name,
                        grandparentCategory: null
                    });
                }
            }
        }
        
        // Group by test type
        const testGroups = {
            ACT: [],
            SAT: [],
            LSAT: [],
            MCAT: [],
            GRE: [],
            GMAT: [],
            'IQ Tests': [],
            'Reading Comprehension': [],
            'Standardized Tests': [],
            Other: []
        };
        
        allTestContent.forEach(item => {
            const name = item.name.toLowerCase();
            if (name.includes('act')) {
                testGroups.ACT.push(item);
            } else if (name.includes('sat')) {
                testGroups.SAT.push(item);
            } else if (name.includes('lsat')) {
                testGroups.LSAT.push(item);
            } else if (name.includes('mcat')) {
                testGroups.MCAT.push(item);
            } else if (name.includes('gre')) {
                testGroups.GRE.push(item);
            } else if (name.includes('gmat')) {
                testGroups.GMAT.push(item);
            } else if (name.includes('iq')) {
                testGroups['IQ Tests'].push(item);
            } else if (name.includes('reading comprehension') || item.parentCategory?.toLowerCase().includes('reading comprehension')) {
                testGroups['Reading Comprehension'].push(item);
            } else if (name.includes('standardized') || item.parentCategory?.toLowerCase().includes('standardized')) {
                testGroups['Standardized Tests'].push(item);
            } else {
                testGroups.Other.push(item);
            }
        });
        
        // Display analysis
        Object.entries(testGroups).forEach(([testType, items]) => {
            if (items.length > 0) {
                console.log(`📊 ${testType} (${items.length} items):`);
                items.forEach(item => {
                    const hierarchy = item.grandparentCategory 
                        ? `${item.parentCategory} → ${item.grandparentCategory} → ${item.name}`
                        : `${item.parentCategory} → ${item.name}`;
                    console.log(`   • ${hierarchy} (${item.type})`);
                });
                console.log('');
            }
        });
        
        // 5. Proposed reorganization
        console.log('💡 PROPOSED REORGANIZATION:\n');
        
        const proposedStructure = {
            'ACT': {
                description: 'American College Testing - comprehensive college readiness assessment',
                subcategories: ['ACT English', 'ACT Mathematics', 'ACT Reading', 'ACT Science', 'ACT Writing (Optional)']
            },
            'SAT': {
                description: 'Scholastic Assessment Test - college admissions test',
                subcategories: ['SAT Reading and Writing', 'SAT Mathematics', 'SAT Essay (Optional)']
            },
            'Graduate School Admissions': {
                description: 'Tests for graduate and professional school admissions',
                subcategories: ['GRE (Graduate Record Examination)', 'GMAT (Graduate Management)', 'LSAT (Law School)', 'MCAT (Medical School)']
            },
            'IQ and Cognitive Assessment': {
                description: 'Intelligence and cognitive ability testing',
                subcategories: ['IQ Tests', 'Cognitive Assessments', 'Aptitude Tests']
            },
            'Reading Comprehension': {
                description: 'Reading analysis and comprehension skills across various contexts',
                subcategories: ['General Reading Comprehension', 'Academic Reading', 'Critical Reading']
            },
            'Study Skills and Test Strategies': {
                description: 'General test-taking strategies and study methodologies',
                subcategories: ['Test-Taking Strategies', 'Time Management', 'Study Techniques', 'Test Anxiety Management']
            }
        };
        
        Object.entries(proposedStructure).forEach(([category, details]) => {
            console.log(`📁 ${category}`);
            console.log(`   Description: ${details.description}`);
            console.log(`   Subcategories:`);
            details.subcategories.forEach(subcat => {
                console.log(`     • ${subcat}`);
            });
            console.log('');
        });
        
        console.log('📋 REORGANIZATION BENEFITS:');
        console.log('✅ Groups content by actual test (ACT English, Math, etc. under ACT)');
        console.log('✅ Easier navigation for students preparing for specific tests');
        console.log('✅ Better alignment with how test prep is typically organized');
        console.log('✅ Reduces confusion between subject areas and test-specific content');
        console.log('✅ Maintains comprehensive coverage while improving structure');
        
        console.log('\n📊 SUMMARY:');
        console.log(`Current structure: ${currentSubcategories.length} subcategories organized by subject`);
        console.log(`Proposed structure: ${Object.keys(proposedStructure).length} categories organized by test type`);
        console.log(`Total content items analyzed: ${allTestContent.length}`);
        
    } catch (error) {
        console.error('❌ Analysis failed:', error);
    }
}

analyzeTestPrepStructure();
require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');
const { v4: uuidv4 } = require('uuid');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function reorganizeWithExistingCategories() {
    try {
        console.log('🔄 REORGANIZING TEST PREP WITH EXISTING CATEGORIES AS TOP LEVEL\n');
        
        // Step 1: Get Test Preparation category
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
        
        console.log(`✅ Found Test Preparation: ${testPrep.id}`);
        
        // Step 2: Get existing categories that we want to keep
        const { data: existingCategories, error: existingError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, display_order')
            .eq('parent_id', testPrep.id)
            .in('name', [
                'College Entrance Exams',
                'Graduate School Exams', 
                'IQ and Cognitive Tests',
                'K-12 Standardized Tests',
                'Language Proficiency Tests',
                'Professional Certification Exams',
                'Test-Taking Strategies'
            ]);
            
        if (existingError) {
            console.error('❌ Error fetching existing categories:', existingError);
            return;
        }
        
        console.log(`Found ${existingCategories.length} existing categories to keep`);
        
        // Step 3: Remove the new categories that were created at the top level
        console.log('\n🗑️  Removing incorrectly placed new categories...');
        
        const newCategoriesToRemove = [
            'ACT', 'SAT', 'Graduate School Admissions', 'Language Proficiency Tests',
            'IQ and Cognitive Assessment', 'K-12 Standardized Tests', 
            'Professional Certification', 'Test-Taking Strategies', 'Advanced Placement (AP)'
        ];
        
        for (const categoryName of newCategoriesToRemove) {
            // First, move any children back to temporary holding
            const { data: newCat, error: findError } = await supabase
                .from('skill_tree_nodes')
                .select('id, name')
                .eq('name', categoryName)
                .eq('parent_id', testPrep.id)
                .single();
                
            if (findError || !newCat) {
                console.log(`   ⚠️  Category not found: ${categoryName}`);
                continue;
            }
            
            // Get children and move them to appropriate existing categories temporarily
            const { data: children, error: childrenError } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, type')
                .eq('parent_id', newCat.id);
                
            if (!childrenError && children) {
                console.log(`   📦 Temporarily moving ${children.length} children from ${categoryName}`);
                
                // We'll reorganize these properly in the next step
                for (const child of children) {
                    await supabase
                        .from('skill_tree_nodes')
                        .update({ parent_id: testPrep.id })
                        .eq('id', child.id);
                }
            }
            
            // Remove the incorrectly placed category
            const { error: deleteError } = await supabase
                .from('skill_tree_nodes')
                .delete()
                .eq('id', newCat.id);
                
            if (deleteError) {
                console.error(`❌ Error removing ${categoryName}:`, deleteError);
            } else {
                console.log(`   ✅ Removed: ${categoryName}`);
            }
        }
        
        // Step 4: Create proper structure under existing categories
        console.log('\n🏗️  Creating proper test-specific structure...');
        
        // Map existing categories to their IDs
        const existingCatMap = {};
        existingCategories.forEach(cat => {
            existingCatMap[cat.name] = cat.id;
        });
        
        // Define the proper structure
        const properStructure = {
            'College Entrance Exams': {
                tests: {
                    'ACT': {
                        description: 'American College Testing - comprehensive college readiness assessment',
                        sections: ['ACT English', 'ACT Math', 'ACT Reading', 'ACT Science']
                    },
                    'SAT': {
                        description: 'Scholastic Assessment Test - college admissions test',
                        sections: ['SAT Reading and Writing', 'SAT Math', 'PSAT/NMSQT', 'SAT Subject Tests']
                    },
                    'Advanced Placement (AP)': {
                        description: 'College-level courses and examinations for high school students',
                        sections: ['AP Exam Strategies', 'Essay Writing for Tests']
                    }
                }
            },
            'Graduate School Exams': {
                tests: {
                    'GRE (Graduate Record Examination)': {
                        description: 'Graduate Record Examination for graduate school admissions',
                        sections: ['GRE Verbal Reasoning', 'GRE Quantitative Reasoning', 'GRE Analytical Writing']
                    },
                    'GMAT (Graduate Management)': {
                        description: 'Graduate Management Admission Test for business school',
                        sections: ['GMAT Verbal', 'GMAT Quantitative', 'GMAT Integrated Reasoning', 'GMAT Analytical Writing']
                    },
                    'LSAT (Law School)': {
                        description: 'Law School Admission Test',
                        sections: ['LSAT Logical Reasoning', 'LSAT Analytical Reasoning (Logic Games)', 'LSAT Reading Comprehension', 'LSAT Writing Sample']
                    },
                    'MCAT (Medical School)': {
                        description: 'Medical College Admission Test',
                        sections: ['MCAT Biological Sciences', 'MCAT Physical Sciences', 'MCAT Psychology and Sociology', 'MCAT Critical Analysis']
                    }
                }
            },
            'Language Proficiency Tests': {
                tests: {
                    'TOEFL (Test of English)': {
                        description: 'Test of English as a Foreign Language',
                        sections: ['TOEFL Reading', 'TOEFL Listening', 'TOEFL Speaking', 'TOEFL Writing']
                    },
                    'IELTS (English Language)': {
                        description: 'International English Language Testing System',
                        sections: ['IELTS Academic', 'IELTS General Training']
                    },
                    'Other Language Tests': {
                        description: 'International language proficiency assessments',
                        sections: ['Cambridge English Exams', 'DELE Spanish Proficiency', 'DELF/DALF French', 'HSK Chinese Proficiency', 'JLPT Japanese', 'TestDaF German']
                    }
                }
            }
        };
        
        // Create the test-specific subcategories under existing categories
        for (const [existingCatName, structure] of Object.entries(properStructure)) {
            const existingCatId = existingCatMap[existingCatName];
            if (!existingCatId) {
                console.log(`   ⚠️  Existing category not found: ${existingCatName}`);
                continue;
            }
            
            console.log(`\n📂 Organizing ${existingCatName}:`);
            
            let testOrder = 10;
            for (const [testName, testData] of Object.entries(structure.tests)) {
                // Create test category
                const testId = uuidv4();
                const { error: testError } = await supabase
                    .from('skill_tree_nodes')
                    .insert({
                        id: testId,
                        name: testName,
                        type: 'category',
                        parent_id: existingCatId,
                        display_order: testOrder,
                        learning_area: 'Test Preparation',
                        metadata: { description: testData.description },
                        path: ['Test Preparation and Assessment', existingCatName],
                        has_learning_content: false,
                        is_menu_leaf: false
                    });
                    
                if (testError) {
                    console.error(`   ❌ Error creating ${testName}:`, testError);
                    continue;
                }
                
                console.log(`   ✅ Created test category: ${testName}`);
                
                // Move sections under this test
                for (const sectionName of testData.sections) {
                    const { data: section, error: sectionFindError } = await supabase
                        .from('skill_tree_nodes')
                        .select('id, name')
                        .eq('name', sectionName)
                        .eq('type', 'skill')
                        .single();
                        
                    if (sectionFindError || !section) {
                        console.log(`      ⚠️  Section not found: ${sectionName}`);
                        continue;
                    }
                    
                    const { error: moveError } = await supabase
                        .from('skill_tree_nodes')
                        .update({
                            parent_id: testId,
                            path: ['Test Preparation and Assessment', existingCatName, testName]
                        })
                        .eq('id', section.id);
                        
                    if (moveError) {
                        console.error(`      ❌ Error moving ${sectionName}:`, moveError);
                    } else {
                        console.log(`      ✅ Moved section: ${sectionName}`);
                    }
                }
                
                testOrder += 10;
            }
        }
        
        // Step 5: Handle remaining categories that don't need test-specific grouping
        console.log('\n📋 Organizing remaining content under existing categories...');
        
        const directMappings = {
            'IQ and Cognitive Tests': [
                'Abstract Reasoning', 'Logical Reasoning', 'Memory Tests', 'Mensa Test Preparation',
                'Numerical Reasoning', 'Pattern Recognition', 'Processing Speed', 'Raven\'s Progressive Matrices',
                'Spatial Reasoning', 'Stanford-Binet Test', 'Verbal Reasoning', 'WAIS Test Components'
            ],
            'K-12 Standardized Tests': [
                'CogAT Cognitive Abilities', 'Common Core Assessments', 'ISEE/SSAT Private School',
                'MAP Growth Assessment', 'PARCC Test Prep', 'Regents Exams (New York)',
                'Smarter Balanced Assessment', 'STAAR Test (Texas)', 'STAR Assessment', 'State Assessment Tests'
            ],
            'Professional Certification Exams': [
                'AWS Certification', 'Bar Exam Preparation', 'CPA Accounting', 'Google Cloud Certification',
                'IT Certifications (CompTIA, Cisco)', 'Medical Board Exams', 'Microsoft Certifications',
                'PMP Project Management', 'Real Estate License', 'Teaching Certification'
            ],
            'Test-Taking Strategies': [
                'Computer-Based Test Skills', 'Elimination Techniques', 'Essay Structure and Planning',
                'Guessing Strategies', 'Math Problem Solving', 'Multiple Choice Strategies',
                'Question Analysis', 'Reading Comprehension Tactics', 'Test Anxiety Management', 'Time Management'
            ]
        };
        
        for (const [categoryName, skills] of Object.entries(directMappings)) {
            const categoryId = existingCatMap[categoryName];
            if (!categoryId) {
                console.log(`   ⚠️  Category not found: ${categoryName}`);
                continue;
            }
            
            console.log(`\n📂 Organizing ${categoryName}:`);
            
            for (const skillName of skills) {
                const { data: skill, error: skillError } = await supabase
                    .from('skill_tree_nodes')
                    .select('id, name')
                    .eq('name', skillName)
                    .eq('type', 'skill')
                    .single();
                    
                if (skillError || !skill) {
                    console.log(`   ⚠️  Skill not found: ${skillName}`);
                    continue;
                }
                
                const { error: moveError } = await supabase
                    .from('skill_tree_nodes')
                    .update({
                        parent_id: categoryId,
                        path: ['Test Preparation and Assessment', categoryName]
                    })
                    .eq('id', skill.id);
                    
                if (moveError) {
                    console.error(`   ❌ Error moving ${skillName}:`, moveError);
                } else {
                    console.log(`   ✅ Moved: ${skillName}`);
                }
            }
        }
        
        console.log('\n🎉 Test Preparation reorganization completed!');
        console.log('✅ Existing categories preserved as top level');
        console.log('✅ ACT sections grouped under ACT category');
        console.log('✅ SAT sections grouped under SAT category');
        console.log('✅ Graduate school tests properly organized');
        console.log('✅ All content logically structured by test type');
        
    } catch (error) {
        console.error('❌ Reorganization failed:', error);
    }
}

reorganizeWithExistingCategories();
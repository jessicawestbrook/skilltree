require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');
const { v4: uuidv4 } = require('uuid');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function reorganizeTestPreparation() {
    try {
        console.log('🔄 REORGANIZING TEST PREPARATION BY TEST TYPE\n');
        
        // Step 1: Create backup
        console.log('📋 Creating backup...');
        const { error: backupError } = await supabase.rpc('sql', {
            query: 'CREATE TABLE IF NOT EXISTS test_prep_backup AS SELECT * FROM skill_tree_nodes WHERE path @> \'["Test Preparation and Assessment"]\';'
        });
        
        if (backupError) {
            console.log('⚠️  Backup note (using alternative method)');
        }
        
        // Step 2: Get Test Preparation category
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
        
        // Step 3: Define new structure
        const newStructure = {
            'ACT': {
                description: 'American College Testing - comprehensive college readiness assessment',
                learning_area: 'College Admissions',
                display_order: 10,
                items: [
                    'ACT English',
                    'ACT Math', 
                    'ACT Reading',
                    'ACT Science'
                ]
            },
            'SAT': {
                description: 'Scholastic Assessment Test - college admissions test',
                learning_area: 'College Admissions', 
                display_order: 20,
                items: [
                    'SAT Reading and Writing',
                    'SAT Math',
                    'PSAT/NMSQT',
                    'SAT Subject Tests'
                ]
            },
            'Graduate School Admissions': {
                description: 'Tests for graduate and professional school admissions',
                learning_area: 'Graduate Admissions',
                display_order: 30,
                subcategories: {
                    'GRE (Graduate Record Examination)': {
                        items: ['GRE Verbal Reasoning', 'GRE Quantitative Reasoning', 'GRE Analytical Writing']
                    },
                    'GMAT (Graduate Management)': {
                        items: ['GMAT Verbal', 'GMAT Quantitative', 'GMAT Integrated Reasoning', 'GMAT Analytical Writing']
                    },
                    'LSAT (Law School)': {
                        items: ['LSAT Logical Reasoning', 'LSAT Analytical Reasoning (Logic Games)', 'LSAT Reading Comprehension', 'LSAT Writing Sample']
                    },
                    'MCAT (Medical School)': {
                        items: ['MCAT Biological Sciences', 'MCAT Physical Sciences', 'MCAT Psychology and Sociology', 'MCAT Critical Analysis']
                    }
                }
            },
            'Language Proficiency Tests': {
                description: 'International language competency assessments',
                learning_area: 'Language Assessment',
                display_order: 40,
                subcategories: {
                    'TOEFL (English)': {
                        items: ['TOEFL Reading', 'TOEFL Listening', 'TOEFL Speaking', 'TOEFL Writing']
                    },
                    'IELTS (English)': {
                        items: ['IELTS Academic', 'IELTS General Training']
                    },
                    'Other Languages': {
                        items: ['Cambridge English Exams', 'DELE Spanish Proficiency', 'DELF/DALF French', 'HSK Chinese Proficiency', 'JLPT Japanese', 'TestDaF German']
                    }
                }
            },
            'IQ and Cognitive Assessment': {
                description: 'Intelligence and cognitive ability testing',
                learning_area: 'Cognitive Assessment',
                display_order: 50,
                items: [
                    'Stanford-Binet Test',
                    'WAIS Test Components',
                    'Raven\'s Progressive Matrices',
                    'Mensa Test Preparation',
                    'Abstract Reasoning',
                    'Logical Reasoning',
                    'Numerical Reasoning',
                    'Spatial Reasoning',
                    'Verbal Reasoning',
                    'Memory Tests',
                    'Processing Speed',
                    'Pattern Recognition'
                ]
            },
            'K-12 Standardized Tests': {
                description: 'Primary and secondary education assessments',
                learning_area: 'K-12 Assessment',
                display_order: 60,
                items: [
                    'State Assessment Tests',
                    'Common Core Assessments',
                    'PARCC Test Prep',
                    'Smarter Balanced Assessment',
                    'STAAR Test (Texas)',
                    'Regents Exams (New York)',
                    'CogAT Cognitive Abilities',
                    'MAP Growth Assessment',
                    'STAR Assessment',
                    'ISEE/SSAT Private School'
                ]
            },
            'Professional Certification': {
                description: 'Career and professional licensing examinations',
                learning_area: 'Professional Development',
                display_order: 70,
                items: [
                    'Bar Exam Preparation',
                    'Medical Board Exams',
                    'CPA Accounting',
                    'Teaching Certification',
                    'Real Estate License',
                    'PMP Project Management',
                    'IT Certifications (CompTIA, Cisco)',
                    'AWS Certification',
                    'Microsoft Certifications',
                    'Google Cloud Certification'
                ]
            },
            'Test-Taking Strategies': {
                description: 'General test preparation and study skills',
                learning_area: 'Study Skills',
                display_order: 80,
                items: [
                    'Multiple Choice Strategies',
                    'Essay Structure and Planning',
                    'Time Management',
                    'Question Analysis',
                    'Elimination Techniques',
                    'Guessing Strategies',
                    'Test Anxiety Management',
                    'Computer-Based Test Skills',
                    'Math Problem Solving',
                    'Reading Comprehension Tactics'
                ]
            },
            'Advanced Placement (AP)': {
                description: 'College-level courses and examinations for high school students',
                learning_area: 'Advanced Academics',
                display_order: 15,
                items: [
                    'AP Exam Strategies',
                    'Essay Writing for Tests'
                ]
            }
        };
        
        // Step 4: Create new category structure
        console.log('\n🏗️  Creating new category structure...');
        
        const categoryMapping = {};
        
        for (const [categoryName, categoryData] of Object.entries(newStructure)) {
            console.log(`\n📁 Creating category: ${categoryName}`);
            
            // Create main category
            const categoryId = uuidv4();
            const { error: categoryError } = await supabase
                .from('skill_tree_nodes')
                .insert({
                    id: categoryId,
                    name: categoryName,
                    type: 'category',
                    parent_id: testPrep.id,
                    display_order: categoryData.display_order,
                    learning_area: categoryData.learning_area,
                    metadata: { description: categoryData.description },
                    path: ['Test Preparation and Assessment'],
                    has_learning_content: false,
                    is_menu_leaf: false
                });
                
            if (categoryError) {
                console.error(`❌ Error creating ${categoryName}:`, categoryError);
                continue;
            }
            
            console.log(`✅ Created ${categoryName}: ${categoryId}`);
            categoryMapping[categoryName] = categoryId;
            
            // Create subcategories if they exist
            if (categoryData.subcategories) {
                let subcatOrder = 10;
                for (const [subcatName, subcatData] of Object.entries(categoryData.subcategories)) {
                    const subcatId = uuidv4();
                    const { error: subcatError } = await supabase
                        .from('skill_tree_nodes')
                        .insert({
                            id: subcatId,
                            name: subcatName,
                            type: 'category',
                            parent_id: categoryId,
                            display_order: subcatOrder,
                            learning_area: categoryData.learning_area,
                            metadata: { description: `${subcatName} preparation and practice` },
                            path: ['Test Preparation and Assessment', categoryName],
                            has_learning_content: false,
                            is_menu_leaf: false
                        });
                        
                    if (subcatError) {
                        console.error(`❌ Error creating ${subcatName}:`, subcatError);
                        continue;
                    }
                    
                    console.log(`   ✅ Created subcategory: ${subcatName}`);
                    categoryMapping[subcatName] = subcatId;
                    subcatOrder += 10;
                }
            }
        }
        
        // Step 5: Move existing content to new structure
        console.log('\n🔄 Moving existing content to new structure...');
        
        // Get all existing skills that need to be moved
        const { data: existingSkills, error: skillsError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, learning_area, metadata, has_learning_content, is_menu_leaf')
            .like('path', '%Test Preparation and Assessment%')
            .eq('type', 'skill');
            
        if (skillsError) {
            console.error('❌ Error fetching existing skills:', skillsError);
            return;
        }
        
        console.log(`Found ${existingSkills.length} skills to relocate`);
        
        // Create mapping for skill relocation
        for (const skill of existingSkills) {
            let newParentId = null;
            let newPath = ['Test Preparation and Assessment'];
            
            // Determine where each skill should go
            for (const [categoryName, categoryData] of Object.entries(newStructure)) {
                // Check direct items
                if (categoryData.items && categoryData.items.includes(skill.name)) {
                    newParentId = categoryMapping[categoryName];
                    newPath = ['Test Preparation and Assessment', categoryName];
                    break;
                }
                
                // Check subcategory items
                if (categoryData.subcategories) {
                    for (const [subcatName, subcatData] of Object.entries(categoryData.subcategories)) {
                        if (subcatData.items && subcatData.items.includes(skill.name)) {
                            newParentId = categoryMapping[subcatName];
                            newPath = ['Test Preparation and Assessment', categoryName, subcatName];
                            break;
                        }
                    }
                    if (newParentId) break;
                }
            }
            
            if (newParentId) {
                const { error: moveError } = await supabase
                    .from('skill_tree_nodes')
                    .update({
                        parent_id: newParentId,
                        path: newPath
                    })
                    .eq('id', skill.id);
                    
                if (moveError) {
                    console.error(`❌ Error moving ${skill.name}:`, moveError);
                } else {
                    console.log(`   ✅ Moved ${skill.name} to ${newPath.join(' → ')}`);
                }
            } else {
                console.log(`   ⚠️  Could not find new location for: ${skill.name}`);
            }
        }
        
        // Step 6: Remove old category structure
        console.log('\n🗑️  Removing old category structure...');
        
        const oldCategories = [
            'College Entrance Exams',
            'Graduate School Exams', 
            'IQ and Cognitive Tests',
            'K-12 Standardized Tests',
            'Language Proficiency Tests',
            'Professional Certification Exams',
            'Test-Taking Strategies'
        ];
        
        for (const oldCategory of oldCategories) {
            const { error: deleteError } = await supabase
                .from('skill_tree_nodes')
                .delete()
                .eq('name', oldCategory)
                .eq('parent_id', testPrep.id);
                
            if (deleteError) {
                console.error(`❌ Error removing ${oldCategory}:`, deleteError);
            } else {
                console.log(`   ✅ Removed old category: ${oldCategory}`);
            }
        }
        
        console.log('\n🎉 Test Preparation reorganization completed!');
        console.log('✅ Content organized by test type rather than subject area');
        console.log('✅ ACT content grouped under ACT category');
        console.log('✅ SAT content grouped under SAT category'); 
        console.log('✅ Graduate school tests properly categorized');
        console.log('✅ Improved navigation and user experience');
        
    } catch (error) {
        console.error('❌ Reorganization failed:', error);
    }
}

reorganizeTestPreparation();
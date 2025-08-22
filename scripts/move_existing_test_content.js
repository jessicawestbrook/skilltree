require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function moveExistingTestContent() {
    try {
        console.log('🔄 MOVING EXISTING TEST CONTENT TO NEW STRUCTURE\n');
        
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
        
        // Get old categories to find their children
        const oldCategories = [
            'College Entrance Exams',
            'Graduate School Exams', 
            'IQ and Cognitive Tests',
            'K-12 Standardized Tests',
            'Language Proficiency Tests',
            'Professional Certification Exams',
            'Test-Taking Strategies'
        ];
        
        // Get new categories
        const { data: newCategories, error: newCatError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .eq('parent_id', testPrep.id)
            .in('name', [
                'ACT', 'SAT', 'Graduate School Admissions', 'Language Proficiency Tests',
                'IQ and Cognitive Assessment', 'K-12 Standardized Tests', 
                'Professional Certification', 'Test-Taking Strategies', 'Advanced Placement (AP)'
            ]);
            
        if (newCatError) {
            console.error('❌ Error fetching new categories:', newCatError);
            return;
        }
        
        console.log(`Found ${newCategories.length} new categories`);
        
        // Get subcategories under Graduate School Admissions and Language Proficiency Tests
        const { data: gradSubcats, error: gradError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .in('name', [
                'GRE (Graduate Record Examination)', 'GMAT (Graduate Management)',
                'LSAT (Law School)', 'MCAT (Medical School)'
            ]);
            
        const { data: langSubcats, error: langError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .in('name', [
                'TOEFL (English)', 'IELTS (English)', 'Other Languages'
            ]);
            
        if (gradError || langError) {
            console.error('❌ Error fetching subcategories');
            return;
        }
        
        // Create mapping for where content should go
        const contentMapping = {
            // ACT content
            'ACT English': { newParent: 'ACT', path: ['Test Preparation and Assessment', 'ACT'] },
            'ACT Math': { newParent: 'ACT', path: ['Test Preparation and Assessment', 'ACT'] },
            'ACT Reading': { newParent: 'ACT', path: ['Test Preparation and Assessment', 'ACT'] },
            'ACT Science': { newParent: 'ACT', path: ['Test Preparation and Assessment', 'ACT'] },
            
            // SAT content
            'SAT Reading and Writing': { newParent: 'SAT', path: ['Test Preparation and Assessment', 'SAT'] },
            'SAT Math': { newParent: 'SAT', path: ['Test Preparation and Assessment', 'SAT'] },
            'PSAT/NMSQT': { newParent: 'SAT', path: ['Test Preparation and Assessment', 'SAT'] },
            'SAT Subject Tests': { newParent: 'SAT', path: ['Test Preparation and Assessment', 'SAT'] },
            
            // AP content
            'AP Exam Strategies': { newParent: 'Advanced Placement (AP)', path: ['Test Preparation and Assessment', 'Advanced Placement (AP)'] },
            'Essay Writing for Tests': { newParent: 'Advanced Placement (AP)', path: ['Test Preparation and Assessment', 'Advanced Placement (AP)'] },
            
            // GRE content
            'GRE Verbal Reasoning': { newParent: 'GRE (Graduate Record Examination)', path: ['Test Preparation and Assessment', 'Graduate School Admissions', 'GRE (Graduate Record Examination)'] },
            'GRE Quantitative Reasoning': { newParent: 'GRE (Graduate Record Examination)', path: ['Test Preparation and Assessment', 'Graduate School Admissions', 'GRE (Graduate Record Examination)'] },
            'GRE Analytical Writing': { newParent: 'GRE (Graduate Record Examination)', path: ['Test Preparation and Assessment', 'Graduate School Admissions', 'GRE (Graduate Record Examination)'] },
            
            // GMAT content
            'GMAT Verbal': { newParent: 'GMAT (Graduate Management)', path: ['Test Preparation and Assessment', 'Graduate School Admissions', 'GMAT (Graduate Management)'] },
            'GMAT Quantitative': { newParent: 'GMAT (Graduate Management)', path: ['Test Preparation and Assessment', 'Graduate School Admissions', 'GMAT (Graduate Management)'] },
            'GMAT Integrated Reasoning': { newParent: 'GMAT (Graduate Management)', path: ['Test Preparation and Assessment', 'Graduate School Admissions', 'GMAT (Graduate Management)'] },
            'GMAT Analytical Writing': { newParent: 'GMAT (Graduate Management)', path: ['Test Preparation and Assessment', 'Graduate School Admissions', 'GMAT (Graduate Management)'] },
            
            // LSAT content
            'LSAT Logical Reasoning': { newParent: 'LSAT (Law School)', path: ['Test Preparation and Assessment', 'Graduate School Admissions', 'LSAT (Law School)'] },
            'LSAT Analytical Reasoning (Logic Games)': { newParent: 'LSAT (Law School)', path: ['Test Preparation and Assessment', 'Graduate School Admissions', 'LSAT (Law School)'] },
            'LSAT Reading Comprehension': { newParent: 'LSAT (Law School)', path: ['Test Preparation and Assessment', 'Graduate School Admissions', 'LSAT (Law School)'] },
            'LSAT Writing Sample': { newParent: 'LSAT (Law School)', path: ['Test Preparation and Assessment', 'Graduate School Admissions', 'LSAT (Law School)'] },
            
            // MCAT content
            'MCAT Biological Sciences': { newParent: 'MCAT (Medical School)', path: ['Test Preparation and Assessment', 'Graduate School Admissions', 'MCAT (Medical School)'] },
            'MCAT Physical Sciences': { newParent: 'MCAT (Medical School)', path: ['Test Preparation and Assessment', 'Graduate School Admissions', 'MCAT (Medical School)'] },
            'MCAT Psychology and Sociology': { newParent: 'MCAT (Medical School)', path: ['Test Preparation and Assessment', 'Graduate School Admissions', 'MCAT (Medical School)'] },
            'MCAT Critical Analysis': { newParent: 'MCAT (Medical School)', path: ['Test Preparation and Assessment', 'Graduate School Admissions', 'MCAT (Medical School)'] },
            
            // TOEFL content  
            'TOEFL Reading': { newParent: 'TOEFL (English)', path: ['Test Preparation and Assessment', 'Language Proficiency Tests', 'TOEFL (English)'] },
            'TOEFL Listening': { newParent: 'TOEFL (English)', path: ['Test Preparation and Assessment', 'Language Proficiency Tests', 'TOEFL (English)'] },
            'TOEFL Speaking': { newParent: 'TOEFL (English)', path: ['Test Preparation and Assessment', 'Language Proficiency Tests', 'TOEFL (English)'] },
            'TOEFL Writing': { newParent: 'TOEFL (English)', path: ['Test Preparation and Assessment', 'Language Proficiency Tests', 'TOEFL (English)'] },
            
            // IELTS content
            'IELTS Academic': { newParent: 'IELTS (English)', path: ['Test Preparation and Assessment', 'Language Proficiency Tests', 'IELTS (English)'] },
            'IELTS General Training': { newParent: 'IELTS (English)', path: ['Test Preparation and Assessment', 'Language Proficiency Tests', 'IELTS (English)'] },
            
            // Other language tests
            'Cambridge English Exams': { newParent: 'Other Languages', path: ['Test Preparation and Assessment', 'Language Proficiency Tests', 'Other Languages'] },
            'DELE Spanish Proficiency': { newParent: 'Other Languages', path: ['Test Preparation and Assessment', 'Language Proficiency Tests', 'Other Languages'] },
            'DELF/DALF French': { newParent: 'Other Languages', path: ['Test Preparation and Assessment', 'Language Proficiency Tests', 'Other Languages'] },
            'HSK Chinese Proficiency': { newParent: 'Other Languages', path: ['Test Preparation and Assessment', 'Language Proficiency Tests', 'Other Languages'] },
            'JLPT Japanese': { newParent: 'Other Languages', path: ['Test Preparation and Assessment', 'Language Proficiency Tests', 'Other Languages'] },
            'TestDaF German': { newParent: 'Other Languages', path: ['Test Preparation and Assessment', 'Language Proficiency Tests', 'Other Languages'] }
        };
        
        // Get all categories to create a full mapping
        const allCategories = [...newCategories, ...gradSubcats, ...langSubcats];
        const categoryIdMap = {};
        allCategories.forEach(cat => {
            categoryIdMap[cat.name] = cat.id;
        });
        
        console.log('📋 Moving individual skills...\n');
        
        let movedCount = 0;
        let notFoundCount = 0;
        
        for (const [skillName, destination] of Object.entries(contentMapping)) {
            // Find the skill
            const { data: skill, error: skillError } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, parent_id')
                .eq('name', skillName)
                .eq('type', 'skill')
                .single();
                
            if (skillError || !skill) {
                console.log(`   ⚠️  Skill not found: ${skillName}`);
                notFoundCount++;
                continue;
            }
            
            const newParentId = categoryIdMap[destination.newParent];
            if (!newParentId) {
                console.log(`   ⚠️  New parent category not found: ${destination.newParent}`);
                continue;
            }
            
            // Move the skill
            const { error: moveError } = await supabase
                .from('skill_tree_nodes')
                .update({
                    parent_id: newParentId,
                    path: destination.path
                })
                .eq('id', skill.id);
                
            if (moveError) {
                console.error(`   ❌ Error moving ${skillName}:`, moveError);
            } else {
                console.log(`   ✅ Moved: ${skillName} → ${destination.path.join(' → ')}`);
                movedCount++;
            }
        }
        
        // Move remaining content to appropriate categories
        console.log('\n📋 Moving remaining content...');
        
        const remainingMappings = {
            'IQ and Cognitive Assessment': [
                'Abstract Reasoning', 'Logical Reasoning', 'Memory Tests', 'Mensa Test Preparation',
                'Numerical Reasoning', 'Pattern Recognition', 'Processing Speed', 'Raven\'s Progressive Matrices',
                'Spatial Reasoning', 'Stanford-Binet Test', 'Verbal Reasoning', 'WAIS Test Components'
            ],
            'K-12 Standardized Tests': [
                'CogAT Cognitive Abilities', 'Common Core Assessments', 'ISEE/SSAT Private School',
                'MAP Growth Assessment', 'PARCC Test Prep', 'Regents Exams (New York)',
                'Smarter Balanced Assessment', 'STAAR Test (Texas)', 'STAR Assessment', 'State Assessment Tests'
            ],
            'Professional Certification': [
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
        
        for (const [categoryName, skills] of Object.entries(remainingMappings)) {
            const categoryId = categoryIdMap[categoryName];
            if (!categoryId) {
                console.log(`   ⚠️  Category not found: ${categoryName}`);
                continue;
            }
            
            for (const skillName of skills) {
                const { data: skill, error: skillError } = await supabase
                    .from('skill_tree_nodes')
                    .select('id, name')
                    .eq('name', skillName)
                    .eq('type', 'skill')
                    .single();
                    
                if (skillError || !skill) {
                    console.log(`   ⚠️  Skill not found: ${skillName}`);
                    notFoundCount++;
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
                    console.log(`   ✅ Moved: ${skillName} → ${categoryName}`);
                    movedCount++;
                }
            }
        }
        
        console.log(`\n📊 Movement Summary:`);
        console.log(`   ✅ Successfully moved: ${movedCount} skills`);
        console.log(`   ⚠️  Not found: ${notFoundCount} skills`);
        
        console.log('\n🎉 Content movement completed!');
        
    } catch (error) {
        console.error('❌ Content movement failed:', error);
    }
}

moveExistingTestContent();
require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');
const { v4: uuidv4 } = require('uuid');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

// Define proper educational hierarchy structure
const PROPER_HIERARCHY = {
    'Mathematics': {
        'Arithmetic': ['Basic Operations', 'Fractions', 'Decimals', 'Percentages', 'Measurements'],
        'Algebra': ['Linear Equations', 'Polynomials', 'Quadratic Equations', 'Systems of Equations'],
        'Geometry': ['Basic Shapes', 'Area and Perimeter', 'Volume', 'Angles', 'Coordinate Geometry'],
        'Calculus': ['Limits', 'Derivatives', 'Integrals', 'Applications'],
        'Statistics': ['Data Analysis', 'Probability', 'Distributions'],
        'Applied Mathematics': ['Mathematical Modeling', 'Optimization', 'Numerical Methods']
    },
    'Languages': {
        'English': ['Grammar', 'Literature', 'Writing', 'Reading Comprehension'],
        'Spanish': ['Grammar', 'Vocabulary', 'Conversation', 'Literature'],
        'French': ['Grammar', 'Vocabulary', 'Conversation', 'Literature'],
        'Latin': ['Grammar', 'Vocabulary', 'Classical Texts'],
        'Mandarin Chinese': ['Grammar', 'Characters', 'Conversation', 'Culture'],
        'Language Learning Theory': ['Phonetics', 'Linguistics', 'Second Language Acquisition']
    },
    'Natural Sciences': {
        'Physics': ['Mechanics', 'Thermodynamics', 'Electromagnetism', 'Quantum Physics'],
        'Chemistry': ['Atomic Structure', 'Chemical Bonds', 'Reactions', 'Organic Chemistry'],
        'Biology': ['Cell Biology', 'Genetics', 'Evolution', 'Ecology', 'Human Biology'],
        'Earth Science': ['Geology', 'Meteorology', 'Oceanography', 'Environmental Science'],
        'Astronomy': ['Solar System', 'Stars and Galaxies', 'Cosmology']
    },
    'Computer Science': {
        'Programming': ['Fundamentals', 'Data Structures', 'Algorithms', 'Object-Oriented Programming'],
        'Web Development': ['HTML/CSS', 'JavaScript', 'Frontend Frameworks', 'Backend Development'],
        'Data Science': ['Statistics', 'Machine Learning', 'Data Analysis', 'Visualization'],
        'Software Engineering': ['Design Patterns', 'Testing', 'Version Control', 'Project Management'],
        'Computer Systems': ['Operating Systems', 'Networks', 'Databases', 'Security']
    },
    'Social Sciences': {
        'Psychology': ['Cognitive Psychology', 'Behavioral Psychology', 'Social Psychology', 'Developmental Psychology'],
        'Sociology': ['Social Theory', 'Social Institutions', 'Social Change', 'Research Methods'],
        'Economics': ['Microeconomics', 'Macroeconomics', 'International Economics', 'Economic Policy'],
        'Political Science': ['Government Systems', 'Political Theory', 'International Relations', 'Public Policy'],
        'Anthropology': ['Cultural Anthropology', 'Physical Anthropology', 'Archaeology', 'Linguistic Anthropology']
    },
    'Humanities': {
        'History': ['Ancient History', 'Medieval History', 'Modern History', 'American History', 'World History'],
        'Philosophy': ['Logic', 'Ethics', 'Metaphysics', 'Political Philosophy', 'Philosophy of Mind'],
        'Literature': ['Classical Literature', 'Modern Literature', 'Poetry', 'Drama', 'Literary Analysis'],
        'Art History': ['Ancient Art', 'Renaissance', 'Modern Art', 'Contemporary Art'],
        'Religion and Theology': ['World Religions', 'Religious History', 'Theology', 'Religious Philosophy']
    },
    'Applied Sciences': {
        'Engineering': ['Mechanical Engineering', 'Electrical Engineering', 'Civil Engineering', 'Computer Engineering'],
        'Medicine': ['Anatomy', 'Physiology', 'Pathology', 'Pharmacology', 'Clinical Medicine'],
        'Agriculture': ['Crop Science', 'Animal Science', 'Soil Science', 'Agricultural Economics'],
        'Environmental Science': ['Ecology', 'Conservation', 'Pollution Control', 'Renewable Energy']
    },
    'Creative Skills': {
        'Visual Arts': ['Drawing', 'Painting', 'Sculpture', 'Digital Art', 'Art Theory'],
        'Music': ['Music Theory', 'Composition', 'Performance', 'Music History'],
        'Writing': ['Creative Writing', 'Poetry', 'Screenwriting', 'Technical Writing'],
        'Design': ['Graphic Design', 'Web Design', 'Industrial Design', 'UX/UI Design'],
        'Media Production': ['Photography', 'Video Production', 'Audio Production', 'Animation']
    },
    'Professional Skills': {
        'Business Management': ['Leadership', 'Project Management', 'Strategic Planning', 'Operations'],
        'Finance': ['Accounting', 'Financial Analysis', 'Investment', 'Personal Finance'],
        'Marketing': ['Market Research', 'Digital Marketing', 'Brand Management', 'Sales'],
        'Human Resources': ['Recruitment', 'Employee Development', 'Organizational Behavior'],
        'Entrepreneurship': ['Business Planning', 'Startup Management', 'Innovation', 'Risk Management']
    },
    'Technical Skills': {
        'Information Technology': ['System Administration', 'Cybersecurity', 'Cloud Computing', 'DevOps'],
        'Manufacturing': ['Quality Control', 'Process Optimization', 'Automation', 'Supply Chain'],
        'Construction': ['Building Techniques', 'Project Planning', 'Safety Protocols'],
        'Healthcare Technology': ['Medical Devices', 'Health Informatics', 'Telemedicine']
    },
    'Life Skills': {
        'Personal Development': ['Goal Setting', 'Time Management', 'Self-Reflection', 'Mindfulness'],
        'Communication': ['Public Speaking', 'Written Communication', 'Interpersonal Skills', 'Conflict Resolution'],
        'Financial Literacy': ['Budgeting', 'Saving', 'Investing', 'Credit Management'],
        'Health and Wellness': ['Nutrition', 'Exercise', 'Mental Health', 'Stress Management'],
        'Critical Thinking': ['Logic', 'Problem Solving', 'Decision Making', 'Research Skills']
    },
    'Test Preparation and Assessment': {
        'Standardized Tests': ['SAT', 'ACT', 'GRE', 'GMAT', 'LSAT', 'MCAT'],
        'Language Proficiency': ['TOEFL', 'IELTS', 'Language Certificates'],
        'Professional Certifications': ['IT Certifications', 'Project Management', 'Industry-Specific Certs'],
        'IQ and Cognitive Assessment': ['IQ Tests', 'Cognitive Abilities', 'Memory Tests'],
        'Academic Assessment': ['Study Strategies', 'Test-Taking Skills', 'Academic Writing']
    }
};

async function rebuildProperHierarchy() {
    try {
        console.log('🏗️ REBUILDING PROPER EDUCATIONAL HIERARCHY...\n');
        
        // Step 1: Get current state
        const { data: allNodes, error: allError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, parent_id, learning_area');
            
        if (allError) throw allError;
        console.log(`Current database has ${allNodes.length} total nodes`);
        
        // Step 2: Ensure 12 top-level categories exist and are clean
        console.log('\n=== STEP 1: Setting up top-level categories ===');
        const topLevelCategories = {};
        
        for (const [categoryName, subcategories] of Object.entries(PROPER_HIERARCHY)) {
            // Find existing top-level category
            let existingCategory = allNodes.find(n => 
                n.name === categoryName && n.type === 'category'
            );
            
            if (existingCategory) {
                // Ensure it's at root level
                if (existingCategory.parent_id !== null) {
                    await supabase
                        .from('skill_tree_nodes')
                        .update({ parent_id: null, learning_area: categoryName })
                        .eq('id', existingCategory.id);
                }
                topLevelCategories[categoryName] = existingCategory;
                console.log(`✅ ${categoryName} (existing)`);
            } else {
                console.log(`❌ ${categoryName} not found - needs creation`);
            }
        }
        
        console.log(`Found ${Object.keys(topLevelCategories).length}/12 top-level categories`);
        
        // Step 3: Create proper subcategory structure
        console.log('\n=== STEP 2: Creating proper subcategory structure ===');
        
        for (const [topLevelName, subcategories] of Object.entries(PROPER_HIERARCHY)) {
            if (!topLevelCategories[topLevelName]) continue;
            
            const topLevelId = topLevelCategories[topLevelName].id;
            console.log(`\nProcessing ${topLevelName}...`);
            
            for (const [subcategoryName, topics] of Object.entries(subcategories)) {
                // Check if subcategory exists
                let subcategory = allNodes.find(n => 
                    n.name === subcategoryName && 
                    n.type === 'category' && 
                    n.learning_area === topLevelName
                );
                
                if (!subcategory) {
                    // Create subcategory
                    const { data: newSubcat, error: subcatError } = await supabase
                        .from('skill_tree_nodes')
                        .insert([{
                            id: uuidv4(),
                            name: subcategoryName,
                            type: 'category',
                            parent_id: topLevelId,
                            learning_area: topLevelName,
                            has_learning_content: false,
                            is_menu_leaf: false,
                            created_at: new Date().toISOString(),
                            updated_at: new Date().toISOString()
                        }])
                        .select()
                        .single();
                        
                    if (subcatError) {
                        console.log(`  ❌ Failed to create ${subcategoryName}: ${subcatError.message}`);
                        continue;
                    }
                    subcategory = newSubcat;
                    console.log(`  ➕ Created ${subcategoryName}`);
                } else {
                    // Ensure it has correct parent
                    if (subcategory.parent_id !== topLevelId) {
                        await supabase
                            .from('skill_tree_nodes')
                            .update({ parent_id: topLevelId })
                            .eq('id', subcategory.id);
                        console.log(`  🔧 Fixed parent for ${subcategoryName}`);
                    } else {
                        console.log(`  ✅ ${subcategoryName} already correct`);
                    }
                }
                
                // Create topic categories under subcategory
                for (const topicName of topics) {
                    let topic = allNodes.find(n => 
                        n.name === topicName && 
                        n.type === 'category' &&
                        n.learning_area === topLevelName
                    );
                    
                    if (!topic) {
                        const { error: topicError } = await supabase
                            .from('skill_tree_nodes')
                            .insert([{
                                id: uuidv4(),
                                name: topicName,
                                type: 'category', 
                                parent_id: subcategory.id,
                                learning_area: topLevelName,
                                has_learning_content: false,
                                is_menu_leaf: false,
                                created_at: new Date().toISOString(),
                                updated_at: new Date().toISOString()
                            }]);
                            
                        if (!topicError) {
                            console.log(`    ➕ Created topic: ${topicName}`);
                        }
                    }
                }
            }
        }
        
        console.log('\n=== STEP 3: Organizing existing skills ===');
        // This would be a complex step to match existing skills to proper parents
        // For now, let's focus on creating the structure
        
        console.log('\n✅ Basic hierarchy structure created!');
        console.log('Next step would be to organize existing skills under proper topic categories.');
        
    } catch (error) {
        console.error('Error rebuilding hierarchy:', error);
    }
}

rebuildProperHierarchy();
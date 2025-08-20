require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

// Ordering frameworks by difficulty/commonness
const orderedCategories = {
    // Top-level Academic Disciplines (foundational to advanced)
    'Academic Disciplines': [
        'Mathematics',           // 1 - Most fundamental
        'Languages',            // 2 - Essential communication
        'Natural Sciences',     // 3 - Core understanding of world
        'Computer Science',     // 4 - Modern essential skill
        'Social Sciences',      // 5 - Human understanding
        'Humanities',          // 6 - Cultural knowledge
        'Applied Sciences'      // 7 - Specialized applications
    ],
    
    // Mathematics (elementary to advanced)
    'Mathematics': [
        'Early Math Concepts',      // 1 - Preschool/Kindergarten
        'Arithmetic Foundations',   // 2 - Elementary
        'Elementary Algebra',       // 3 - Middle school
        'Geometry',                // 4 - Middle/High school
        'Algebra',                 // 5 - High school (includes advanced algebra)
        'Statistics and Probability', // 6 - High school/College
        'Calculus',                // 7 - Advanced high school/College
        'Linear Algebra',          // 8 - College
        'Discrete Mathematics',    // 9 - College
        'Applied Mathematics'      // 10 - College/Graduate
    ],
    
    // Languages (commonness/practical utility)
    'Languages': [
        'Spanish',              // 1 - Most common second language
        'French',               // 2 - Widely taught romance language
        'German',               // 3 - Common in academics/business
        'Italian',              // 4 - Popular romance language
        'Portuguese',           // 5 - Growing importance
        'Mandarin Chinese',     // 6 - Most speakers globally
        'Japanese',             // 7 - Popular/cultural interest
        'Korean',               // 8 - Growing cultural interest
        'Arabic',               // 9 - Important but more specialized
        'Russian',              // 10 - Specialized
        'Latin',                // 11 - Academic/historical
        'Ancient Greek'         // 12 - Most specialized
    ],
    
    // Computer Science (foundational to advanced)
    'Computer Science': [
        'Programming Fundamentals',     // 1 - Must learn first
        'Object-Oriented Programming', // 2 - Core programming concept
        'Data Structures',             // 3 - Essential CS knowledge
        'Algorithms',                  // 4 - Core CS theory
        'Databases',                   // 5 - Practical necessity
        'Web Development',             // 6 - High demand skill
        'Machine Learning'             // 7 - Advanced/specialized
    ],
    
    // Creative Skills (accessibility to complexity)
    'Creative Skills': [
        'Visual Arts & Design',          // 1 - Most accessible entry point
        'Writing & Literature',          // 2 - Essential communication skill
        'Performing Arts',               // 3 - Physical/performance skills
        'Media & Film Arts',             // 4 - Technical creativity
        'Crafts & Applied Arts',         // 5 - Hands-on making
        'Design Thinking & Innovation'   // 6 - Abstract/advanced methodology
    ],
    
    // Professional Skills (foundational to advanced)
    'Professional Skills': [
        'Communication & Interpersonal Skills',  // 1 - Essential for all work
        'Digital & Technology Skills',           // 2 - Modern workplace necessity
        'Project Management & Operations',       // 3 - Core business skill
        'Sales & Marketing',                     // 4 - Business development
        'Finance & Accounting',                  // 5 - Financial literacy
        'Human Resources & People Management',   // 6 - People leadership
        'Business Strategy & Analysis',          // 7 - Strategic thinking
        'Leadership & Management'                // 8 - Executive level
    ]
};

// Specific sub-category orderings for complex areas
const subCategoryOrders = {
    // Algebra subcategories (elementary to advanced)
    'Algebra': [
        'Elementary Algebra',    // 1 - Basic algebra
        'Linear Algebra',        // 2 - Matrix operations
        'Abstract Algebra',      // 3 - Advanced mathematical structures
        'Boolean Algebra'        // 4 - Logic/computer science
    ],
    
    // Visual Arts subcategories (accessible to specialized)
    'Visual Arts & Design': [
        'Fine Arts',            // 1 - Traditional foundation
        'Graphic Design',       // 2 - Practical application
        'Digital Art',          // 3 - Modern tools
        'UI/UX Design'         // 4 - Specialized field
    ],
    
    // Writing subcategories (basic to specialized)
    'Writing & Literature': [
        'Creative Writing',         // 1 - Personal expression
        'Professional Writing',     // 2 - Business application
        'Storytelling Techniques'   // 3 - Advanced craft
    ]
};

async function reorderByDifficulty() {
    try {
        console.log('Starting reordering by difficulty/commonness...\n');
        
        // Process each category in our ordering framework
        for (const [parentName, orderedChildren] of Object.entries(orderedCategories)) {
            await updateCategoryOrder(parentName, orderedChildren);
        }
        
        // Process specific subcategory orders
        for (const [parentName, orderedChildren] of Object.entries(subCategoryOrders)) {
            await updateCategoryOrder(parentName, orderedChildren);
        }
        
        console.log('🎉 Reordering complete!');
        
    } catch (error) {
        console.error('Unexpected error:', error);
    }
}

async function updateCategoryOrder(parentName, orderedChildren) {
    try {
        console.log(`\n=== Updating ${parentName} ===`);
        
        // Find the parent node
        const { data: parentNode, error: parentError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .eq('name', parentName)
            .single();
            
        if (parentError) {
            console.log(`Parent ${parentName} not found, skipping...`);
            return;
        }
        
        console.log(`Found parent: ${parentNode.name} (${parentNode.id})`);
        
        // Get all children of this parent
        const { data: children, error: childrenError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, display_order')
            .eq('parent_id', parentNode.id);
            
        if (childrenError) {
            console.error(`Error getting children of ${parentName}:`, childrenError);
            return;
        }
        
        console.log(`Found ${children.length} children`);
        
        // Update display_order for each child according to our ordering
        let updateCount = 0;
        for (let i = 0; i < orderedChildren.length; i++) {
            const childName = orderedChildren[i];
            const child = children.find(c => c.name === childName);
            
            if (child) {
                const newDisplayOrder = i + 1; // 1-based ordering
                
                if (child.display_order !== newDisplayOrder) {
                    const { error: updateError } = await supabase
                        .from('skill_tree_nodes')
                        .update({ 
                            display_order: newDisplayOrder,
                            updated_at: new Date().toISOString()
                        })
                        .eq('id', child.id);
                        
                    if (updateError) {
                        console.error(`Error updating ${childName}:`, updateError);
                    } else {
                        console.log(`  ✅ ${childName}: display_order ${child.display_order} → ${newDisplayOrder}`);
                        updateCount++;
                    }
                } else {
                    console.log(`  ⏸️  ${childName}: already has correct order ${newDisplayOrder}`);
                }
            } else {
                console.log(`  ⚠️  ${childName}: not found in children`);
            }
        }
        
        // List any children not in our ordering (will remain at display_order 0)
        const unorderedChildren = children.filter(c => !orderedChildren.includes(c.name));
        if (unorderedChildren.length > 0) {
            console.log(`  📝 Unordered children (will remain at display_order 0):`);
            unorderedChildren.forEach(c => {
                console.log(`    - ${c.name}`);
            });
        }
        
        console.log(`Updated ${updateCount} children for ${parentName}`);
        
    } catch (error) {
        console.error(`Error updating ${parentName}:`, error);
    }
}

// Run the reordering
reorderByDifficulty();
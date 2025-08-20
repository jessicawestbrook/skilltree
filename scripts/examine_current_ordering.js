require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function examineCurrentOrdering() {
    try {
        console.log('Examining current skill tree ordering...\n');
        
        // Get Academic Disciplines as the root
        const { data: academicDisciplines, error: academicError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .eq('name', 'Academic Disciplines')
            .single();
            
        if (academicError) {
            console.error('Error finding Academic Disciplines:', academicError);
            return;
        }
        
        // Get top-level categories
        const { data: topCategories, error: topError } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .eq('parent_id', academicDisciplines.id)
            .order('display_order')
            .order('name');
            
        if (topError) {
            console.error('Error getting top categories:', topError);
            return;
        }
        
        console.log('=== TOP-LEVEL ACADEMIC DISCIPLINES ===');
        topCategories.forEach((cat, i) => {
            console.log(`${i+1}. ${cat.name} (display_order: ${cat.display_order}, learning_area: ${cat.learning_area})`);
        });
        
        // Examine some key subcategories for examples
        console.log('\n=== SAMPLE SUBCATEGORY ORDERINGS ===');
        
        // Mathematics subcategories
        const mathNode = topCategories.find(c => c.name === 'Mathematics');
        if (mathNode) {
            const { data: mathChildren, error: mathError } = await supabase
                .from('skill_tree_nodes')
                .select('*')
                .eq('parent_id', mathNode.id)
                .order('display_order')
                .order('name');
                
            if (!mathError) {
                console.log('\nMathematics subcategories:');
                mathChildren.forEach((child, i) => {
                    console.log(`  ${i+1}. ${child.name} (display_order: ${child.display_order})`);
                });
            }
        }
        
        // Languages subcategories  
        const langNode = topCategories.find(c => c.name === 'Languages');
        if (langNode) {
            const { data: langChildren, error: langError } = await supabase
                .from('skill_tree_nodes')
                .select('*')
                .eq('parent_id', langNode.id)
                .order('display_order')
                .order('name');
                
            if (!langError) {
                console.log('\nLanguages subcategories:');
                langChildren.forEach((child, i) => {
                    console.log(`  ${i+1}. ${child.name} (display_order: ${child.display_order})`);
                });
            }
        }
        
        // Computer Science subcategories
        const csNode = topCategories.find(c => c.name === 'Computer Science');
        if (csNode) {
            const { data: csChildren, error: csError } = await supabase
                .from('skill_tree_nodes')
                .select('*')
                .eq('parent_id', csNode.id)
                .order('display_order')
                .order('name');
                
            if (!csError) {
                console.log('\nComputer Science subcategories:');
                csChildren.forEach((child, i) => {
                    console.log(`  ${i+1}. ${child.name} (display_order: ${child.display_order})`);
                });
            }
        }
        
        // Let's also look at some specific examples like Algebra
        console.log('\n=== SAMPLE SKILL ORDERINGS ===');
        
        // Find Algebra category and its children
        const { data: algebraNodes, error: algebraError } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .ilike('name', '%algebra%')
            .order('name');
            
        if (!algebraError && algebraNodes.length > 0) {
            console.log('\nAlgebra-related nodes:');
            algebraNodes.forEach(node => {
                console.log(`  - ${node.name} (type: ${node.type}, display_order: ${node.display_order})`);
            });
        }
        
    } catch (error) {
        console.error('Unexpected error:', error);
    }
}

examineCurrentOrdering();
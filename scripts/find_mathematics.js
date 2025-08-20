require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function findMathematics() {
    try {
        console.log('🔍 Looking for Mathematics in the hierarchy...\n');
        
        // Search for Mathematics
        const { data: mathNodes, error: mathError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, parent_id, learning_area, path')
            .ilike('name', '%mathemat%');
            
        if (mathError) throw mathError;
        
        console.log(`Found ${mathNodes.length} nodes with "mathemat" in the name:`);
        mathNodes.forEach(node => {
            console.log(`  - ${node.name} (${node.type}) - Parent: ${node.parent_id ? 'has parent' : 'root'} - Area: ${node.learning_area}`);
        });
        
        // Check what's under Formal Sciences
        const { data: formalSciencesNode, error: formalError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .eq('name', 'Formal Sciences')
            .is('parent_id', null)
            .single();
            
        if (formalError) throw formalError;
        
        const { data: formalChildren, error: childrenError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type')
            .eq('parent_id', formalSciencesNode.id)
            .order('name');
            
        if (childrenError) throw childrenError;
        
        console.log(`\nFormal Sciences children (${formalChildren.length}):`);
        formalChildren.forEach(child => {
            console.log(`  - ${child.name} (${child.type})`);
        });
        
        // Check for missing top-level categories that should exist
        const expectedTopLevel = [
            'Mathematics', 'Languages', 'Computer Science', 'Natural Sciences',
            'Social Sciences', 'Humanities', 'Applied Sciences', 'Creative Skills',
            'Professional Skills', 'Technical Skills', 'Life Skills', 
            'Test Preparation and Assessment'
        ];
        
        console.log('\n=== Checking for expected top-level categories ===');
        for (const expectedName of expectedTopLevel) {
            const { data: found, error } = await supabase
                .from('skill_tree_nodes')
                .select('name, parent_id, learning_area')
                .eq('name', expectedName)
                .eq('type', 'category');
                
            if (error) throw error;
            
            if (found.length === 0) {
                console.log(`❌ Missing: ${expectedName}`);
            } else {
                const node = found[0];
                const isTopLevel = node.parent_id === null;
                console.log(`${isTopLevel ? '✅' : '⚠️'} ${expectedName} - ${isTopLevel ? 'Top-level' : 'Under parent'} (area: ${node.learning_area})`);
            }
        }
        
    } catch (error) {
        console.error('Error finding mathematics:', error);
    }
}

findMathematics();
require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function examineProfessionalSkills() {
    try {
        console.log('Examining Professional Skills structure...\n');
        
        // Find Professional Skills node
        const { data: professionalSkillsNode, error: findError } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .eq('name', 'Professional Skills')
            .single();
            
        if (findError) {
            console.error('Error finding Professional Skills node:', findError);
            return;
        }
        
        console.log('Professional Skills root node:', {
            id: professionalSkillsNode.id,
            name: professionalSkillsNode.name,
            learning_area: professionalSkillsNode.learning_area,
            parent_id: professionalSkillsNode.parent_id
        });
        
        // Get all descendants recursively
        await getDescendants(professionalSkillsNode.id, '', 0);
        
    } catch (error) {
        console.error('Unexpected error:', error);
    }
}

async function getDescendants(parentId, parentName, depth) {
    try {
        const { data: children, error } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, learning_area, has_learning_content, is_menu_leaf')
            .eq('parent_id', parentId)
            .order('display_order', { ascending: true })
            .order('name', { ascending: true });
            
        if (error) {
            console.error(`Error getting children of ${parentName}:`, error);
            return;
        }
        
        if (children && children.length > 0) {
            const indent = '  '.repeat(depth + 1);
            console.log(`\n${indent}Children of ${parentName || 'Professional Skills'}:`);
            
            for (const child of children) {
                const hasContent = child.has_learning_content ? '📚' : '';
                const isLeaf = child.is_menu_leaf ? '🍃' : '';
                console.log(`${indent}- ${child.name} (${child.type}) ${hasContent}${isLeaf}`);
                
                // Recursively get this child's descendants
                await getDescendants(child.id, child.name, depth + 1);
            }
        } else {
            const indent = '  '.repeat(depth + 1);
            console.log(`${indent}(No children found for ${parentName})`);
        }
    } catch (error) {
        console.error(`Error in getDescendants for ${parentName}:`, error);
    }
}

examineProfessionalSkills();
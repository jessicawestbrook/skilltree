require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseServiceKey) {
    console.error('Missing environment variables. Make sure REACT_APP_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are set.');
    process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function moveCSAndMathToAcademicDisciplines() {
    try {
        console.log('Starting reorganization to move Computer Science and Mathematics to Academic Disciplines...');
        
        // Get the Academic Disciplines node ID
        const { data: academicDisciplinesNode, error: academicError } = await supabase
            .from('skill_tree_nodes')
            .select('id')
            .eq('name', 'Academic Disciplines')
            .single();
            
        if (academicError) {
            console.error('Error finding Academic Disciplines node:', academicError);
            return;
        }
        
        console.log('Academic Disciplines node ID:', academicDisciplinesNode.id);
        
        // Get Computer Science node
        const { data: csNode, error: csError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id')
            .eq('name', 'Computer Science')
            .single();
            
        if (csError) {
            console.error('Error finding Computer Science node:', csError);
            return;
        }
        
        // Get Mathematics node
        const { data: mathNode, error: mathError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id')
            .eq('name', 'Mathematics')
            .single();
            
        if (mathError) {
            console.error('Error finding Mathematics node:', mathError);
            return;
        }
        
        console.log('Found Computer Science node:', csNode);
        console.log('Found Mathematics node:', mathNode);
        
        // Update Computer Science to be a child of Academic Disciplines
        const { error: updateCSError } = await supabase
            .from('skill_tree_nodes')
            .update({ 
                parent_id: academicDisciplinesNode.id,
                learning_area: 'Computer Science',
                updated_at: new Date().toISOString()
            })
            .eq('id', csNode.id);
            
        if (updateCSError) {
            console.error('Error updating Computer Science node:', updateCSError);
            return;
        }
        
        // Update Mathematics to be a child of Academic Disciplines
        const { error: updateMathError } = await supabase
            .from('skill_tree_nodes')
            .update({ 
                parent_id: academicDisciplinesNode.id,
                learning_area: 'Mathematics', 
                updated_at: new Date().toISOString()
            })
            .eq('id', mathNode.id);
            
        if (updateMathError) {
            console.error('Error updating Mathematics node:', updateMathError);
            return;
        }
        
        console.log('✅ Successfully moved Computer Science to Academic Disciplines');
        console.log('✅ Successfully moved Mathematics to Academic Disciplines');
        
        // Update all Computer Science descendants to have Computer Science learning area
        await updateDescendantsRecursively(csNode.id, 'Computer Science');
        
        // Update all Mathematics descendants to have Mathematics learning area
        await updateDescendantsRecursively(mathNode.id, 'Mathematics');
        
        console.log('🎉 Reorganization complete! Computer Science and Mathematics are now direct children of Academic Disciplines.');
        
    } catch (error) {
        console.error('Unexpected error:', error);
    }
}

async function updateDescendantsRecursively(parentId, learningArea) {
    try {
        // Get all children of this parent
        const { data: children, error } = await supabase
            .from('skill_tree_nodes')
            .select('id')
            .eq('parent_id', parentId);
            
        if (error) {
            console.error(`Error getting children of ${parentId}:`, error);
            return;
        }
        
        if (children && children.length > 0) {
            // Update all children to have the correct learning area
            const { error: updateError } = await supabase
                .from('skill_tree_nodes')
                .update({ 
                    learning_area: learningArea,
                    updated_at: new Date().toISOString()
                })
                .in('id', children.map(child => child.id));
                
            if (updateError) {
                console.error(`Error updating descendants of ${parentId}:`, updateError);
            } else {
                console.log(`✅ Updated ${children.length} descendants of ${parentId} to learning area: ${learningArea}`);
            }
            
            // Recursively update each child's descendants
            for (const child of children) {
                await updateDescendantsRecursively(child.id, learningArea);
            }
        }
        
    } catch (error) {
        console.error(`Error in recursive update for ${parentId}:`, error);
    }
}

// Run the reorganization
moveCSAndMathToAcademicDisciplines();
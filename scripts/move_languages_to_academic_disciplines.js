require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseServiceKey) {
    console.error('Missing environment variables. Make sure REACT_APP_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are set.');
    process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function moveLanguagesToAcademicDisciplines() {
    try {
        console.log('Starting reorganization to move Languages to Academic Disciplines level...');
        
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
        
        // Get Languages node
        const { data: languagesNode, error: languagesError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id, learning_area')
            .eq('name', 'Languages')
            .eq('learning_area', 'Humanities')
            .single();
            
        if (languagesError) {
            console.error('Error finding Languages node:', languagesError);
            return;
        }
        
        console.log('Found Languages node:', languagesNode);
        
        // Update Languages to be a child of Academic Disciplines and update learning area
        const { error: updateError } = await supabase
            .from('skill_tree_nodes')
            .update({ 
                parent_id: academicDisciplinesNode.id,
                learning_area: 'Languages',
                updated_at: new Date().toISOString()
            })
            .eq('id', languagesNode.id);
            
        if (updateError) {
            console.error('Error updating Languages node:', updateError);
            return;
        }
        
        console.log('✅ Successfully moved Languages to Academic Disciplines level');
        
        // Update all Languages descendants to have Languages learning area
        await updateDescendantsRecursively(languagesNode.id, 'Languages');
        
        console.log('🎉 Reorganization complete! Languages is now at the same level as Humanities.');
        
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
moveLanguagesToAcademicDisciplines();
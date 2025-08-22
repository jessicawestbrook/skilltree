require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function findTopLevelCategories() {
    try {
        console.log('🔍 FINDING TOP LEVEL CATEGORIES AND PHYSICS\n');
        
        // Get all nodes first and filter
        const { data: allNodes, error: allError } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .order('path');
            
        if (allError) {
            console.error('Error fetching all nodes:', allError);
            return;
        }
        
        // Find nodes with no path or empty path (Level 0/1)
        const level1Nodes = allNodes.filter(node => 
            !node.path || node.path === null || (Array.isArray(node.path) && node.path.length === 0)
        );
            
        
        console.log(`Found ${level1Nodes.length} Level 1 (top-level) nodes:\n`);
        level1Nodes.forEach(node => {
            const hasDesc = node.description && node.description.trim() !== '';
            console.log(`${node.name}`);
            console.log(`  ID: ${node.id}`);
            console.log(`  Path: ${node.path ? JSON.stringify(node.path) : 'null/empty'}`);
            console.log(`  Parent ID: ${node.parent_id || 'None'}`);
            console.log(`  Has Description: ${hasDesc ? 'YES' : 'NO'}`);
            console.log('');
        });
        
        // Now check all nodes that have path length of 1
        
        const pathLength1Nodes = allNodes.filter(node => 
            node.path && Array.isArray(node.path) && node.path.length === 1
        );
        
        console.log(`Found ${pathLength1Nodes.length} nodes with path length 1:\n`);
        pathLength1Nodes.forEach(node => {
            const hasDesc = node.description && node.description.trim() !== '';
            console.log(`${node.name}`);
            console.log(`  Path: ${node.path.join(' > ')}`);
            console.log(`  Parent ID: ${node.parent_id || 'None'}`);
            console.log(`  Has Description: ${hasDesc ? 'YES' : 'NO'}`);
            console.log('');
        });
        
        // Check specifically for nodes containing "science"
        const scienceNodes = allNodes.filter(node => 
            node.name.toLowerCase().includes('science')
        );
        
        console.log(`\nNodes containing "science":\n`);
        scienceNodes.forEach(node => {
            const level = node.path ? node.path.length : 'no path';
            const hasDesc = node.description && node.description.trim() !== '';
            console.log(`${node.name} (Level ${level})`);
            console.log(`  Path: ${node.path ? node.path.join(' > ') : 'No path'}`);
            console.log(`  Has Description: ${hasDesc ? 'YES' : 'NO'}`);
            console.log('');
        });
        
    } catch (error) {
        console.error('Error in analysis:', error);
    }
}

findTopLevelCategories();
require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function checkPhysicsDescription() {
    try {
        console.log('🔍 CHECKING PHYSICS DESCRIPTION\n');
        
        // Search for Physics nodes
        const { data: physicsNodes, error } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .ilike('name', '%physics%')
            .order('path');
            
        if (error) {
            console.error('Error fetching physics nodes:', error);
            return;
        }
        
        console.log(`Found ${physicsNodes.length} nodes containing "physics":\n`);
        
        for (const node of physicsNodes) {
            const level = node.path ? node.path.length : 'unknown';
            const hasDesc = node.description && node.description.trim() !== '';
            
            console.log(`${node.name}`);
            console.log(`  ID: ${node.id}`);
            console.log(`  Level: ${level}`);
            console.log(`  Path: ${node.path ? node.path.join(' > ') : 'No path'}`);
            console.log(`  Has Description: ${hasDesc ? 'YES' : 'NO'}`);
            if (hasDesc) {
                console.log(`  Description: "${node.description}"`);
            }
            console.log('');
        }
        
        // Also check level 2 science nodes
        console.log('🔬 CHECKING ALL LEVEL 2 SCIENCE NODES:\n');
        
        const { data: scienceNodes, error: scienceError } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .order('path');
            
        if (scienceError) {
            console.error('Error fetching science nodes:', scienceError);
            return;
        }
        
        const level2ScienceNodes = scienceNodes.filter(node => {
            if (!node.path || !Array.isArray(node.path) || node.path.length !== 2) return false;
            const pathStr = node.path.join(' > ').toLowerCase();
            return pathStr.includes('science');
        });
        
        console.log(`Found ${level2ScienceNodes.length} Level 2 science-related nodes:\n`);
        
        for (const node of level2ScienceNodes) {
            const hasDesc = node.description && node.description.trim() !== '';
            console.log(`${node.name}`);
            console.log(`  Path: ${node.path.join(' > ')}`);
            console.log(`  Has Description: ${hasDesc ? 'YES' : 'NO'}`);
            if (hasDesc) {
                console.log(`  Description: "${node.description.substring(0, 100)}..."`);
            }
            console.log('');
        }
        
    } catch (error) {
        console.error('Error in analysis:', error);
    }
}

checkPhysicsDescription();
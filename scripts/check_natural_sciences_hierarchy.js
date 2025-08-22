require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function checkNaturalSciencesHierarchy() {
    try {
        console.log('🔬 CHECKING NATURAL SCIENCES HIERARCHY\n');
        
        // Get all nodes related to Natural Sciences
        const { data: nodes, error } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .order('path');
            
        if (error) {
            console.error('Error fetching nodes:', error);
            return;
        }
        
        // Filter for Natural Sciences hierarchy
        const naturalScienceNodes = nodes.filter(node => {
            if (!node.path || !Array.isArray(node.path)) return false;
            const pathStr = node.path.join(' > ').toLowerCase();
            return pathStr.includes('natural sciences') || 
                   (node.path.length === 1 && node.name.toLowerCase() === 'natural sciences') ||
                   (node.path.length === 1 && node.name.toLowerCase() === 'physics');
        });
        
        console.log('Natural Sciences Hierarchy:');
        console.log('=========================\n');
        
        // Group by level
        const byLevel = {};
        for (const node of naturalScienceNodes) {
            const level = node.path ? node.path.length : 0;
            if (!byLevel[level]) byLevel[level] = [];
            byLevel[level].push(node);
        }
        
        // Display by level
        for (const level of [0, 1, 2, 3, 4].filter(l => byLevel[l])) {
            console.log(`LEVEL ${level}:`);
            for (const node of byLevel[level]) {
                const hasDesc = node.description && node.description.trim() !== '';
                console.log(`  ${node.name}`);
                console.log(`    ID: ${node.id}`);
                console.log(`    Path: ${node.path ? node.path.join(' > ') : 'No path'}`);
                console.log(`    Has Description: ${hasDesc ? 'YES' : 'NO'}`);
                console.log('');
            }
        }
        
        // Check specifically for Physics
        const physicsNode = nodes.find(node => node.name === 'Physics');
        if (physicsNode) {
            console.log('🎯 PHYSICS NODE DETAILS:');
            console.log('========================');
            console.log(`Name: ${physicsNode.name}`);
            console.log(`ID: ${physicsNode.id}`);
            console.log(`Path: ${physicsNode.path ? physicsNode.path.join(' > ') : 'No path'}`);
            console.log(`Level: ${physicsNode.path ? physicsNode.path.length : 'No path'}`);
            console.log(`Parent ID: ${physicsNode.parent_id || 'None'}`);
            console.log(`Has Description: ${physicsNode.description ? 'YES' : 'NO'}`);
            
            // Find parent
            if (physicsNode.parent_id) {
                const parent = nodes.find(node => node.id === physicsNode.parent_id);
                if (parent) {
                    console.log(`Parent Name: ${parent.name}`);
                    console.log(`Parent Path: ${parent.path ? parent.path.join(' > ') : 'No path'}`);
                } else {
                    console.log('Parent not found!');
                }
            }
        }
        
    } catch (error) {
        console.error('Error in analysis:', error);
    }
}

checkNaturalSciencesHierarchy();
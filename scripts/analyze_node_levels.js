require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function analyzeNodeLevels() {
    try {
        console.log('🔍 ANALYZING SKILL TREE NODE LEVELS\n');
        
        const { data: allNodes, error } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, path, parent_id, description')
            .order('path');
        
        if (error) {
            console.error('❌ Error fetching nodes:', error);
            return;
        }
        
        // Categorize nodes by level
        const levels = {
            1: [], 2: [], 3: [], 4: [], 5: [], 6: []
        };
        
        allNodes.forEach(node => {
            if (node.path && Array.isArray(node.path)) {
                const level = node.path.length;
                if (level >= 1 && level <= 5) {
                    levels[level].push(node);
                } else if (level >= 6) {
                    levels[6].push(node);
                }
            }
        });
        
        console.log('NODE LEVEL BREAKDOWN:');
        console.log('====================');
        console.log(`Level 1: ${levels[1].length} nodes`);
        console.log(`Level 2: ${levels[2].length} nodes`);
        console.log(`Level 3: ${levels[3].length} nodes`);
        console.log(`Level 4: ${levels[4].length} nodes`);
        console.log(`Level 5: ${levels[5].length} nodes`);
        console.log(`Level 6+: ${levels[6].length} nodes`);
        
        // Focus on levels 2 and 3
        const level2 = levels[2];
        const level3 = levels[3];
        
        const level2WithoutDesc = level2.filter(n => !n.description || n.description.trim() === '');
        const level3WithoutDesc = level3.filter(n => !n.description || n.description.trim() === '');
        
        console.log('\n🎯 TARGET: LEVELS 2 & 3 (Main Categories & Subcategories)');
        console.log('==========================================================');
        console.log(`Level 2 - Total: ${level2.length} | Without descriptions: ${level2WithoutDesc.length}`);
        console.log(`Level 3 - Total: ${level3.length} | Without descriptions: ${level3WithoutDesc.length}`);
        
        const totalToProcess = level2WithoutDesc.length + level3WithoutDesc.length;
        console.log(`\n📊 TOTAL NODES TO PROCESS: ${totalToProcess}`);
        
        // Calculate estimates
        const timePerNode = 30; // seconds
        const totalTimeMinutes = (totalToProcess * timePerNode) / 60;
        const costPerNode = 0.02; // dollars
        const totalCost = totalToProcess * costPerNode;
        
        console.log('\n💰 GENERATION ESTIMATES:');
        console.log('========================');
        console.log(`⏱️  Time: ${Math.round(totalTimeMinutes)} minutes (${(totalTimeMinutes/60).toFixed(1)} hours)`);
        console.log(`💵 Cost: $${totalCost.toFixed(2)}`);
        
        // Show examples
        console.log('\n📋 LEVEL 2 EXAMPLES (Main Categories):');
        level2.slice(0, 8).forEach((node, i) => {
            const hasDesc = node.description ? '✅' : '❌';
            console.log(`   ${i+1}. ${node.name} ${hasDesc}`);
            console.log(`      Path: ${JSON.stringify(node.path)}`);
        });
        
        console.log('\n📋 LEVEL 3 EXAMPLES (Subcategories):');
        level3.slice(0, 8).forEach((node, i) => {
            const hasDesc = node.description ? '✅' : '❌';
            console.log(`   ${i+1}. ${node.name} ${hasDesc}`);
            console.log(`      Path: ${JSON.stringify(node.path)}`);
        });
        
        console.log(`\n✨ Ready to proceed with batch generation for ${totalToProcess} nodes!`);
        
    } catch (error) {
        console.error('❌ Error analyzing nodes:', error);
    }
}

analyzeNodeLevels();
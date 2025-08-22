require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function checkMissingDescriptions() {
    try {
        console.log('🔍 CHECKING FOR MISSING DESCRIPTIONS\n');
        
        // Get all level 2 and 3 nodes
        const { data: nodes, error } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, path, description')
            .order('path');
            
        if (error) {
            console.error('Error fetching nodes:', error);
            return;
        }
        
        const level2Missing = [];
        const level3Missing = [];
        const level2WithDesc = [];
        const level3WithDesc = [];
        
        for (const node of nodes) {
            if (node.path && Array.isArray(node.path)) {
                const level = node.path.length;
                
                if (level === 2) {
                    if (!node.description || node.description.trim() === '') {
                        level2Missing.push(node);
                    } else {
                        level2WithDesc.push(node);
                    }
                } else if (level === 3) {
                    if (!node.description || node.description.trim() === '') {
                        level3Missing.push(node);
                    } else {
                        level3WithDesc.push(node);
                    }
                }
            }
        }
        
        console.log('📊 DESCRIPTION STATUS SUMMARY');
        console.log('=============================');
        console.log(`Level 2 categories: ${level2WithDesc.length} with descriptions, ${level2Missing.length} missing`);
        console.log(`Level 3 categories: ${level3WithDesc.length} with descriptions, ${level3Missing.length} missing`);
        console.log(`Total missing: ${level2Missing.length + level3Missing.length}`);
        
        if (level2Missing.length > 0) {
            console.log('\n📝 LEVEL 2 MISSING DESCRIPTIONS:');
            level2Missing.forEach((node, i) => {
                console.log(`${i + 1}. ${node.name} (${node.path?.join(' > ')})`);
            });
        }
        
        if (level3Missing.length > 0) {
            console.log('\n📝 LEVEL 3 MISSING DESCRIPTIONS:');
            level3Missing.forEach((node, i) => {
                console.log(`${i + 1}. ${node.name} (${node.path?.join(' > ')})`);
            });
        }
        
        // Show a few examples of existing descriptions
        if (level2WithDesc.length > 0) {
            console.log('\n✅ EXAMPLE EXISTING LEVEL 2 DESCRIPTIONS:');
            level2WithDesc.slice(0, 3).forEach(node => {
                console.log(`• ${node.name}: "${node.description}"`);
            });
        }
        
        if (level3WithDesc.length > 0) {
            console.log('\n✅ EXAMPLE EXISTING LEVEL 3 DESCRIPTIONS:');
            level3WithDesc.slice(0, 3).forEach(node => {
                console.log(`• ${node.name}: "${node.description}"`);
            });
        }
        
        console.log('\n🎯 NEXT STEPS:');
        console.log('1. Run the enhanced content generator to fill missing descriptions');
        console.log('2. Review generated descriptions for quality and accuracy');
        console.log('3. Update any that need refinement');
        
    } catch (error) {
        console.error('Error in analysis:', error);
    }
}

checkMissingDescriptions();
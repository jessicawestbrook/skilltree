require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function analyzeCurrentDescriptions() {
    try {
        console.log('🔍 ANALYZING CURRENT DESCRIPTIONS FOR PROBLEMS\n');
        
        // Get all level 2 and 3 nodes with descriptions
        const { data: nodes, error } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, path, description')
            .not('description', 'is', null)
            .order('path');
            
        if (error) {
            console.error('Error fetching nodes:', error);
            return;
        }
        
        const level2Nodes = nodes.filter(node => node.path && Array.isArray(node.path) && node.path.length === 2);
        const level3Nodes = nodes.filter(node => node.path && Array.isArray(node.path) && node.path.length === 3);
        
        console.log(`📊 Found ${level2Nodes.length} Level 2 and ${level3Nodes.length} Level 3 nodes with descriptions\n`);
        
        // Problematic phrases to look for
        const problematicPhrases = [
            'hands-on',
            'real-world applications',
            'practical experience',
            'become a professional',
            'career preparation',
            'master',
            'expertise',
            'field work',
            'lab work',
            'laboratory',
            'industry experience',
            'professional practice',
            'gain experience',
            'hands-on experience'
        ];
        
        let problemCount = 0;
        const problemDescriptions = [];
        
        console.log('🔍 CHECKING FOR PROBLEMATIC PHRASES...\n');
        
        for (const node of [...level2Nodes, ...level3Nodes]) {
            if (!node.description) continue;
            
            const description = node.description.toLowerCase();
            const foundProblems = [];
            
            for (const phrase of problematicPhrases) {
                if (description.includes(phrase.toLowerCase())) {
                    foundProblems.push(phrase);
                }
            }
            
            if (foundProblems.length > 0) {
                problemCount++;
                problemDescriptions.push({
                    name: node.name,
                    path: node.path?.join(' > '),
                    level: node.path?.length,
                    problems: foundProblems,
                    description: node.description
                });
            }
        }
        
        console.log(`⚠️  FOUND ${problemCount} DESCRIPTIONS WITH PROBLEMATIC PHRASES:\n`);
        
        // Show first 10 problematic descriptions
        problemDescriptions.slice(0, 10).forEach((item, i) => {
            console.log(`${i + 1}. ${item.name} (Level ${item.level})`);
            console.log(`   Path: ${item.path}`);
            console.log(`   Problems: ${item.problems.join(', ')}`);
            console.log(`   Description: "${item.description}"`);
            console.log('');
        });
        
        if (problemDescriptions.length > 10) {
            console.log(`... and ${problemDescriptions.length - 10} more\n`);
        }
        
        // Show some good examples (descriptions without problems)
        const goodDescriptions = [...level2Nodes, ...level3Nodes].filter(node => {
            if (!node.description) return false;
            const description = node.description.toLowerCase();
            return !problematicPhrases.some(phrase => description.includes(phrase.toLowerCase()));
        });
        
        if (goodDescriptions.length > 0) {
            console.log(`✅ FOUND ${goodDescriptions.length} DESCRIPTIONS WITHOUT PROBLEMS:\n`);
            goodDescriptions.slice(0, 3).forEach((node, i) => {
                console.log(`${i + 1}. ${node.name}`);
                console.log(`   Description: "${node.description}"`);
                console.log('');
            });
        }
        
        console.log('📋 SUMMARY:');
        console.log(`   Total descriptions analyzed: ${level2Nodes.length + level3Nodes.length}`);
        console.log(`   Descriptions with problems: ${problemCount}`);
        console.log(`   Descriptions without problems: ${goodDescriptions.length}`);
        console.log(`   Percentage needing improvement: ${Math.round(problemCount / (level2Nodes.length + level3Nodes.length) * 100)}%`);
        
    } catch (error) {
        console.error('Error in analysis:', error);
    }
}

analyzeCurrentDescriptions();
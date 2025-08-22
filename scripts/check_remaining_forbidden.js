const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

async function checkRemainingForbidden() {
    const supabase = createClient(
        process.env.REACT_APP_SUPABASE_URL,
        process.env.SUPABASE_SERVICE_ROLE_KEY
    );

    const forbiddenPhrases = [
        'dive into', 'delve into', 'discover', 'uncover', 'unlock',
        'unleash', 'embark', 'explore', 'captivating', 'fascinating',
        'dynamic world', 'art of', 'secrets of', 'intricate world',
        'vibrant world', 'rich tapestry', 'intriguing world', 'hands-on',
        'hands on', 'become a professional', 'become an expert', 'master the art',
        'become a master', 'professional level', 'expert level',
        'industry professional', 'career as a', 'launch your career',
        'become proficient', 'immerse yourself', 'witness', 'dynamic'
    ];

    try {
        const { data: nodes, error } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, description')
            .not('description', 'is', null)
            .neq('description', '')
            .limit(1000);
        
        if (error) throw error;
        
        const problematic = nodes.filter(node => {
            if (!node.description) return false;
            const descLower = node.description.toLowerCase();
            return forbiddenPhrases.some(phrase => descLower.includes(phrase));
        });
        
        console.log(`Found ${problematic.length} nodes still containing forbidden phrases`);
        
        if (problematic.length > 0) {
            console.log('\nExamples of remaining problematic descriptions:');
            problematic.slice(0, 10).forEach((node, i) => {
                console.log(`${i + 1}. ${node.name}: ${node.description.substring(0, 120)}...`);
            });
        }
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

checkRemainingForbidden();
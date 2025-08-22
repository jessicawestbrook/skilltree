require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function checkCurrentStructure() {
    try {
        console.log('🔍 CHECKING CURRENT STRUCTURE\n');
        
        // Check if we have direct SQL access via any method
        console.log('Testing SQL execution methods...\n');
        
        // Get sample data to understand structure
        const { data: sampleNodes, error: sampleError } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .limit(3);
            
        if (sampleError) {
            console.error('Error fetching sample data:', sampleError);
            return;
        }
        
        console.log('Current columns:');
        if (sampleNodes && sampleNodes.length > 0) {
            Object.keys(sampleNodes[0]).forEach(column => {
                const value = sampleNodes[0][column];
                const type = typeof value;
                console.log(`  • ${column}: ${type}`);
            });
        }
        
        // Check metadata structure for descriptions
        console.log('\n📋 Checking metadata for descriptions...');
        let metadataCount = 0;
        let descriptionCount = 0;
        
        for (const node of sampleNodes) {
            if (node.metadata) {
                metadataCount++;
                if (typeof node.metadata === 'object' && node.metadata.description) {
                    descriptionCount++;
                    console.log(`  Found description in ${node.name}: "${node.metadata.description}"`);
                }
            }
        }
        
        console.log(`\nMetadata summary: ${metadataCount} nodes have metadata, ${descriptionCount} have descriptions`);
        
        // Since we can't add columns directly, let's work with the existing structure
        console.log('\n💡 Strategy: Use metadata.description for new entries until schema can be updated');
        
        console.log('\n✅ Analysis complete - proceeding with metadata-based approach');
        
    } catch (error) {
        console.error('Error in analysis:', error);
    }
}

checkCurrentStructure();
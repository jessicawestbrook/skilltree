require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function analyzeHierarchy() {
    try {
        console.log('Analyzing current skill tree hierarchy...\n');
        
        // Level 1: Root nodes (parent_id is null)
        const { data: level1, error: level1Error } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, parent_id')
            .is('parent_id', null)
            .order('name');
            
        if (level1Error) throw level1Error;
        
        console.log('=== LEVEL 1 (ROOT NODES) ===');
        level1.forEach(node => {
            console.log(`${node.name} (${node.type}, id: ${node.id})`);
        });
        
        if (level1.length === 0) {
            console.log('No root nodes found!');
            return;
        }
        
        // Level 2: Children of root nodes
        const { data: level2, error: level2Error } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, parent_id')
            .in('parent_id', level1.map(n => n.id))
            .order('name');
            
        if (level2Error) throw level2Error;
        
        console.log('\n=== LEVEL 2 (CHILDREN OF ROOT) ===');
        level2.forEach(node => {
            const parent = level1.find(p => p.id === node.parent_id);
            console.log(`${node.name} (${node.type}, parent: ${parent?.name}, id: ${node.id})`);
        });
        
        if (level2.length === 0) {
            console.log('No level 2 nodes found!');
            return;
        }
        
        // Level 3: Third level (these will become our new top level)
        const { data: level3, error: level3Error } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, parent_id, learning_area, display_order')
            .in('parent_id', level2.map(n => n.id))
            .order('display_order')
            .order('name');
            
        if (level3Error) throw level3Error;
        
        console.log('\n=== LEVEL 3 (WILL BECOME NEW TOP LEVEL) ===');
        level3.forEach(node => {
            const parent = level2.find(p => p.id === node.parent_id);
            const grandparent = level1.find(gp => gp.id === parent?.parent_id);
            console.log(`${node.name} (${node.type}, display_order: ${node.display_order}, learning_area: ${node.learning_area})`);
            console.log(`  Current path: ${grandparent?.name} > ${parent?.name} > ${node.name}`);
        });
        
        console.log(`\nSUMMARY:`);
        console.log(`- Level 1 nodes to remove: ${level1.length}`);
        console.log(`- Level 2 nodes to remove: ${level2.length}`);
        console.log(`- Level 3 nodes to promote to top level: ${level3.length}`);
        
        // Check for any nodes that depend on level 1 or 2 nodes
        console.log('\n=== DEPENDENCY CHECK ===');
        
        // Check level 4 nodes (children of level 3)
        const { data: level4, error: level4Error } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id')
            .in('parent_id', level3.map(n => n.id));
            
        if (!level4Error) {
            console.log(`Level 4 nodes that will remain: ${level4.length}`);
        }
        
        return { level1, level2, level3 };
        
    } catch (error) {
        console.error('Error analyzing hierarchy:', error);
    }
}

analyzeHierarchy();
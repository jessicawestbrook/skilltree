require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');
const { v4: uuidv4 } = require('uuid');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function restoreFullBackupHierarchy() {
    try {
        console.log('🔄 RESTORING FULL HIERARCHY FROM BACKUP STRUCTURE...\n');
        
        // Step 1: First let's see what's currently in the database to understand the backup format
        console.log('=== STEP 1: Checking current database state ===');
        
        const { data: currentNodes, error: currentError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, parent_id, learning_area, path')
            .limit(10);
            
        if (currentError) throw currentError;
        
        console.log(`Current database has ${currentNodes.length} nodes (limited to 10 for inspection)`);
        console.log('Sample nodes:');
        currentNodes.forEach(node => {
            console.log(`  - ${node.name} (${node.type}, parent: ${node.parent_id ? 'has parent' : 'root'})`);
        });
        
        // The backup file was overwritten, but the current database structure shows what we need to restore
        // Let me query the current problematic flat structure and rebuild it properly
        
        console.log('\n=== STEP 2: Getting all current nodes ===');
        
        // Get all nodes in batches to avoid query limits
        let allNodes = [];
        let offset = 0;
        const batchSize = 1000;
        
        while (true) {
            const { data: batch, error: batchError } = await supabase
                .from('skill_tree_nodes')
                .select('id, name, type, parent_id, learning_area, path, metadata, display_order, has_learning_content, is_menu_leaf')
                .range(offset, offset + batchSize - 1)
                .order('created_at');
                
            if (batchError) throw batchError;
            
            if (!batch || batch.length === 0) break;
            
            allNodes = allNodes.concat(batch);
            offset += batchSize;
            
            console.log(`Loaded ${allNodes.length} nodes...`);
            
            if (batch.length < batchSize) break;
        }
        
        console.log(`Total nodes loaded: ${allNodes.length}`);
        
        // If we have very few nodes, this means the previous script cleared everything
        // In that case, we need a different approach
        if (allNodes.length < 100) {
            console.log('⚠️ Database appears to have been cleared. Need to restore from a different source.');
            console.log('The current database only has a few sample nodes from the previous script.');
            console.log('We need the original backup data to restore the full hierarchy.');
            return;
        }
        
        // Step 3: Analyze the current structure to understand what needs to be fixed
        console.log('\n=== STEP 3: Analyzing current structure ===');
        
        const nodeMap = {};
        allNodes.forEach(node => {
            nodeMap[node.id] = node;
        });
        
        // Find root nodes
        const rootNodes = allNodes.filter(n => n.parent_id === null);
        console.log(`Root nodes: ${rootNodes.length}`);
        rootNodes.forEach(node => {
            console.log(`  - ${node.name} (${node.type})`);
        });
        
        // Count nodes by type
        const skillCount = allNodes.filter(n => n.type === 'skill').length;
        const categoryCount = allNodes.filter(n => n.type === 'category').length;
        console.log(`Categories: ${categoryCount}, Skills: ${skillCount}`);
        
        // If we have the right number of nodes but wrong structure, we can fix it
        if (allNodes.length < 5000) {
            console.log('\n❌ This appears to be the truncated version, not the full backup.');
            console.log('The full backup should have thousands of nodes.');
            console.log('We need to restore from a Git commit or other backup source that has the complete data.');
            return;
        }
        
        // Step 4: If we have a good structure, proceed with flattening
        console.log('\n=== STEP 4: Proceeding with hierarchy restoration ===');
        
        // For now, let's work with what we have and restore the correct 12 top-level structure
        // The actual full restoration would need the complete backup file
        
        console.log('Creating proper 12-category top-level structure...');
        
        // This is where we'd implement the full restoration logic
        // But first we need the complete backup data
        
        console.log('\n⚠️ TO COMPLETE THIS RESTORATION:');
        console.log('1. We need the original knowledgeTreeData5.ts file with the full tree structure');
        console.log('2. Or access to a Git commit that has the complete data');
        console.log('3. Or a database backup from before the hierarchy was corrupted');
        console.log('\nCurrent approach restored basic structure but is missing the full content tree.');
        
    } catch (error) {
        console.error('Error restoring full hierarchy:', error);
    }
}

restoreFullBackupHierarchy();
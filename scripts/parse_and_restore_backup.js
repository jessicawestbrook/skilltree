require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');
const path = require('path');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

function parseBackupFile() {
    console.log('📖 Parsing backup file knowledgeTreeData5.ts...');
    
    const backupPath = path.join(__dirname, '../src/data/knowledgeTreeData5.ts');
    
    if (!fs.existsSync(backupPath)) {
        throw new Error('Backup file not found. Please restore the original knowledgeTreeData5.ts file.');
    }
    
    const content = fs.readFileSync(backupPath, 'utf8');
    console.log(`File content length: ${content.length} characters`);
    console.log('First 200 characters:', content.substring(0, 200));
    
    // Check if the file was truncated/emptied
    if (content.length < 1000) {
        throw new Error('Backup file appears to be truncated or empty. Please restore the original full knowledgeTreeData5.ts file with thousands of nodes.');
    }
    
    // Try to extract the data structure
    // The file should export knowledgeTreeData with a large nested structure
    
    // Method 1: Try to require it directly (if it's valid JS/TS)
    try {
        // Remove the TypeScript import and type annotation to make it valid JS
        let jsContent = content
            .replace(/import.*from.*['"];?\s*/g, '')
            .replace(/export\s+const\s+knowledgeTreeData:\s*\w+\s*=/, 'module.exports =')
            .replace(/type:\s*"(category|skill)"/g, 'type: "$1"');
            
        // Write temporary JS file
        const tempPath = path.join(__dirname, 'temp_backup.js');
        fs.writeFileSync(tempPath, jsContent);
        
        const data = require(tempPath);
        
        // Clean up temp file
        fs.unlinkSync(tempPath);
        
        return data;
        
    } catch (error) {
        console.error('Could not parse as JavaScript:', error.message);
        throw new Error('Could not parse backup file. Please ensure knowledgeTreeData5.ts contains the original full backup data.');
    }
}

function flattenHierarchy(node, currentPath = [], topLevelMap = {}) {
    const result = [];
    
    // Skip the first 2 levels: "Knowledge" and "Academic Disciplines"
    const pathDepth = currentPath.length;
    
    if (pathDepth === 0 && node.name === 'Knowledge') {
        // Skip Knowledge root, process its children
        if (node.children) {
            for (const child of node.children) {
                result.push(...flattenHierarchy(child, [...currentPath, node.name], topLevelMap));
            }
        }
        return result;
    }
    
    if (pathDepth === 1 && node.name === 'Academic Disciplines') {
        // Skip Academic Disciplines, process its children as new top-level
        if (node.children) {
            for (const child of node.children) {
                result.push(...flattenHierarchy(child, currentPath, topLevelMap)); // Don't add to path
            }
        }
        return result;
    }
    
    // For "Applied Knowledge" at depth 1, also skip and process children as top-level
    if (pathDepth === 1 && node.name === 'Applied Knowledge') {
        if (node.children) {
            for (const child of node.children) {
                result.push(...flattenHierarchy(child, currentPath, topLevelMap));
            }
        }
        return result;
    }
    
    // Now we're at the level that should become top-level or below
    let adjustedPath = [...currentPath];
    
    // If this is now a top-level node (originally under Academic Disciplines)
    if (pathDepth === 1 || (pathDepth === 2 && currentPath[1] === 'Academic Disciplines')) {
        adjustedPath = []; // Make this a root node
        
        // Special handling: Mathematics was under Natural Sciences, promote it to top-level
        if (node.name === 'Mathematics' || node.name === 'Natural Sciences') {
            adjustedPath = [];
        }
    } else if (pathDepth > 1) {
        // Remove the first 2 levels from the path
        adjustedPath = currentPath.slice(2);
    }
    
    // Create the flattened node
    const flatNode = {
        id: uuidv4(),
        name: node.name,
        type: node.type || 'category',
        parent_id: null, // Will be set when processing relationships
        learning_area: node.learning_area || (adjustedPath.length === 0 ? node.name : adjustedPath[0]),
        path: adjustedPath,
        metadata: node.metadata || {},
        display_order: node.display_order || null,
        has_learning_content: node.type === 'skill' || node.has_learning_content || false,
        is_menu_leaf: node.type === 'skill' || !node.children || node.children.length === 0,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        original_path: currentPath,
        children_data: node.children || []
    };
    
    result.push(flatNode);
    
    // If this is a top-level node, remember it
    if (adjustedPath.length === 0) {
        topLevelMap[node.name] = flatNode;
    }
    
    // Process children
    if (node.children && node.children.length > 0) {
        for (const child of node.children) {
            result.push(...flattenHierarchy(child, [...currentPath, node.name], topLevelMap));
        }
    }
    
    return result;
}

function establishRelationships(flatNodes) {
    console.log('🔗 Establishing parent-child relationships...');
    
    const nodesByName = {};
    const nodesByPath = {};
    
    // Index nodes by name and path for quick lookup
    flatNodes.forEach(node => {
        if (!nodesByName[node.name]) {
            nodesByName[node.name] = [];
        }
        nodesByName[node.name].push(node);
        
        const pathKey = node.path.join(' → ');
        if (!nodesByPath[pathKey]) {
            nodesByPath[pathKey] = [];
        }
        nodesByPath[pathKey].push(node);
    });
    
    // Set parent relationships
    let relationshipsSet = 0;
    
    flatNodes.forEach(node => {
        if (node.path.length > 0) {
            // Find parent by path
            const parentPath = node.path.slice(0, -1);
            const parentPathKey = parentPath.join(' → ');
            const parentName = node.path[node.path.length - 1];
            
            // Try to find parent by path first
            let parent = null;
            if (parentPath.length === 0) {
                // Parent is top-level, find by name
                const candidates = nodesByName[parentName] || [];
                parent = candidates.find(p => p.path.length === 0);
            } else {
                // Parent has a path
                const candidates = nodesByPath[parentPathKey] || [];
                parent = candidates.find(p => p.name === parentName);
            }
            
            if (parent) {
                node.parent_id = parent.id;
                relationshipsSet++;
            } else {
                console.warn(`Could not find parent for ${node.name} (looking for ${parentName} at path: ${parentPathKey})`);
            }
        }
    });
    
    console.log(`Set ${relationshipsSet} parent relationships`);
    return flatNodes;
}

async function insertNodes(nodes) {
    console.log(`📝 Inserting ${nodes.length} nodes into database...`);
    
    // First clear existing data
    const { error: deleteError } = await supabase
        .from('skill_tree_nodes')
        .delete()
        .neq('id', '00000000-0000-0000-0000-000000000000');
        
    if (deleteError) throw deleteError;
    console.log('✅ Cleared existing data');
    
    // Insert in batches
    const batchSize = 100;
    let inserted = 0;
    
    for (let i = 0; i < nodes.length; i += batchSize) {
        const batch = nodes.slice(i, i + batchSize);
        
        // Remove temporary fields before insertion
        const cleanBatch = batch.map(node => {
            const { children_data, original_path, ...cleanNode } = node;
            return cleanNode;
        });
        
        const { error: insertError } = await supabase
            .from('skill_tree_nodes')
            .insert(cleanBatch);
            
        if (insertError) {
            console.error(`Error inserting batch ${Math.floor(i/batchSize) + 1}:`, insertError);
            throw insertError;
        }
        
        inserted += cleanBatch.length;
        console.log(`Inserted ${inserted}/${nodes.length} nodes...`);
    }
    
    console.log('✅ All nodes inserted successfully');
}

async function parseAndRestoreBackup() {
    try {
        console.log('🚀 PARSING AND RESTORING FULL BACKUP...\n');
        
        // Step 1: Parse the backup file
        console.log('=== STEP 1: Parsing backup file ===');
        const backupData = parseBackupFile();
        console.log(`✅ Parsed backup data: ${backupData.name}`);
        
        // Step 2: Flatten the hierarchy
        console.log('\n=== STEP 2: Flattening hierarchy ===');
        const topLevelMap = {};
        const flatNodes = flattenHierarchy(backupData, [], topLevelMap);
        
        console.log(`✅ Flattened to ${flatNodes.length} nodes`);
        console.log(`Top-level categories: ${Object.keys(topLevelMap).length}`);
        Object.keys(topLevelMap).forEach(name => {
            console.log(`  - ${name}`);
        });
        
        // Step 3: Establish relationships
        console.log('\n=== STEP 3: Establishing relationships ===');
        const nodesWithRelationships = establishRelationships(flatNodes);
        
        // Step 4: Insert into database
        console.log('\n=== STEP 4: Inserting into database ===');
        await insertNodes(nodesWithRelationships);
        
        // Step 5: Verify
        console.log('\n=== STEP 5: Verification ===');
        const { count, error: countError } = await supabase
            .from('skill_tree_nodes')
            .select('*', { count: 'exact', head: true });
            
        if (countError) throw countError;
        
        console.log(`\n🎉 RESTORATION COMPLETE!`);
        console.log(`Total nodes restored: ${count}`);
        
        if (count > 1000) {
            console.log('✅ Successfully restored thousands of nodes from backup!');
        } else {
            console.log('⚠️ Fewer nodes than expected - please check backup file completeness');
        }
        
    } catch (error) {
        console.error('❌ Error during restoration:', error.message);
        console.log('\n💡 To fix this:');
        console.log('1. Ensure knowledgeTreeData5.ts contains the original full backup data');
        console.log('2. The file should be several thousand lines long');
        console.log('3. It should export a knowledgeTreeData object with nested children');
    }
}

parseAndRestoreBackup();
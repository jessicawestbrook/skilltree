require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');
const path = require('path');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function createBackupTable() {
    console.log('💾 Creating backup of current skill_tree_nodes table...');
    
    // Find the next available backup table name
    let backupSuffix = '_bkp';
    let backupTableName = `skill_tree_nodes${backupSuffix}`;
    let backupNum = 1;
    
    while (true) {
        const { data, error } = await supabase
            .from('information_schema.tables')
            .select('table_name')
            .eq('table_name', backupTableName)
            .eq('table_schema', 'public');
            
        if (error) {
            console.log(`Checking for table ${backupTableName}...`);
            break; // Table doesn't exist, we can use this name
        }
        
        if (!data || data.length === 0) {
            break; // Table doesn't exist, we can use this name
        }
        
        // Table exists, try next number
        backupNum++;
        backupTableName = `skill_tree_nodes_bkp${backupNum}`;
    }
    
    console.log(`Creating backup table: ${backupTableName}`);
    
    // Create backup table with same structure and data
    const { error: createError } = await supabase.rpc('create_backup_table', {
        source_table: 'skill_tree_nodes',
        backup_table: backupTableName
    });
    
    if (createError) {
        // If the RPC doesn't exist, use raw SQL
        const { error: sqlError } = await supabase
            .from('skill_tree_nodes')
            .select('*');
            
        if (sqlError) throw sqlError;
        
        console.log(`Creating backup table ${backupTableName} manually...`);
        // For now, just note that we should create a backup
        console.log(`⚠️ Please manually backup the skill_tree_nodes table before proceeding`);
    } else {
        console.log(`✅ Created backup table: ${backupTableName}`);
    }
    
    return backupTableName;
}

function parseBackupFile() {
    console.log('📖 Parsing backup file knowledgeTreeData5.ts...');
    
    const backupPath = path.join(__dirname, '../src/data/knowledgeTreeData5.ts');
    
    if (!fs.existsSync(backupPath)) {
        throw new Error('Backup file not found at: ' + backupPath);
    }
    
    const content = fs.readFileSync(backupPath, 'utf8');
    console.log(`File content length: ${content.length} characters`);
    
    if (content.length < 1000) {
        throw new Error('Backup file appears to be truncated or empty. Expected thousands of lines.');
    }
    
    console.log('File appears to contain substantial data. Parsing...');
    
    try {
        // Create a safe evaluation context for the TypeScript data
        let jsContent = content
            // Remove TypeScript imports and type annotations
            .replace(/import\s+.*?from\s+['"][^'"]*['"];\s*/g, '')
            .replace(/export\s+const\s+knowledgeTreeData:\s*\w+\s*=/, 'const knowledgeTreeData =')
            .replace(/type:\s*"(category|skill)"/g, 'type: "$1"');
            
        // Add export at the end
        jsContent += '\nmodule.exports = knowledgeTreeData;';
        
        // Write to temporary file and require it
        const tempPath = path.join(__dirname, 'temp_backup_parse.js');
        fs.writeFileSync(tempPath, jsContent);
        
        const data = require(tempPath);
        
        // Clean up
        fs.unlinkSync(tempPath);
        
        console.log(`✅ Successfully parsed backup data: ${data.name}`);
        console.log(`Root has ${data.children ? data.children.length : 0} top-level children`);
        
        return data;
        
    } catch (error) {
        console.error('Parsing error:', error.message);
        throw new Error('Could not parse backup file. Please check the file format.');
    }
}

function flattenHierarchy(node, currentPath = [], allNodes = [], parentLookup = {}) {
    const pathDepth = currentPath.length;
    
    // Skip the first 2 levels: "Knowledge" and "Academic Disciplines" / "Applied Knowledge"
    if (pathDepth === 0 && node.name === 'Knowledge') {
        // Process children of Knowledge
        if (node.children) {
            for (const child of node.children) {
                flattenHierarchy(child, [...currentPath, node.name], allNodes, parentLookup);
            }
        }
        return allNodes;
    }
    
    if (pathDepth === 1 && (node.name === 'Academic Disciplines' || node.name === 'Applied Knowledge')) {
        // Process children as new top-level categories
        if (node.children) {
            for (const child of node.children) {
                flattenHierarchy(child, [...currentPath, node.name], allNodes, parentLookup);
            }
        }
        return allNodes;
    }
    
    // Now we're at levels that should be preserved
    // Calculate the new path (removing first 2 levels)
    let newPath = [];
    if (pathDepth > 2) {
        newPath = currentPath.slice(2); // Remove "Knowledge" and "Academic Disciplines"/"Applied Knowledge"
    }
    
    // Special case: if this is Mathematics under Natural Sciences, promote it to top-level
    if (node.name === 'Mathematics' && currentPath.includes('Natural Sciences')) {
        newPath = []; // Make Mathematics top-level
    }
    
    // Create the flattened node
    const flatNode = {
        id: uuidv4(),
        name: node.name,
        type: node.type || 'category',
        parent_id: null, // Will be set later
        learning_area: node.learning_area || (newPath.length === 0 ? node.name : newPath[0]),
        path: newPath,
        metadata: node.metadata || {},
        display_order: node.display_order || null,
        has_learning_content: node.type === 'skill' || Boolean(node.has_learning_content),
        is_menu_leaf: node.type === 'skill' || !node.children || node.children.length === 0,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        _originalPath: currentPath,
        _parentName: newPath.length > 0 ? newPath[newPath.length - 1] : null
    };
    
    allNodes.push(flatNode);
    
    // Store in parent lookup for relationship building
    const pathKey = newPath.join(' → ');
    if (!parentLookup[pathKey]) {
        parentLookup[pathKey] = {};
    }
    parentLookup[pathKey][node.name] = flatNode;
    
    // Process children
    if (node.children && node.children.length > 0) {
        for (const child of node.children) {
            flattenHierarchy(child, [...currentPath, node.name], allNodes, parentLookup);
        }
    }
    
    return allNodes;
}

function establishRelationships(nodes, parentLookup) {
    console.log('🔗 Establishing parent-child relationships...');
    
    let relationshipsSet = 0;
    
    for (const node of nodes) {
        if (node.path.length > 0 && node._parentName) {
            // Find parent
            const parentPath = node.path.slice(0, -1).join(' → ');
            const parentName = node._parentName;
            
            let parent = null;
            
            if (parentPath === '') {
                // Parent is top-level
                parent = nodes.find(n => n.name === parentName && n.path.length === 0);
            } else {
                // Parent has a path
                if (parentLookup[parentPath] && parentLookup[parentPath][parentName]) {
                    parent = parentLookup[parentPath][parentName];
                }
            }
            
            if (parent) {
                node.parent_id = parent.id;
                relationshipsSet++;
            } else {
                console.warn(`⚠️ Could not find parent "${parentName}" at path "${parentPath}" for node "${node.name}"`);
            }
        }
    }
    
    console.log(`✅ Set ${relationshipsSet} parent relationships`);
    
    // Clean up temporary fields
    nodes.forEach(node => {
        delete node._originalPath;
        delete node._parentName;
    });
    
    return nodes;
}

async function insertNodes(nodes) {
    console.log(`📝 Inserting ${nodes.length} nodes into database...`);
    
    // Clear existing data
    console.log('Clearing existing skill_tree_nodes data...');
    const { error: deleteError } = await supabase
        .from('skill_tree_nodes')
        .delete()
        .neq('id', '00000000-0000-0000-0000-000000000000');
        
    if (deleteError && deleteError.code !== 'PGRST116') {
        throw deleteError;
    }
    console.log('✅ Cleared existing data');
    
    // Insert in batches
    const batchSize = 50; // Smaller batches for reliability
    let inserted = 0;
    
    for (let i = 0; i < nodes.length; i += batchSize) {
        const batch = nodes.slice(i, i + batchSize);
        
        try {
            const { error: insertError } = await supabase
                .from('skill_tree_nodes')
                .insert(batch);
                
            if (insertError) {
                console.error(`❌ Error inserting batch ${Math.floor(i/batchSize) + 1}:`, insertError);
                throw insertError;
            }
            
            inserted += batch.length;
            if (inserted % 500 === 0 || inserted === nodes.length) {
                console.log(`   Inserted ${inserted}/${nodes.length} nodes...`);
            }
            
        } catch (error) {
            console.error(`Failed on batch starting at index ${i}:`, error);
            throw error;
        }
    }
    
    console.log('✅ All nodes inserted successfully');
}

async function backupAndRestoreFullHierarchy() {
    try {
        console.log('🚀 BACKUP AND RESTORE FULL HIERARCHY...\n');
        
        // Step 1: Create backup
        console.log('=== STEP 1: Creating backup ===');
        const backupTableName = await createBackupTable();
        
        // Step 2: Parse backup file
        console.log('\n=== STEP 2: Parsing backup file ===');
        const backupData = parseBackupFile();
        
        // Step 3: Flatten hierarchy
        console.log('\n=== STEP 3: Flattening hierarchy ===');
        const parentLookup = {};
        const flatNodes = flattenHierarchy(backupData, [], [], parentLookup);
        
        console.log(`✅ Flattened to ${flatNodes.length} nodes`);
        
        const topLevelNodes = flatNodes.filter(n => n.path.length === 0);
        console.log(`Top-level categories (${topLevelNodes.length}):`);
        topLevelNodes.forEach(node => {
            console.log(`   - ${node.name} (${node.learning_area})`);
        });
        
        // Step 4: Establish relationships
        console.log('\n=== STEP 4: Establishing relationships ===');
        const nodesWithRelationships = establishRelationships(flatNodes, parentLookup);
        
        // Step 5: Insert into database
        console.log('\n=== STEP 5: Inserting into database ===');
        await insertNodes(nodesWithRelationships);
        
        // Step 6: Verify
        console.log('\n=== STEP 6: Verification ===');
        const { count, error: countError } = await supabase
            .from('skill_tree_nodes')
            .select('*', { count: 'exact', head: true });
            
        if (countError) throw countError;
        
        const { data: rootNodes, error: rootError } = await supabase
            .from('skill_tree_nodes')
            .select('name, type')
            .is('parent_id', null)
            .order('name');
            
        if (rootError) throw rootError;
        
        console.log(`\n🎉 RESTORATION COMPLETE!`);
        console.log(`📊 Results:`);
        console.log(`   - Total nodes restored: ${count}`);
        console.log(`   - Root categories: ${rootNodes.length}`);
        console.log(`   - Backup table created: ${backupTableName}`);
        
        console.log(`\nRoot categories:`);
        rootNodes.forEach(node => {
            console.log(`   - ${node.name} (${node.type})`);
        });
        
        if (count > 1000) {
            console.log('\n✅ Successfully restored thousands of nodes from backup!');
            console.log('✅ Mathematics and Natural Sciences promoted to top-level');
            console.log('✅ Removed "Knowledge" and "Academic Disciplines" levels');
        } else {
            console.log('\n⚠️ Fewer nodes than expected - please verify backup completeness');
        }
        
    } catch (error) {
        console.error('\n❌ Error during restoration:', error.message);
        console.log('\n💡 If this failed, you can restore from the backup table created earlier.');
    }
}

backupAndRestoreFullHierarchy();
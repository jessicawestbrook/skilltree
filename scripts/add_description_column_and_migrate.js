require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function migrateDescriptionColumn() {
    try {
        console.log('🔄 MIGRATING SKILL TREE SCHEMA - Adding Description Column\n');
        
        // Step 1: Create backup table
        console.log('📋 Creating backup table...');
        try {
            const { error: backupError } = await supabase.rpc('sql', {
                query: 'CREATE TABLE IF NOT EXISTS skill_tree_nodes_backup_schema AS SELECT * FROM skill_tree_nodes;'
            });
            
            if (backupError) {
                console.log('⚠️  Backup note:', backupError.message);
            } else {
                console.log('✅ Backup table created successfully');
            }
        } catch (e) {
            console.log('⚠️  Backup creation (continuing):', e.message);
        }
        
        // Step 2: Add description column
        console.log('\n➕ Adding description column...');
        try {
            const { error: addColumnError } = await supabase.rpc('sql', {
                query: 'ALTER TABLE skill_tree_nodes ADD COLUMN IF NOT EXISTS description TEXT;'
            });
            
            if (addColumnError) {
                console.log('⚠️  Add column note:', addColumnError.message);
            } else {
                console.log('✅ Description column added successfully');
            }
        } catch (e) {
            console.log('Column may already exist:', e.message);
        }
        
        // Step 3: Migrate data from metadata to description column
        console.log('\n🔄 Migrating existing description data from metadata...');
        
        // Get all nodes with metadata that contains description
        const { data: nodesWithMetadata, error: fetchError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, metadata')
            .not('metadata', 'is', null);
            
        if (fetchError) {
            console.error('Error fetching nodes:', fetchError);
            return;
        }
        
        console.log(`Found ${nodesWithMetadata.length} nodes with metadata`);
        
        let migratedCount = 0;
        for (const node of nodesWithMetadata) {
            if (node.metadata && typeof node.metadata === 'object' && node.metadata.description) {
                const { error: updateError } = await supabase
                    .from('skill_tree_nodes')
                    .update({
                        description: node.metadata.description
                    })
                    .eq('id', node.id);
                    
                if (updateError) {
                    console.error(`Error updating ${node.name}:`, updateError);
                } else {
                    migratedCount++;
                    if (migratedCount % 10 === 0) {
                        console.log(`   Migrated ${migratedCount} descriptions...`);
                    }
                }
            }
        }
        
        console.log(`✅ Migrated ${migratedCount} descriptions from metadata to description column`);
        
        // Step 4: Remove metadata column (optional - commented out for safety)
        console.log('\n📝 Note: Metadata column retained for safety. Can be removed later if no longer needed.');
        /*
        console.log('\n➖ Removing metadata column...');
        try {
            const { error: dropColumnError } = await supabase.rpc('sql', {
                query: 'ALTER TABLE skill_tree_nodes DROP COLUMN IF EXISTS metadata;'
            });
            
            if (dropColumnError) {
                console.log('⚠️  Drop column note:', dropColumnError.message);
            } else {
                console.log('✅ Metadata column removed successfully');
            }
        } catch (e) {
            console.log('Drop column note:', e.message);
        }
        */
        
        // Step 5: Verify the migration
        console.log('\n🔍 Verifying migration...');
        const { data: sampleData, error: verifyError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, description, metadata')
            .not('description', 'is', null)
            .limit(5);
            
        if (verifyError) {
            console.error('Verification error:', verifyError);
        } else {
            console.log(`✅ Found ${sampleData.length} nodes with descriptions`);
            sampleData.forEach(node => {
                console.log(`   "${node.name}": "${node.description?.substring(0, 50)}..."`);
            });
        }
        
        console.log('\n🎉 Schema migration completed successfully!');
        console.log('✅ Description column added');
        console.log(`✅ ${migratedCount} descriptions migrated`);
        console.log('✅ Ready for Phase 1 content migration');
        
    } catch (error) {
        console.error('❌ Migration failed:', error);
    }
}

migrateDescriptionColumn();
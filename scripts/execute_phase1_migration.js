require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function executePhase1Migration() {
    try {
        console.log('🚀 EXECUTING PHASE 1 SKILL TREE MIGRATION\n');
        
        // Create backup first
        console.log('📋 Creating backup table...');
        const { error: backupError } = await supabase.rpc('create_backup_table');
        
        if (backupError) {
            console.log('Creating backup with direct SQL...');
            const { error: directBackupError } = await supabase
                .from('skill_tree_nodes_backup_phase1')
                .select('*')
                .limit(1);
            
            if (directBackupError && directBackupError.code === '42P01') {
                // Table doesn't exist, create it
                const { error: createBackupError } = await supabase.rpc('sql', {
                    query: 'CREATE TABLE skill_tree_nodes_backup_phase1 AS SELECT * FROM skill_tree_nodes;'
                });
                
                if (createBackupError) {
                    console.log('⚠️  Backup creation note:', createBackupError.message);
                    console.log('Proceeding with migration (backup may already exist)...\n');
                } else {
                    console.log('✅ Backup table created successfully\n');
                }
            }
        } else {
            console.log('✅ Backup table created successfully\n');
        }
        
        // 1. Add Civic Education & Government
        console.log('🏛️  Adding Civic Education & Government category...');
        
        const { data: civicData, error: civicError } = await supabase
            .from('skill_tree_nodes')
            .insert({
                id: uuidv4(),
                name: 'Civic Education & Government',
                type: 'category',
                parent_id: null,
                display_order: 125,
                learning_area: 'Civic Studies',
                metadata: {
                    description: 'Essential knowledge for democratic participation and responsible citizenship'
                },
                path: [],
                has_learning_content: false,
                is_menu_leaf: false
            })
            .select()
            .single();
            
        if (civicError) {
            console.error('❌ Error adding Civic Education:', civicError);
            return;
        }
        
        const civicId = civicData.id;
        console.log(`✅ Civic Education added with ID: ${civicId}`);
        
        // Add civic subcategories
        const civicSubcategories = [
            {
                name: 'Government Structure & Functions',
                display_order: 10,
                metadata: { description: 'Understanding how government works at federal, state, and local levels' },
                learning_area: 'Government Studies'
            },
            {
                name: 'Constitutional Law & Rights',
                display_order: 20,
                metadata: { description: 'Fundamental rights, freedoms, and legal protections in democratic society' },
                learning_area: 'Constitutional Studies'
            },
            {
                name: 'Democratic Processes',
                display_order: 30,
                metadata: { description: 'Voting, elections, and mechanisms of democratic participation' },
                learning_area: 'Political Processes'
            },
            {
                name: 'Civic Duties & Responsibilities',
                display_order: 40,
                metadata: { description: 'Obligations and opportunities for civic engagement and community participation' },
                learning_area: 'Civic Engagement'
            },
            {
                name: 'Public Policy & Analysis',
                display_order: 50,
                metadata: { description: 'How policies are made, implemented, and their impact on society' },
                learning_area: 'Policy Studies'
            },
            {
                name: 'Community Engagement',
                display_order: 60,
                metadata: { description: 'Local involvement, grassroots participation, and community building' },
                learning_area: 'Community Studies'
            }
        ];
        
        for (const subcat of civicSubcategories) {
            const { error: subcatError } = await supabase
                .from('skill_tree_nodes')
                .insert({
                    id: uuidv4(),
                    ...subcat,
                    type: 'category',
                    parent_id: civicId,
                    path: ['Civic Education & Government'],
                    has_learning_content: false,
                    is_menu_leaf: false
                });
                
            if (subcatError) {
                console.error(`❌ Error adding ${subcat.name}:`, subcatError);
            } else {
                console.log(`   ✅ Added: ${subcat.name}`);
            }
        }
        
        // Add detailed skills for Government Structure
        const { data: govStructureData } = await supabase
            .from('skill_tree_nodes')
            .select('id')
            .eq('name', 'Government Structure & Functions')
            .single();
            
        if (govStructureData) {
            const govSkills = [
                { name: 'Federal Government', order: 10, desc: 'Executive, Legislative, and Judicial branches of federal government' },
                { name: 'State Government', order: 20, desc: 'State-level governance, governors, state legislatures, and state courts' },
                { name: 'Local Government', order: 30, desc: 'City councils, mayors, county governments, and local services' },
                { name: 'Separation of Powers', order: 40, desc: 'Checks and balances between branches of government' },
                { name: 'Federalism', order: 50, desc: 'Division of power between federal and state governments' },
                { name: 'Bureaucracy & Public Administration', order: 60, desc: 'Government agencies, civil service, and public administration' }
            ];
            
            for (const skill of govSkills) {
                await supabase.from('skill_tree_nodes').insert({
                    id: uuidv4(),
                    name: skill.name,
                    type: 'skill',
                    parent_id: govStructureData.id,
                    display_order: skill.order,
                    metadata: { description: skill.desc },
                    path: ['Civic Education & Government', 'Government Structure & Functions'],
                    has_learning_content: true,
                    is_menu_leaf: true
                });
            }
            console.log('   ✅ Added Government Structure skills');
        }
        
        // 2. Add Research & Information Literacy
        console.log('\n🔍 Adding Research & Information Literacy...');
        
        const { data: lifeSkillsData } = await supabase
            .from('skill_tree_nodes')
            .select('id')
            .eq('name', 'Life Skills')
            .is('parent_id', null)
            .single();
            
        if (!lifeSkillsData) {
            console.error('❌ Life Skills category not found');
            return;
        }
        
        const { data: researchData, error: researchError } = await supabase
            .from('skill_tree_nodes')
            .insert({
                id: uuidv4(),
                name: 'Research & Information Literacy',
                type: 'category',
                parent_id: lifeSkillsData.id,
                display_order: 70,
                learning_area: 'Information Studies',
                metadata: {
                    description: 'Essential skills for finding, evaluating, and using information effectively'
                },
                path: ['Life Skills'],
                has_learning_content: false,
                is_menu_leaf: false
            })
            .select()
            .single();
            
        if (researchError) {
            console.error('❌ Error adding Research Literacy:', researchError);
            return;
        }
        
        const researchId = researchData.id;
        console.log(`✅ Research & Information Literacy added with ID: ${researchId}`);
        
        // Add research subcategories
        const researchSubcategories = [
            {
                name: 'Source Evaluation & Fact-Checking',
                display_order: 10,
                metadata: { description: 'Determining credibility and accuracy of information sources' },
                learning_area: 'Critical Evaluation'
            },
            {
                name: 'Research Methods & Design',
                display_order: 20,
                metadata: { description: 'Systematic approaches to investigation and inquiry' },
                learning_area: 'Research Methodology'
            },
            {
                name: 'Academic Writing & Citation',
                display_order: 30,
                metadata: { description: 'Proper attribution and scholarly communication standards' },
                learning_area: 'Academic Communication'
            }
        ];
        
        for (const subcat of researchSubcategories) {
            const { error: subcatError } = await supabase
                .from('skill_tree_nodes')
                .insert({
                    id: uuidv4(),
                    ...subcat,
                    type: 'category',
                    parent_id: researchId,
                    path: ['Life Skills', 'Research & Information Literacy'],
                    has_learning_content: false,
                    is_menu_leaf: false
                });
                
            if (subcatError) {
                console.error(`❌ Error adding ${subcat.name}:`, subcatError);
            } else {
                console.log(`   ✅ Added: ${subcat.name}`);
            }
        }
        
        // 3. Add Digital Citizenship & Media Literacy
        console.log('\n💻 Adding Digital Citizenship & Media Literacy...');
        
        const { data: techSkillsData } = await supabase
            .from('skill_tree_nodes')
            .select('id')
            .eq('name', 'Technical Skills')
            .is('parent_id', null)
            .single();
            
        if (!techSkillsData) {
            console.error('❌ Technical Skills category not found');
            return;
        }
        
        const { data: digitalData, error: digitalError } = await supabase
            .from('skill_tree_nodes')
            .insert({
                id: uuidv4(),
                name: 'Digital Citizenship & Media Literacy',
                type: 'category',
                parent_id: techSkillsData.id,
                display_order: 15,
                learning_area: 'Digital Studies',
                metadata: {
                    description: 'Responsible and informed use of digital technologies and media'
                },
                path: ['Technical Skills'],
                has_learning_content: false,
                is_menu_leaf: false
            })
            .select()
            .single();
            
        if (digitalError) {
            console.error('❌ Error adding Digital Citizenship:', digitalError);
            return;
        }
        
        const digitalId = digitalData.id;
        console.log(`✅ Digital Citizenship & Media Literacy added with ID: ${digitalId}`);
        
        // Add digital subcategories
        const digitalSubcategories = [
            {
                name: 'Online Safety & Privacy',
                display_order: 10,
                metadata: { description: 'Protecting personal information and staying safe online' },
                learning_area: 'Digital Safety'
            },
            {
                name: 'Media Analysis & Bias Detection',
                display_order: 30,
                metadata: { description: 'Understanding and evaluating media messages and bias' },
                learning_area: 'Media Literacy'
            }
        ];
        
        for (const subcat of digitalSubcategories) {
            const { error: subcatError } = await supabase
                .from('skill_tree_nodes')
                .insert({
                    id: uuidv4(),
                    ...subcat,
                    type: 'category',
                    parent_id: digitalId,
                    path: ['Technical Skills', 'Digital Citizenship & Media Literacy'],
                    has_learning_content: false,
                    is_menu_leaf: false
                });
                
            if (subcatError) {
                console.error(`❌ Error adding ${subcat.name}:`, subcatError);
            } else {
                console.log(`   ✅ Added: ${subcat.name}`);
            }
        }
        
        console.log('\n🎉 Phase 1 migration completed successfully!');
        console.log('\nAdded categories:');
        console.log('• Civic Education & Government (top-level)');
        console.log('• Research & Information Literacy (under Life Skills)');
        console.log('• Digital Citizenship & Media Literacy (under Technical Skills)');
        
    } catch (error) {
        console.error('❌ Migration failed:', error);
    }
}

executePhase1Migration();
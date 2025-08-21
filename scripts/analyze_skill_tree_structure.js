const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = 'https://ozujqlucqdyszxmzhigf.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im96dWpxbHVjcWR5c3p4bXpoaWdmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUyNDEzMzUsImV4cCI6MjA3MDgxNzMzNX0.k21_FmGqGsojgPMKN97-dZI-y5kwrbxKGZcGpDnikG4';

const supabase = createClient(supabaseUrl, supabaseKey);

async function analyzeSkillTreeStructure() {
    console.log('=== ANALYZING SKILL_TREE_NODES TABLE STRUCTURE ===\n');
    
    try {
        // Get sample data to understand current structure first
        console.log('1. Getting sample data to understand table structure...');
        const { data: sampleData, error: sampleError } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .limit(1);

        if (sampleError) {
            console.error('Error getting sample data:', sampleError);
            return;
        }

        if (sampleData && sampleData.length > 0) {
            console.log('Table columns found:');
            const columns = Object.keys(sampleData[0]);
            columns.forEach(col => {
                const value = sampleData[0][col];
                const type = value === null ? 'null' : typeof value;
                console.log(`  - ${col}: ${type} (sample: ${value})`);
            });

            // Check for existing ordering fields
            console.log('\n2. Checking for existing ordering fields...');
            const orderingFields = columns.filter(col => 
                col.toLowerCase().includes('order') || 
                col.toLowerCase().includes('sort') ||
                col.toLowerCase().includes('position') ||
                col.toLowerCase().includes('rank')
            );

            if (orderingFields.length > 0) {
                console.log('Found potential ordering fields:');
                orderingFields.forEach(field => {
                    console.log(`  - ${field}`);
                });
            } else {
                console.log('No existing ordering fields found.');
            }
        }

        // Get more sample data to understand current structure
        console.log('\n3. Getting more sample data...');
        const { data: moreSampleData, error: moreSampleError } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .limit(5);

        if (moreSampleError) {
            console.error('Error getting sample data:', moreSampleError);
            return;
        }

        console.log('Sample records:');
        moreSampleData.forEach((record, index) => {
            console.log(`\nRecord ${index + 1}:`);
            Object.keys(record).forEach(key => {
                if (record[key] !== null && record[key] !== undefined) {
                    console.log(`  ${key}: ${typeof record[key] === 'object' ? JSON.stringify(record[key]) : record[key]}`);
                }
            });
        });

        // Get statistics about the table
        console.log('\n4. Getting table statistics...');
        const { count, error: countError } = await supabase
            .from('skill_tree_nodes')
            .select('*', { count: 'exact', head: true });

        if (countError) {
            console.error('Error getting count:', countError);
        } else {
            console.log(`Total records: ${count}`);
        }

        // Check for nodes with specific characteristics
        console.log('\n5. Analyzing node characteristics...');
        
        // Count nodes by level
        const { data: levelData, error: levelError } = await supabase
            .from('skill_tree_nodes')
            .select('level')
            .not('level', 'is', null);

        if (!levelError && levelData) {
            const levelCounts = {};
            levelData.forEach(node => {
                levelCounts[node.level] = (levelCounts[node.level] || 0) + 1;
            });
            console.log('Nodes by level:');
            Object.keys(levelCounts).sort((a, b) => parseInt(a) - parseInt(b)).forEach(level => {
                console.log(`  Level ${level}: ${levelCounts[level]} nodes`);
            });
        }

        // Check parent-child relationships
        const { data: rootNodes, error: rootError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, parent_id')
            .is('parent_id', null);

        if (!rootError && rootNodes) {
            console.log(`\nRoot nodes (no parent): ${rootNodes.length}`);
            rootNodes.forEach(node => {
                console.log(`  - ${node.name} (ID: ${node.id})`);
            });
        }

        // If there are ordering fields, analyze their usage
        if (sampleData && sampleData.length > 0) {
            const columns = Object.keys(sampleData[0]);
            const orderingFields = columns.filter(col => 
                col.toLowerCase().includes('order') || 
                col.toLowerCase().includes('sort') ||
                col.toLowerCase().includes('position') ||
                col.toLowerCase().includes('rank')
            );

            if (orderingFields.length > 0) {
                console.log('\n6. Analyzing ordering field usage...');
                for (const field of orderingFields) {
                    const { data: orderData, error: orderError } = await supabase
                        .from('skill_tree_nodes')
                        .select(`${field}`)
                        .not(field, 'is', null);

                    if (!orderError && orderData) {
                        console.log(`\n${field} field analysis:`);
                        console.log(`  - Non-null values: ${orderData.length}`);
                        
                        const values = orderData.map(d => d[field]);
                        if (values.length > 0) {
                            console.log(`  - Min value: ${Math.min(...values)}`);
                            console.log(`  - Max value: ${Math.max(...values)}`);
                            console.log(`  - Unique values: ${new Set(values).size}`);
                        }
                    }
                }
            }
        }

    } catch (error) {
        console.error('Error analyzing table:', error);
    }
}

// Run the analysis
analyzeSkillTreeStructure().then(() => {
    console.log('\n=== ANALYSIS COMPLETE ===');
    process.exit(0);
});
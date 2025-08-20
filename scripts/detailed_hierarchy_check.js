require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function detailedHierarchyCheck() {
    try {
        console.log('🔍 DETAILED HIERARCHY ANALYSIS...\n');
        
        // Check total node count
        const { data: allNodes, error: allError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, parent_id, learning_area')
            .order('name');
            
        if (allError) throw allError;
        
        console.log(`Total nodes in database: ${allNodes.length}`);
        
        // Analyze by type
        const categories = allNodes.filter(n => n.type === 'category');
        const skills = allNodes.filter(n => n.type === 'skill');
        
        console.log(`- Categories: ${categories.length}`);
        console.log(`- Skills: ${skills.length}`);
        
        // Check for nodes with null parent_id
        const rootNodes = allNodes.filter(n => n.parent_id === null);
        console.log(`\nRoot nodes (parent_id = null): ${rootNodes.length}`);
        
        rootNodes.forEach(node => {
            console.log(`  - ${node.name} (${node.type})`);
        });
        
        // Check for orphaned nodes (parent_id points to non-existent node)
        const nodeIds = new Set(allNodes.map(n => n.id));
        const orphanedNodes = allNodes.filter(n => 
            n.parent_id !== null && !nodeIds.has(n.parent_id)
        );
        
        if (orphanedNodes.length > 0) {
            console.log(`\n❌ ORPHANED NODES: ${orphanedNodes.length}`);
            orphanedNodes.forEach(node => {
                console.log(`  - ${node.name} (${node.type}) -> missing parent: ${node.parent_id}`);
            });
        } else {
            console.log('\n✅ No orphaned nodes found');
        }
        
        // Check depth distribution
        console.log('\n=== HIERARCHY DEPTH ANALYSIS ===');
        const depthAnalysis = {};
        
        // Helper function to calculate depth
        function getDepth(nodeId, visited = new Set()) {
            if (visited.has(nodeId)) return -1; // Circular reference
            visited.add(nodeId);
            
            const node = allNodes.find(n => n.id === nodeId);
            if (!node || node.parent_id === null) return 0;
            
            return 1 + getDepth(node.parent_id, visited);
        }
        
        allNodes.forEach(node => {
            const depth = getDepth(node.id);
            if (depth >= 0) {
                if (!depthAnalysis[depth]) depthAnalysis[depth] = [];
                depthAnalysis[depth].push(node);
            }
        });
        
        Object.keys(depthAnalysis).sort().forEach(depth => {
            const nodes = depthAnalysis[depth];
            console.log(`Depth ${depth}: ${nodes.length} nodes`);
            
            if (depth <= 2) {
                nodes.slice(0, 10).forEach(node => {
                    console.log(`  - ${node.name} (${node.type})`);
                });
                if (nodes.length > 10) {
                    console.log(`  ... and ${nodes.length - 10} more`);
                }
            }
        });
        
        // Check specific expected categories
        console.log('\n=== EXPECTED TOP-LEVEL CATEGORIES CHECK ===');
        const expectedTopLevel = [
            'Mathematics', 'Languages', 'Natural Sciences', 'Computer Science',
            'Social Sciences', 'Humanities', 'Applied Sciences', 'Creative Skills',
            'Professional Skills', 'Technical Skills', 'Life Skills', 'Test Preparation and Assessment'
        ];
        
        expectedTopLevel.forEach(name => {
            const node = allNodes.find(n => n.name === name && n.parent_id === null);
            if (node) {
                const children = allNodes.filter(n => n.parent_id === node.id);
                console.log(`✅ ${name}: ${children.length} children`);
            } else {
                console.log(`❌ ${name}: NOT FOUND at root level`);
            }
        });
        
        // Look for potential issues
        console.log('\n=== POTENTIAL ISSUES ===');
        
        // Skills that should probably have parents
        const rootSkills = allNodes.filter(n => n.type === 'skill' && n.parent_id === null);
        if (rootSkills.length > 0) {
            console.log(`❌ ${rootSkills.length} skills at root level (should have parents):`);
            rootSkills.slice(0, 10).forEach(skill => {
                console.log(`  - ${skill.name} (learning_area: ${skill.learning_area})`);
            });
        }
        
        // Categories with no children
        const emptyCats = categories.filter(cat => {
            return allNodes.filter(n => n.parent_id === cat.id).length === 0;
        });
        
        if (emptyCats.length > 0) {
            console.log(`⚠️ ${emptyCats.length} categories with no children:`);
            emptyCats.slice(0, 10).forEach(cat => {
                console.log(`  - ${cat.name}`);
            });
        }
        
    } catch (error) {
        console.error('Error in detailed hierarchy check:', error);
    }
}

detailedHierarchyCheck();
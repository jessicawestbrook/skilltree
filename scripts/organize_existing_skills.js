require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

// Mapping patterns for organizing skills into proper topic categories
const SKILL_MAPPINGS = {
    // Mathematics patterns
    'mathematics': {
        'addition|subtraction|multiplication|division|basic operations': 'Basic Operations',
        'fraction|fractions': 'Fractions', 
        'decimal|decimals': 'Decimals',
        'percentage|percent': 'Percentages',
        'measurement|measure|length|weight|volume|area|perimeter': 'Measurements',
        'equation|linear|solve|variable': 'Linear Equations',
        'polynomial|quadratic|factor': 'Polynomials',
        'quadratic equation': 'Quadratic Equations',
        'system|systems of equations': 'Systems of Equations',
        'geometry|shape|angle|triangle|circle|square': 'Basic Shapes',
        'area|perimeter': 'Area and Perimeter',
        'volume|3d|cube|sphere': 'Volume', 
        'angle|angles|degree': 'Angles',
        'coordinate|graph|plot|point': 'Coordinate Geometry',
        'limit|limits': 'Limits',
        'derivative|differentiation': 'Derivatives', 
        'integral|integration': 'Integrals',
        'application|optimization|rate': 'Applications',
        'statistics|data|mean|median|mode': 'Data Analysis',
        'probability|chance|random': 'Probability',
        'distribution|normal|bell curve': 'Distributions',
        'optimization|minimize|maximize': 'Optimization',
        'numerical|computation|algorithm': 'Numerical Methods'
    },
    
    // Languages patterns  
    'languages': {
        'english grammar|grammar english': 'Grammar',
        'literature|novel|story|poem': 'Literature', 
        'writing|essay|composition': 'Writing',
        'reading comprehension|comprehension': 'Reading Comprehension',
        'spanish grammar|grammar spanish': 'Grammar',
        'spanish vocabulary|vocabulary spanish': 'Vocabulary',
        'spanish conversation|conversation spanish': 'Conversation', 
        'spanish literature': 'Literature',
        'french grammar|grammar french': 'Grammar',
        'french vocabulary|vocabulary french': 'Vocabulary', 
        'french conversation|conversation french': 'Conversation',
        'french literature': 'Literature',
        'latin grammar|latin|ablative|accusative|dative|genitive|nominative': 'Grammar',
        'latin vocabulary|latin word': 'Vocabulary',
        'classical text|caesar|cicero|virgil': 'Classical Texts',
        'chinese grammar|mandarin grammar': 'Grammar',
        'chinese character|hanzi|character': 'Characters',
        'chinese conversation|mandarin conversation': 'Conversation',
        'chinese culture|china culture': 'Culture',
        'phonetic|phoneme|sound|pronunciation': 'Phonetics',
        'linguistic|language structure': 'Linguistics',
        'second language|language acquisition': 'Second Language Acquisition'
    },
    
    // Computer Science patterns
    'computer science': {
        'programming fundamentals|basic programming|programming basics': 'Fundamentals',
        'data structure|array|list|stack|queue|tree|hash': 'Data Structures', 
        'algorithm|sorting|searching|complexity': 'Algorithms',
        'object oriented|oop|class|inheritance|polymorphism': 'Object-Oriented Programming',
        'html|css|markup|stylesheet': 'HTML/CSS',
        'javascript|js|dom|jquery': 'JavaScript',
        'react|angular|vue|frontend framework': 'Frontend Frameworks', 
        'backend|server|api|database|node': 'Backend Development',
        'machine learning|ml|neural network|ai': 'Machine Learning',
        'data analysis|pandas|numpy': 'Data Analysis',
        'visualization|chart|graph|plot': 'Visualization',
        'design pattern|mvc|singleton|observer': 'Design Patterns',
        'testing|unit test|integration test': 'Testing',
        'git|github|version control|svn': 'Version Control',
        'project management|agile|scrum': 'Project Management',
        'operating system|os|linux|windows': 'Operating Systems',
        'network|tcp|ip|http|protocol': 'Networks',
        'security|encryption|cybersecurity|hack': 'Security'
    }
};

async function organizeExistingSkills() {
    try {
        console.log('🔧 ORGANIZING EXISTING SKILLS INTO PROPER HIERARCHY...\n');
        
        // Get all current nodes
        const { data: allNodes, error: allError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, parent_id, learning_area');
            
        if (allError) throw allError;
        
        // Create lookup maps
        const nodeMap = {};
        allNodes.forEach(node => {
            nodeMap[node.id] = node;
        });
        
        // Find skills that need to be moved
        const skillsToMove = allNodes.filter(node => 
            node.type === 'skill' && 
            node.parent_id !== null &&
            nodeMap[node.parent_id]?.type === 'category' &&
            nodeMap[node.parent_id]?.parent_id === null  // Direct child of top-level category
        );
        
        console.log(`Found ${skillsToMove.length} skills that need to be moved from top-level categories`);
        
        let movedCount = 0;
        let errorCount = 0;
        
        // Process each misplaced skill
        for (const skill of skillsToMove) {
            const topLevelParent = nodeMap[skill.parent_id];
            const learningArea = topLevelParent.name.toLowerCase();
            
            console.log(`\nProcessing: ${skill.name} (currently under ${topLevelParent.name})`);
            
            let targetTopicCategory = null;
            
            // Try to match skill to appropriate topic category
            if (SKILL_MAPPINGS[learningArea]) {
                const skillNameLower = skill.name.toLowerCase();
                
                for (const [pattern, topicName] of Object.entries(SKILL_MAPPINGS[learningArea])) {
                    const regex = new RegExp(pattern, 'i');
                    if (regex.test(skillNameLower)) {
                        // Find the topic category
                        targetTopicCategory = allNodes.find(node => 
                            node.name === topicName &&
                            node.type === 'category' &&
                            node.learning_area === topLevelParent.name
                        );
                        
                        if (targetTopicCategory) {
                            console.log(`  → Matched pattern "${pattern}" → ${topicName}`);
                            break;
                        }
                    }
                }
            }
            
            // If no specific match, try to find a reasonable subcategory
            if (!targetTopicCategory && topLevelParent.name === 'Mathematics') {
                // Default math skills to Basic Operations if no specific match
                targetTopicCategory = allNodes.find(node => 
                    node.name === 'Basic Operations' &&
                    node.learning_area === 'Mathematics'
                );
            } else if (!targetTopicCategory && topLevelParent.name === 'Languages') {
                // Try to determine language and default to Grammar
                const skillNameLower = skill.name.toLowerCase();
                let languageSubcategory = 'English'; // default
                
                if (skillNameLower.includes('spanish')) languageSubcategory = 'Spanish';
                else if (skillNameLower.includes('french')) languageSubcategory = 'French'; 
                else if (skillNameLower.includes('latin')) languageSubcategory = 'Latin';
                else if (skillNameLower.includes('chinese') || skillNameLower.includes('mandarin')) languageSubcategory = 'Mandarin Chinese';
                
                targetTopicCategory = allNodes.find(node =>
                    node.name === 'Grammar' &&
                    nodeMap[node.parent_id]?.name === languageSubcategory
                );
            }
            
            // Move the skill if we found a target
            if (targetTopicCategory) {
                try {
                    const { error: updateError } = await supabase
                        .from('skill_tree_nodes')
                        .update({ 
                            parent_id: targetTopicCategory.id,
                            updated_at: new Date().toISOString()
                        })
                        .eq('id', skill.id);
                        
                    if (updateError) {
                        console.log(`  ❌ Failed to move: ${updateError.message}`);
                        errorCount++;
                    } else {
                        console.log(`  ✅ Moved to: ${nodeMap[targetTopicCategory.parent_id]?.name} → ${targetTopicCategory.name}`);
                        movedCount++;
                    }
                } catch (err) {
                    console.log(`  ❌ Error moving skill: ${err.message}`);
                    errorCount++;
                }
            } else {
                console.log(`  ⚠️ No suitable topic category found - leaving under ${topLevelParent.name}`);
            }
            
            // Small delay to prevent overwhelming the database
            if ((movedCount + errorCount) % 10 === 0) {
                await new Promise(resolve => setTimeout(resolve, 100));
            }
        }
        
        console.log(`\n📊 RESULTS:`);
        console.log(`- Skills processed: ${skillsToMove.length}`);
        console.log(`- Successfully moved: ${movedCount}`);
        console.log(`- Errors: ${errorCount}`);
        console.log(`- Left unmoved: ${skillsToMove.length - movedCount - errorCount}`);
        
        // Final verification
        console.log('\n=== FINAL VERIFICATION ===');
        
        const { data: finalCheck, error: finalError } = await supabase
            .from('skill_tree_nodes') 
            .select('id, name, type, parent_id')
            .eq('type', 'skill');
            
        if (finalError) throw finalError;
        
        // Count skills still directly under top-level categories
        const stillMisplaced = finalCheck.filter(skill => {
            const parent = nodeMap[skill.parent_id];
            return parent?.type === 'category' && parent?.parent_id === null;
        });
        
        console.log(`Skills still directly under top-level categories: ${stillMisplaced.length}`);
        
        if (stillMisplaced.length > 0 && stillMisplaced.length <= 10) {
            console.log('Examples:');
            stillMisplaced.slice(0, 5).forEach(skill => {
                const parent = nodeMap[skill.parent_id];
                console.log(`  - ${skill.name} (under ${parent?.name})`);
            });
        }
        
        console.log('\n✅ Skill organization complete!');
        
    } catch (error) {
        console.error('Error organizing skills:', error);
    }
}

organizeExistingSkills();
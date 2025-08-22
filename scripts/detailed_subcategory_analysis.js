require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function analyzeSubcategoryGaps() {
    try {
        console.log('🔍 DETAILED SUBCATEGORY GAP ANALYSIS\n');
        
        // Get all nodes with their hierarchy
        const { data: allNodes, error } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, parent_id, learning_area')
            .order('name');
            
        if (error) throw error;
        
        // Build hierarchy map
        const nodeMap = {};
        allNodes.forEach(node => {
            nodeMap[node.id] = { ...node, children: [] };
        });
        
        allNodes.forEach(node => {
            if (node.parent_id && nodeMap[node.parent_id]) {
                nodeMap[node.parent_id].children.push(nodeMap[node.id]);
            }
        });
        
        // Get top-level categories
        const topLevel = allNodes.filter(node => !node.parent_id);
        
        console.log('=== SUBCATEGORY ANALYSIS BY MAJOR AREA ===\n');
        
        // Analyze key categories for gaps
        const analysisAreas = [
            {
                category: 'Humanities',
                expectedSubcategories: [
                    'History', 'Geography', 'Literature', 'Philosophy', 'Language Arts', 'Law',
                    'Anthropology', 'Archaeology', 'Art History', 'Religious Studies', 
                    'Cultural Studies', 'Classics', 'Ethics', 'Logic'
                ]
            },
            {
                category: 'Social Sciences', 
                expectedSubcategories: [
                    'Psychology', 'Sociology', 'Political Science', 'Economics', 'Linguistics',
                    'Anthropology', 'Criminology', 'Social Work', 'International Relations',
                    'Public Policy', 'Urban Studies', 'Gender Studies', 'Media Studies'
                ]
            },
            {
                category: 'Natural Sciences',
                expectedSubcategories: [
                    'Physics', 'Chemistry', 'Biology', 'Earth Sciences', 'Astronomy', 'Environmental Science',
                    'Geology', 'Meteorology', 'Oceanography', 'Ecology', 'Botany', 'Zoology', 
                    'Genetics', 'Neuroscience', 'Materials Science'
                ]
            },
            {
                category: 'Mathematics',
                expectedSubcategories: [
                    'Arithmetic', 'Algebra', 'Geometry', 'Calculus', 'Statistics', 'Probability',
                    'Discrete Mathematics', 'Applied Mathematics', 'Mathematical Logic', 
                    'Number Theory', 'Topology', 'Analysis', 'Linear Algebra', 'Differential Equations'
                ]
            },
            {
                category: 'Life Skills',
                expectedSubcategories: [
                    'Critical Thinking', 'Communication', 'Financial Literacy', 'Time Management',
                    'Study Skills', 'Problem Solving', 'Decision Making', 'Emotional Intelligence',
                    'Stress Management', 'Goal Setting', 'Self-Advocacy', 'Conflict Resolution',
                    'Civic Engagement', 'Digital Citizenship', 'Health & Wellness'
                ]
            },
            {
                category: 'Applied Sciences',
                expectedSubcategories: [
                    'Engineering', 'Medicine', 'Agriculture', 'Business', 'Education',
                    'Architecture', 'Urban Planning', 'Public Health', 'Veterinary Science',
                    'Forestry', 'Nutrition', 'Sports Science', 'Library Science', 'Information Science'
                ]
            }
        ];
        
        analysisAreas.forEach(area => {
            const categoryNode = topLevel.find(node => 
                node.name.toLowerCase().includes(area.category.toLowerCase())
            );
            
            if (categoryNode) {
                const currentSubs = nodeMap[categoryNode.id].children.map(child => 
                    child.name.toLowerCase()
                );
                
                console.log(`📚 ${area.category.toUpperCase()}`);
                console.log(`Current subcategories (${currentSubs.length}):`);
                nodeMap[categoryNode.id].children.forEach(child => {
                    console.log(`   ✓ ${child.name}`);
                });
                
                const missing = area.expectedSubcategories.filter(expected => 
                    !currentSubs.some(current => 
                        current.includes(expected.toLowerCase()) || 
                        expected.toLowerCase().includes(current.split(' ')[0])
                    )
                );
                
                if (missing.length > 0) {
                    console.log(`Missing/Underrepresented areas (${missing.length}):`);
                    missing.forEach(miss => {
                        console.log(`   ⚠️  ${miss}`);
                    });
                }
                console.log('');
            }
        });
        
        // Analyze specific gaps in detail
        console.log('=== CRITICAL GAPS REQUIRING ATTENTION ===\n');
        
        const criticalGaps = [
            {
                area: 'Civic Education',
                currentLocation: 'Missing entirely',
                importance: 'Essential for democratic participation',
                specificTopics: [
                    'Government Structure & Functions',
                    'Constitutional Law & Rights',
                    'Voting & Elections',
                    'Civic Duties & Responsibilities', 
                    'Community Engagement',
                    'Political Processes',
                    'Public Policy Analysis'
                ],
                recommendation: 'Add as new top-level category or major subcategory under Social Sciences'
            },
            {
                area: 'Information & Research Literacy',
                currentLocation: 'Scattered/incomplete',
                importance: 'Foundation for all learning and critical thinking',
                specificTopics: [
                    'Source Evaluation',
                    'Research Methods',
                    'Academic Writing',
                    'Citation & Documentation',
                    'Database Navigation',
                    'Fact-Checking',
                    'Primary vs Secondary Sources'
                ],
                recommendation: 'Add as category bridging Life Skills and Humanities'
            },
            {
                area: 'Ethics & Moral Reasoning',
                currentLocation: 'Limited coverage under Philosophy',
                importance: 'Critical for character development and decision-making',
                specificTopics: [
                    'Ethical Frameworks',
                    'Applied Ethics',
                    'Professional Ethics',
                    'Bioethics',
                    'Environmental Ethics',
                    'Technology Ethics',
                    'Moral Psychology'
                ],
                recommendation: 'Expand Philosophy or create standalone Ethics category'
            },
            {
                area: 'Social-Emotional Learning',
                currentLocation: 'Partially covered in Life Skills',
                importance: 'Critical for mental health and interpersonal success',
                specificTopics: [
                    'Self-Awareness',
                    'Self-Regulation',
                    'Social Awareness',
                    'Relationship Skills',
                    'Responsible Decision-Making',
                    'Empathy Development',
                    'Mindfulness'
                ],
                recommendation: 'Expand Life Skills or create dedicated SEL category'
            },
            {
                area: 'Environmental Literacy',
                currentLocation: 'Limited to Environmental Science',
                importance: 'Critical for understanding global challenges',
                specificTopics: [
                    'Sustainability Principles',
                    'Climate Change',
                    'Conservation',
                    'Environmental Policy',
                    'Renewable Energy',
                    'Waste Management',
                    'Environmental Justice'
                ],
                recommendation: 'Expand Environmental Science or create interdisciplinary category'
            },
            {
                area: 'Digital Citizenship',
                currentLocation: 'Scattered across Technical Skills',
                importance: 'Essential for safe and responsible technology use',
                specificTopics: [
                    'Online Safety & Privacy',
                    'Digital Footprint',
                    'Cyberbullying Prevention',
                    'Intellectual Property',
                    'Digital Communication Etiquette',
                    'Information Verification',
                    'Screen Time Management'
                ],
                recommendation: 'Add as major subcategory under Technical Skills or Life Skills'
            },
            {
                area: 'Study Skills & Learning How to Learn',
                currentLocation: 'Missing as organized category',
                importance: 'Meta-cognitive skills essential for lifelong learning',
                specificTopics: [
                    'Note-Taking Strategies',
                    'Active Reading',
                    'Memory Techniques',
                    'Test-Taking Skills',
                    'Learning Styles',
                    'Spaced Repetition',
                    'Growth Mindset'
                ],
                recommendation: 'Add as major subcategory under Life Skills or Test Preparation'
            }
        ];
        
        criticalGaps.forEach((gap, index) => {
            console.log(`${index + 1}. ${gap.area.toUpperCase()}`);
            console.log(`   Current Status: ${gap.currentLocation}`);
            console.log(`   Importance: ${gap.importance}`);
            console.log(`   Key Topics Missing:`);
            gap.specificTopics.forEach(topic => {
                console.log(`      • ${topic}`);
            });
            console.log(`   Recommendation: ${gap.recommendation}\n`);
        });
        
        // Check for underrepresented populations and inclusive content
        console.log('=== INCLUSIVITY & ACCESSIBILITY ANALYSIS ===\n');
        
        const diversityAreas = [
            'Disability Studies & Accessibility',
            'Multicultural Education',
            'Indigenous Knowledge Systems',
            'Global Perspectives',
            'Neurodiversity',
            'Gender & Sexuality Studies',
            'Special Educational Needs',
            'English as Second Language (ESL)',
            'Universal Design for Learning'
        ];
        
        console.log('Areas to consider for inclusive education:');
        diversityAreas.forEach(area => {
            console.log(`   📝 ${area}`);
        });
        
        console.log('\n=== FINAL RECOMMENDATIONS ===\n');
        console.log('🎯 IMMEDIATE PRIORITIES:');
        console.log('1. Add Civic Education as major category');
        console.log('2. Expand Information & Research Literacy');
        console.log('3. Strengthen Ethics & Moral Reasoning');
        console.log('4. Develop comprehensive Digital Citizenship');
        console.log('5. Add Study Skills & Meta-Learning');
        
        console.log('\n🔄 MEDIUM-TERM ENHANCEMENTS:');
        console.log('1. Expand Social-Emotional Learning');
        console.log('2. Strengthen Environmental Literacy');
        console.log('3. Add missing subcategories in core subjects');
        console.log('4. Integrate inclusive and multicultural perspectives');
        console.log('5. Bridge interdisciplinary connections');
        
        console.log('\n🌟 LONG-TERM VISION:');
        console.log('1. Ensure comprehensive coverage of 21st-century skills');
        console.log('2. Integrate emerging fields and technologies');
        console.log('3. Maintain balance between academic and practical skills');
        console.log('4. Support diverse learning needs and styles');
        console.log('5. Align with major educational standards and frameworks');
        
    } catch (error) {
        console.error('Error in subcategory analysis:', error);
    }
}

analyzeSubcategoryGaps();
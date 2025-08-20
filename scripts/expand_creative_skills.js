require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');
const { v4: uuidv4 } = require('uuid');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseServiceKey) {
    console.error('Missing environment variables. Make sure REACT_APP_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are set.');
    process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseServiceKey);

const creativeSkillsStructure = {
    "Visual Arts & Design": {
        type: "category",
        children: {
            "Fine Arts": {
                type: "category",
                children: [
                    "Drawing Fundamentals",
                    "Painting Techniques", 
                    "Sculpture Basics",
                    "Printmaking",
                    "Mixed Media Art",
                    "Art History and Analysis",
                    "Color Theory",
                    "Composition and Design Principles"
                ]
            },
            "Digital Art": {
                type: "category",
                children: [
                    "Digital Painting",
                    "3D Modeling and Sculpting",
                    "Digital Photography",
                    "Photo Editing and Retouching",
                    "Digital Illustration",
                    "Concept Art",
                    "Matte Painting",
                    "NFT and Crypto Art"
                ]
            },
            "Graphic Design": {
                type: "category",
                children: [
                    "Typography",
                    "Logo Design",
                    "Brand Identity Design",
                    "Layout and Composition",
                    "Print Design",
                    "Packaging Design",
                    "Infographic Design",
                    "Design Software Mastery"
                ]
            },
            "UI/UX Design": {
                type: "category",
                children: [
                    "User Experience Research",
                    "User Interface Design",
                    "Wireframing and Prototyping",
                    "Usability Testing",
                    "Interaction Design",
                    "Mobile App Design",
                    "Web Design Principles",
                    "Design Systems"
                ]
            }
        }
    },
    "Writing & Literature": {
        type: "category",
        children: {
            "Creative Writing": {
                type: "category",
                children: [
                    "Fiction Writing",
                    "Poetry and Verse",
                    "Screenwriting",
                    "Playwriting",
                    "Flash Fiction",
                    "Character Development",
                    "Plot Structure and Pacing",
                    "Dialogue Writing"
                ]
            },
            "Professional Writing": {
                type: "category", 
                children: [
                    "Content Writing",
                    "Copywriting",
                    "Technical Writing",
                    "Journalism",
                    "Grant Writing",
                    "Academic Writing",
                    "Business Writing",
                    "SEO Writing"
                ]
            },
            "Storytelling Techniques": {
                type: "category",
                children: [
                    "Narrative Structure",
                    "World Building",
                    "Point of View",
                    "Theme and Symbolism",
                    "Genre Writing",
                    "Editing and Revision",
                    "Publishing and Distribution",
                    "Reading Comprehension and Analysis"
                ]
            }
        }
    },
    "Performing Arts": {
        type: "category",
        children: {
            "Music": {
                type: "category",
                children: [
                    "Music Theory Fundamentals",
                    "Vocal Techniques",
                    "Instrumental Performance",
                    "Music Composition",
                    "Music Production",
                    "Audio Engineering",
                    "Music History and Appreciation",
                    "Ensemble Performance"
                ]
            },
            "Theater and Drama": {
                type: "category",
                children: [
                    "Acting Fundamentals",
                    "Method Acting",
                    "Stage Presence",
                    "Voice and Speech",
                    "Character Study",
                    "Improvisation",
                    "Stage Makeup and Costuming",
                    "Theater Direction"
                ]
            },
            "Dance and Movement": {
                type: "category",
                children: [
                    "Basic Dance Techniques",
                    "Choreography",
                    "Ballet Fundamentals",
                    "Contemporary Dance",
                    "Cultural Dance Forms",
                    "Movement Therapy",
                    "Dance History",
                    "Performance Skills"
                ]
            }
        }
    },
    "Media & Film Arts": {
        type: "category",
        children: {
            "Filmmaking": {
                type: "category",
                children: [
                    "Cinematography",
                    "Film Direction",
                    "Video Editing",
                    "Sound Design",
                    "Production Management",
                    "Documentary Filmmaking",
                    "Animation Principles",
                    "Film Theory and Criticism"
                ]
            },
            "Animation": {
                type: "category",
                children: [
                    "2D Animation",
                    "3D Animation",
                    "Stop Motion Animation",
                    "Character Animation",
                    "Motion Graphics",
                    "Visual Effects (VFX)",
                    "Storyboarding",
                    "Animation Software"
                ]
            },
            "Photography": {
                type: "category",
                children: [
                    "Camera Fundamentals",
                    "Portrait Photography",
                    "Landscape Photography",
                    "Street Photography",
                    "Commercial Photography",
                    "Photo Composition",
                    "Lighting Techniques",
                    "Photo Post-Processing"
                ]
            }
        }
    },
    "Design Thinking & Innovation": {
        type: "category",
        children: {
            "Design Process": {
                type: "category",
                children: [
                    "Design Thinking Methodology",
                    "User Research Methods",
                    "Ideation Techniques",
                    "Prototyping Methods",
                    "Design Testing and Validation",
                    "Design Documentation",
                    "Collaborative Design",
                    "Design Ethics"
                ]
            },
            "Innovation Methods": {
                type: "category",
                children: [
                    "Creative Problem Solving",
                    "Brainstorming Techniques",
                    "Lateral Thinking",
                    "SCAMPER Method",
                    "Mind Mapping",
                    "Innovation Management",
                    "Disruptive Innovation",
                    "Entrepreneurial Creativity"
                ]
            },
            "Systems Thinking": {
                type: "category", 
                children: [
                    "Systems Analysis",
                    "Complex Problem Solving",
                    "Pattern Recognition",
                    "Scenario Planning",
                    "Design for Sustainability",
                    "Service Design",
                    "Social Innovation",
                    "Future Thinking"
                ]
            }
        }
    },
    "Crafts & Applied Arts": {
        type: "category",
        children: {
            "Traditional Crafts": {
                type: "category",
                children: [
                    "Woodworking",
                    "Ceramics and Pottery",
                    "Textile Arts",
                    "Metalworking",
                    "Glassblowing",
                    "Bookbinding",
                    "Calligraphy",
                    "Embroidery and Needlework"
                ]
            },
            "Modern Making": {
                type: "category",
                children: [
                    "3D Printing",
                    "Laser Cutting",
                    "Electronics and Arduino",
                    "Robotics for Art",
                    "Wearable Technology",
                    "Interactive Installations",
                    "Maker Space Skills",
                    "Digital Fabrication"
                ]
            },
            "Fashion and Jewelry": {
                type: "category",
                children: [
                    "Fashion Design",
                    "Pattern Making",
                    "Sewing and Tailoring",
                    "Jewelry Making",
                    "Accessory Design",
                    "Fashion Illustration",
                    "Sustainable Fashion",
                    "Fashion Business"
                ]
            }
        }
    }
};

async function expandCreativeSkills() {
    try {
        console.log('Starting Creative Skills expansion...\n');
        
        // Find the Creative Skills root node
        const { data: creativeSkillsRoot, error: findError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .eq('name', 'Creative Skills')
            .single();
            
        if (findError) {
            console.error('Error finding Creative Skills root:', findError);
            return;
        }
        
        console.log('Found Creative Skills root:', creativeSkillsRoot.id);
        
        // First, remove the existing basic skills to replace with comprehensive structure
        console.log('Removing existing basic skills...');
        const { error: deleteError } = await supabase
            .from('skill_tree_nodes')
            .delete()
            .eq('parent_id', creativeSkillsRoot.id);
            
        if (deleteError) {
            console.error('Error removing existing skills:', deleteError);
            return;
        }
        
        console.log('✅ Removed existing basic skills\n');
        
        // Add the comprehensive structure
        let displayOrder = 0;
        for (const [categoryName, categoryData] of Object.entries(creativeSkillsStructure)) {
            await createCategoryHierarchy(
                categoryName, 
                categoryData, 
                creativeSkillsRoot.id, 
                displayOrder++, 
                'Creative Skills'
            );
        }
        
        console.log('\n🎉 Creative Skills expansion complete!');
        
    } catch (error) {
        console.error('Unexpected error:', error);
    }
}

async function createCategoryHierarchy(name, data, parentId, displayOrder, learningArea, depth = 0) {
    try {
        const indent = '  '.repeat(depth);
        console.log(`${indent}Creating: ${name} (${data.type})`);
        
        // Create the node
        const nodeId = uuidv4();
        const { data: newNode, error: createError } = await supabase
            .from('skill_tree_nodes')
            .insert({
                id: nodeId,
                name: name,
                type: data.type,
                parent_id: parentId,
                learning_area: 'Creative Skills',
                display_order: displayOrder,
                has_learning_content: false,
                learning_content_ids: [],
                is_menu_leaf: data.type === 'skill',
                metadata: {},
                created_at: new Date().toISOString(),
                updated_at: new Date().toISOString()
            })
            .select('id')
            .single();
            
        if (createError) {
            console.error(`${indent}Error creating ${name}:`, createError);
            return;
        }
        
        // If this has children, create them recursively
        if (data.children) {
            let childOrder = 0;
            
            if (Array.isArray(data.children)) {
                // Simple array of skill names
                for (const childName of data.children) {
                    await createCategoryHierarchy(
                        childName,
                        { type: 'skill' },
                        newNode.id,
                        childOrder++,
                        learningArea,
                        depth + 1
                    );
                }
            } else {
                // Object with nested categories
                for (const [childName, childData] of Object.entries(data.children)) {
                    await createCategoryHierarchy(
                        childName,
                        childData,
                        newNode.id,
                        childOrder++,
                        learningArea,
                        depth + 1
                    );
                }
            }
        }
        
    } catch (error) {
        console.error(`Error creating hierarchy for ${name}:`, error);
    }
}

// Run the expansion
expandCreativeSkills();
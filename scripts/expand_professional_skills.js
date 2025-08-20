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

const professionalSkillsStructure = {
    "Leadership & Management": {
        type: "category",
        children: {
            "Leadership Fundamentals": {
                type: "category",
                children: [
                    "Leadership Styles and Approaches",
                    "Emotional Intelligence",
                    "Decision Making",
                    "Conflict Resolution",
                    "Team Building",
                    "Delegation and Empowerment",
                    "Vision and Strategic Thinking",
                    "Influence and Persuasion"
                ]
            },
            "Management Skills": {
                type: "category",
                children: [
                    "Planning and Organization",
                    "Performance Management",
                    "Resource Allocation",
                    "Change Management",
                    "Risk Management",
                    "Budget Management",
                    "Quality Management",
                    "Process Improvement"
                ]
            },
            "Executive Skills": {
                type: "category",
                children: [
                    "Strategic Planning",
                    "Organizational Development",
                    "Stakeholder Management",
                    "Corporate Governance",
                    "Mergers and Acquisitions",
                    "Crisis Leadership",
                    "Board Relations",
                    "Executive Communication"
                ]
            }
        }
    },
    "Communication & Interpersonal Skills": {
        type: "category",
        children: {
            "Verbal Communication": {
                type: "category",
                children: [
                    "Public Speaking",
                    "Presentation Skills",
                    "Meeting Management",
                    "Negotiation",
                    "Sales Communication",
                    "Interview Skills",
                    "Difficult Conversations",
                    "Storytelling for Business"
                ]
            },
            "Written Communication": {
                type: "category",
                children: [
                    "Business Writing",
                    "Email Etiquette",
                    "Report Writing",
                    "Proposal Writing",
                    "Documentation Skills",
                    "Social Media Communication",
                    "Marketing Copy",
                    "Technical Writing"
                ]
            },
            "Interpersonal Skills": {
                type: "category",
                children: [
                    "Active Listening",
                    "Empathy and Emotional Awareness",
                    "Relationship Building",
                    "Networking Strategies",
                    "Cross-Cultural Communication",
                    "Customer Service",
                    "Mentoring and Coaching",
                    "Collaboration Skills"
                ]
            }
        }
    },
    "Project Management & Operations": {
        type: "category",
        children: {
            "Project Management Fundamentals": {
                type: "category",
                children: [
                    "Project Planning",
                    "Scope Management",
                    "Schedule Management",
                    "Cost Management",
                    "Quality Assurance",
                    "Risk Assessment",
                    "Stakeholder Communication",
                    "Project Closure"
                ]
            },
            "Agile and Methodologies": {
                type: "category",
                children: [
                    "Agile Project Management",
                    "Scrum Framework",
                    "Kanban Method",
                    "Waterfall Methodology",
                    "Lean Management",
                    "Six Sigma",
                    "Design Thinking Process",
                    "DevOps Practices"
                ]
            },
            "Operations Management": {
                type: "category",
                children: [
                    "Supply Chain Management",
                    "Inventory Management",
                    "Production Planning",
                    "Workflow Optimization",
                    "Vendor Management",
                    "Facility Management",
                    "Health and Safety",
                    "Environmental Compliance"
                ]
            }
        }
    },
    "Business Strategy & Analysis": {
        type: "category",
        children: {
            "Strategic Planning": {
                type: "category",
                children: [
                    "Market Analysis",
                    "Competitive Intelligence",
                    "SWOT Analysis",
                    "Business Model Development",
                    "Strategic Implementation",
                    "Performance Metrics",
                    "Innovation Strategy",
                    "Digital Transformation"
                ]
            },
            "Business Analysis": {
                type: "category",
                children: [
                    "Requirements Gathering",
                    "Process Mapping",
                    "Data Analysis",
                    "Financial Analysis",
                    "Cost-Benefit Analysis",
                    "Business Case Development",
                    "Gap Analysis",
                    "Solution Design"
                ]
            },
            "Entrepreneurship": {
                type: "category",
                children: [
                    "Business Planning",
                    "Startup Fundamentals",
                    "Fundraising",
                    "Pitch Development",
                    "Product Development",
                    "Market Validation",
                    "Scaling Strategies",
                    "Exit Planning"
                ]
            }
        }
    },
    "Digital & Technology Skills": {
        type: "category",
        children: {
            "Digital Literacy": {
                type: "category",
                children: [
                    "Computer Fundamentals",
                    "Internet and Web Skills",
                    "Digital Security",
                    "Cloud Computing Basics",
                    "Mobile Technology",
                    "Digital Collaboration Tools",
                    "Data Privacy",
                    "Digital Etiquette"
                ]
            },
            "Data and Analytics": {
                type: "category",
                children: [
                    "Excel and Spreadsheets",
                    "Data Visualization",
                    "Basic Statistics",
                    "Database Management",
                    "Business Intelligence",
                    "Reporting and Dashboards",
                    "Predictive Analytics",
                    "SQL Fundamentals"
                ]
            },
            "Emerging Technologies": {
                type: "category",
                children: [
                    "Artificial Intelligence Basics",
                    "Machine Learning Applications",
                    "Blockchain Fundamentals",
                    "Internet of Things (IoT)",
                    "Automation Tools",
                    "Virtual and Augmented Reality",
                    "Cybersecurity Awareness",
                    "Digital Marketing Technologies"
                ]
            }
        }
    },
    "Sales & Marketing": {
        type: "category",
        children: {
            "Sales Skills": {
                type: "category",
                children: [
                    "Sales Process",
                    "Lead Generation",
                    "Customer Relationship Management",
                    "Sales Presentations",
                    "Closing Techniques",
                    "Account Management",
                    "Sales Analytics",
                    "B2B vs B2C Sales"
                ]
            },
            "Marketing Fundamentals": {
                type: "category",
                children: [
                    "Market Research",
                    "Brand Development",
                    "Marketing Strategy",
                    "Campaign Planning",
                    "Content Marketing",
                    "Event Marketing",
                    "Public Relations",
                    "Marketing Analytics"
                ]
            },
            "Digital Marketing": {
                type: "category",
                children: [
                    "Search Engine Optimization (SEO)",
                    "Pay-Per-Click Advertising (PPC)",
                    "Social Media Marketing",
                    "Email Marketing",
                    "Influencer Marketing",
                    "Marketing Automation",
                    "Conversion Optimization",
                    "Online Reputation Management"
                ]
            }
        }
    },
    "Finance & Accounting": {
        type: "category",
        children: {
            "Financial Fundamentals": {
                type: "category",
                children: [
                    "Financial Statements",
                    "Budgeting and Forecasting",
                    "Cash Flow Management",
                    "Investment Analysis",
                    "Financial Planning",
                    "Tax Fundamentals",
                    "Insurance and Risk",
                    "Personal Finance"
                ]
            },
            "Corporate Finance": {
                type: "category",
                children: [
                    "Capital Structure",
                    "Valuation Methods",
                    "Mergers and Acquisitions Finance",
                    "International Finance",
                    "Financial Modeling",
                    "Corporate Treasury",
                    "Investor Relations",
                    "Financial Compliance"
                ]
            },
            "Accounting Skills": {
                type: "category",
                children: [
                    "Bookkeeping Fundamentals",
                    "Accounts Payable and Receivable",
                    "Payroll Management",
                    "Financial Reporting",
                    "Audit Preparation",
                    "Cost Accounting",
                    "Management Accounting",
                    "Accounting Software"
                ]
            }
        }
    },
    "Human Resources & People Management": {
        type: "category",
        children: {
            "Recruitment and Hiring": {
                type: "category",
                children: [
                    "Job Analysis and Design",
                    "Recruitment Strategies",
                    "Interview Techniques",
                    "Candidate Assessment",
                    "Reference Checking",
                    "Onboarding Process",
                    "Employment Law",
                    "Diversity and Inclusion"
                ]
            },
            "Employee Development": {
                type: "category",
                children: [
                    "Training Design",
                    "Performance Coaching",
                    "Career Planning",
                    "Succession Planning",
                    "Learning and Development",
                    "Skills Assessment",
                    "Mentorship Programs",
                    "Employee Engagement"
                ]
            },
            "HR Administration": {
                type: "category",
                children: [
                    "HR Policies and Procedures",
                    "Compensation and Benefits",
                    "Employee Relations",
                    "Disciplinary Procedures",
                    "Workplace Safety",
                    "HR Information Systems",
                    "Labor Relations",
                    "HR Analytics"
                ]
            }
        }
    }
};

async function expandProfessionalSkills() {
    try {
        console.log('Starting Professional Skills expansion...\n');
        
        // Find the Professional Skills root node
        const { data: professionalSkillsRoot, error: findError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .eq('name', 'Professional Skills')
            .single();
            
        if (findError) {
            console.error('Error finding Professional Skills root:', findError);
            return;
        }
        
        console.log('Found Professional Skills root:', professionalSkillsRoot.id);
        
        // First, remove the existing basic skills to replace with comprehensive structure
        console.log('Removing existing basic skills...');
        const { error: deleteError } = await supabase
            .from('skill_tree_nodes')
            .delete()
            .eq('parent_id', professionalSkillsRoot.id);
            
        if (deleteError) {
            console.error('Error removing existing skills:', deleteError);
            return;
        }
        
        console.log('✅ Removed existing basic skills\n');
        
        // Add the comprehensive structure
        let displayOrder = 0;
        for (const [categoryName, categoryData] of Object.entries(professionalSkillsStructure)) {
            await createCategoryHierarchy(
                categoryName, 
                categoryData, 
                professionalSkillsRoot.id, 
                displayOrder++, 
                'Professional Skills'
            );
        }
        
        console.log('\n🎉 Professional Skills expansion complete!');
        
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
                learning_area: 'Professional Skills',
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
expandProfessionalSkills();
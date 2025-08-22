-- Skill Tree Expansion: Phase 1 - Critical Foundations
-- Adding missing fundamental knowledge categories
-- Created: 2025-08-21

-- ===================================
-- BACKUP CURRENT STATE
-- ===================================
-- Create backup before making changes
CREATE TABLE IF NOT EXISTS skill_tree_nodes_backup_phase1 AS
SELECT * FROM skill_tree_nodes;

-- ===================================
-- 1. CIVIC EDUCATION & GOVERNMENT
-- ===================================

-- Add new top-level category: Civic Education & Government
INSERT INTO skill_tree_nodes (
    name, 
    type, 
    parent_id, 
    display_order, 
    description,
    learning_area,
    has_learning_content,
    is_menu_leaf
) VALUES (
    'Civic Education & Government',
    'category',
    NULL,
    125, -- After Test Preparation (110)
    'Essential knowledge for democratic participation and responsible citizenship',
    'Civic Studies',
    false,
    false
);

-- Get the ID of the newly created category
-- This will be used for the subcategories

-- Add major subcategories under Civic Education
DO $$
DECLARE
    civic_id UUID;
BEGIN
    -- Get the civic education category ID
    SELECT id INTO civic_id FROM skill_tree_nodes 
    WHERE name = 'Civic Education & Government' AND parent_id IS NULL;
    
    -- Insert subcategories
    INSERT INTO skill_tree_nodes (name, type, parent_id, display_order, description, learning_area, has_learning_content, is_menu_leaf) VALUES
    ('Government Structure & Functions', 'category', civic_id, 10, 'Understanding how government works at federal, state, and local levels', 'Government Studies', false, false),
    ('Constitutional Law & Rights', 'category', civic_id, 20, 'Fundamental rights, freedoms, and legal protections in democratic society', 'Constitutional Studies', false, false),
    ('Democratic Processes', 'category', civic_id, 30, 'Voting, elections, and mechanisms of democratic participation', 'Political Processes', false, false),
    ('Civic Duties & Responsibilities', 'category', civic_id, 40, 'Obligations and opportunities for civic engagement and community participation', 'Civic Engagement', false, false),
    ('Public Policy & Analysis', 'category', civic_id, 50, 'How policies are made, implemented, and their impact on society', 'Policy Studies', false, false),
    ('Community Engagement', 'category', civic_id, 60, 'Local involvement, grassroots participation, and community building', 'Community Studies', false, false);
END $$;

-- Add detailed subcategories for Government Structure & Functions
DO $$
DECLARE
    gov_structure_id UUID;
BEGIN
    SELECT id INTO gov_structure_id FROM skill_tree_nodes 
    WHERE name = 'Government Structure & Functions';
    
    INSERT INTO skill_tree_nodes (name, type, parent_id, display_order, description, has_learning_content, is_menu_leaf) VALUES
    ('Federal Government', 'skill', gov_structure_id, 10, 'Executive, Legislative, and Judicial branches of federal government', true, true),
    ('State Government', 'skill', gov_structure_id, 20, 'State-level governance, governors, state legislatures, and state courts', true, true),
    ('Local Government', 'skill', gov_structure_id, 30, 'City councils, mayors, county governments, and local services', true, true),
    ('Separation of Powers', 'skill', gov_structure_id, 40, 'Checks and balances between branches of government', true, true),
    ('Federalism', 'skill', gov_structure_id, 50, 'Division of power between federal and state governments', true, true),
    ('Bureaucracy & Public Administration', 'skill', gov_structure_id, 60, 'Government agencies, civil service, and public administration', true, true);
END $$;

-- Add detailed subcategories for Constitutional Law & Rights
DO $$
DECLARE
    constitutional_id UUID;
BEGIN
    SELECT id INTO constitutional_id FROM skill_tree_nodes 
    WHERE name = 'Constitutional Law & Rights';
    
    INSERT INTO skill_tree_nodes (name, type, parent_id, display_order, description, has_learning_content, is_menu_leaf) VALUES
    ('Bill of Rights', 'skill', constitutional_id, 10, 'First ten amendments to the Constitution and fundamental freedoms', true, true),
    ('Civil Liberties', 'skill', constitutional_id, 20, 'Individual freedoms protected from government interference', true, true),
    ('Civil Rights', 'skill', constitutional_id, 30, 'Equal protection and anti-discrimination protections', true, true),
    ('Due Process', 'skill', constitutional_id, 40, 'Legal protections in criminal and civil proceedings', true, true),
    ('Freedom of Speech & Press', 'skill', constitutional_id, 50, 'First Amendment protections and their limits', true, true),
    ('Privacy Rights', 'skill', constitutional_id, 60, 'Constitutional and legal protections of personal privacy', true, true);
END $$;

-- ===================================
-- 2. RESEARCH & INFORMATION LITERACY
-- ===================================

-- Add Research & Information Literacy under Life Skills
DO $$
DECLARE
    life_skills_id UUID;
    research_id UUID;
BEGIN
    -- Get Life Skills category ID
    SELECT id INTO life_skills_id FROM skill_tree_nodes 
    WHERE name = 'Life Skills' AND parent_id IS NULL;
    
    -- Add Research & Information Literacy category
    INSERT INTO skill_tree_nodes (
        name, 
        type, 
        parent_id, 
        display_order, 
        description,
        learning_area,
        has_learning_content,
        is_menu_leaf
    ) VALUES (
        'Research & Information Literacy',
        'category',
        life_skills_id,
        70, -- After existing Life Skills subcategories
        'Essential skills for finding, evaluating, and using information effectively',
        'Information Studies',
        false,
        false
    ) RETURNING id INTO research_id;
    
    -- Add major subcategories
    INSERT INTO skill_tree_nodes (name, type, parent_id, display_order, description, learning_area, has_learning_content, is_menu_leaf) VALUES
    ('Source Evaluation & Fact-Checking', 'category', research_id, 10, 'Determining credibility and accuracy of information sources', 'Critical Evaluation', false, false),
    ('Research Methods & Design', 'category', research_id, 20, 'Systematic approaches to investigation and inquiry', 'Research Methodology', false, false),
    ('Academic Writing & Citation', 'category', research_id, 30, 'Proper attribution and scholarly communication standards', 'Academic Communication', false, false),
    ('Information Search Strategies', 'category', research_id, 40, 'Effective techniques for finding relevant and reliable information', 'Information Retrieval', false, false),
    ('Data Analysis & Interpretation', 'category', research_id, 50, 'Understanding and working with quantitative and qualitative data', 'Data Literacy', false, false),
    ('Critical Thinking & Logic', 'category', research_id, 60, 'Reasoning skills and logical analysis for information evaluation', 'Critical Analysis', false, false);
END $$;

-- Add detailed skills for Source Evaluation & Fact-Checking
DO $$
DECLARE
    source_eval_id UUID;
BEGIN
    SELECT id INTO source_eval_id FROM skill_tree_nodes 
    WHERE name = 'Source Evaluation & Fact-Checking';
    
    INSERT INTO skill_tree_nodes (name, type, parent_id, display_order, description, has_learning_content, is_menu_leaf) VALUES
    ('Credible vs Non-credible Sources', 'skill', source_eval_id, 10, 'Identifying reliable and unreliable information sources', true, true),
    ('Bias Recognition & Analysis', 'skill', source_eval_id, 20, 'Detecting and analyzing bias in information and media', true, true),
    ('Fact-Checking Tools & Websites', 'skill', source_eval_id, 30, 'Using professional fact-checking resources effectively', true, true),
    ('Primary vs Secondary Sources', 'skill', source_eval_id, 40, 'Understanding different types of sources and their uses', true, true),
    ('Peer Review Process', 'skill', source_eval_id, 50, 'Understanding how scholarly information is vetted and validated', true, true),
    ('Authority & Expertise Assessment', 'skill', source_eval_id, 60, 'Evaluating the qualifications and credibility of authors and experts', true, true);
END $$;

-- ===================================
-- 3. DIGITAL CITIZENSHIP & MEDIA LITERACY
-- ===================================

-- Add Digital Citizenship under Technical Skills
DO $$
DECLARE
    tech_skills_id UUID;
    digital_citizenship_id UUID;
BEGIN
    -- Get Technical Skills category ID
    SELECT id INTO tech_skills_id FROM skill_tree_nodes 
    WHERE name = 'Technical Skills' AND parent_id IS NULL;
    
    -- Add Digital Citizenship & Media Literacy category
    INSERT INTO skill_tree_nodes (
        name, 
        type, 
        parent_id, 
        display_order, 
        description,
        learning_area,
        has_learning_content,
        is_menu_leaf
    ) VALUES (
        'Digital Citizenship & Media Literacy',
        'category',
        tech_skills_id,
        15, -- Early in Technical Skills
        'Responsible and informed use of digital technologies and media',
        'Digital Studies',
        false,
        false
    ) RETURNING id INTO digital_citizenship_id;
    
    -- Add major subcategories
    INSERT INTO skill_tree_nodes (name, type, parent_id, display_order, description, learning_area, has_learning_content, is_menu_leaf) VALUES
    ('Online Safety & Privacy', 'category', digital_citizenship_id, 10, 'Protecting personal information and staying safe online', 'Digital Safety', false, false),
    ('Digital Communication & Etiquette', 'category', digital_citizenship_id, 20, 'Appropriate online behavior and communication standards', 'Digital Communication', false, false),
    ('Media Analysis & Bias Detection', 'category', digital_citizenship_id, 30, 'Understanding and evaluating media messages and bias', 'Media Literacy', false, false),
    ('Digital Rights & Responsibilities', 'category', digital_citizenship_id, 40, 'Legal and ethical aspects of digital participation', 'Digital Ethics', false, false),
    ('Information Management', 'category', digital_citizenship_id, 50, 'Organizing and managing digital information effectively', 'Digital Organization', false, false),
    ('Digital Wellness', 'category', digital_citizenship_id, 60, 'Maintaining healthy relationships with technology', 'Digital Health', false, false);
END $$;

-- Add detailed skills for Online Safety & Privacy
DO $$
DECLARE
    online_safety_id UUID;
BEGIN
    SELECT id INTO online_safety_id FROM skill_tree_nodes 
    WHERE name = 'Online Safety & Privacy';
    
    INSERT INTO skill_tree_nodes (name, type, parent_id, display_order, description, has_learning_content, is_menu_leaf) VALUES
    ('Password Security & Two-Factor Authentication', 'skill', online_safety_id, 10, 'Creating strong passwords and using multi-factor authentication', true, true),
    ('Social Media Privacy Settings', 'skill', online_safety_id, 20, 'Configuring privacy controls on social media platforms', true, true),
    ('Recognizing & Avoiding Online Scams', 'skill', online_safety_id, 30, 'Identifying phishing, fraud, and other online scams', true, true),
    ('Identity Theft Prevention', 'skill', online_safety_id, 40, 'Protecting personal information from unauthorized use', true, true),
    ('Safe Online Shopping & Banking', 'skill', online_safety_id, 50, 'Secure practices for financial transactions online', true, true),
    ('Cyberbullying Recognition & Response', 'skill', online_safety_id, 60, 'Understanding and responding to online harassment', true, true);
END $$;

-- Add detailed skills for Media Analysis & Bias Detection
DO $$
DECLARE
    media_analysis_id UUID;
BEGIN
    SELECT id INTO media_analysis_id FROM skill_tree_nodes 
    WHERE name = 'Media Analysis & Bias Detection';
    
    INSERT INTO skill_tree_nodes (name, type, parent_id, display_order, description, has_learning_content, is_menu_leaf) VALUES
    ('Identifying Media Bias & Propaganda', 'skill', media_analysis_id, 10, 'Recognizing bias, propaganda, and persuasion techniques in media', true, true),
    ('Understanding Media Ownership & Influence', 'skill', media_analysis_id, 20, 'How media ownership affects content and perspective', true, true),
    ('Fake News & Misinformation Recognition', 'skill', media_analysis_id, 30, 'Identifying false or misleading information in media', true, true),
    ('Visual Media & Photo Manipulation', 'skill', media_analysis_id, 40, 'Understanding how images and videos can be altered or misleading', true, true),
    ('Algorithm Influence on Content', 'skill', media_analysis_id, 50, 'How algorithms shape what content we see online', true, true),
    ('Comparing Multiple News Sources', 'skill', media_analysis_id, 60, 'Using multiple sources to get complete and accurate information', true, true);
END $$;

-- ===================================
-- 4. SOCIAL-EMOTIONAL LEARNING EXPANSION
-- ===================================

-- Add comprehensive SEL categories under Life Skills
DO $$
DECLARE
    life_skills_id UUID;
BEGIN
    -- Get Life Skills category ID
    SELECT id INTO life_skills_id FROM skill_tree_nodes 
    WHERE name = 'Life Skills' AND parent_id IS NULL;
    
    -- Add new SEL categories
    INSERT INTO skill_tree_nodes (name, type, parent_id, display_order, description, learning_area, has_learning_content, is_menu_leaf) VALUES
    ('Self-Awareness & Self-Management', 'category', life_skills_id, 15, 'Understanding and regulating emotions and behaviors', 'Social-Emotional Learning', false, false),
    ('Social Awareness & Empathy', 'category', life_skills_id, 25, 'Understanding others and developing compassion', 'Social-Emotional Learning', false, false),
    ('Relationship Skills', 'category', life_skills_id, 35, 'Building and maintaining healthy relationships', 'Social-Emotional Learning', false, false),
    ('Responsible Decision-Making', 'category', life_skills_id, 45, 'Making ethical and constructive choices', 'Social-Emotional Learning', false, false),
    ('Mental Health & Wellness', 'category', life_skills_id, 55, 'Understanding and maintaining psychological well-being', 'Social-Emotional Learning', false, false);
END $$;

-- ===================================
-- 5. ETHICS EXPANSION
-- ===================================

-- Expand Philosophy with comprehensive Ethics
DO $$
DECLARE
    philosophy_id UUID;
BEGIN
    -- Get Philosophy category ID (under Humanities)
    SELECT id INTO philosophy_id FROM skill_tree_nodes 
    WHERE name = 'Philosophy';
    
    -- Add new Ethics subcategories
    INSERT INTO skill_tree_nodes (name, type, parent_id, display_order, description, learning_area, has_learning_content, is_menu_leaf) VALUES
    ('Ethical Frameworks & Theories', 'category', philosophy_id, 15, 'Major approaches to moral reasoning and decision-making', 'Ethics', false, false),
    ('Applied Ethics', 'category', philosophy_id, 25, 'Ethics in specific contexts, professions, and real-world situations', 'Ethics', false, false),
    ('Moral Psychology & Development', 'category', philosophy_id, 35, 'How moral reasoning develops and functions in individuals', 'Ethics', false, false),
    ('Character & Virtue Development', 'category', philosophy_id, 45, 'Building moral character and ethical habits', 'Ethics', false, false),
    ('Ethics in Technology & Science', 'category', philosophy_id, 55, 'Ethical considerations in modern technological and scientific fields', 'Ethics', false, false);
END $$;

-- ===================================
-- VERIFICATION QUERIES
-- ===================================

-- Verify new top-level categories
SELECT name, display_order, description 
FROM skill_tree_nodes 
WHERE parent_id IS NULL 
ORDER BY display_order;

-- Verify Civic Education structure
SELECT stn.name, stn.type, stn.display_order, stn.description,
       parent.name as parent_name
FROM skill_tree_nodes stn
LEFT JOIN skill_tree_nodes parent ON stn.parent_id = parent.id
WHERE stn.name LIKE '%Civic%' OR parent.name LIKE '%Civic%'
ORDER BY stn.display_order;

-- Verify Research & Information Literacy structure
SELECT stn.name, stn.type, stn.display_order, stn.description,
       parent.name as parent_name
FROM skill_tree_nodes stn
LEFT JOIN skill_tree_nodes parent ON stn.parent_id = parent.id
WHERE stn.name LIKE '%Research%' OR parent.name LIKE '%Research%'
ORDER BY stn.display_order;

-- Verify Digital Citizenship structure
SELECT stn.name, stn.type, stn.display_order, stn.description,
       parent.name as parent_name
FROM skill_tree_nodes stn
LEFT JOIN skill_tree_nodes parent ON stn.parent_id = parent.id
WHERE stn.name LIKE '%Digital%' OR parent.name LIKE '%Digital%'
ORDER BY stn.display_order;

-- Check total node count after additions
SELECT 
    COUNT(*) as total_nodes,
    COUNT(CASE WHEN type = 'category' THEN 1 END) as categories,
    COUNT(CASE WHEN type = 'skill' THEN 1 END) as skills
FROM skill_tree_nodes;

-- ===================================
-- ROLLBACK INSTRUCTIONS
-- ===================================

-- If needed to rollback changes:
-- DROP TABLE skill_tree_nodes;
-- ALTER TABLE skill_tree_nodes_backup_phase1 RENAME TO skill_tree_nodes;

-- ===================================
-- SUCCESS MESSAGE
-- ===================================
DO $$
BEGIN
    RAISE NOTICE 'Phase 1 fundamental categories successfully added to skill tree!';
    RAISE NOTICE 'Added: Civic Education & Government, Research & Information Literacy, Digital Citizenship & Media Literacy';
    RAISE NOTICE 'Expanded: Social-Emotional Learning, Ethics & Moral Reasoning';
    RAISE NOTICE 'Backup table created: skill_tree_nodes_backup_phase1';
END $$;
require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function analyzeSkillGaps() {
    try {
        console.log('🎯 SKILL TREE GAP ANALYSIS\n');
        
        // Get top-level categories
        const { data: topLevel, error: topError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type')
            .is('parent_id', null)
            .order('name');
            
        if (topError) throw topError;
        
        console.log('=== CURRENT TOP-LEVEL CATEGORIES ===');
        topLevel.forEach((node, index) => {
            console.log(`${index + 1}. ${node.name}`);
        });
        
        // Get second level to see structure
        const topLevelIds = topLevel.map(n => n.id);
        const { data: secondLevel, error: secondError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, type, parent_id')
            .in('parent_id', topLevelIds)
            .order('name');
            
        if (secondError) throw secondError;
        
        console.log('\n=== CURRENT STRUCTURE BY CATEGORY ===');
        topLevel.forEach(parent => {
            const children = secondLevel.filter(child => child.parent_id === parent.id);
            console.log(`\n📁 ${parent.name} (${children.length} subcategories):`);
            children.slice(0, 10).forEach(child => {
                console.log(`   • ${child.name}`);
            });
            if (children.length > 10) {
                console.log(`   ... and ${children.length - 10} more`);
            }
        });
        
        // Get total counts
        const { count: totalNodes } = await supabase
            .from('skill_tree_nodes')
            .select('*', { count: 'exact', head: true });
            
        const { count: skillNodes } = await supabase
            .from('skill_tree_nodes')
            .select('*', { count: 'exact', head: true })
            .eq('type', 'skill');
            
        const { count: categoryNodes } = await supabase
            .from('skill_tree_nodes')
            .select('*', { count: 'exact', head: true })
            .eq('type', 'category');
        
        console.log('\n=== DATABASE STATISTICS ===');
        console.log(`Total nodes: ${totalNodes}`);
        console.log(`Skills: ${skillNodes}`);
        console.log(`Categories: ${categoryNodes}`);
        console.log(`Top-level categories: ${topLevel.length}`);
        
        // Analyze gaps based on standard educational frameworks
        console.log('\n=== GAP ANALYSIS ===');
        
        const currentCategories = topLevel.map(c => c.name.toLowerCase());
        
        // Standard academic subjects that should be present
        const expectedAcademicAreas = [
            'mathematics',
            'natural sciences', 
            'social sciences',
            'humanities',
            'languages',
            'computer science',
            'applied sciences'
        ];
        
        // Life skills and modern competencies
        const expectedLifeSkills = [
            'life skills',
            'critical thinking',
            'communication',
            'financial literacy',
            'health and wellness',
            'civic education',
            'digital citizenship'
        ];
        
        // Professional and career skills
        const expectedProfessionalSkills = [
            'professional skills',
            'entrepreneurship',
            'leadership',
            'project management',
            'technical skills'
        ];
        
        // Creative and artistic areas
        const expectedCreativeAreas = [
            'creative skills',
            'performing arts',
            'visual arts',
            'media arts',
            'design'
        ];
        
        // Assessment and testing
        const expectedAssessmentAreas = [
            'test preparation and assessment',
            'standardized testing',
            'cognitive assessment'
        ];
        
        console.log('✅ WELL-COVERED AREAS:');
        const allExpected = [
            ...expectedAcademicAreas,
            ...expectedLifeSkills,
            ...expectedProfessionalSkills,
            ...expectedCreativeAreas,
            ...expectedAssessmentAreas
        ];
        
        const covered = allExpected.filter(expected => 
            currentCategories.some(current => 
                current.includes(expected.split(' ')[0]) || 
                expected.split(' ').some(word => current.includes(word))
            )
        );
        
        covered.forEach(area => console.log(`   • ${area}`));
        
        console.log('\n⚠️  POTENTIAL GAPS TO INVESTIGATE:');
        
        // Check for missing fundamental areas
        const gaps = [];
        
        // Academic gaps
        if (!currentCategories.some(c => c.includes('civic') || c.includes('government') || c.includes('citizenship'))) {
            gaps.push({
                area: 'Civic Education & Government',
                importance: 'Essential for democratic participation and understanding rights/responsibilities',
                suggestion: 'Add as separate category or expand Social Sciences'
            });
        }
        
        if (!currentCategories.some(c => c.includes('logic') || c.includes('reasoning'))) {
            gaps.push({
                area: 'Logic & Formal Reasoning',
                importance: 'Foundation for critical thinking, mathematics, and philosophy',
                suggestion: 'Add as category bridging Mathematics and Philosophy'
            });
        }
        
        if (!currentCategories.some(c => c.includes('research') || c.includes('information'))) {
            gaps.push({
                area: 'Research & Information Literacy',
                importance: 'Critical skill for lifelong learning and academic success',
                suggestion: 'Add as category or expand Life Skills'
            });
        }
        
        if (!currentCategories.some(c => c.includes('ethics') || c.includes('moral'))) {
            gaps.push({
                area: 'Ethics & Moral Philosophy',
                importance: 'Foundation for decision-making and character development',
                suggestion: 'Add as category or expand Philosophy/Life Skills'
            });
        }
        
        // Life skills gaps
        if (!currentCategories.some(c => c.includes('social') && c.includes('emotional'))) {
            gaps.push({
                area: 'Social-Emotional Learning (SEL)',
                importance: 'Critical for mental health, relationships, and success',
                suggestion: 'Add as separate category or expand Life Skills'
            });
        }
        
        if (!currentCategories.some(c => c.includes('digital') && c.includes('citizenship'))) {
            gaps.push({
                area: 'Digital Citizenship & Online Safety',
                importance: 'Essential in digital age for safety and responsible technology use',
                suggestion: 'Add as category or expand Technical Skills'
            });
        }
        
        if (!currentCategories.some(c => c.includes('environmental') && c.includes('sustainability'))) {
            gaps.push({
                area: 'Environmental Literacy & Sustainability',
                importance: 'Critical for understanding global challenges and responsible living',
                suggestion: 'Add as category or expand Environmental Science'
            });
        }
        
        // STEM integration gaps
        if (!currentCategories.some(c => c.includes('engineering') && c.includes('design'))) {
            gaps.push({
                area: 'Engineering Design & STEM Integration',
                importance: 'Bridges theory and application, essential for innovation',
                suggestion: 'Add as category bridging Applied Sciences and Technical Skills'
            });
        }
        
        // Modern literacy gaps
        if (!currentCategories.some(c => c.includes('media') && c.includes('literacy'))) {
            gaps.push({
                area: 'Media Literacy & Critical Analysis',
                importance: 'Essential for navigating information age and avoiding misinformation',
                suggestion: 'Add as category or expand Critical Thinking'
            });
        }
        
        if (!currentCategories.some(c => c.includes('global') || c.includes('cultural'))) {
            gaps.push({
                area: 'Global Competency & Cultural Awareness',
                importance: 'Critical for success in interconnected world',
                suggestion: 'Add as category or expand Social Sciences'
            });
        }
        
        // Career preparation gaps
        if (!currentCategories.some(c => c.includes('career') || c.includes('college'))) {
            gaps.push({
                area: 'College & Career Readiness',
                importance: 'Essential bridge between education and life preparation',
                suggestion: 'Add as category or expand Life Skills/Professional Skills'
            });
        }
        
        // Special populations
        if (!currentCategories.some(c => c.includes('special') || c.includes('inclusive'))) {
            gaps.push({
                area: 'Inclusive Education & Accessibility',
                importance: 'Ensures education is accessible to learners with diverse needs',
                suggestion: 'Consider how to make all categories accessible and inclusive'
            });
        }
        
        gaps.forEach((gap, index) => {
            console.log(`\n${index + 1}. ${gap.area}`);
            console.log(`   Why important: ${gap.importance}`);
            console.log(`   Suggestion: ${gap.suggestion}`);
        });
        
        console.log('\n=== RECOMMENDATIONS ===');
        console.log('1. Consider adding missing fundamental areas as new top-level categories');
        console.log('2. Evaluate if current categories can be expanded to include missing areas');
        console.log('3. Ensure balance between academic, practical, and life skills');
        console.log('4. Consider modern literacy and 21st-century skills integration');
        console.log('5. Review against major educational frameworks (Common Core, UNESCO, etc.)');
        
        return { topLevel, secondLevel, gaps };
        
    } catch (error) {
        console.error('Error analyzing skill gaps:', error);
    }
}

analyzeSkillGaps();
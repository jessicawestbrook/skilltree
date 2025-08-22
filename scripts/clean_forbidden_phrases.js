const { createClient } = require('@supabase/supabase-js');
const Anthropic = require('@anthropic-ai/sdk');
require('dotenv').config({ path: '.env.local' });

class ForbiddenPhrasesCleaner {
    constructor() {
        this.supabase = createClient(
            process.env.REACT_APP_SUPABASE_URL,
            process.env.SUPABASE_SERVICE_ROLE_KEY
        );
        
        this.anthropic = new Anthropic({
            apiKey: process.env.ANTHROPIC_API_KEY,
        });
        
        this.processedCount = 0;
        this.successCount = 0;
        this.errorCount = 0;
        this.apiDelay = 1000;
        
        // Define forbidden phrases to target
        this.forbiddenPhrases = [
            'dive into',
            'delve into',
            'discover',
            'uncover',
            'unlock',
            'unleash',
            'embark',
            'explore',
            'captivating',
            'fascinating',
            'dynamic world',
            'art of',
            'secrets of',
            'intricate world',
            'vibrant world',
            'rich tapestry',
            'intriguing world',
            'hands-on',
            'hands on',
            'hands-on learning',
            'practical experience',
            'hands-on activities',
            'interactive learning',
            'experiential learning',
            'become a professional',
            'become an expert',
            'master the art',
            'become a master',
            'professional level',
            'expert level',
            'industry professional',
            'career as a',
            'launch your career',
            'become proficient',
            'professional mastery',
            'expert mastery',
            'achieve mastery',
            'complete mastery',
            'full mastery',
            'total mastery',
            'mastery of',
            'master of',
            'expertise in',
            'professional expertise',
            'become certified',
            'certification in',
            'professional certification',
            'this course examines',
            'this course covers',
            'students will study',
            'this topic explores',
            'this course introduces',
            'students will learn'
        ];
    }

    logProgress(message) {
        const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
        console.log(`[${timestamp}] ${message}`);
    }

    containsForbiddenPhrases(description) {
        if (!description) return false;
        const descLower = description.toLowerCase();
        return this.forbiddenPhrases.some(phrase => descLower.includes(phrase));
    }

    async getNodesWithForbiddenPhrases(limit = 50) {
        try {
            // Get all nodes with descriptions
            const { data: nodes, error } = await this.supabase
                .from('skill_tree_nodes')
                .select('id, name, parent_id, description')
                .not('description', 'is', null)
                .neq('description', '')
                .limit(1000); // Get more to filter

            if (error) throw error;

            // Filter for nodes containing forbidden phrases
            const problematicNodes = nodes.filter(node => 
                this.containsForbiddenPhrases(node.description)
            );

            return problematicNodes.slice(0, limit);
        } catch (error) {
            this.logProgress(`Error fetching nodes with forbidden phrases: ${error.message}`);
            return [];
        }
    }

    determineTargetAudience(nodeName, parentName = null) {
        const nodeNameLower = nodeName.toLowerCase();
        const parentNameLower = parentName ? parentName.toLowerCase() : '';

        // Elementary/Primary subjects (younger children)
        const elementarySubjects = [
            'elementary', 'primary', 'basic math', 'counting', 'addition', 'subtraction',
            'multiplication', 'division', 'fractions', 'decimals', 'shapes', 'colors',
            'alphabet', 'phonics', 'reading', 'simple', 'beginning', 'intro'
        ];

        // Teen subjects  
        const teenSubjects = [
            'algebra', 'geometry', 'pre-calculus', 'trigonometry', 'physics', 'chemistry',
            'biology', 'world history', 'us history', 'geography', 'literature',
            'spanish', 'french', 'german', 'foreign language', 'language', 'programming',
            'classic', 'novel', 'poetry', 'modernist', 'victorian', 'contemporary'
        ];

        // Adult/Professional subjects
        const adultSubjects = [
            'business', 'finance', 'marketing', 'management', 'economics', 'accounting',
            'psychology', 'philosophy', 'advanced', 'graduate', 'professional', 'career',
            'investment', 'entrepreneurship', 'leadership', 'statistics', 'calculus',
            'engineering', 'computer science', 'data science', 'machine learning',
            'artificial intelligence', 'law', 'medicine', 'research'
        ];

        if (elementarySubjects.some(elem => nodeNameLower.includes(elem) || parentNameLower.includes(elem))) {
            return 'younger children (ages 6-10)';
        }

        if (adultSubjects.some(adult => nodeNameLower.includes(adult) || parentNameLower.includes(adult))) {
            return 'adults and professionals';
        }

        if (teenSubjects.some(teen => nodeNameLower.includes(teen) || parentNameLower.includes(teen))) {
            return 'teens and young adults (ages 13-18)';
        }

        return 'students and lifelong learners';
    }

    async cleanDescription(nodeName, currentDescription, parentName = null) {
        const targetAudience = this.determineTargetAudience(nodeName, parentName);
        const contextInfo = parentName ? `Part of: ${parentName}` : 'Top-level category';
        
        const prompt = `Rewrite this description to be more direct and factual. CRITICAL: Do NOT start with "This course" or "Students will" - start directly with the topic name or subject matter.

Current description: "${currentDescription}"

Topic: "${nodeName}"
Context: ${contextInfo}
Target Audience: ${targetAudience}

CRITICAL REQUIREMENTS:
- NEVER start with "This course covers/examines/introduces"
- NEVER start with "Students will study/learn/explore"
- NEVER start with "This topic explores/covers"
- START DIRECTLY with the topic name or key concepts
- Be direct and factual about what the content covers
- Keep it 1-3 sentences (50-150 words maximum)
- Remove all marketing language (captivating, fascinating, dynamic, etc.)
- No assumptions about hands-on activities (online platform only)
- No promises of professional outcomes or mastery
- Write for ${targetAudience}

GOOD EXAMPLES:
- "Ancient Rome was a civilization that..."
- "Algebra involves mathematical operations with variables..."  
- "Photosynthesis is the process by which plants..."
- "The Civil War occurred between 1861 and 1865..."

BAD EXAMPLES (DO NOT USE):
- "This course examines Ancient Rome..."
- "Students will study algebra..."
- "This topic explores photosynthesis..."
- "Learn about the Civil War..."

Return ONLY the cleaned description text, no formatting or extra text.`;

        try {
            this.logProgress(`Cleaning description for: ${nodeName}`);
            
            const response = await this.anthropic.messages.create({
                model: "claude-3-haiku-20240307",
                max_tokens: 300,
                temperature: 0.3,
                messages: [{ role: "user", content: prompt }]
            });
            
            let cleanedDescription = response.content[0].text.trim();
            
            if (cleanedDescription.startsWith('"') && cleanedDescription.endsWith('"')) {
                cleanedDescription = cleanedDescription.slice(1, -1);
            }
            
            return cleanedDescription;
                
        } catch (error) {
            this.logProgress(`Error cleaning description for ${nodeName}: ${error.message}`);
            return null;
        }
    }

    async getParentName(parentId) {
        if (!parentId) return null;

        try {
            const { data, error } = await this.supabase
                .from('skill_tree_nodes')
                .select('name')
                .eq('id', parentId)
                .single();

            if (error) throw error;
            return data?.name || null;
        } catch (error) {
            this.logProgress(`Error getting parent name for ${parentId}: ${error.message}`);
            return null;
        }
    }

    async saveCleanedDescription(nodeId, description) {
        try {
            const { data, error } = await this.supabase
                .from('skill_tree_nodes')
                .update({
                    description: description,
                    updated_at: new Date().toISOString()
                })
                .eq('id', nodeId);

            if (error) throw error;
            return true;
        } catch (error) {
            this.logProgress(`Database error saving description for ${nodeId}: ${error.message}`);
            return false;
        }
    }

    async processBatch(batchSize = 10) {
        const nodes = await this.getNodesWithForbiddenPhrases(batchSize);

        if (nodes.length === 0) {
            this.logProgress('No more nodes found with forbidden phrases!');
            return false;
        }

        this.logProgress(`Processing batch of ${nodes.length} nodes with forbidden phrases...`);

        let batchSuccess = 0;
        let batchErrors = 0;

        for (const node of nodes) {
            this.processedCount++;
            const { name: nodeName, id: nodeId, parent_id: parentId, description: currentDescription } = node;

            // Get parent name for context
            const parentName = parentId ? await this.getParentName(parentId) : null;

            // Clean the description
            const cleanedDescription = await this.cleanDescription(nodeName, currentDescription, parentName);

            if (cleanedDescription) {
                // Save to database
                if (await this.saveCleanedDescription(nodeId, cleanedDescription)) {
                    this.successCount++;
                    batchSuccess++;
                    this.logProgress(`CLEANED ${nodeName}:`);
                    this.logProgress(`  BEFORE: ${currentDescription.substring(0, 80)}...`);
                    this.logProgress(`  AFTER:  ${cleanedDescription.substring(0, 80)}...`);
                } else {
                    this.errorCount++;
                    batchErrors++;
                    this.logProgress(`ERROR Failed to save cleaned description for ${nodeName}`);
                }
            } else {
                this.errorCount++;
                batchErrors++;
                this.logProgress(`ERROR Failed to clean description for ${nodeName}`);
            }

            // Rate limiting
            if (node !== nodes[nodes.length - 1]) {
                await new Promise(resolve => setTimeout(resolve, this.apiDelay));
            }
        }

        this.logProgress(`Batch complete: ${batchSuccess} cleaned, ${batchErrors} errors`);
        return true;
    }

    async cleanAllForbiddenPhrases(maxBatches = 20) {
        this.logProgress('Starting cleanup of forbidden phrases...');

        let batchesProcessed = 0;

        while (batchesProcessed < maxBatches) {
            batchesProcessed++;
            this.logProgress(`\nBATCH ${batchesProcessed}`);

            const hasMore = await this.processBatch(10);

            if (!hasMore) {
                this.logProgress('All forbidden phrases cleaned!');
                break;
            }

            this.logProgress(`Overall Progress: ${this.successCount} cleaned, ${this.errorCount} errors`);

            if (batchesProcessed < maxBatches) {
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
        }

        this.logProgress(`\nFINAL CLEANUP SUMMARY:`);
        this.logProgress(`  Batches processed: ${batchesProcessed}`);
        this.logProgress(`  Total nodes processed: ${this.processedCount}`);
        this.logProgress(`  Successfully cleaned: ${this.successCount}`);
        this.logProgress(`  Errors: ${this.errorCount}`);

        if (this.processedCount > 0) {
            const successRate = (this.successCount / this.processedCount) * 100;
            this.logProgress(`  Success rate: ${successRate.toFixed(1)}%`);
        }
    }
}

async function main() {
    console.log('Forbidden Phrases Cleaner');
    console.log('='.repeat(50));

    try {
        const cleaner = new ForbiddenPhrasesCleaner();

        // Check how many nodes have forbidden phrases
        const nodesWithForbidden = await cleaner.getNodesWithForbiddenPhrases(1000);
        console.log(`\nFound ${nodesWithForbidden.length} nodes with forbidden marketing phrases`);

        if (nodesWithForbidden.length === 0) {
            console.log('All descriptions are clean!');
            return;
        }

        console.log('\nStarting cleanup process...');
        await cleaner.cleanAllForbiddenPhrases(20);

    } catch (error) {
        console.error('Error:', error.message);
        console.error('Stack:', error.stack);
    }
}

main().catch(console.error);
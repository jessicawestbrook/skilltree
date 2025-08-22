const { createClient } = require('@supabase/supabase-js');
const Anthropic = require('@anthropic-ai/sdk');
require('dotenv').config({ path: '.env.local' });

class ProperDescriptionGenerator {
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
        this.apiDelay = 800; // 0.8 seconds between API calls
    }

    logProgress(message) {
        const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
        console.log(`[${timestamp}] ${message}`);
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

        // Check for elementary subjects
        if (elementarySubjects.some(elem => nodeNameLower.includes(elem) || parentNameLower.includes(elem))) {
            return 'younger children (ages 6-10)';
        }

        // Check for adult/professional subjects
        if (adultSubjects.some(adult => nodeNameLower.includes(adult) || parentNameLower.includes(adult))) {
            return 'adults and professionals';
        }

        // Check for teen subjects or default to teens for most academic subjects
        if (teenSubjects.some(teen => nodeNameLower.includes(teen) || parentNameLower.includes(teen))) {
            return 'teens and young adults (ages 13-18)';
        }

        // Default to general learners for unclassified topics
        return 'students and lifelong learners';
    }

    async generateDescription(nodeName, parentName = null) {
        const targetAudience = this.determineTargetAudience(nodeName, parentName);
        const contextInfo = parentName ? `Part of: ${parentName}` : 'Top-level category';
        
        const prompt = `Create a concise, engaging description for the learning topic: "${nodeName}"

Context: ${contextInfo}
Target Audience: ${targetAudience}

Requirements:
1. Write 1-3 sentences (50-150 words maximum)
2. Be specific to "${nodeName}" - avoid generic language
3. Mention concrete concepts, skills, or applications unique to this topic
4. Target the language and complexity level for ${targetAudience}
5. Make it sound interesting and educational for this age group
6. Be accurate and factual
7. Focus on what learners will actually understand or be able to do

AVOID these overused phrases - DO NOT USE ANY OF THESE:
- "building blocks", "foundation", "unlock the power"
- "dive into", "explore", "master", "essential skills"
- "real-world applications", "complex problems"
- "logical thinking", "problem-solving"
- "captivating", "fascinating", "discover", "delve into"
- "unleash", "embark", "uncover", "immerse yourself"
- "dynamic world", "art of", "secrets of"

WRITING STYLE:
- Avoid adjectives like "amazing", "incredible", "powerful", "innovative", "cutting-edge"
- Use concrete nouns and active verbs instead of descriptive adjectives
- Focus on WHAT students will learn and DO, not how "wonderful" it is
- Be factual and specific rather than promotional

Return ONLY the description text, no formatting or extra text.`;

        try {
            this.logProgress(`Generating description for: ${nodeName}`);
            
            const response = await this.anthropic.messages.create({
                model: "claude-3-haiku-20240307",
                max_tokens: 300,
                temperature: 0.7,
                messages: [{ role: "user", content: prompt }]
            });
            
            let description = response.content[0].text.trim();
            
            // Clean up the description - remove quotes if present
            if (description.startsWith('"') && description.endsWith('"')) {
                description = description.slice(1, -1);
            }
            
            return description;
                
        } catch (error) {
            this.logProgress(`Error generating description for ${nodeName}: ${error.message}`);
            return null;
        }
    }

    async getNodesWithBadDescriptions(limit = 10) {
        try {
            // Get nodes with terrible generic descriptions or null descriptions
            const { data: nodes, error } = await this.supabase
                .from('skill_tree_nodes')
                .select('id, name, parent_id, description')
                .or('description.like.Learning content for%,description.is.null,description.eq.')
                .limit(limit);

            if (error) throw error;
            return nodes || [];
        } catch (error) {
            this.logProgress(`Error fetching nodes with bad descriptions: ${error.message}`);
            return [];
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

    async saveDescription(nodeId, description) {
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

    async processBatch(batchSize = 100) {
        const nodes = await this.getNodesWithBadDescriptions(batchSize);

        if (nodes.length === 0) {
            this.logProgress('No more nodes found with bad descriptions!');
            return false;
        }

        this.logProgress(`Processing batch of ${nodes.length} nodes...`);

        let batchSuccess = 0;
        let batchErrors = 0;

        for (const node of nodes) {
            this.processedCount++;
            const { name: nodeName, id: nodeId, parent_id: parentId } = node;

            // Get parent name for context
            const parentName = parentId ? await this.getParentName(parentId) : null;

            // Generate description using Claude API
            const description = await this.generateDescription(nodeName, parentName);

            if (description) {
                // Save to database
                if (await this.saveDescription(nodeId, description)) {
                    this.successCount++;
                    batchSuccess++;
                    this.logProgress(`SUCCESS ${nodeName}: ${description.substring(0, 100)}...`);
                } else {
                    this.errorCount++;
                    batchErrors++;
                    this.logProgress(`ERROR Failed to save description for ${nodeName}`);
                }
            } else {
                this.errorCount++;
                batchErrors++;
                this.logProgress(`ERROR Failed to generate description for ${nodeName}`);
            }

            // Rate limiting
            if (node !== nodes[nodes.length - 1]) {
                await new Promise(resolve => setTimeout(resolve, this.apiDelay));
            }
        }

        this.logProgress(`Batch complete: ${batchSuccess} successful, ${batchErrors} errors`);
        return true;
    }

    async generateProperDescriptions(maxBatches = 50) {
        this.logProgress('Starting proper description generation with Claude API...');

        let batchesProcessed = 0;

        while (batchesProcessed < maxBatches) {
            batchesProcessed++;
            this.logProgress(`\nBATCH ${batchesProcessed}`);

            const hasMore = await this.processBatch(100); // Larger batches for faster processing

            if (!hasMore) {
                this.logProgress('All bad descriptions have been replaced!');
                break;
            }

            this.logProgress(`Overall Progress: ${this.successCount} successful, ${this.errorCount} errors`);

            // Brief pause between batches
            if (batchesProcessed < maxBatches) {
                await new Promise(resolve => setTimeout(resolve, 2000)); // 2 seconds between batches
            }
        }

        this.logProgress(`\nFINAL SUMMARY:`);
        this.logProgress(`  Batches processed: ${batchesProcessed}`);
        this.logProgress(`  Total nodes processed: ${this.processedCount}`);
        this.logProgress(`  Successful: ${this.successCount}`);
        this.logProgress(`  Errors: ${this.errorCount}`);

        if (this.processedCount > 0) {
            const successRate = (this.successCount / this.processedCount) * 100;
            this.logProgress(`  Success rate: ${successRate.toFixed(1)}%`);
        }
    }
}

async function main() {
    console.log('Proper Description Generator with Claude API');
    console.log('='.repeat(50));

    try {
        const generator = new ProperDescriptionGenerator();

        // Check how many nodes have bad descriptions
        const nodesWithBadDesc = await generator.getNodesWithBadDescriptions(1000);
        const totalBad = nodesWithBadDesc.length;

        console.log(`\nFound ${totalBad} nodes with terrible generic descriptions`);

        if (totalBad === 0) {
            console.log('All nodes already have proper descriptions!');
            return;
        }

        console.log('\nStarting proper generation process with Claude API...');
        await generator.generateProperDescriptions(50);

    } catch (error) {
        console.error('Error:', error.message);
        console.error('Stack:', error.stack);
    }
}

main().catch(console.error);
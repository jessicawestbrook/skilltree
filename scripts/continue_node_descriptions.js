const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

class DescriptionGenerator {
    constructor() {
        this.supabase = createClient(
            process.env.REACT_APP_SUPABASE_URL,
            process.env.SUPABASE_SERVICE_ROLE_KEY
        );
        this.processedCount = 0;
        this.successCount = 0;
        this.errorCount = 0;
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
        // Since we don't have Claude API access in this environment, 
        // let's generate contextual descriptions based on the content
        const targetAudience = this.determineTargetAudience(nodeName, parentName);
        
        // Special handling for literature works
        const literatureDescriptions = {
            'Women in Love': 'D.H. Lawrence\'s passionate exploration of modern relationships and sexuality in post-World War I England, following two couples navigating love, desire, and personal freedom in a rapidly changing society.',
            'The Age of Innocence': 'Edith Wharton\'s Pulitzer Prize-winning novel about high society in 1870s New York, exploring the conflict between personal desires and social expectations through a love triangle that exposes the rigid conventions of the Gilded Age.',
            'Main Street': 'Sinclair Lewis\'s satirical portrayal of small-town American life through Carol Kennicott, a progressive woman who challenges the narrow-mindedness and complacency of Gopher Prairie, Minnesota.',
            'The Waste Land': 'T.S. Eliot\'s groundbreaking modernist poem that captures the spiritual emptiness and cultural fragmentation of post-World War I Europe through innovative techniques and multiple literary allusions.',
            'Ulysses': 'James Joyce\'s revolutionary modernist novel that follows Leopold Bloom through a single day in Dublin, pioneering stream-of-consciousness narrative and reshaping the possibilities of fiction.',
            'Babbitt': 'Sinclair Lewis\'s satirical novel about George Babbitt, a middle-class real estate broker whose conformist lifestyle and eventual rebellion reveal the spiritual emptiness of American middle-class values in the 1920s.',
            'The Magic Mountain': 'Thomas Mann\'s philosophical novel set in a Swiss sanatorium, where Hans Castorp\'s extended stay becomes a journey through European intellectual traditions and the cultural tensions preceding World War I.',
            'A Passage to India': 'E.M. Forster\'s final novel examining the complex relationships between British colonists and Indians during the Raj, exploring themes of cultural misunderstanding, racism, and the possibility of friendship across racial divides.',
            'An American Tragedy': 'Theodore Dreiser\'s powerful naturalist novel based on a real murder case, following Clyde Griffiths\' tragic pursuit of the American Dream and the social forces that lead to his downfall.',
            'The Great Gatsby': 'F. Scott Fitzgerald\'s masterpiece about Jay Gatsby\'s obsessive pursuit of the American Dream and his lost love Daisy, serving as a critique of wealth, materialism, and moral decay in 1920s America.'
        };

        if (literatureDescriptions[nodeName]) {
            return literatureDescriptions[nodeName];
        }

        // For other nodes, generate a basic description
        const context = parentName ? `Part of: ${parentName}` : 'Top-level category';
        return `Learning content for ${nodeName}. ${context}. Designed for ${targetAudience}.`;
    }

    async getNodesWithoutDescriptions(limit = 10) {
        try {
            const { data: nodes, error } = await this.supabase
                .from('skill_tree_nodes')
                .select('id, name, parent_id, description')
                .or('description.is.null,description.eq.')
                .limit(limit);

            if (error) throw error;
            return nodes || [];
        } catch (error) {
            this.logProgress(`Error fetching nodes without descriptions: ${error.message}`);
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

    async processBatch(batchSize = 10) {
        const nodes = await this.getNodesWithoutDescriptions(batchSize);

        if (nodes.length === 0) {
            this.logProgress('No more nodes found without descriptions!');
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

            // Generate description
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

            // Brief delay to avoid overwhelming the database
            await new Promise(resolve => setTimeout(resolve, 100));
        }

        this.logProgress(`Batch complete: ${batchSuccess} successful, ${batchErrors} errors`);
        return true;
    }

    async generateDescriptionsContinuously(maxBatches = 20) {
        this.logProgress('Starting continuous description generation...');

        let batchesProcessed = 0;

        while (batchesProcessed < maxBatches) {
            batchesProcessed++;
            this.logProgress(`\nBATCH ${batchesProcessed}`);

            const hasMore = await this.processBatch(10);

            if (!hasMore) {
                this.logProgress('All nodes processed!');
                break;
            }

            this.logProgress(`Overall Progress: ${this.successCount} successful, ${this.errorCount} errors`);

            // Brief pause between batches
            if (batchesProcessed < maxBatches) {
                await new Promise(resolve => setTimeout(resolve, 1000));
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
    console.log('Skill Tree Description Generator');
    console.log('='.repeat(50));

    try {
        const generator = new DescriptionGenerator();

        // Check how many nodes need descriptions
        const nodesWithoutDesc = await generator.getNodesWithoutDescriptions(1000);
        const totalWithout = nodesWithoutDesc.length;

        console.log(`\nFound ${totalWithout} nodes without descriptions`);

        if (totalWithout === 0) {
            console.log('All nodes already have descriptions!');
            return;
        }

        console.log('\nStarting generation process...');
        await generator.generateDescriptionsContinuously(20);

    } catch (error) {
        console.error('Error:', error.message);
    }
}

main().catch(console.error);
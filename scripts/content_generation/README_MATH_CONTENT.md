# Math Content Generation System

## Overview

This system generates comprehensive learning content for mathematics topics using Claude API, incorporating storytelling and philosophical elements based on Kieran Egan's educational philosophy.

## Prerequisites

1. **Anthropic API Key**: Add to `.env.local`:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```
   Get your key from: https://console.anthropic.com/

2. **Node.js packages**: Already installed via main project

## Scripts

### 1. `test_single_node.js`
Tests content generation for a single math node.
```bash
node scripts/content_generation/test_single_node.js
```
- Finds a simple math node
- Generates content and questions
- Saves output to `output/test_content/`
- Creates HTML preview for review

### 2. `generate_math_content_v2.js`
Main batch processor for generating math content.
```bash
node scripts/content_generation/generate_math_content_v2.js
```
- Processes math nodes from easiest to hardest
- Generates 10-30 minutes of content per topic
- Creates 25-30 questions per topic
- Saves for review before database insertion
- Includes checkpoint/resume functionality

### 3. `insert_reviewed_content.js`
Inserts reviewed content into the database.
```bash
node scripts/content_generation/insert_reviewed_content.js
```
- Reads from `output/math_content/content_for_review.json`
- Inserts into `learning_content` table
- Creates questions in `questions` table
- Updates `skill_tree_nodes` with content IDs

## Content Structure

Each generated lesson includes:

1. **The Story Begins** - Engaging introduction with a problem
2. **The Human Story** - Historical context and discoverers
3. **Understanding [Topic]** - Core concepts with examples
4. **Why This Matters** - Real-world applications
5. **See It In Action** - Worked examples
6. **The Bigger Picture** - How this changed humanity
7. **Questions to Ponder** - Philosophical/ethical considerations
8. **Key Takeaways** - Summary points

## Educational Philosophy

Based on Kieran Egan's approach from "The Lost Tools of Learning":

- **Make it Matter**: Connect math to students' lives and big questions
- **Use Stories**: Include human stories of mathematical discoveries
- **Add Conflict**: Show problems that needed solving
- **Show Impact**: Explain how each concept changed the world
- **Ask Deep Questions**: Connect math to ethics and life choices

## Workflow

1. **Test Single Node**:
   ```bash
   node scripts/content_generation/test_single_node.js
   ```
   Review output in `output/test_content/test_content.html`

2. **Generate Batch Content**:
   ```bash
   node scripts/content_generation/generate_math_content_v2.js
   ```
   This generates content for 3 nodes by default.
   
3. **Review Generated Content**:
   - Open `output/math_content/content_for_review.json`
   - Review content quality, accuracy, and engagement
   - Make any necessary manual edits

4. **Insert to Database**:
   ```bash
   node scripts/content_generation/insert_reviewed_content.js
   ```

5. **Process More Nodes**:
   Edit `generate_math_content_v2.js` line 460:
   ```javascript
   const nodesToProcess = mathNodes.slice(0, 20) // Process 20 nodes
   ```

## Output Files

- `output/test_content/` - Single node test outputs
- `output/math_content/checkpoint.json` - Processing checkpoint
- `output/math_content/progress.log` - Processing log
- `output/math_content/content_for_review.json` - Generated content for review
- `output/math_content/inserted_content.json` - Successfully inserted content IDs
- `output/math_content/insertion_errors.json` - Any insertion errors

## Cost Estimates

Using Claude-3 Opus:
- Input: ~$15 per 1M tokens
- Output: ~$75 per 1M tokens
- Per node estimate: ~$0.50-$1.00
- Full set (128 nodes): ~$64-$128

## Database Schema

### learning_content table
- `id`: Auto-generated integer
- `title`: Content title
- `content`: HTML-formatted content
- `estimated_time_minutes`: Reading time
- `difficulty_level`: beginner/intermediate/advanced
- `question_ids`: Array of question IDs
- `images`: Optional image URLs

### questions table
- `id`: UUID
- `question_text`: The question
- `options`: Array of 4 options
- `correct_answer`: Index (0-3)
- `explanation`: Detailed explanation
- `difficulty`: easy/medium/hard

### skill_tree_nodes table
- `learning_content_ids`: Array of content IDs
- Updated when content is added

## Troubleshooting

### API Key Issues
- Ensure `ANTHROPIC_API_KEY` is in `.env.local`
- Check key validity at https://console.anthropic.com/

### Rate Limiting
- Default delay: 5 seconds between API calls
- Adjust `CONFIG.apiDelay` if needed

### Database Errors
- Check Supabase connection in `.env.local`
- Verify table permissions in Supabase dashboard

### Content Quality
- Review generated content before insertion
- Adjust temperature (0.7-0.9) for creativity
- Modify prompts for better results

## Next Steps

After initial batch:
1. Review generated content quality
2. Adjust prompts if needed
3. Process remaining 125+ math nodes
4. Extend to other subject areas (science, history, etc.)
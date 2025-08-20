# Content Generation Scripts

## 📖 **Complete Documentation**

For comprehensive documentation of the Content Generation System, see:
**[documentation/CONTENT_GENERATION_SYSTEM.md](../../documentation/CONTENT_GENERATION_SYSTEM.md)**

---

# Learning Content Generator

This script automatically generates comprehensive learning content and multiple choice questions for skill tree nodes using the Claude API.

## Features

- **Comprehensive Content Generation**: Creates 10-30 minutes of engaging learning content for each skill tree node
- **Question Generation**: Generates 10-20 multiple choice questions with detailed explanations (expandable to 50+)
- **Batch Processing**: Processes multiple nodes with progress tracking and checkpointing
- **Recovery/Resume**: Automatically resumes from where it left off if interrupted
- **Cost Estimation**: Provides API cost estimates before processing
- **Rate Limiting**: Implements 25-second delays between API calls to respect Claude API Tier 1 limits
- **Duplicate Prevention**: Advanced system to prevent duplicate questions when expanding question banks
- **Database Integration**: Saves all content directly to Supabase database
- **Progress Logging**: Detailed logging of processing progress and statistics

## Prerequisites

1. **API Keys Required**:
   - `ANTHROPIC_API_KEY`: Your Anthropic Claude API key
   - `REACT_APP_SUPABASE_URL`: Your Supabase project URL
   - `REACT_APP_SUPABASE_ANON_KEY`: Your Supabase anon key

2. **Database Tables**: Ensure your Supabase database has these tables:
   - `skill_tree_nodes`
   - `learning_content`
   - `questions`

3. **Python Dependencies**: Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
# Generate content for all nodes that need it
python learning_content_generator.py

# Process only a limited number of nodes (for testing)
python learning_content_generator.py --max-nodes 5

# Get cost estimate without processing
python learning_content_generator.py --estimate-only

# Start fresh (ignore previous checkpoint)
python learning_content_generator.py --no-resume
```

### Environment Setup

Set your environment variables:

```bash
# On Windows
set ANTHROPIC_API_KEY=your_api_key_here
set REACT_APP_SUPABASE_URL=your_supabase_url
set REACT_APP_SUPABASE_ANON_KEY=your_supabase_key

# On macOS/Linux
export ANTHROPIC_API_KEY=your_api_key_here
export REACT_APP_SUPABASE_URL=your_supabase_url
export REACT_APP_SUPABASE_ANON_KEY=your_supabase_key
```

Or create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your_api_key_here
REACT_APP_SUPABASE_URL=your_supabase_url
REACT_APP_SUPABASE_ANON_KEY=your_supabase_key
```

## How It Works

### 1. Node Selection
The script automatically identifies skill tree nodes that need content generation by filtering for:
- Leaf nodes (`is_menu_leaf = true`)
- Nodes without existing learning content (`has_learning_content = false`)
- Nodes without existing content IDs

### 2. Content Generation
For each selected node, the script:

**Learning Content**:
- Generates 800-2000 words of educational content
- Creates structured content with headers and examples
- Estimates reading time (10-30 minutes)
- Assigns appropriate difficulty level

**Questions**:
- Generates 50-100 multiple choice questions
- Creates 4 options per question with one correct answer
- Provides detailed explanations for all answers
- Mixes difficulty levels (30% easy, 50% medium, 20% hard)

### 3. Database Storage
All generated content is saved to your Supabase database:
- Learning content → `learning_content` table
- Questions → `questions` table  
- Node updates → `skill_tree_nodes` table (marks as having content)

### 4. Progress Tracking
The script maintains:
- **Checkpoint files**: Resume processing if interrupted
- **Progress logs**: Detailed logging of all operations
- **Statistics tracking**: Success rates, API usage, timing

## Output Files

The script creates several output files in `scripts/content_generation/output/`:

- `checkpoint.json`: Processing progress and resumption data
- `progress.log`: Detailed processing log with timestamps
- Individual batch files (if processing in batches)

## Cost Estimation

The script provides cost estimates based on:
- Claude-3 Sonnet pricing (~$0.003/1K input tokens, ~$0.015/1K output tokens)
- Estimated token usage per node:
  - Content generation: ~500 input + 2000 output tokens
  - Question generation: ~800 input + 5000 output tokens

Example cost for 100 nodes: ~$50-75 USD

## Error Handling & Recovery

### Automatic Recovery
- Saves progress checkpoints every 10 nodes
- Automatically resumes from last successful checkpoint
- Handles API rate limits with built-in delays
- Retries failed operations with exponential backoff

### Manual Recovery
If processing fails:
1. Check the `progress.log` for specific errors
2. Verify API keys and database connectivity
3. Run with `--no-resume` to start fresh if needed
4. Use `--max-nodes 1` to test single node processing

## Troubleshooting

### Common Issues

**Authentication Errors**:
- Verify `ANTHROPIC_API_KEY` is correct and has sufficient credits
- Check Supabase credentials are valid

**Database Errors**:
- Ensure database tables exist with correct schema
- Verify Supabase key has write permissions
- Check for database connection issues

**API Rate Limits**:
- Script includes 2-second delays between calls
- Increase `api_delay` in code if needed
- Monitor API usage in Anthropic console

**Content Quality Issues**:
- Review generated samples before bulk processing
- Adjust prompts in the code for better results
- Consider filtering or post-processing generated content

### Performance Optimization

- Use `--max-nodes` for testing before full runs
- Monitor memory usage for large datasets
- Process during off-peak hours for better API performance
- Consider running in smaller batches for very large datasets

## Configuration Options

Key configuration variables in the script:

```python
self.batch_size = 5              # Process nodes in batches
self.api_delay = 2.0             # Seconds between API calls
self.max_retries = 3             # Retry attempts for failed calls
self.checkpoint_frequency = 10    # Save progress every N nodes
```

## Sample Output Structure

### Generated Learning Content
```json
{
  "title": "Introduction to Photosynthesis",
  "content": "# Photosynthesis: Nature's Energy Conversion...",
  "estimated_time_minutes": 15,
  "difficulty_level": "intermediate"
}
```

### Generated Questions
```json
{
  "question_text": "What is the primary purpose of photosynthesis?",
  "options": [
    "To produce oxygen for animals",
    "To convert sunlight into chemical energy",
    "To create carbon dioxide",
    "To absorb water from soil"
  ],
  "correct_answer": 1,
  "explanation": "Photosynthesis converts light energy into chemical energy...",
  "difficulty": "medium"
}
```

## Support

For issues or questions:
1. Check the `progress.log` file for detailed error information
2. Verify all prerequisites are met
3. Test with a small number of nodes first (`--max-nodes 1`)
4. Review the database schema matches expected format

## License

This script is part of the SkillTree project and follows the same licensing terms.
# Complete Database Migration Guide for NeuroQuest

## Overview
This guide covers the complete migration of NeuroQuest data to Supabase, including:
- Knowledge graph nodes and hierarchy
- Prerequisites and relationships
- Learning paths
- Quiz questions
- User progress tracking

## Prerequisites
1. Supabase account with a project created
2. Environment variables configured in `.env.local`:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

## Step 1: Create Database Schema

Run these SQL scripts in your Supabase SQL Editor in order:

### 1.1 Create Knowledge Graph Tables
```bash
# Run the knowledge schema SQL
# File: scripts/create-knowledge-schema.sql
```

This creates:
- `knowledge_nodes` - All learning nodes
- `node_prerequisites` - Prerequisite relationships
- `learning_paths` - Learning path definitions
- `learning_path_nodes` - Nodes in each path
- `user_progress` - User completion tracking

### 1.2 Create Quiz Questions Table
```bash
# Run the quiz schema SQL
# File: scripts/create-quiz-table.sql
```

This creates:
- `quiz_questions` - Quiz questions for each node

## Step 2: Run Migrations

### Option A: Migrate Everything at Once
```bash
npm run migrate:all
```

This runs all three migrations in sequence:
1. Knowledge graph nodes
2. Learning paths
3. Quiz questions

### Option B: Run Individual Migrations

#### Migrate Knowledge Graph (Run First!)
```bash
npm run migrate:knowledge
```

This migrates:
- All knowledge nodes (foundation, fundamentals, domains, mastery)
- Parent-child relationships for expandable nodes
- Prerequisites between nodes

#### Migrate Learning Paths (Run Second)
```bash
npm run migrate:paths
```

This migrates:
- 7 predefined learning paths
- Links between paths and nodes

#### Migrate Quiz Questions (Run Last)
```bash
npm run migrate:questions
```

This migrates:
- Quiz questions for available nodes
- Answer options and explanations

## Step 3: Verify Migration

### Check in Supabase Dashboard
1. Go to your Supabase project
2. Navigate to Table Editor
3. Verify these tables have data:
   - `knowledge_nodes` (~100+ nodes)
   - `node_prerequisites` (~50+ relationships)
   - `learning_paths` (7 paths)
   - `learning_path_nodes` (~35 path-node links)
   - `quiz_questions` (~17+ questions)

### Check via SQL
Run this in SQL Editor to get counts:

```sql
SELECT 
  (SELECT COUNT(*) FROM knowledge_nodes) as nodes,
  (SELECT COUNT(*) FROM node_prerequisites) as prerequisites,
  (SELECT COUNT(*) FROM learning_paths) as paths,
  (SELECT COUNT(*) FROM learning_path_nodes) as path_nodes,
  (SELECT COUNT(*) FROM quiz_questions) as questions;
```

## Database Structure

### Knowledge Nodes
```typescript
{
  id: string,              // Unique identifier
  name: string,            // Display name
  category: string,        // foundation/fundamentals/domains/mastery
  domain: string,          // Subject area
  difficulty: number,      // 1-6 scale
  points: number,          // Points awarded
  level: number,           // 0 for main, 1 for subnodes
  is_parent: boolean,      // Has expandable children
  parent_id: string | null // Parent node if subnode
}
```

### Prerequisites
```typescript
{
  node_id: string,         // Target node
  prerequisite_id: string  // Required node
}
```

### Learning Paths
```typescript
{
  id: uuid,
  name: string,
  description: string,
  icon_name: string,
  nodes: string[]          // Ordered list of node IDs
}
```

### Quiz Questions
```typescript
{
  id: uuid,
  node_id: string,
  question: string,
  options: string[],
  correct_answer: number,
  explanation: string
}
```

## Troubleshooting

### Migration Fails
1. **Check environment variables**
   ```bash
   node -e "require('dotenv').config({ path: '.env.local' }); console.log(process.env.NEXT_PUBLIC_SUPABASE_URL ? 'URL Found' : 'URL Missing');"
   ```

2. **Check Supabase connection**
   - Ensure your project is active
   - Verify API keys are correct
   - Check network connectivity

3. **Foreign key errors**
   - Run migrations in order: knowledge → paths → questions
   - Ensure parent nodes exist before subnodes

### Data Not Appearing in App
1. Check browser console for errors
2. Verify RLS policies allow public read access
3. Check that Supabase client is initialized correctly

### Duplicate Key Errors
The migrations use `upsert` with conflict resolution, so you can safely re-run them.

## Adding Custom Data

### Add New Knowledge Nodes
```javascript
// In scripts/migrate-knowledge-graph.js, add to hierarchicalKnowledgeGraph
{
  id: 'your-node-id',
  name: 'Your Node Name',
  prereqs: ['prerequisite-id'],
  category: 'domains',
  domain: 'your-domain',
  difficulty: 3,
  points: 150,
  level: 0,
  isParent: false
}
```

### Add New Learning Paths
```javascript
// In scripts/migrate-learning-paths.js, add to learningPaths
{
  name: 'Your Path Name',
  icon: 'IconName',
  description: 'Path description',
  nodes: ['node-id-1', 'node-id-2', 'node-id-3']
}
```

### Add New Quiz Questions
```javascript
// In scripts/migrate-questions.js, add to quizQuestions
'your-node-id': [
  {
    question: "Your question?",
    options: ["Option 1", "Option 2", "Option 3", "Option 4"],
    correct: 0,
    explanation: "Explanation here"
  }
]
```

## Security Considerations

1. **Row Level Security (RLS)** is enabled on all tables
2. **Public read access** is allowed for knowledge data
3. **User progress** requires authentication
4. **Write operations** should be restricted to authenticated users

## Next Steps

After migration:
1. Test the app locally with `npm run dev`
2. Verify nodes display correctly
3. Test quiz functionality
4. Check learning paths
5. Implement user authentication for progress tracking

## Support

If you encounter issues:
1. Check the Supabase logs
2. Review browser console errors
3. Ensure all environment variables are set
4. Verify database schema matches expected structure
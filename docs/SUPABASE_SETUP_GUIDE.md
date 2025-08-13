# Supabase Database Setup Guide for NeuroQuest

## Complete Setup Process

### Step 1: Run the Complete Safe Schema Script

The `scripts/complete-safe-schema.sql` file contains the COMPLETE schema with ALL tables that handles all potential conflicts and can be run multiple times without errors.

1. Open your Supabase Dashboard
2. Go to SQL Editor
3. Copy the entire contents of `scripts/complete-safe-schema.sql`
4. Paste and run in the SQL Editor

This script:
- Creates all necessary tables safely (using IF NOT EXISTS)
- Handles existing policies without errors
- Sets up proper constraints and indexes
- Creates triggers for automatic profile creation
- Implements achievement tracking

### Step 2: Run Data Migrations

After the schema is created, run the data migrations:

```bash
# Migrate all data at once
npm run migrate:all

# Or migrate individually:
npm run migrate:knowledge  # Knowledge graph nodes (run first)
npm run migrate:paths      # Learning paths (run second)  
npm run migrate:questions  # Quiz questions (run last)
```

### Step 3: Verify Setup

#### Check via SQL Editor
Run this query to verify data was migrated:

```sql
SELECT 
  'knowledge_nodes' as table_name, COUNT(*) as count FROM knowledge_nodes
UNION ALL
SELECT 'node_prerequisites', COUNT(*) FROM node_prerequisites
UNION ALL
SELECT 'quiz_questions', COUNT(*) FROM quiz_questions
UNION ALL
SELECT 'learning_paths', COUNT(*) FROM learning_paths
UNION ALL
SELECT 'learning_path_nodes', COUNT(*) FROM learning_path_nodes
UNION ALL
SELECT 'achievements', COUNT(*) FROM achievements
UNION ALL
SELECT 'user_profiles', COUNT(*) FROM user_profiles;
```

Expected counts:
- knowledge_nodes: 100+ nodes
- node_prerequisites: 50+ relationships
- quiz_questions: 17+ questions
- learning_paths: 7 paths
- achievements: 8 default achievements

### Step 4: Environment Variables

Ensure `.env.local` has your Supabase credentials:

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## Database Schema Overview

### Core Learning Tables
- **knowledge_nodes**: All learning nodes with hierarchy
- **node_prerequisites**: Prerequisites between nodes
- **quiz_questions**: Questions for each node
- **learning_paths**: Predefined learning paths
- **learning_path_nodes**: Nodes in each path

### User Profile & Gaming Tables
- **user_profiles**: Extended user profiles with stats
- **achievements**: Available achievements
- **user_achievements**: Earned achievements
- **user_connections**: Friend/connection system
- **user_progress**: Node completion tracking
- **user_stats**: Aggregated user statistics

### Key Features
- Row Level Security (RLS) enabled on all tables
- Automatic profile creation on user signup
- Achievement tracking with triggers
- Leaderboard view for rankings
- Friend/connection system

## Troubleshooting

### Common Issues

1. **"Policy already exists" error**
   - Solution: Use the safe-create-schema.sql script which handles this

2. **"Cannot change view column" error**
   - Solution: The safe script drops views before recreating them

3. **"ON CONFLICT" error**
   - Solution: The safe script checks table existence and uses WHERE NOT EXISTS

4. **Migration fails with connection error**
   - Check your .env.local file has correct credentials
   - Verify Supabase project is active
   - Test connection in Supabase dashboard

5. **Data not appearing in app**
   - Check browser console for errors
   - Verify RLS policies allow public read
   - Ensure Supabase client is initialized

## Testing the Setup

1. **Start the development server:**
   ```bash
   npm run dev
   ```

2. **Open the app:**
   Navigate to http://localhost:3000

3. **Test features:**
   - Knowledge graph should display all nodes
   - Click nodes to see quiz questions
   - Expandable nodes should work (Languages, Algorithms, etc.)
   - Learning paths should show in sidebar

## Next Steps

1. **Authentication**: 
   - Set up Supabase Auth for user accounts
   - Enable progress tracking per user

2. **Real-time Features**:
   - Add real-time leaderboard updates
   - Implement collaborative learning features

3. **Content Management**:
   - Add admin panel for managing nodes
   - Create quiz question editor

## Script Files

### SQL Schema Scripts (run in order)
- `scripts/00-prepare-for-migration.sql` - Disables RLS for migration
- `scripts/01-create-core-tables.sql` - Core tables without dependencies
- `scripts/02-create-dependent-tables.sql` - Tables with foreign keys
- `scripts/03-create-user-tables.sql` - User profile and achievement tables
- `scripts/04-create-views-and-functions.sql` - Views, functions, and triggers
- `scripts/05-enable-security.sql` - Re-enables RLS with proper policies

### Data Migration Scripts
- `scripts/migrate-knowledge-graph.js` - Migrates knowledge nodes and prerequisites
- `scripts/migrate-learning-paths.js` - Migrates learning paths
- `scripts/migrate-questions.js` - Migrates quiz questions

### Documentation
- `docs/STEP_BY_STEP_SETUP.md` - Detailed step-by-step setup guide
- `docs/COMPLETE_MIGRATION_GUIDE.md` - Migration process documentation

## Quick Commands Reference

```bash
# Run migrations
npm run migrate:all

# Start development server
npm run dev

# Run linting
npm run lint

# Build for production
npm run build
```
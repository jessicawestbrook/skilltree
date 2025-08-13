# Step-by-Step Database Setup for NeuroQuest

## Why Step-by-Step?

The database schema has complex foreign key relationships. Tables must be created in a specific order to avoid "relation does not exist" errors.

## Setup Instructions

### Step 0: Prepare for Migration (IMPORTANT!)

Run `scripts/00-prepare-for-migration.sql` in Supabase SQL Editor

This temporarily disables Row Level Security to allow data migration.

### Step 1: Create Core Tables

Run `scripts/01-create-core-tables.sql` in Supabase SQL Editor

This creates:
- `knowledge_nodes` (without self-referencing foreign key)
- `learning_paths`
- `user_stats`

### Step 2: Create Dependent Tables

Run `scripts/02-create-dependent-tables.sql` in Supabase SQL Editor

This creates:
- Adds self-referencing foreign key to `knowledge_nodes`
- `node_prerequisites`
- `quiz_questions`
- `learning_path_nodes`
- `user_progress`

### Step 3: Create User Tables

Run `scripts/03-create-user-tables.sql` in Supabase SQL Editor

This creates:
- `user_profiles`
- `achievements`
- `user_achievements`
- `user_connections`

### Step 4: Create Views and Functions

Run `scripts/04-create-views-and-functions.sql` in Supabase SQL Editor

This creates:
- Views: `leaderboard`, `nodes_with_prereq_count`, `learning_paths_detailed`
- Helper functions for prerequisites and level calculation
- Triggers for automatic profile creation and stats updates

### Step 5: Populate Data

After all tables are created AND Step 0 has been run, run the migration scripts:

```bash
npm run migrate:all
```

### Step 6: Re-enable Security

After migration completes successfully, run `scripts/05-enable-security.sql` in Supabase SQL Editor

This re-enables Row Level Security with proper policies for production use.

Or individually:
```bash
npm run migrate:knowledge  # Knowledge nodes (run first)
npm run migrate:paths      # Learning paths (run second)
npm run migrate:questions  # Quiz questions (run last)
```

## Verification

After completing all steps, run this query to verify:

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

Expected results after migration:
- knowledge_nodes: 100+ records
- node_prerequisites: 50+ records
- quiz_questions: 17+ records
- learning_paths: 7 records
- learning_path_nodes: 35+ records
- achievements: 8 records

## Troubleshooting

### "relation does not exist" error
- Make sure you run the scripts in order (01, 02, 03, 04)
- Each script builds on the previous one

### "policy already exists" error
- The scripts handle this safely by dropping existing policies first
- You can re-run the scripts without issues

### Migration fails
- Ensure all 4 SQL scripts have been run successfully first
- Check your `.env.local` file has correct Supabase credentials
- Verify your Supabase project is active

## Alternative: Single File Setup

If you prefer, you can also use the complete schema file:
- `scripts/complete-safe-schema.sql` - Contains everything in one file

However, if you get foreign key errors, use the step-by-step approach instead.

## Quick Reference

```bash
# SQL Scripts (run in Supabase SQL Editor in order)
00-prepare-for-migration.sql      # Disable RLS for migration
01-create-core-tables.sql
02-create-dependent-tables.sql  
03-create-user-tables.sql
04-create-views-and-functions.sql

# Then run data migration
npm run migrate:all

# Re-enable security after migration
05-enable-security.sql             # Re-enable RLS with policies

# Start the app
npm run dev
```
# Renaming node_id and skill_node_id to skill_id - Changes Summary

## Database Changes

### Tables and Columns to be Renamed:
1. **user_progress** table:
   - `skill_node_id` → `skill_id`
   
2. **starred_categories** table (if exists):
   - `skill_node_id` → `skill_id`
   
3. **questions** table (if column exists):
   - `node_id` → `skill_id`
   
4. **money_counting_progress** table (if exists):
   - `skill_tree_node_id` → `skill_id`

### Backup Tables Created:
- `user_progress_bkp` (or `_bkp2`, `_bkp3` if previous backups exist)
- `starred_categories_bkp` (if table exists)

## Code Changes Required

### TypeScript Type Definitions (`src/types/database.types.ts`):
- **UserProgress** interface: `skill_node_id` → `skill_id`
- **StarredCategory** interface: `skill_node_id` → `skill_id`

### React Components:
1. **src/components/LearningContentModal.tsx** (line 223):
   - Change `skill_node_id: node.id` to `skill_id: node.id`

2. **src/pages/CategoryPage.tsx** (lines 203, 707):
   - Change `.in('skill_node_id', ...)` to `.in('skill_id', ...)`
   - Change `skill_node_id: resolvedCategoryId` to `skill_id: resolvedCategoryId`

3. **src/pages/ProfilePage.tsx** (multiple occurrences):
   - Lines 42, 135, 169, 183, 216, 389-390, 711
   - Replace all `skill_node_id` with `skill_id`
   - Replace `node_id` references in questions context with `skill_id`

4. **src/pages/LearningPathsPage.tsx** (lines 137, 142):
   - Change `skill_tree_node_id` to `skill_id`

### Services:
1. **src/services/recommendationService.ts** (multiple lines):
   - Lines 18, 191, 193, 339, 351, 354, 356, 418, 516, 520
   - Replace `skill_node_id` with `skill_id`
   - Replace `skill_tree_node_id` with `skill_id`

2. **src/services/adaptiveAssessmentService.ts** (lines 13, 295):
   - Replace `skill_node_id` with `skill_id`

## Migration Process

1. **Backup Creation**: Automatic backup tables will be created before any changes
2. **Column Renaming**: All specified columns will be renamed
3. **Foreign Key Updates**: Foreign key constraints will be updated with new names
4. **RLS Policy Updates**: Row Level Security policies will be updated
5. **Code Updates**: All TypeScript/React code will be updated to use new column names

## Rollback Plan

If issues occur, you can restore from backup:
```sql
-- Example rollback for user_progress
DROP TABLE public.user_progress;
ALTER TABLE public.user_progress_bkp RENAME TO user_progress;
```

## Testing Required After Migration

1. Verify user progress tracking works
2. Test starred categories functionality
3. Ensure questions load correctly
4. Check money counting module (if applicable)
5. Run full test suite
6. Test all pages that display user progress or skill tree navigation
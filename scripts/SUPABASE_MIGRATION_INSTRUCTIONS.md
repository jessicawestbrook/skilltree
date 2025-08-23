# Supabase Migration Instructions: Add is_hidden Column

## Steps to Add the is_hidden Column

1. **Open Supabase Dashboard**
   - Go to: https://supabase.com/dashboard/project/ozujqlucqdyszxmzhigf
   - Navigate to the SQL Editor (left sidebar)

2. **Run the Migration**
   - Copy the contents of `add_is_hidden_column_manual.sql`
   - Paste into the SQL Editor
   - Click "Run" button

3. **Verify the Migration**
   - Go to Table Editor
   - Select `skill_tree_nodes` table
   - Check that `is_hidden` column exists (boolean, default: false)

4. **Test the Column**
   - You can manually set some test nodes to hidden:
   ```sql
   -- Example: Hide a specific node by name
   UPDATE skill_tree_nodes 
   SET is_hidden = TRUE 
   WHERE name = 'Test Category';
   ```

5. **Once Complete**
   - The application will automatically use the database column
   - The admin interface will persist changes to the database
   - Hidden nodes will be filtered from navigation menus

## Alternative: Quick Column Addition

If the full migration has issues, you can simply add the column:

1. Go to Table Editor
2. Select `skill_tree_nodes`
3. Click "Add column"
4. Settings:
   - Name: `is_hidden`
   - Type: `boolean`
   - Default value: `false`
   - Click "Save"

## Notes
- The column defaults to FALSE, so all existing nodes will be visible
- The admin interface will allow toggling visibility
- Changes will persist in the database
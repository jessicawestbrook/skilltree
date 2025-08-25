# Data Fixes Needed

## Spelling Words Table

### Issue 1: Combined Word Entry
**ID:** 18aefd86-92c5-4037-a544-0547fd5c9e32
**Current Word:** centennialcertiorari
**Problem:** Two separate words were accidentally combined into one entry

**Details:**
- The word "centennialcertiorari" is actually two words: "centennial" and "certiorari"
- Both words already exist as separate entries in the database:
  - "centennial" (ID: 30d90264-1ac5-47b9-bb3a-fb5837404184) - with correct definition
  - "certiorari" (ID: 0e7aee7c-bbde-46bb-ac44-12bf28e87d5a) - with correct definition
- The combined entry has the definition for "certiorari" only
- The pronunciation guide incorrectly combines both words

**Recommended Fix:**
Delete the entry with ID 18aefd86-92c5-4037-a544-0547fd5c9e32 from the spelling_words table.

**SQL to Execute (requires admin privileges):**
```sql
DELETE FROM spelling_words 
WHERE id = '18aefd86-92c5-4037-a544-0547fd5c9e32';
```

**Verification Query:**
```sql
-- Check that both correct entries exist
SELECT id, word, definition 
FROM spelling_words 
WHERE word IN ('centennial', 'certiorari');

-- Confirm the combined entry is gone
SELECT id, word 
FROM spelling_words 
WHERE word = 'centennialcertiorari';
```

**Note:** Attempted to fix programmatically but RLS policies are preventing deletion/update. This needs to be done with admin database access.
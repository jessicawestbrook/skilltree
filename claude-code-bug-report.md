# Bug Report: "Don't Ask Again" Overwrites Entire Permissions Array

## Description
When clicking "Don't ask again" for a command permission in Claude Code, the entire `allow` array in `.claude/settings.local.json` gets replaced with just the new permission, causing all previously saved permissions to be lost.

## Expected Behavior
New permissions should be **appended** to the existing `allow` array, preserving all previously saved permissions.

## Actual Behavior
The entire `allow` array is **replaced** with only the new permission, deleting all existing permissions.

## Steps to Reproduce
1. Have multiple permissions in `.claude/settings.local.json`:
   ```json
   {
     "permissions": {
       "allow": [
         "Bash(npm install:*)",
         "Bash(npm run dev:*)",
         "Bash(git status:*)"
       ]
     }
   }
   ```

2. Run a new command that triggers a permission prompt (e.g., `npx tsc`)
3. Click "Don't ask again"
4. Check `.claude/settings.local.json`
5. The file now contains only:
   ```json
   {
     "permissions": {
       "allow": [
         "Bash(npx tsc:*)"
       ]
     }
   }
   ```

## Impact
- Users lose all their saved permissions every time they add a new one
- Have to manually restore permissions or re-approve commands repeatedly
- Makes the "Don't ask again" feature counterproductive

## Environment
- Claude Code version: [Current version]
- OS: Windows
- Project type: Next.js/TypeScript

## Workaround
Created a script to restore permissions:
```javascript
// restore-permissions.js
const fs = require('fs');
const path = require('path');

const settingsPath = path.join(__dirname, '.claude', 'settings.local.json');
const desiredPermissions = [
  "Bash(npm install:*)",
  "Bash(npm run dev:*)",
  // ... other permissions
];

const currentSettings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
const currentAllow = currentSettings.permissions?.allow || [];
const mergedPermissions = [...new Set([...desiredPermissions, ...currentAllow])];
currentSettings.permissions.allow = mergedPermissions;
fs.writeFileSync(settingsPath, JSON.stringify(currentSettings, null, 2));
```

## Suggested Fix
When adding a new permission, the code should:
1. Read the current permissions array
2. Add the new permission if it doesn't exist
3. Write back the merged array

Example fix:
```javascript
// Instead of:
settings.permissions.allow = [newPermission];

// Should be:
settings.permissions.allow = [...new Set([...settings.permissions.allow, newPermission])];
```

## Additional Context
This happens consistently - observed multiple times in a single session where permissions were overwritten with:
- `Bash(npx tsc:*)`
- `Bash(taskkill:*)`
- `Bash(powershell:*)`

Each time, all previous permissions were lost.
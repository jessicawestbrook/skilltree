// Script to restore Claude Code permissions after they get overwritten
const fs = require('fs');
const path = require('path');

const settingsPath = path.join(__dirname, '.claude', 'settings.local.json');

// Define all the permissions you want to keep
const desiredPermissions = [
  "Bash(npm install:*)",
  "Bash(npm run dev:*)",
  "Bash(npm run build:*)",
  "Bash(npm run test:*)",
  "Bash(npm run lint:*)",
  "Bash(git status:*)",
  "Bash(git diff:*)",
  "Bash(git log:*)",
  "Bash(git add:*)",
  "Bash(git commit:*)",
  "Bash(git push:*)",
  "Bash(git pull:*)",
  "Bash(npx:*)",
  "Bash(node:*)",
  "Bash(taskkill:*)",
  "Bash(kill:*)",
  "Bash(ps:*)",
  "Bash(netstat:*)"
];

try {
  // Read current settings
  const currentSettings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
  
  // Get current permissions
  const currentAllow = currentSettings.permissions?.allow || [];
  
  // Merge permissions (keeping any new ones that were added)
  const mergedPermissions = [...new Set([...desiredPermissions, ...currentAllow])];
  
  // Update settings
  currentSettings.permissions.allow = mergedPermissions;
  
  // Write back
  fs.writeFileSync(settingsPath, JSON.stringify(currentSettings, null, 2));
  
  console.log('✅ Permissions restored successfully!');
  console.log('📝 Current permissions:', mergedPermissions);
} catch (error) {
  console.error('❌ Error restoring permissions:', error.message);
}
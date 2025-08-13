#!/usr/bin/env node

/**
 * PWA Icon Generation Script
 * This script helps generate the required PWA icons from a source image
 * 
 * Note: This is a helper script that provides instructions for icon generation.
 * For actual icon generation, you'll need to use tools like:
 * - https://realfavicongenerator.net/
 * - https://app-manifest.firebaseapp.com/
 * - Or manually create icons with image editing software
 */

const path = require('path');
const fs = require('fs');

console.log('🎨 PWA Icon Generation Helper\n');

const requiredSizes = [
  { size: '72x72', purpose: 'any' },
  { size: '96x96', purpose: 'any' },
  { size: '128x128', purpose: 'any' },
  { size: '144x144', purpose: 'any' },
  { size: '152x152', purpose: 'any' },
  { size: '192x192', purpose: 'any' },
  { size: '384x384', purpose: 'any' },
  { size: '512x512', purpose: 'any' },
  { size: '192x192', purpose: 'maskable', suffix: '-maskable' },
  { size: '512x512', purpose: 'maskable', suffix: '-maskable' },
];

const shortcuts = [
  { name: 'learn', size: '192x192' },
  { name: 'graph', size: '192x192' },
  { name: 'profile', size: '192x192' },
  { name: 'offline', size: '192x192' },
];

const iconsDir = path.join(__dirname, '..', 'public', 'icons');

// Create icons directory if it doesn't exist
if (!fs.existsSync(iconsDir)) {
  fs.mkdirSync(iconsDir, { recursive: true });
  console.log('📁 Created icons directory');
}

console.log('📋 Required PWA Icons:\n');

console.log('🎯 Main App Icons:');
requiredSizes.forEach(icon => {
  const filename = `icon${icon.suffix || ''}-${icon.size}.png`;
  const filepath = path.join(iconsDir, filename);
  const exists = fs.existsSync(filepath);
  
  console.log(`  ${exists ? '✅' : '❌'} ${filename} (${icon.purpose})`);
});

console.log('\n🔗 Shortcut Icons:');
shortcuts.forEach(shortcut => {
  const filename = `shortcut-${shortcut.name}.png`;
  const filepath = path.join(iconsDir, filename);
  const exists = fs.existsSync(filepath);
  
  console.log(`  ${exists ? '✅' : '❌'} ${filename} (${shortcut.size})`);
});

console.log('\n📱 Additional Assets:');
const additionalAssets = [
  'apple-touch-icon.png (180x180)',
  'favicon.ico (32x32)',
  'og-image.png (1200x630)',
  'badge-72x72.png (72x72)',
];

additionalAssets.forEach(asset => {
  const filename = asset.split(' ')[0];
  const filepath = path.join(__dirname, '..', 'public', filename);
  const exists = fs.existsSync(filepath);
  
  console.log(`  ${exists ? '✅' : '❌'} ${asset}`);
});

console.log('\n🛠️  Icon Generation Tools:\n');

console.log('🌐 Online Tools:');
console.log('  • Real Favicon Generator: https://realfavicongenerator.net/');
console.log('  • PWA Manifest Generator: https://app-manifest.firebaseapp.com/');
console.log('  • PWA Builder: https://www.pwabuilder.com/');

console.log('\n💻 Command Line Tools:');
console.log('  • Sharp CLI: npm install -g sharp-cli');
console.log('  • PWA Asset Generator: npm install -g pwa-asset-generator');

console.log('\n📐 Icon Guidelines:\n');

console.log('🎨 Design Requirements:');
console.log('  • Use a simple, recognizable design');
console.log('  • Ensure good contrast and readability');
console.log('  • Test at small sizes (48x48)');
console.log('  • Use vector graphics when possible');

console.log('\n🖼️  Maskable Icons:');
console.log('  • Include 15% safe zone around main content');
console.log('  • Use solid background color');
console.log('  • Main icon should be centered');
console.log('  • Test with different mask shapes');

console.log('\n📋 Generation Commands:\n');

console.log('Using Sharp CLI:');
requiredSizes.forEach(icon => {
  const size = icon.size.split('x')[0];
  const suffix = icon.suffix || '';
  console.log(`  sharp source.png --resize ${size} --output public/icons/icon${suffix}-${icon.size}.png`);
});

console.log('\nUsing ImageMagick:');
requiredSizes.forEach(icon => {
  const suffix = icon.suffix || '';
  console.log(`  convert source.png -resize ${icon.size} public/icons/icon${suffix}-${icon.size}.png`);
});

console.log('\n✨ Quick Start:\n');
console.log('1. Create a high-resolution source image (1024x1024 or larger)');
console.log('2. Use one of the online tools above to generate all required sizes');
console.log('3. Download and extract icons to the public/icons/ directory');
console.log('4. Update manifest.json if needed');
console.log('5. Test the PWA with Lighthouse');

console.log('\n🔍 Testing:\n');
console.log('After generating icons:');
console.log('  • Run: npm run build');
console.log('  • Open Chrome DevTools > Lighthouse');
console.log('  • Run PWA audit');
console.log('  • Check all icon requirements are met');

// Generate a simple placeholder script
const placeholderScript = `
#!/bin/bash
# PWA Icon Generation Script
# Replace 'source.png' with your high-resolution logo

echo "Generating PWA icons..."

# Create icons directory
mkdir -p public/icons

# Generate main icons (requires ImageMagick)
${requiredSizes.map(icon => {
  const suffix = icon.suffix || '';
  return `convert source.png -resize ${icon.size} public/icons/icon${suffix}-${icon.size}.png`;
}).join('\n')}

# Generate shortcut icons
${shortcuts.map(shortcut => {
  return `convert source.png -resize ${shortcut.size} public/icons/shortcut-${shortcut.name}.png`;
}).join('\n')}

# Generate additional assets
convert source.png -resize 180x180 public/apple-touch-icon.png
convert source.png -resize 32x32 public/favicon.ico
convert source.png -resize 1200x630 public/og-image.png
convert source.png -resize 72x72 public/icons/badge-72x72.png

echo "Icon generation complete!"
echo "Don't forget to optimize the images for web use."
`;

const scriptPath = path.join(__dirname, 'generate-icons.sh');
fs.writeFileSync(scriptPath, placeholderScript.trim());
console.log(`\n📝 Generated helper script: ${scriptPath}`);
console.log('   Make executable with: chmod +x scripts/generate-icons.sh');

console.log('\n🎉 Ready to create your PWA icons!\n');
#!/usr/bin/env node

/**
 * PWA Testing Script
 * Validates PWA implementation and checks for common issues
 */

const fs = require('fs');
const path = require('path');

console.log('🔍 PWA Testing & Validation\n');

const projectRoot = path.join(__dirname, '..');

// Check required files
const requiredFiles = [
  'public/manifest.json',
  'public/sw.js',
  'src/components/PWAProvider.tsx',
  'src/components/PWAInstallPrompt.tsx',
  'src/hooks/usePWA.ts',
  'src/app/offline/page.tsx',
];

console.log('📁 Required Files:');
requiredFiles.forEach(file => {
  const filepath = path.join(projectRoot, file);
  const exists = fs.existsSync(filepath);
  console.log(`  ${exists ? '✅' : '❌'} ${file}`);
});

// Check manifest.json
console.log('\n📱 Web App Manifest:');
try {
  const manifestPath = path.join(projectRoot, 'public/manifest.json');
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  
  const requiredFields = ['name', 'short_name', 'start_url', 'display', 'theme_color', 'background_color', 'icons'];
  
  requiredFields.forEach(field => {
    const exists = manifest.hasOwnProperty(field);
    console.log(`  ${exists ? '✅' : '❌'} ${field}: ${exists ? '✓' : 'Missing'}`);
  });
  
  if (manifest.icons && manifest.icons.length > 0) {
    console.log(`  ℹ️  Icons: ${manifest.icons.length} defined`);
    
    const requiredSizes = ['192x192', '512x512'];
    requiredSizes.forEach(size => {
      const hasSize = manifest.icons.some(icon => icon.sizes === size);
      console.log(`    ${hasSize ? '✅' : '❌'} ${size} icon`);
    });
  }
  
} catch (error) {
  console.log('  ❌ Invalid or missing manifest.json');
}

// Check service worker
console.log('\n⚙️  Service Worker:');
try {
  const swPath = path.join(projectRoot, 'public/sw.js');
  const swContent = fs.readFileSync(swPath, 'utf8');
  
  const swFeatures = [
    { name: 'Install event', pattern: /addEventListener\s*\(\s*['"']install['"']/ },
    { name: 'Activate event', pattern: /addEventListener\s*\(\s*['"']activate['"']/ },
    { name: 'Fetch event', pattern: /addEventListener\s*\(\s*['"']fetch['"']/ },
    { name: 'Background sync', pattern: /addEventListener\s*\(\s*['"']sync['"']/ },
    { name: 'Push notifications', pattern: /addEventListener\s*\(\s*['"']push['"']/ },
    { name: 'Cache management', pattern: /caches\.(open|match|delete)/ },
  ];
  
  swFeatures.forEach(feature => {
    const hasFeature = feature.pattern.test(swContent);
    console.log(`  ${hasFeature ? '✅' : '❌'} ${feature.name}`);
  });
  
} catch (error) {
  console.log('  ❌ Service worker not found or invalid');
}

// Check Next.js configuration
console.log('\n⚡ Next.js Configuration:');
try {
  const configPath = path.join(projectRoot, 'next.config.ts');
  const configContent = fs.readFileSync(configPath, 'utf8');
  
  const configChecks = [
    { name: 'PWA plugin imported', pattern: /import.*next-pwa/ },
    { name: 'withPWA wrapper', pattern: /withPWA\s*\(/ },
    { name: 'PWA configuration', pattern: /dest:\s*['"']public['"']/ },
    { name: 'Runtime caching', pattern: /runtimeCaching/ },
  ];
  
  configChecks.forEach(check => {
    const hasConfig = check.pattern.test(configContent);
    console.log(`  ${hasConfig ? '✅' : '❌'} ${check.name}`);
  });
  
} catch (error) {
  console.log('  ❌ Next.js config not found or invalid');
}

// Check package.json dependencies
console.log('\n📦 Dependencies:');
try {
  const packagePath = path.join(projectRoot, 'package.json');
  const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
  
  const requiredDeps = [
    'next-pwa',
    'workbox-webpack-plugin',
  ];
  
  requiredDeps.forEach(dep => {
    const hasDepMain = packageJson.dependencies && packageJson.dependencies[dep];
    const hasDepDev = packageJson.devDependencies && packageJson.devDependencies[dep];
    const hasDep = hasDepMain || hasDepDev;
    
    console.log(`  ${hasDep ? '✅' : '❌'} ${dep}`);
  });
  
} catch (error) {
  console.log('  ❌ package.json not found or invalid');
}

// Check icons directory
console.log('\n🎨 PWA Icons:');
const iconsDir = path.join(projectRoot, 'public/icons');
if (fs.existsSync(iconsDir)) {
  const iconFiles = fs.readdirSync(iconsDir);
  console.log(`  ℹ️  Found ${iconFiles.length} icon files`);
  
  const requiredIcons = [
    'icon-192x192.png',
    'icon-512x512.png',
    'icon-maskable-192x192.png',
    'icon-maskable-512x512.png',
  ];
  
  requiredIcons.forEach(icon => {
    const hasIcon = iconFiles.includes(icon);
    console.log(`  ${hasIcon ? '✅' : '❌'} ${icon}`);
  });
  
  if (iconFiles.length === 0) {
    console.log('  ⚠️  No icons found - run: node scripts/generate-pwa-icons.js');
  }
} else {
  console.log('  ❌ Icons directory not found');
  console.log('  ℹ️  Run: node scripts/generate-pwa-icons.js for help');
}

// Environment variables check
console.log('\n🔐 Environment Configuration:');
const envPath = path.join(projectRoot, '.env.local');
const envExamplePath = path.join(projectRoot, '.env.example');

if (fs.existsSync(envPath)) {
  console.log('  ✅ .env.local found');
} else if (fs.existsSync(envExamplePath)) {
  console.log('  ⚠️  .env.example found, but no .env.local');
  console.log('  ℹ️  Copy .env.example to .env.local and configure');
} else {
  console.log('  ❌ No environment configuration found');
}

console.log('\n🚀 Testing Instructions:\n');

console.log('1. **Build and Test**:');
console.log('   npm run build');
console.log('   npm start');
console.log('');

console.log('2. **Lighthouse PWA Audit**:');
console.log('   • Open Chrome DevTools (F12)');
console.log('   • Go to Lighthouse tab');
console.log('   • Select "Progressive Web App"');
console.log('   • Click "Generate report"');
console.log('');

console.log('3. **Manual Testing**:');
console.log('   • Test install prompt on supported browsers');
console.log('   • Go offline and test functionality');
console.log('   • Check service worker in DevTools > Application');
console.log('   • Verify caching in DevTools > Network (disable cache)');
console.log('');

console.log('4. **Common Issues**:');
console.log('   • HTTPS required for PWA features');
console.log('   • Icons must be correctly sized and formatted');
console.log('   • Service worker must be in public/ directory');
console.log('   • Manifest.json must be valid JSON');
console.log('');

console.log('🔧 **Debugging Tools**:');
console.log('   • Chrome DevTools > Application > Service Workers');
console.log('   • Chrome DevTools > Application > Storage');
console.log('   • PWA Builder: https://www.pwabuilder.com/');
console.log('   • Lighthouse CI for automated testing');

console.log('\n✨ PWA validation complete!\n');
const sharp = require('sharp');
const fs = require('fs').promises;
const path = require('path');

// Define all the icon sizes needed for PWA
const iconSizes = [
  72, 96, 128, 144, 152, 192, 384, 512
];

// Additional sizes for shortcuts
const shortcutIcons = [
  { name: 'shortcut-learn', color: '#10b981' },
  { name: 'shortcut-graph', color: '#3b82f6' },
  { name: 'shortcut-profile', color: '#8b5cf6' },
  { name: 'shortcut-offline', color: '#f59e0b' }
];

async function ensureDirectoryExists(dirPath) {
  try {
    await fs.access(dirPath);
  } catch {
    await fs.mkdir(dirPath, { recursive: true });
  }
}

async function generateIconFromSVG() {
  const svgPath = path.join(__dirname, '..', 'public', 'favicon.svg');
  const iconsDir = path.join(__dirname, '..', 'public', 'icons');
  const screenshotsDir = path.join(__dirname, '..', 'public', 'screenshots');
  
  // Ensure directories exist
  await ensureDirectoryExists(iconsDir);
  await ensureDirectoryExists(screenshotsDir);

  // Read the SVG file
  const svgBuffer = await fs.readFile(svgPath);

  // Generate standard icons
  console.log('Generating standard icons...');
  for (const size of iconSizes) {
    const outputPath = path.join(iconsDir, `icon-${size}x${size}.png`);
    await sharp(svgBuffer)
      .resize(size, size)
      .png()
      .toFile(outputPath);
    console.log(`✓ Generated ${size}x${size} icon`);
  }

  // Generate maskable icons (with padding)
  console.log('\nGenerating maskable icons...');
  for (const size of [192, 512]) {
    const outputPath = path.join(iconsDir, `icon-maskable-${size}x${size}.png`);
    const paddedSize = Math.floor(size * 0.8);
    
    await sharp(svgBuffer)
      .resize(paddedSize, paddedSize)
      .extend({
        top: Math.floor((size - paddedSize) / 2),
        bottom: Math.ceil((size - paddedSize) / 2),
        left: Math.floor((size - paddedSize) / 2),
        right: Math.ceil((size - paddedSize) / 2),
        background: { r: 255, g: 255, b: 255, alpha: 0 }
      })
      .png()
      .toFile(outputPath);
    console.log(`✓ Generated maskable ${size}x${size} icon`);
  }

  // Copy some icons to root for compatibility
  console.log('\nCopying icons to root...');
  await fs.copyFile(
    path.join(iconsDir, 'icon-192x192.png'),
    path.join(__dirname, '..', 'public', 'icon-192.png')
  );
  await fs.copyFile(
    path.join(iconsDir, 'icon-512x512.png'),
    path.join(__dirname, '..', 'public', 'icon-512.png')
  );
  console.log('✓ Copied icons to root');

  // Generate shortcut icons
  console.log('\nGenerating shortcut icons...');
  for (const shortcut of shortcutIcons) {
    const outputPath = path.join(iconsDir, `${shortcut.name}.png`);
    
    // Create a colored background with the tree icon
    await sharp({
      create: {
        width: 192,
        height: 192,
        channels: 4,
        background: shortcut.color
      }
    })
    .composite([{
      input: await sharp(svgBuffer)
        .resize(120, 120)
        .png()
        .toBuffer(),
      top: 36,
      left: 36
    }])
    .png()
    .toFile(outputPath);
    
    console.log(`✓ Generated ${shortcut.name} icon`);
  }

  // Generate placeholder screenshots
  console.log('\nGenerating placeholder screenshots...');
  
  // Desktop screenshot
  await sharp({
    create: {
      width: 1280,
      height: 720,
      channels: 4,
      background: { r: 250, g: 250, b: 245, alpha: 1 }
    }
  })
  .composite([{
    input: await sharp(svgBuffer)
      .resize(200, 200)
      .png()
      .toBuffer(),
    top: 260,
    left: 540
  }])
  .composite([{
    input: Buffer.from(`
      <svg width="1280" height="720">
        <text x="640" y="500" font-family="Arial" font-size="32" text-anchor="middle" fill="#059669">
          SkillTree - Grow Your Skills
        </text>
        <text x="640" y="540" font-family="Arial" font-size="20" text-anchor="middle" fill="#6b7280">
          Interactive Learning Platform
        </text>
      </svg>
    `),
    top: 0,
    left: 0
  }])
  .png()
  .toFile(path.join(screenshotsDir, 'desktop-home.png'));
  console.log('✓ Generated desktop screenshot');

  // Mobile screenshot
  await sharp({
    create: {
      width: 360,
      height: 640,
      channels: 4,
      background: { r: 250, g: 250, b: 245, alpha: 1 }
    }
  })
  .composite([{
    input: await sharp(svgBuffer)
      .resize(120, 120)
      .png()
      .toBuffer(),
    top: 200,
    left: 120
  }])
  .composite([{
    input: Buffer.from(`
      <svg width="360" height="640">
        <text x="180" y="350" font-family="Arial" font-size="24" text-anchor="middle" fill="#059669">
          SkillTree
        </text>
        <text x="180" y="380" font-family="Arial" font-size="16" text-anchor="middle" fill="#6b7280">
          Learn on the go
        </text>
      </svg>
    `),
    top: 0,
    left: 0
  }])
  .png()
  .toFile(path.join(screenshotsDir, 'mobile-learn.png'));
  console.log('✓ Generated mobile screenshot');

  console.log('\n✅ All icons and screenshots generated successfully!');
}

// Run the generation
generateIconFromSVG().catch(console.error);
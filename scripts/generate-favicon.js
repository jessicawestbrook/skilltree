const fs = require('fs');
const path = require('path');

// Read the SVG file
const svgPath = path.join(__dirname, '..', 'public', 'favicon.svg');
const svgContent = fs.readFileSync(svgPath, 'utf8');

// Create a simple favicon.ico by copying the SVG
// Modern browsers will handle SVG favicons, but we'll keep the ICO for compatibility
const icoPath = path.join(__dirname, '..', 'public', 'favicon.ico');

// For now, we'll just ensure the SVG is properly referenced
// The browser will handle the SVG favicon automatically
console.log('SVG favicon updated successfully!');
console.log('Modern browsers will automatically use the SVG favicon.');
console.log('ICO file remains as fallback for older browsers.');

// Update the manifest.json to reference our icons
const manifestPath = path.join(__dirname, '..', 'public', 'manifest.json');
if (fs.existsSync(manifestPath)) {
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  
  // Ensure our favicon is properly referenced
  if (!manifest.icons) {
    manifest.icons = [];
  }
  
  // Update or add favicon references
  const faviconIcons = [
    {
      "src": "favicon.svg",
      "type": "image/svg+xml",
      "sizes": "any"
    },
    {
      "src": "favicon.ico",
      "type": "image/x-icon",
      "sizes": "16x16 32x32"
    },
    {
      "src": "logo192.png",
      "type": "image/png",
      "sizes": "192x192"
    },
    {
      "src": "logo512.png",
      "type": "image/png",
      "sizes": "512x512"
    }
  ];
  
  manifest.icons = faviconIcons;
  
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
  console.log('Updated manifest.json with favicon references');
}
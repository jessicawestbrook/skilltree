const fs = require('fs');
const path = require('path');

// Create SVG data for PNG logos (simplified version for better scaling)
const createLogoSVG = (size) => `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${size} ${size}" width="${size}" height="${size}">
  <defs>
    <radialGradient id="bgGrad" cx="50%" cy="30%" r="70%">
      <stop offset="0%" style="stop-color:#34d399;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#059669;stop-opacity:1" />
    </radialGradient>
    <linearGradient id="trunkGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#92400e;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#a16207;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#92400e;stop-opacity:1" />
    </linearGradient>
    <radialGradient id="foliageGrad" cx="50%" cy="40%" r="60%">
      <stop offset="0%" style="stop-color:#fbbf24;stop-opacity:1" />
      <stop offset="70%" style="stop-color:#f59e0b;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#d97706;stop-opacity:1" />
    </radialGradient>
  </defs>
  
  <!-- Background circle -->
  <circle cx="${size/2}" cy="${size/2}" r="${size/2 - 5}" fill="url(#bgGrad)" stroke="#047857" stroke-width="${size/32}"/>
  
  <!-- Tree trunk -->
  <rect x="${size/2 - size/12.8}" y="${size * 0.59}" width="${size/6.4}" height="${size/4}" fill="url(#trunkGrad)" rx="${size/64}"/>
  
  <!-- Tree foliage -->
  <path d="M ${size/2} ${size*0.125} C ${size*0.375} ${size*0.125} ${size*0.28} ${size*0.22} ${size*0.28} ${size*0.34} C ${size*0.19} ${size*0.34} ${size*0.125} ${size*0.41} ${size*0.125} ${size/2} C ${size*0.125} ${size*0.56} ${size*0.16} ${size*0.61} ${size*0.2} ${size*0.64} C ${size*0.25} ${size*0.69} ${size*0.31} ${size*0.69} ${size*0.375} ${size*0.67} C ${size*0.44} ${size*0.7} ${size*0.56} ${size*0.7} ${size*0.625} ${size*0.67} C ${size*0.69} ${size*0.69} ${size*0.75} ${size*0.69} ${size*0.8} ${size*0.64} C ${size*0.84} ${size*0.61} ${size*0.875} ${size*0.56} ${size*0.875} ${size/2} C ${size*0.875} ${size*0.41} ${size*0.81} ${size*0.34} ${size*0.72} ${size*0.34} C ${size*0.72} ${size*0.22} ${size*0.625} ${size*0.125} ${size/2} ${size*0.125} Z" fill="url(#foliageGrad)" stroke="#d97706" stroke-width="${size/64}"/>
  
  <!-- Skill tree lines -->
  <path d="M ${size/2} ${size*0.375} L ${size*0.375} ${size/2} M ${size/2} ${size*0.375} L ${size*0.625} ${size/2} M ${size*0.375} ${size/2} L ${size*0.25} ${size*0.59} M ${size*0.375} ${size/2} L ${size/2} ${size*0.59} M ${size*0.625} ${size/2} L ${size*0.75} ${size*0.59}" stroke="#ffffff" stroke-width="${size/32}" opacity="0.8"/>
  
  <!-- Skill nodes -->
  <circle cx="${size/2}" cy="${size*0.375}" r="${size/17.8}" fill="#ffffff" stroke="#d97706" stroke-width="${size/40}"/>
  <circle cx="${size*0.375}" cy="${size/2}" r="${size/21.3}" fill="#fbbf24" stroke="#ffffff" stroke-width="${size/64}"/>
  <circle cx="${size*0.625}" cy="${size/2}" r="${size/21.3}" fill="#fbbf24" stroke="#ffffff" stroke-width="${size/64}"/>
  <circle cx="${size*0.25}" cy="${size*0.59}" r="${size/26.7}" fill="#e5e7eb" stroke="#9ca3af" stroke-width="${size/64}"/>
  <circle cx="${size*0.75}" cy="${size*0.59}" r="${size/26.7}" fill="#e5e7eb" stroke="#9ca3af" stroke-width="${size/64}"/>
  <circle cx="${size/2}" cy="${size*0.59}" r="${size/26.7}" fill="#22c55e" stroke="#ffffff" stroke-width="${size/64}"/>
</svg>`;

// Write logo files as SVG (browsers can handle these better than trying to convert to PNG)
const logo192SVG = createLogoSVG(192);
const logo512SVG = createLogoSVG(512);

fs.writeFileSync(path.join(__dirname, '..', 'public', 'logo192.svg'), logo192SVG);
fs.writeFileSync(path.join(__dirname, '..', 'public', 'logo512.svg'), logo512SVG);

console.log('Created logo192.svg and logo512.svg');
console.log('Note: For better browser compatibility, consider converting these to PNG using an online tool or image editor.');
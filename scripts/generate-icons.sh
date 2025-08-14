#!/bin/bash
# PWA Icon Generation Script
# Replace 'source.png' with your high-resolution logo

echo "Generating PWA icons..."

# Create icons directory
mkdir -p public/icons

# Generate main icons (requires ImageMagick)
convert source.png -resize 72x72 public/icons/icon-72x72.png
convert source.png -resize 96x96 public/icons/icon-96x96.png
convert source.png -resize 128x128 public/icons/icon-128x128.png
convert source.png -resize 144x144 public/icons/icon-144x144.png
convert source.png -resize 152x152 public/icons/icon-152x152.png
convert source.png -resize 192x192 public/icons/icon-192x192.png
convert source.png -resize 384x384 public/icons/icon-384x384.png
convert source.png -resize 512x512 public/icons/icon-512x512.png
convert source.png -resize 192x192 public/icons/icon-maskable-192x192.png
convert source.png -resize 512x512 public/icons/icon-maskable-512x512.png

# Generate shortcut icons
convert source.png -resize 192x192 public/icons/shortcut-learn.png
convert source.png -resize 192x192 public/icons/shortcut-graph.png
convert source.png -resize 192x192 public/icons/shortcut-profile.png
convert source.png -resize 192x192 public/icons/shortcut-offline.png

# Generate additional assets
convert source.png -resize 180x180 public/apple-touch-icon.png
convert source.png -resize 32x32 public/favicon.ico
convert source.png -resize 1200x630 public/og-image.png
convert source.png -resize 72x72 public/icons/badge-72x72.png

echo "Icon generation complete!"
echo "Don't forget to optimize the images for web use."
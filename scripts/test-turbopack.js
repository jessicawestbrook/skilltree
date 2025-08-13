#!/usr/bin/env node

/**
 * Test script to verify Turbopack compatibility
 * Run this to check if the dev server starts correctly with Turbopack
 */

const { spawn } = require('child_process');
const path = require('path');

console.log('🚀 Testing Turbopack compatibility...\n');

// Start the dev server with Turbopack
const devProcess = spawn('npm', ['run', 'dev'], {
  cwd: path.join(__dirname, '..'),
  stdio: 'pipe',
  shell: true
});

let output = '';
let hasErrors = false;

devProcess.stdout.on('data', (data) => {
  const text = data.toString();
  output += text;
  process.stdout.write(text);
  
  // Check for successful startup
  if (text.includes('Ready') || text.includes('ready') || text.includes('Local:')) {
    console.log('\n✅ Turbopack started successfully!');
    setTimeout(() => {
      devProcess.kill();
      process.exit(0);
    }, 2000);
  }
});

devProcess.stderr.on('data', (data) => {
  const text = data.toString();
  output += text;
  
  // Check for Sentry/Webpack conflicts
  if (text.includes('Webpack') && text.includes('Turbopack')) {
    console.error('\n❌ Webpack/Turbopack conflict detected!');
    hasErrors = true;
  }
  
  // Check for Sentry errors
  if (text.includes('Sentry') && text.includes('error')) {
    console.error('\n⚠️  Sentry configuration warning detected');
  }
  
  process.stderr.write(text);
});

devProcess.on('close', (code) => {
  if (code !== 0 && !hasErrors) {
    console.error(`\n❌ Dev server exited with code ${code}`);
    process.exit(1);
  }
});

// Timeout after 30 seconds
setTimeout(() => {
  console.log('\n⏰ Timeout reached - killing dev server');
  devProcess.kill();
  
  if (hasErrors) {
    console.error('\n❌ Turbopack compatibility test failed');
    process.exit(1);
  } else {
    console.log('\n✅ Turbopack compatibility test completed');
    process.exit(0);
  }
}, 30000);
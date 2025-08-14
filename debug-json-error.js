#!/usr/bin/env node

const http = require('http');
const https = require('https');

console.log('🔍 Debugging JSON parsing errors...\n');

const endpoints = [
  'http://localhost:3000/api/health',
  'http://localhost:3000/api/progress',
  'http://localhost:3000/api/activity-feed',
  'http://localhost:3000/api/analytics',
  'http://localhost:3000/api/auth/session'
];

async function checkEndpoint(url) {
  return new Promise((resolve) => {
    const client = url.startsWith('https') ? https : http;
    
    const req = client.get(url, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        const isHtml = data.trim().startsWith('<!DOCTYPE') || data.trim().startsWith('<html');
        const contentType = res.headers['content-type'] || 'unknown';
        
        resolve({
          url,
          status: res.statusCode,
          contentType,
          isHtml,
          dataLength: data.length,
          preview: data.substring(0, 200)
        });
      });
    });
    
    req.on('error', (error) => {
      resolve({
        url,
        error: error.message,
        status: 'ERROR'
      });
    });
    
    req.setTimeout(5000, () => {
      req.destroy();
      resolve({
        url,
        error: 'Timeout',
        status: 'TIMEOUT'
      });
    });
  });
}

async function runChecks() {
  console.log('Checking API endpoints...\n');
  
  for (const endpoint of endpoints) {
    console.log(`📡 Checking: ${endpoint}`);
    const result = await checkEndpoint(endpoint);
    
    if (result.error) {
      console.log(`❌ ERROR: ${result.error}`);
      if (result.error.includes('ECONNREFUSED')) {
        console.log('   💡 Development server might not be running. Try: npm run dev');
      }
    } else {
      console.log(`✅ Status: ${result.status}`);
      console.log(`📄 Content-Type: ${result.contentType}`);
      console.log(`📏 Data Length: ${result.dataLength} bytes`);
      
      if (result.isHtml) {
        console.log('🚨 WARNING: Received HTML instead of JSON!');
        console.log('   This will cause "Unexpected token \'<\'" errors');
        console.log(`   Preview: ${result.preview.substring(0, 100)}...`);
      } else if (result.contentType.includes('application/json')) {
        console.log('✅ Correctly returning JSON');
      } else {
        console.log(`⚠️ Unexpected content type: ${result.contentType}`);
      }
    }
    console.log('');
  }
  
  console.log('🔧 Troubleshooting Tips:');
  console.log('1. Make sure development server is running: npm run dev');
  console.log('2. Check browser network tab for failed API calls');
  console.log('3. Look for unhandled errors in API routes');
  console.log('4. Verify environment variables are set correctly');
  console.log('5. Check authentication - logged out users might get redirected');
  console.log('6. Clear browser cache and cookies');
  console.log('');
  console.log('If APIs are returning HTML, check:');
  console.log('- Next.js error pages instead of proper error handling');
  console.log('- Authentication middleware redirecting to login');
  console.log('- Missing error boundaries in API routes');
}

runChecks().catch(console.error);
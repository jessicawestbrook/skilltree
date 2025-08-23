/**
 * Generate math content with working images and skip counting demonstrations
 */

const fs = require('fs').promises
const path = require('path')

// Using SVG representations with realistic styling
function getCoinSVG(type, size = 80) {
  const coins = {
    penny: `<svg width="${size}" height="${size}" viewBox="0 0 100 100" class="coin-svg penny">
      <defs>
        <radialGradient id="pennyGradient">
          <stop offset="0%" style="stop-color:#d4824b;stop-opacity:1" />
          <stop offset="50%" style="stop-color:#b87333;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#8b4513;stop-opacity:1" />
        </radialGradient>
      </defs>
      <circle cx="50" cy="50" r="48" fill="url(#pennyGradient)" stroke="#6b3410" stroke-width="1"/>
      <circle cx="50" cy="50" r="44" fill="none" stroke="#8b4513" stroke-width="0.5"/>
      <text x="50" y="40" text-anchor="middle" font-size="14" font-family="serif" fill="#4a2c17">LINCOLN</text>
      <text x="50" y="55" text-anchor="middle" font-size="20" font-weight="bold" fill="#4a2c17">1¢</text>
      <text x="50" y="70" text-anchor="middle" font-size="10" fill="#4a2c17">ONE CENT</text>
    </svg>`,
    
    nickel: `<svg width="${size}" height="${size}" viewBox="0 0 100 100" class="coin-svg nickel">
      <defs>
        <radialGradient id="nickelGradient">
          <stop offset="0%" style="stop-color:#e8e8e8;stop-opacity:1" />
          <stop offset="50%" style="stop-color:#c0c0c0;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#999999;stop-opacity:1" />
        </radialGradient>
      </defs>
      <circle cx="50" cy="50" r="48" fill="url(#nickelGradient)" stroke="#666666" stroke-width="1"/>
      <circle cx="50" cy="50" r="44" fill="none" stroke="#808080" stroke-width="0.5"/>
      <text x="50" y="40" text-anchor="middle" font-size="14" font-family="serif" fill="#333">JEFFERSON</text>
      <text x="50" y="55" text-anchor="middle" font-size="20" font-weight="bold" fill="#333">5¢</text>
      <text x="50" y="70" text-anchor="middle" font-size="10" fill="#333">FIVE CENTS</text>
    </svg>`,
    
    dime: `<svg width="${size}" height="${size}" viewBox="0 0 100 100" class="coin-svg dime">
      <defs>
        <radialGradient id="dimeGradient">
          <stop offset="0%" style="stop-color:#f0f0f0;stop-opacity:1" />
          <stop offset="50%" style="stop-color:#d0d0d0;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#a0a0a0;stop-opacity:1" />
        </radialGradient>
      </defs>
      <circle cx="50" cy="50" r="40" fill="url(#dimeGradient)" stroke="#666666" stroke-width="1"/>
      <circle cx="50" cy="50" r="36" fill="none" stroke="#808080" stroke-width="0.5"/>
      <text x="50" y="40" text-anchor="middle" font-size="12" font-family="serif" fill="#333">ROOSEVELT</text>
      <text x="50" y="55" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">10¢</text>
      <text x="50" y="68" text-anchor="middle" font-size="9" fill="#333">ONE DIME</text>
    </svg>`,
    
    quarter: `<svg width="${size}" height="${size}" viewBox="0 0 100 100" class="coin-svg quarter">
      <defs>
        <radialGradient id="quarterGradient">
          <stop offset="0%" style="stop-color:#e8e8e8;stop-opacity:1" />
          <stop offset="50%" style="stop-color:#c0c0c0;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#999999;stop-opacity:1" />
        </radialGradient>
      </defs>
      <circle cx="50" cy="50" r="48" fill="url(#quarterGradient)" stroke="#666666" stroke-width="1"/>
      <circle cx="50" cy="50" r="44" fill="none" stroke="#808080" stroke-width="0.5"/>
      <text x="50" y="40" text-anchor="middle" font-size="14" font-family="serif" fill="#333">WASHINGTON</text>
      <text x="50" y="55" text-anchor="middle" font-size="20" font-weight="bold" fill="#333">25¢</text>
      <text x="50" y="70" text-anchor="middle" font-size="10" fill="#333">QUARTER DOLLAR</text>
    </svg>`
  }
  return coins[type] || coins.penny
}

function getBillSVG(type, width = 200) {
  const height = Math.round(width * 0.43)
  const bills = {
    dollar: `<svg width="${width}" height="${height}" viewBox="0 0 200 86" class="bill-svg dollar">
      <defs>
        <linearGradient id="dollarGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#93c47d;stop-opacity:1" />
          <stop offset="50%" style="stop-color:#85bb65;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#6aa84f;stop-opacity:1" />
        </linearGradient>
      </defs>
      <rect x="2" y="2" width="196" height="82" fill="url(#dollarGradient)" stroke="#2e7d32" stroke-width="2" rx="4"/>
      <rect x="10" y="10" width="180" height="66" fill="none" stroke="#4a8c4e" stroke-width="1" rx="2"/>
      <circle cx="100" cy="43" r="25" fill="none" stroke="#2e7d32" stroke-width="1"/>
      <text x="100" y="35" text-anchor="middle" font-size="12" font-family="serif" fill="#1a5d1f">THE UNITED STATES OF AMERICA</text>
      <text x="100" y="50" text-anchor="middle" font-size="28" font-weight="bold" fill="#0d3d10">$1</text>
      <text x="100" y="65" text-anchor="middle" font-size="10" fill="#1a5d1f">ONE DOLLAR</text>
      <text x="20" y="50" text-anchor="middle" font-size="16" fill="#2e7d32">1</text>
      <text x="180" y="50" text-anchor="middle" font-size="16" fill="#2e7d32">1</text>
    </svg>`,
    
    five: `<svg width="${width}" height="${height}" viewBox="0 0 200 86" class="bill-svg five">
      <defs>
        <linearGradient id="fiveGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#a3c293;stop-opacity:1" />
          <stop offset="50%" style="stop-color:#85bb65;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#5a9c3f;stop-opacity:1" />
        </linearGradient>
      </defs>
      <rect x="2" y="2" width="196" height="82" fill="url(#fiveGradient)" stroke="#2e7d32" stroke-width="2" rx="4"/>
      <rect x="10" y="10" width="180" height="66" fill="none" stroke="#4a8c4e" stroke-width="1" rx="2"/>
      <circle cx="100" cy="43" r="25" fill="none" stroke="#2e7d32" stroke-width="1"/>
      <text x="100" y="35" text-anchor="middle" font-size="12" font-family="serif" fill="#1a5d1f">THE UNITED STATES OF AMERICA</text>
      <text x="100" y="50" text-anchor="middle" font-size="28" font-weight="bold" fill="#0d3d10">$5</text>
      <text x="100" y="65" text-anchor="middle" font-size="10" fill="#1a5d1f">FIVE DOLLARS</text>
      <text x="20" y="50" text-anchor="middle" font-size="16" fill="#2e7d32">5</text>
      <text x="180" y="50" text-anchor="middle" font-size="16" fill="#2e7d32">5</text>
    </svg>`,
    
    ten: `<svg width="${width}" height="${height}" viewBox="0 0 200 86" class="bill-svg ten">
      <defs>
        <linearGradient id="tenGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#b3d2a3;stop-opacity:1" />
          <stop offset="50%" style="stop-color:#85bb65;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#4a8c2f;stop-opacity:1" />
        </linearGradient>
      </defs>
      <rect x="2" y="2" width="196" height="82" fill="url(#tenGradient)" stroke="#2e7d32" stroke-width="2" rx="4"/>
      <rect x="10" y="10" width="180" height="66" fill="none" stroke="#4a8c4e" stroke-width="1" rx="2"/>
      <circle cx="100" cy="43" r="25" fill="none" stroke="#2e7d32" stroke-width="1"/>
      <text x="100" y="35" text-anchor="middle" font-size="12" font-family="serif" fill="#1a5d1f">THE UNITED STATES OF AMERICA</text>
      <text x="100" y="50" text-anchor="middle" font-size="28" font-weight="bold" fill="#0d3d10">$10</text>
      <text x="100" y="65" text-anchor="middle" font-size="10" fill="#1a5d1f">TEN DOLLARS</text>
      <text x="20" y="50" text-anchor="middle" font-size="14" fill="#2e7d32">10</text>
      <text x="180" y="50" text-anchor="middle" font-size="14" fill="#2e7d32">10</text>
    </svg>`,
    
    twenty: `<svg width="${width}" height="${height}" viewBox="0 0 200 86" class="bill-svg twenty">
      <defs>
        <linearGradient id="twentyGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#c3e2b3;stop-opacity:1" />
          <stop offset="50%" style="stop-color:#85bb65;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#3a7c1f;stop-opacity:1" />
        </linearGradient>
      </defs>
      <rect x="2" y="2" width="196" height="82" fill="url(#twentyGradient)" stroke="#2e7d32" stroke-width="2" rx="4"/>
      <rect x="10" y="10" width="180" height="66" fill="none" stroke="#4a8c4e" stroke-width="1" rx="2"/>
      <circle cx="100" cy="43" r="25" fill="none" stroke="#2e7d32" stroke-width="1"/>
      <text x="100" y="35" text-anchor="middle" font-size="12" font-family="serif" fill="#1a5d1f">THE UNITED STATES OF AMERICA</text>
      <text x="100" y="50" text-anchor="middle" font-size="28" font-weight="bold" fill="#0d3d10">$20</text>
      <text x="100" y="65" text-anchor="middle" font-size="10" fill="#1a5d1f">TWENTY DOLLARS</text>
      <text x="20" y="50" text-anchor="middle" font-size="14" fill="#2e7d32">20</text>
      <text x="180" y="50" text-anchor="middle" font-size="14" fill="#2e7d32">20</text>
    </svg>`
  }
  return bills[type] || bills.dollar
}

function generateContent() {
  return `
<h1>Let's Learn to Count Money! 💰</h1>

<div class="intro-section">
  <h2>🎯 Today's Mission</h2>
  <p>Today we're going to become money counting experts! We'll learn about different coins and bills, and the super cool trick of skip counting!</p>
</div>

<div class="coin-guide">
  <h2>🪙 Meet the Coins!</h2>
  
  <div class="coin-card">
    <h3>Penny - 1 cent (1¢)</h3>
    <div class="coin-display">
      ${getCoinSVG('penny', 100)}
    </div>
    <p>This is a penny! It's copper colored (brownish-orange) and worth 1 cent.</p>
    <p><strong>Fun fact:</strong> President Abraham Lincoln is on the real penny!</p>
  </div>
  
  <div class="coin-card">
    <h3>Nickel - 5 cents (5¢)</h3>
    <div class="coin-display">
      ${getCoinSVG('nickel', 100)}
    </div>
    <p>This is a nickel! It's silver colored and bigger than a penny. It's worth 5 cents.</p>
    <p><strong>That means:</strong> 1 nickel = 5 pennies!</p>
  </div>
  
  <div class="coin-card">
    <h3>Dime - 10 cents (10¢)</h3>
    <div class="coin-display">
      ${getCoinSVG('dime', 100)}
    </div>
    <p>This is a dime! It's the smallest coin but worth 10 cents.</p>
    <p><strong>That means:</strong> 1 dime = 10 pennies = 2 nickels!</p>
  </div>
  
  <div class="coin-card">
    <h3>Quarter - 25 cents (25¢)</h3>
    <div class="coin-display">
      ${getCoinSVG('quarter', 100)}
    </div>
    <p>This is a quarter! It's the biggest everyday coin and worth 25 cents.</p>
    <p><strong>That means:</strong> 1 quarter = 25 pennies = 5 nickels!</p>
  </div>
</div>

<div class="skip-counting-section">
  <h2>🎮 The Skip Counting Trick!</h2>
  <p class="intro">Skip counting means counting by a number other than 1. It makes counting money MUCH faster!</p>
  
  <div class="skip-count-card">
    <h3>Counting Pennies (by 1s)</h3>
    <div class="coin-row">
      ${getCoinSVG('penny', 60)}
      ${getCoinSVG('penny', 60)}
      ${getCoinSVG('penny', 60)}
      ${getCoinSVG('penny', 60)}
      ${getCoinSVG('penny', 60)}
    </div>
    <p class="counting-sequence">1 → 2 → 3 → 4 → 5 = <strong>5 cents</strong></p>
  </div>
  
  <div class="skip-count-card">
    <h3>Counting Nickels (by 5s)</h3>
    <div class="coin-row">
      ${getCoinSVG('nickel', 60)}
      ${getCoinSVG('nickel', 60)}
      ${getCoinSVG('nickel', 60)}
      ${getCoinSVG('nickel', 60)}
    </div>
    <p class="counting-sequence">5 → 10 → 15 → 20 = <strong>20 cents</strong></p>
    <p class="tip">💡 Count by 5s: five, ten, fifteen, twenty!</p>
  </div>
  
  <div class="skip-count-card">
    <h3>Counting Dimes (by 10s)</h3>
    <div class="coin-row">
      ${getCoinSVG('dime', 60)}
      ${getCoinSVG('dime', 60)}
      ${getCoinSVG('dime', 60)}
      ${getCoinSVG('dime', 60)}
    </div>
    <p class="counting-sequence">10 → 20 → 30 → 40 = <strong>40 cents</strong></p>
    <p class="tip">💡 Count by 10s: ten, twenty, thirty, forty!</p>
  </div>
  
  <div class="skip-count-card">
    <h3>Counting Quarters (by 25s)</h3>
    <div class="coin-row">
      ${getCoinSVG('quarter', 60)}
      ${getCoinSVG('quarter', 60)}
      ${getCoinSVG('quarter', 60)}
      ${getCoinSVG('quarter', 60)}
    </div>
    <p class="counting-sequence">25 → 50 → 75 → 100 = <strong>$1.00</strong></p>
    <p class="tip">💡 Count by 25s: twenty-five, fifty, seventy-five, one hundred (that's a dollar!)</p>
  </div>
</div>

<div class="bill-guide">
  <h2>💵 Meet the Bills!</h2>
  
  <div class="bill-card">
    <h3>One Dollar Bill - $1.00</h3>
    ${getBillSVG('dollar', 250)}
    <p>This is a one dollar bill! It's worth 100 cents.</p>
    <p><strong>That means:</strong> $1 = 4 quarters = 10 dimes = 20 nickels = 100 pennies!</p>
  </div>
  
  <div class="bill-card">
    <h3>Five Dollar Bill - $5.00</h3>
    ${getBillSVG('five', 250)}
    <p>This is a five dollar bill! It's worth 500 cents.</p>
    <p><strong>That means:</strong> $5 = 5 one dollar bills = 20 quarters!</p>
  </div>
  
  <div class="bill-card">
    <h3>Ten Dollar Bill - $10.00</h3>
    ${getBillSVG('ten', 250)}
    <p>This is a ten dollar bill! It's worth 1,000 cents.</p>
    <p><strong>That means:</strong> $10 = 10 one dollar bills = 2 five dollar bills!</p>
  </div>
  
  <div class="bill-card">
    <h3>Twenty Dollar Bill - $20.00</h3>
    ${getBillSVG('twenty', 250)}
    <p>This is a twenty dollar bill! It's worth 2,000 cents.</p>
    <p><strong>That means:</strong> $20 = 20 one dollar bills = 4 five dollar bills = 2 ten dollar bills!</p>
  </div>
  
</div>

<div class="practice-section">
  <h2>🎮 Practice Time! Let's Count Money Together</h2>
  
  <div class="example-problem">
    <h3>Example 1: Count These Coins Using Skip Counting</h3>
    <div class="coin-display">
      ${getCoinSVG('quarter', 70)}
      ${getCoinSVG('quarter', 70)}
      ${getCoinSVG('dime', 70)}
      ${getCoinSVG('nickel', 70)}
    </div>
    <p><strong>Let's count together:</strong></p>
    <ol>
      <li>Start with quarters (count by 25s): <span class="highlight">25¢ → 50¢</span></li>
      <li>Add the dime (add 10): <span class="highlight">50¢ + 10¢ = 60¢</span></li>
      <li>Add the nickel (add 5): <span class="highlight">60¢ + 5¢ = 65¢</span></li>
    </ol>
    <p class="answer">Total: 65 cents! 🎉</p>
  </div>
  
  <div class="example-problem">
    <h3>Example 2: Skip Count These Dimes</h3>
    <div class="coin-display">
      ${getCoinSVG('dime', 70)}
      ${getCoinSVG('dime', 70)}
      ${getCoinSVG('dime', 70)}
      ${getCoinSVG('dime', 70)}
      ${getCoinSVG('dime', 70)}
    </div>
    <p><strong>Let's skip count by 10s:</strong></p>
    <p class="big-counting">10 → 20 → 30 → 40 → 50</p>
    <p class="answer">Total: 50 cents! 🎉</p>
  </div>
  
  <div class="example-problem">
    <h3>Example 3: Mix of Bills and Coins</h3>
    <div class="money-display">
      ${getBillSVG('dollar', 180)}
      ${getCoinSVG('quarter', 70)}
      ${getCoinSVG('quarter', 70)}
      ${getCoinSVG('quarter', 70)}
    </div>
    <p><strong>Let's count together:</strong></p>
    <ol>
      <li>Start with the dollar bill: <span class="highlight">$1.00</span></li>
      <li>Skip count the quarters (by 25s): <span class="highlight">25¢ → 50¢ → 75¢</span></li>
      <li>Add them together: <span class="highlight">$1.00 + 75¢ = $1.75</span></li>
    </ol>
    <p class="answer">Total: One dollar and seventy-five cents ($1.75)! 🎉</p>
  </div>
  
  <div class="example-problem">
    <h3>Example 4: Practice Skip Counting Nickels</h3>
    <div class="coin-display">
      ${getCoinSVG('nickel', 70)}
      ${getCoinSVG('nickel', 70)}
      ${getCoinSVG('nickel', 70)}
      ${getCoinSVG('nickel', 70)}
      ${getCoinSVG('nickel', 70)}
      ${getCoinSVG('nickel', 70)}
    </div>
    <p><strong>Let's skip count by 5s:</strong></p>
    <p class="big-counting">5 → 10 → 15 → 20 → 25 → 30</p>
    <p class="answer">Total: 30 cents! 🎉</p>
  </div>
  
  <div class="example-problem">
    <h3>Example 5: All Coins Challenge!</h3>
    <div class="coin-display">
      ${getCoinSVG('quarter', 70)}
      ${getCoinSVG('dime', 70)}
      ${getCoinSVG('dime', 70)}
      ${getCoinSVG('nickel', 70)}
      ${getCoinSVG('penny', 70)}
      ${getCoinSVG('penny', 70)}
      ${getCoinSVG('penny', 70)}
    </div>
    <p><strong>Let's count from biggest to smallest:</strong></p>
    <ol>
      <li>Quarter: <span class="highlight">25¢</span></li>
      <li>Two dimes (count by 10s): <span class="highlight">25¢ + 10¢ = 35¢ → 35¢ + 10¢ = 45¢</span></li>
      <li>Nickel: <span class="highlight">45¢ + 5¢ = 50¢</span></li>
      <li>Three pennies: <span class="highlight">50¢ + 1¢ + 1¢ + 1¢ = 53¢</span></li>
    </ol>
    <p class="answer">Total: 53 cents! 🎉</p>
  </div>
  
  <div class="example-problem">
    <h3>Example 6: Counting All Bills (No Coins)</h3>
    <div class="money-display">
      ${getBillSVG('twenty', 150)}
      ${getBillSVG('ten', 150)}
      ${getBillSVG('five', 150)}
      ${getBillSVG('dollar', 150)}
      ${getBillSVG('dollar', 150)}
    </div>
    <p><strong>Let's count from biggest to smallest:</strong></p>
    <ol>
      <li>Twenty dollar bill: <span class="highlight">$20.00</span></li>
      <li>Ten dollar bill: <span class="highlight">$20 + $10 = $30</span></li>
      <li>Five dollar bill: <span class="highlight">$30 + $5 = $35</span></li>
      <li>Two one dollar bills: <span class="highlight">$35 + $1 + $1 = $37</span></li>
    </ol>
    <p class="answer">Total: Thirty-seven dollars ($37.00)! 🎉</p>
  </div>
  
  <div class="example-problem">
    <h3>Example 7: Making Change - Store Practice</h3>
    <div class="scenario-box">
      <p>🛍️ <strong>Scenario:</strong> You buy a toy that costs $3.75. You pay with a $5 bill.</p>
    </div>
    <p><strong>How much change do you get?</strong></p>
    <ol>
      <li>Money given: <span class="highlight">$5.00</span></li>
      <li>Cost of toy: <span class="highlight">$3.75</span></li>
      <li>Change: <span class="highlight">$5.00 - $3.75 = $1.25</span></li>
    </ol>
    <p><strong>Your change would be:</strong></p>
    <div class="coin-display">
      ${getBillSVG('dollar', 120)}
      ${getCoinSVG('quarter', 70)}
    </div>
    <p class="answer">Change: $1.25 (one dollar and one quarter)! 🎉</p>
  </div>
  
  <div class="example-problem">
    <h3>Example 8: Saving Money - Piggy Bank Count</h3>
    <div class="scenario-box">
      <p>🐷 <strong>Your piggy bank has:</strong></p>
    </div>
    <div class="coin-display">
      ${getCoinSVG('quarter', 60)}
      ${getCoinSVG('quarter', 60)}
      ${getCoinSVG('quarter', 60)}
      ${getCoinSVG('quarter', 60)}
      ${getCoinSVG('quarter', 60)}
      ${getCoinSVG('quarter', 60)}
      ${getCoinSVG('quarter', 60)}
      ${getCoinSVG('quarter', 60)}
    </div>
    <p><strong>Let's skip count these 8 quarters by 25s:</strong></p>
    <p class="big-counting">25 → 50 → 75 → 100 → 125 → 150 → 175 → 200</p>
    <p class="answer">Total: $2.00 (Two dollars)! 🎉</p>
    <p class="tip">💡 Remember: 4 quarters = $1.00, so 8 quarters = $2.00!</p>
  </div>
  
  <div class="example-problem">
    <h3>Example 9: Mixed Bills and Coins</h3>
    <div class="money-display">
      ${getBillSVG('five', 150)}
      ${getBillSVG('dollar', 150)}
      ${getBillSVG('dollar', 150)}
      ${getCoinSVG('quarter', 70)}
      ${getCoinSVG('dime', 70)}
      ${getCoinSVG('dime', 70)}
      ${getCoinSVG('nickel', 70)}
    </div>
    <p><strong>Let's count everything:</strong></p>
    <ol>
      <li>Five dollar bill: <span class="highlight">$5.00</span></li>
      <li>Two one dollar bills: <span class="highlight">$5 + $1 + $1 = $7</span></li>
      <li>One quarter: <span class="highlight">$7.00 + 25¢ = $7.25</span></li>
      <li>Two dimes: <span class="highlight">$7.25 + 10¢ + 10¢ = $7.45</span></li>
      <li>One nickel: <span class="highlight">$7.45 + 5¢ = $7.50</span></li>
    </ol>
    <p class="answer">Total: Seven dollars and fifty cents ($7.50)! 🎉</p>
  </div>
  
  <div class="example-problem">
    <h3>Example 10: All Pennies Challenge!</h3>
    <div class="scenario-box">
      <p>🪙 <strong>Challenge:</strong> If you have 100 pennies, how much money do you have?</p>
    </div>
    <p><strong>Remember:</strong> 100 pennies = 100 cents = $1.00</p>
    <p class="answer">Total: One dollar ($1.00)! 🎉</p>
    <p class="tip">💡 Fun fact: That's why we call it a "cent" - there are 100 cents in a dollar, just like 100 years in a century!</p>
  </div>
</div>

<div class="tips-section">
  <h2>💡 Super Tips for Counting Money</h2>
  <ul>
    <li>🎯 <strong>Always start with the biggest coins or bills first</strong> - it makes counting easier!</li>
    <li>🎯 <strong>Group the same coins together</strong> - put all quarters in one pile, all dimes in another</li>
    <li>🎯 <strong>Use skip counting</strong>:
      <ul>
        <li>Pennies: count by 1s (1, 2, 3, 4...)</li>
        <li>Nickels: count by 5s (5, 10, 15, 20...)</li>
        <li>Dimes: count by 10s (10, 20, 30, 40...)</li>
        <li>Quarters: count by 25s (25, 50, 75, 100...)</li>
      </ul>
    </li>
    <li>🎯 <strong>Remember:</strong> 100 cents = 1 dollar</li>
  </ul>
</div>

<div class="fun-facts">
  <h2>🌟 Fun Money Facts!</h2>
  <ul>
    <li>🪙 The penny is the only copper-colored coin</li>
    <li>🪙 The dime is the smallest coin but not the least valuable!</li>
    <li>🪙 4 quarters make exactly $1.00</li>
    <li>💵 You can fold a dollar bill about 4,000 times before it tears!</li>
    <li>🎮 Arcade games often use quarters - that's why knowing 25¢ is important!</li>
  </ul>
</div>`
}

async function createVisualPreview() {
  const outputDir = path.join(__dirname, 'output', 'math_content', 'visual_fixed')
  await fs.mkdir(outputDir, { recursive: true })
  
  const content = {
    title: "Let's Learn to Count Money!",
    content: generateContent(),
    estimated_time_minutes: 15,
    difficulty_level: "beginner"
  }
  
  // Generate test questions
  const questions = [
    // Basic coin identification (5 questions)
    {
      id: "mc_001",
      question: "How many cents is a penny worth?",
      options: ["1 cent", "5 cents", "10 cents", "25 cents"],
      correct_answer: 0,
      explanation: "A penny is worth 1 cent. It's the smallest value coin and is copper-colored.",
      difficulty: "easy"
    },
    {
      id: "mc_002", 
      question: "How many cents is a nickel worth?",
      options: ["1 cent", "5 cents", "10 cents", "25 cents"],
      correct_answer: 1,
      explanation: "A nickel is worth 5 cents. One nickel equals 5 pennies.",
      difficulty: "easy"
    },
    {
      id: "mc_003",
      question: "How many cents is a dime worth?",
      options: ["1 cent", "5 cents", "10 cents", "25 cents"],
      correct_answer: 2,
      explanation: "A dime is worth 10 cents. It's the smallest coin in size but not in value!",
      difficulty: "easy"
    },
    {
      id: "mc_004",
      question: "How many cents is a quarter worth?",
      options: ["10 cents", "15 cents", "20 cents", "25 cents"],
      correct_answer: 3,
      explanation: "A quarter is worth 25 cents. Four quarters make one dollar.",
      difficulty: "easy"
    },
    {
      id: "mc_005",
      question: "Which coin is copper-colored?",
      options: ["Penny", "Nickel", "Dime", "Quarter"],
      correct_answer: 0,
      explanation: "The penny is the only copper-colored coin. All other coins are silver-colored.",
      difficulty: "easy"
    },
    
    // Coin equivalencies (5 questions)
    {
      id: "mc_006",
      question: "How many pennies equal one nickel?",
      options: ["2 pennies", "3 pennies", "5 pennies", "10 pennies"],
      correct_answer: 2,
      explanation: "One nickel (5¢) equals 5 pennies (5 × 1¢ = 5¢).",
      difficulty: "easy"
    },
    {
      id: "mc_007",
      question: "How many nickels equal one dime?",
      options: ["1 nickel", "2 nickels", "3 nickels", "4 nickels"],
      correct_answer: 1,
      explanation: "One dime (10¢) equals 2 nickels (2 × 5¢ = 10¢).",
      difficulty: "medium"
    },
    {
      id: "mc_008",
      question: "How many nickels equal one quarter?",
      options: ["3 nickels", "4 nickels", "5 nickels", "6 nickels"],
      correct_answer: 2,
      explanation: "One quarter (25¢) equals 5 nickels (5 × 5¢ = 25¢).",
      difficulty: "medium"
    },
    {
      id: "mc_009",
      question: "How many dimes equal one dollar?",
      options: ["5 dimes", "8 dimes", "10 dimes", "20 dimes"],
      correct_answer: 2,
      explanation: "One dollar (100¢) equals 10 dimes (10 × 10¢ = 100¢).",
      difficulty: "medium"
    },
    {
      id: "mc_010",
      question: "How many quarters equal one dollar?",
      options: ["2 quarters", "3 quarters", "4 quarters", "5 quarters"],
      correct_answer: 2,
      explanation: "One dollar (100¢) equals 4 quarters (4 × 25¢ = 100¢).",
      difficulty: "medium"
    },
    
    // Skip counting (5 questions)
    {
      id: "mc_011",
      question: "If you count 3 nickels by skip counting, what numbers do you say?",
      options: ["1, 2, 3", "5, 10, 15", "10, 20, 30", "25, 50, 75"],
      correct_answer: 1,
      explanation: "When counting nickels, you skip count by 5s: 5, 10, 15.",
      difficulty: "medium"
    },
    {
      id: "mc_012",
      question: "If you have 4 dimes and skip count them, what is your final total?",
      options: ["20 cents", "30 cents", "40 cents", "50 cents"],
      correct_answer: 2,
      explanation: "Skip counting 4 dimes by 10s: 10, 20, 30, 40. Total is 40 cents.",
      difficulty: "medium"
    },
    {
      id: "mc_013",
      question: "Skip counting 3 quarters gives you: 25, 50, ___?",
      options: ["60", "65", "70", "75"],
      correct_answer: 3,
      explanation: "When counting quarters by 25s: 25, 50, 75.",
      difficulty: "medium"
    },
    {
      id: "mc_014",
      question: "What do you count by when skip counting dimes?",
      options: ["Count by 1s", "Count by 5s", "Count by 10s", "Count by 25s"],
      correct_answer: 2,
      explanation: "Dimes are worth 10 cents each, so you count by 10s.",
      difficulty: "easy"
    },
    {
      id: "mc_015",
      question: "If you skip count 6 nickels, what is your total?",
      options: ["25 cents", "30 cents", "35 cents", "40 cents"],
      correct_answer: 1,
      explanation: "Skip counting 6 nickels by 5s: 5, 10, 15, 20, 25, 30. Total is 30 cents.",
      difficulty: "medium"
    },
    
    // Counting mixed coins (5 questions)
    {
      id: "mc_016",
      question: "You have 2 quarters and 1 dime. How much money do you have?",
      options: ["35 cents", "45 cents", "60 cents", "75 cents"],
      correct_answer: 2,
      explanation: "2 quarters = 50¢, plus 1 dime = 10¢. Total: 50¢ + 10¢ = 60¢.",
      difficulty: "medium"
    },
    {
      id: "mc_017",
      question: "You have 1 quarter, 2 dimes, and 1 nickel. How much money is that?",
      options: ["40 cents", "45 cents", "50 cents", "55 cents"],
      correct_answer: 2,
      explanation: "1 quarter (25¢) + 2 dimes (20¢) + 1 nickel (5¢) = 50¢.",
      difficulty: "medium"
    },
    {
      id: "mc_018",
      question: "You have 3 dimes and 3 pennies. What's your total?",
      options: ["30 cents", "33 cents", "36 cents", "39 cents"],
      correct_answer: 1,
      explanation: "3 dimes = 30¢, plus 3 pennies = 3¢. Total: 30¢ + 3¢ = 33¢.",
      difficulty: "medium"
    },
    {
      id: "mc_019",
      question: "You have 1 quarter, 1 dime, 1 nickel, and 1 penny. How much is that?",
      options: ["36 cents", "41 cents", "46 cents", "51 cents"],
      correct_answer: 1,
      explanation: "Quarter (25¢) + dime (10¢) + nickel (5¢) + penny (1¢) = 41¢.",
      difficulty: "hard"
    },
    {
      id: "mc_020",
      question: "You have 5 dimes and 2 quarters. What's the total?",
      options: ["75 cents", "$1.00", "$1.25", "$1.50"],
      correct_answer: 1,
      explanation: "5 dimes = 50¢, plus 2 quarters = 50¢. Total: 50¢ + 50¢ = 100¢ = $1.00.",
      difficulty: "hard"
    },
    
    // Bills and larger amounts (5 questions)
    {
      id: "mc_021",
      question: "How many cents are in one dollar?",
      options: ["50 cents", "75 cents", "100 cents", "125 cents"],
      correct_answer: 2,
      explanation: "One dollar equals 100 cents. That's why we write $1.00.",
      difficulty: "easy"
    },
    {
      id: "mc_022",
      question: "You have one $5 bill. How many $1 bills is that worth?",
      options: ["3 one dollar bills", "4 one dollar bills", "5 one dollar bills", "10 one dollar bills"],
      correct_answer: 2,
      explanation: "One $5 bill equals 5 one dollar bills.",
      difficulty: "medium"
    },
    {
      id: "mc_023",
      question: "You have $1.75. That's the same as:",
      options: ["1 dollar and 3 quarters", "1 dollar and 5 dimes", "1 dollar and 7 nickels", "2 dollars"],
      correct_answer: 0,
      explanation: "$1.75 = $1.00 + 75¢ = 1 dollar and 3 quarters (3 × 25¢ = 75¢).",
      difficulty: "hard"
    },
    {
      id: "mc_024",
      question: "How many quarters do you need to make $2.00?",
      options: ["4 quarters", "6 quarters", "8 quarters", "10 quarters"],
      correct_answer: 2,
      explanation: "$2.00 = 200 cents. Each quarter is 25¢. 200 ÷ 25 = 8 quarters.",
      difficulty: "hard"
    },
    {
      id: "mc_025",
      question: "You have one $10 bill. How many $5 bills is that worth?",
      options: ["1 five dollar bill", "2 five dollar bills", "3 five dollar bills", "5 five dollar bills"],
      correct_answer: 1,
      explanation: "One $10 bill equals 2 five dollar bills (2 × $5 = $10).",
      difficulty: "medium"
    },
    
    // Word problems (5 questions)
    {
      id: "mc_026",
      question: "You buy a toy for $3.25 and pay with a $5 bill. How much change do you get?",
      options: ["$1.25", "$1.50", "$1.75", "$2.25"],
      correct_answer: 2,
      explanation: "$5.00 - $3.25 = $1.75 in change.",
      difficulty: "hard"
    },
    {
      id: "mc_027",
      question: "Your piggy bank has 8 quarters. How much money is that?",
      options: ["$1.50", "$1.75", "$2.00", "$2.25"],
      correct_answer: 2,
      explanation: "8 quarters × 25¢ = 200¢ = $2.00. Remember: 4 quarters = $1, so 8 quarters = $2.",
      difficulty: "hard"
    },
    {
      id: "mc_028",
      question: "You want to buy candy that costs 50 cents. You have 3 dimes and 4 nickels. Do you have enough?",
      options: ["Yes, exactly enough", "Yes, with change", "No, need 5 more cents", "No, need 10 more cents"],
      correct_answer: 0,
      explanation: "3 dimes = 30¢, plus 4 nickels = 20¢. Total: 30¢ + 20¢ = 50¢. Exactly enough!",
      difficulty: "hard"
    },
    {
      id: "mc_029",
      question: "You save 2 quarters every week. After 4 weeks, how much have you saved?",
      options: ["$1.00", "$1.50", "$2.00", "$2.50"],
      correct_answer: 2,
      explanation: "2 quarters = 50¢ per week. After 4 weeks: 50¢ × 4 = 200¢ = $2.00.",
      difficulty: "hard"
    },
    {
      id: "mc_030",
      question: "You have 100 pennies. How much money is that?",
      options: ["50 cents", "75 cents", "$1.00", "$1.25"],
      correct_answer: 2,
      explanation: "100 pennies = 100 cents = $1.00. That's why it's called a cent - 100 in a dollar!",
      difficulty: "medium"
    }
  ]
  
  // Save JSON
  await fs.writeFile(
    path.join(outputDir, 'money_counting_visual.json'),
    JSON.stringify({
      nodeId: "fea1ba27-904d-4a1c-85d3-7e708a80727c",
      nodeName: "Money Counting",
      content: content,
      questions: questions
    }, null, 2)
  )
  
  // Create HTML preview with proper styling
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${content.title}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', 'Arial', sans-serif;
            line-height: 1.8;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #667eea;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        h2 {
            color: #764ba2;
            margin-top: 40px;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 3px solid #f0f0f0;
            padding-bottom: 10px;
        }
        
        h3 {
            color: #555;
            margin-top: 25px;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .intro-section {
            background: linear-gradient(135deg, #e3f2fd, #f3e5f5);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        .coin-guide, .bill-guide, .skip-counting-section {
            background: #f9f9f9;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        .coin-card, .bill-card, .skip-count-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }
        
        .coin-display, .coin-row, .bill-row {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        
        .coin-svg, .bill-svg {
            filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.2));
            transition: transform 0.3s;
        }
        
        .coin-svg:hover {
            transform: scale(1.1) rotate(10deg);
        }
        
        .bill-svg:hover {
            transform: scale(1.05);
        }
        
        .counting-sequence {
            font-size: 1.3em;
            text-align: center;
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            font-weight: bold;
            color: #2e7d32;
        }
        
        .big-counting {
            font-size: 1.8em;
            text-align: center;
            background: linear-gradient(135deg, #4caf50, #8bc34a);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-weight: bold;
            letter-spacing: 2px;
        }
        
        .tip {
            background: #fff3e0;
            padding: 10px;
            border-left: 4px solid #ff9800;
            margin: 10px 0;
            border-radius: 5px;
        }
        
        .practice-section {
            background: #e8f5e9;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        .example-problem {
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 25px;
            border-left: 5px solid #4caf50;
        }
        
        .money-display {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            background: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border: 2px dashed #ddd;
            flex-wrap: wrap;
        }
        
        .highlight {
            background: #ffeb3b;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        ol {
            margin: 15px 0;
            padding-left: 30px;
        }
        
        ol li {
            margin: 10px 0;
            font-size: 1.1em;
        }
        
        .answer {
            background: linear-gradient(135deg, #4caf50, #8bc34a);
            color: white;
            padding: 15px;
            border-radius: 10px;
            font-size: 1.3em;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
        }
        
        .tips-section {
            background: #fff3e0;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        .fun-facts {
            background: #f3e5f5;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        ul {
            margin: 15px 0;
            padding-left: 30px;
        }
        
        ul li {
            margin: 10px 0;
            font-size: 1.1em;
        }
        
        p {
            margin: 15px 0;
            font-size: 1.1em;
            line-height: 1.6;
        }
        
        .intro {
            font-size: 1.2em;
            color: #667eea;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }
            
            h1 {
                font-size: 1.8em;
            }
            
            h2 {
                font-size: 1.4em;
            }
            
            .coin-svg, .bill-svg {
                max-width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        ${content.content}
    </div>
</body>
</html>`
  
  await fs.writeFile(
    path.join(outputDir, 'money_counting_preview.html'),
    html
  )
  
  console.log(`
✅ Visual content with skip counting created successfully!

Files saved:
1. JSON: ${path.join(outputDir, 'money_counting_visual.json')}
2. HTML: ${path.join(outputDir, 'money_counting_preview.html')}

The content includes:
- SVG representations of all coins (penny, nickel, dime, quarter)
- SVG representations of bills ($1, $5)
- Detailed skip counting demonstrations for each coin type
- Step-by-step counting examples with visual displays
- Interactive hover effects on coins
- Kid-friendly design perfect for elementary students
`)
}

// Run the generator
createVisualPreview().catch(console.error)
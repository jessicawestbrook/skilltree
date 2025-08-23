/**
 * Generate math content with visual elements and example problems
 * Especially for elementary-level topics that need visual aids
 */

const fs = require('fs').promises
const path = require('path')
const Anthropic = require('@anthropic-ai/sdk')

// Load environment variables
require('dotenv').config({ path: path.join(__dirname, '../..', '.env.local') })

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
})

// URLs for US coin and bill images (using public domain/educational resources)
const MONEY_IMAGES = {
  penny_front: 'https://www.usmint.gov/wordpress/wp-content/uploads/2022/12/2023-lincoln-penny-uncirculated-obverse.jpg',
  penny_back: 'https://www.usmint.gov/wordpress/wp-content/uploads/2022/12/2023-lincoln-penny-uncirculated-reverse.jpg',
  nickel_front: 'https://www.usmint.gov/wordpress/wp-content/uploads/2022/06/2022-jefferson-nickel-uncirculated-obverse.jpg',
  nickel_back: 'https://www.usmint.gov/wordpress/wp-content/uploads/2022/06/2022-jefferson-nickel-uncirculated-reverse.jpg',
  dime_front: 'https://www.usmint.gov/wordpress/wp-content/uploads/2022/06/2022-roosevelt-dime-uncirculated-obverse.jpg',
  dime_back: 'https://www.usmint.gov/wordpress/wp-content/uploads/2022/06/2022-roosevelt-dime-uncirculated-reverse.jpg',
  quarter_front: 'https://www.usmint.gov/wordpress/wp-content/uploads/2022/01/2022-america-the-beautiful-quarters-coin-uncirculated-obverse.jpg',
  quarter_back: 'https://www.usmint.gov/wordpress/wp-content/uploads/2022/01/2022-america-the-beautiful-quarters-coin-uncirculated-reverse.jpg',
  dollar_bill: 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/US_one_dollar_bill%2C_obverse%2C_series_2009.jpg/1024px-US_one_dollar_bill%2C_obverse%2C_series_2009.jpg',
  five_dollar: 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/US_%245_Series_2006_obverse.jpg/1024px-US_%245_Series_2006_obverse.jpg',
  ten_dollar: 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/US10dollarbill-Series_2004A.jpg/1024px-US10dollarbill-Series_2004A.jpg',
  twenty_dollar: 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/US_%2420_Series_2006_Obverse.jpg/1024px-US_%2420_Series_2006_Obverse.jpg'
}

async function generateVisualMoneyContent() {
  const prompt = `Generate fun, visual learning content about "Money Counting" for elementary school children (ages 6-11).

Create an HTML lesson that teaches kids to recognize and count US coins and bills.

IMPORTANT: Include placeholders for images like [IMAGE: penny_front] that I will replace with actual images.

Structure the content as follows:

<h1>Let's Learn to Count Money!</h1>

<div class="intro-section">
  <h2>🎯 Today's Mission</h2>
  <p>Today we're going to become money counting experts! We'll learn about different coins and bills, and practice counting them together.</p>
</div>

<div class="coin-guide">
  <h2>🪙 Meet the Coins!</h2>
  
  <div class="coin-card">
    <h3>Penny - 1 cent (1¢)</h3>
    [IMAGE: penny_front]
    <p>This is a penny! It's copper colored (brownish) and worth 1 cent.</p>
    <p>Fun fact: It has President Abraham Lincoln on the front!</p>
  </div>
  
  <div class="coin-card">
    <h3>Nickel - 5 cents (5¢)</h3>
    [IMAGE: nickel_front]
    <p>This is a nickel! It's silver colored and bigger than a penny. It's worth 5 cents.</p>
    <p>That means 1 nickel = 5 pennies!</p>
  </div>
  
  <div class="coin-card">
    <h3>Dime - 10 cents (10¢)</h3>
    [IMAGE: dime_front]
    <p>This is a dime! It's the smallest coin but worth 10 cents.</p>
    <p>That means 1 dime = 10 pennies or 2 nickels!</p>
  </div>
  
  <div class="coin-card">
    <h3>Quarter - 25 cents (25¢)</h3>
    [IMAGE: quarter_front]
    <p>This is a quarter! It's the biggest common coin and worth 25 cents.</p>
    <p>That means 1 quarter = 25 pennies or 5 nickels!</p>
  </div>
</div>

<div class="bill-guide">
  <h2>💵 Meet the Bills!</h2>
  
  <div class="bill-card">
    <h3>One Dollar Bill - $1.00</h3>
    [IMAGE: dollar_bill]
    <p>This is a one dollar bill! It's worth 100 cents.</p>
    <p>That means $1 = 4 quarters = 10 dimes = 20 nickels = 100 pennies!</p>
  </div>
  
  <div class="bill-card">
    <h3>Five Dollar Bill - $5.00</h3>
    [IMAGE: five_dollar]
    <p>This is a five dollar bill! It's worth 500 cents.</p>
    <p>That means $5 = 5 one dollar bills!</p>
  </div>
</div>

<div class="practice-section">
  <h2>🎮 Practice Time! Let's Count Money Together</h2>
  
  <div class="example-problem">
    <h3>Example 1: Count These Coins</h3>
    <div class="coin-display">
      [IMAGE: quarter_front] [IMAGE: quarter_front] [IMAGE: dime_front] [IMAGE: nickel_front]
    </div>
    <p><strong>Let's count together:</strong></p>
    <ol>
      <li>First quarter: 25¢</li>
      <li>Second quarter: 25¢ + 25¢ = 50¢</li>
      <li>Add the dime: 50¢ + 10¢ = 60¢</li>
      <li>Add the nickel: 60¢ + 5¢ = 65¢</li>
    </ol>
    <p class="answer">Total: 65 cents!</p>
  </div>
  
  <div class="example-problem">
    <h3>Example 2: Count These Coins</h3>
    <div class="coin-display">
      [IMAGE: dime_front] [IMAGE: dime_front] [IMAGE: dime_front] [IMAGE: penny_front] [IMAGE: penny_front] [IMAGE: penny_front]
    </div>
    <p><strong>Let's count together:</strong></p>
    <ol>
      <li>Three dimes: 10¢ + 10¢ + 10¢ = 30¢</li>
      <li>Three pennies: 1¢ + 1¢ + 1¢ = 3¢</li>
      <li>Add them together: 30¢ + 3¢ = 33¢</li>
    </ol>
    <p class="answer">Total: 33 cents!</p>
  </div>
  
  <div class="example-problem">
    <h3>Example 3: Count Bills and Coins</h3>
    <div class="money-display">
      [IMAGE: dollar_bill] [IMAGE: quarter_front] [IMAGE: quarter_front] [IMAGE: quarter_front]
    </div>
    <p><strong>Let's count together:</strong></p>
    <ol>
      <li>One dollar bill: $1.00 (that's 100¢)</li>
      <li>Three quarters: 25¢ + 25¢ + 25¢ = 75¢</li>
      <li>Add them together: $1.00 + 75¢ = $1.75</li>
    </ol>
    <p class="answer">Total: One dollar and seventy-five cents ($1.75)!</p>
  </div>
</div>

<div class="tips-section">
  <h2>💡 Super Tips for Counting Money</h2>
  <ul>
    <li>Always start with the biggest coins or bills first - it makes counting easier!</li>
    <li>Group the same coins together (all quarters together, all dimes together)</li>
    <li>Count by skip counting: quarters by 25s, dimes by 10s, nickels by 5s</li>
    <li>Remember: 100 cents = 1 dollar</li>
  </ul>
</div>

<div class="fun-facts">
  <h2>🌟 Fun Money Facts!</h2>
  <ul>
    <li>The penny is the only copper-colored coin</li>
    <li>The dime is the smallest coin but not the least valuable!</li>
    <li>Quarters are used in gumball machines and arcade games</li>
    <li>A dollar bill can be folded about 4,000 times before it tears!</li>
  </ul>
</div>

Return as JSON:
{
  "title": "Let's Learn to Count Money!",
  "content": "[The HTML content above]",
  "estimated_time_minutes": 15,
  "difficulty_level": "beginner",
  "images_needed": ["penny", "nickel", "dime", "quarter", "dollar", "five_dollar"]
}`

  try {
    const response = await anthropic.messages.create({
      model: "claude-3-haiku-20240307",
      max_tokens: 4000,
      temperature: 0.7,
      messages: [{ role: "user", content: prompt }]
    })
    
    let responseText = response.content[0].text
    
    // Try to extract JSON
    const jsonMatch = responseText.match(/\{[\s\S]*\}/)
    if (jsonMatch) {
      try {
        const parsed = JSON.parse(jsonMatch[0])
        
        // Replace image placeholders with actual images
        let content = parsed.content
        
        // Replace coin image placeholders
        content = content.replace(/\[IMAGE: penny_front\]/g, 
          `<img src="${MONEY_IMAGES.penny_front}" alt="Penny" class="coin-img">`)
        content = content.replace(/\[IMAGE: nickel_front\]/g, 
          `<img src="${MONEY_IMAGES.nickel_front}" alt="Nickel" class="coin-img">`)
        content = content.replace(/\[IMAGE: dime_front\]/g, 
          `<img src="${MONEY_IMAGES.dime_front}" alt="Dime" class="coin-img">`)
        content = content.replace(/\[IMAGE: quarter_front\]/g, 
          `<img src="${MONEY_IMAGES.quarter_front}" alt="Quarter" class="coin-img">`)
        
        // Replace bill image placeholders
        content = content.replace(/\[IMAGE: dollar_bill\]/g, 
          `<img src="${MONEY_IMAGES.dollar_bill}" alt="One Dollar Bill" class="bill-img">`)
        content = content.replace(/\[IMAGE: five_dollar\]/g, 
          `<img src="${MONEY_IMAGES.five_dollar}" alt="Five Dollar Bill" class="bill-img">`)
        
        parsed.content = content
        return parsed
        
      } catch (e) {
        console.log('JSON parse error:', e.message)
      }
    }
    
    // Fallback: create structured content manually
    return {
      title: "Let's Learn to Count Money!",
      content: generateManualContent(),
      estimated_time_minutes: 15,
      difficulty_level: "beginner"
    }
    
  } catch (error) {
    console.error('API error:', error.message)
    // Return manual content as fallback
    return {
      title: "Let's Learn to Count Money!",
      content: generateManualContent(),
      estimated_time_minutes: 15,
      difficulty_level: "beginner"
    }
  }
}

function generateManualContent() {
  return `
<h1>Let's Learn to Count Money! 💰</h1>

<div class="intro-section">
  <h2>🎯 Today's Mission</h2>
  <p>Today we're going to become money counting experts! We'll learn about different coins and bills, and practice counting them together.</p>
</div>

<div class="coin-guide">
  <h2>🪙 Meet the Coins!</h2>
  
  <div class="coin-card">
    <h3>Penny - 1 cent (1¢)</h3>
    <img src="${MONEY_IMAGES.penny_front}" alt="Penny" class="coin-img">
    <p>This is a penny! It's copper colored (brownish) and worth 1 cent.</p>
    <p>Fun fact: It has President Abraham Lincoln on the front!</p>
  </div>
  
  <div class="coin-card">
    <h3>Nickel - 5 cents (5¢)</h3>
    <img src="${MONEY_IMAGES.nickel_front}" alt="Nickel" class="coin-img">
    <p>This is a nickel! It's silver colored and bigger than a penny. It's worth 5 cents.</p>
    <p>That means 1 nickel = 5 pennies!</p>
  </div>
  
  <div class="coin-card">
    <h3>Dime - 10 cents (10¢)</h3>
    <img src="${MONEY_IMAGES.dime_front}" alt="Dime" class="coin-img">
    <p>This is a dime! It's the smallest coin but worth 10 cents.</p>
    <p>That means 1 dime = 10 pennies or 2 nickels!</p>
  </div>
  
  <div class="coin-card">
    <h3>Quarter - 25 cents (25¢)</h3>
    <img src="${MONEY_IMAGES.quarter_front}" alt="Quarter" class="coin-img">
    <p>This is a quarter! It's the biggest common coin and worth 25 cents.</p>
    <p>That means 1 quarter = 25 pennies or 5 nickels!</p>
  </div>
</div>

<div class="bill-guide">
  <h2>💵 Meet the Bills!</h2>
  
  <div class="bill-card">
    <h3>One Dollar Bill - $1.00</h3>
    <img src="${MONEY_IMAGES.dollar_bill}" alt="One Dollar Bill" class="bill-img">
    <p>This is a one dollar bill! It's worth 100 cents.</p>
    <p>That means $1 = 4 quarters = 10 dimes = 20 nickels = 100 pennies!</p>
  </div>
  
  <div class="bill-card">
    <h3>Five Dollar Bill - $5.00</h3>
    <img src="${MONEY_IMAGES.five_dollar}" alt="Five Dollar Bill" class="bill-img">
    <p>This is a five dollar bill! It's worth 500 cents.</p>
    <p>That means $5 = 5 one dollar bills!</p>
  </div>
</div>

<div class="practice-section">
  <h2>🎮 Practice Time! Let's Count Money Together</h2>
  
  <div class="example-problem">
    <h3>Example 1: Count These Coins</h3>
    <div class="coin-display">
      <img src="${MONEY_IMAGES.quarter_front}" alt="Quarter" class="coin-img">
      <img src="${MONEY_IMAGES.quarter_front}" alt="Quarter" class="coin-img">
      <img src="${MONEY_IMAGES.dime_front}" alt="Dime" class="coin-img">
      <img src="${MONEY_IMAGES.nickel_front}" alt="Nickel" class="coin-img">
    </div>
    <p><strong>Let's count together:</strong></p>
    <ol>
      <li>First quarter: 25¢</li>
      <li>Second quarter: 25¢ + 25¢ = 50¢</li>
      <li>Add the dime: 50¢ + 10¢ = 60¢</li>
      <li>Add the nickel: 60¢ + 5¢ = 65¢</li>
    </ol>
    <p class="answer">Total: 65 cents! 🎉</p>
  </div>
  
  <div class="example-problem">
    <h3>Example 2: Count These Coins</h3>
    <div class="coin-display">
      <img src="${MONEY_IMAGES.dime_front}" alt="Dime" class="coin-img">
      <img src="${MONEY_IMAGES.dime_front}" alt="Dime" class="coin-img">
      <img src="${MONEY_IMAGES.dime_front}" alt="Dime" class="coin-img">
      <img src="${MONEY_IMAGES.penny_front}" alt="Penny" class="coin-img">
      <img src="${MONEY_IMAGES.penny_front}" alt="Penny" class="coin-img">
      <img src="${MONEY_IMAGES.penny_front}" alt="Penny" class="coin-img">
    </div>
    <p><strong>Let's count together:</strong></p>
    <ol>
      <li>Three dimes: 10¢ + 10¢ + 10¢ = 30¢</li>
      <li>Three pennies: 1¢ + 1¢ + 1¢ = 3¢</li>
      <li>Add them together: 30¢ + 3¢ = 33¢</li>
    </ol>
    <p class="answer">Total: 33 cents! 🎉</p>
  </div>
  
  <div class="example-problem">
    <h3>Example 3: Count Bills and Coins</h3>
    <div class="money-display">
      <img src="${MONEY_IMAGES.dollar_bill}" alt="One Dollar Bill" class="bill-img">
      <img src="${MONEY_IMAGES.quarter_front}" alt="Quarter" class="coin-img">
      <img src="${MONEY_IMAGES.quarter_front}" alt="Quarter" class="coin-img">
      <img src="${MONEY_IMAGES.quarter_front}" alt="Quarter" class="coin-img">
    </div>
    <p><strong>Let's count together:</strong></p>
    <ol>
      <li>One dollar bill: $1.00 (that's 100¢)</li>
      <li>Three quarters: 25¢ + 25¢ + 25¢ = 75¢</li>
      <li>Add them together: $1.00 + 75¢ = $1.75</li>
    </ol>
    <p class="answer">Total: One dollar and seventy-five cents ($1.75)! 🎉</p>
  </div>
</div>

<div class="tips-section">
  <h2>💡 Super Tips for Counting Money</h2>
  <ul>
    <li>🎯 Always start with the biggest coins or bills first - it makes counting easier!</li>
    <li>🎯 Group the same coins together (all quarters together, all dimes together)</li>
    <li>🎯 Count by skip counting: quarters by 25s, dimes by 10s, nickels by 5s</li>
    <li>🎯 Remember: 100 cents = 1 dollar</li>
  </ul>
</div>

<div class="fun-facts">
  <h2>🌟 Fun Money Facts!</h2>
  <ul>
    <li>The penny is the only copper-colored coin</li>
    <li>The dime is the smallest coin but not the least valuable!</li>
    <li>Quarters are used in gumball machines and arcade games</li>
    <li>A dollar bill can be folded about 4,000 times before it tears!</li>
  </ul>
</div>`
}

async function createVisualPreview() {
  const content = await generateVisualMoneyContent()
  
  const outputDir = path.join(__dirname, 'output', 'math_content', 'visual')
  await fs.mkdir(outputDir, { recursive: true })
  
  // Save JSON
  await fs.writeFile(
    path.join(outputDir, 'money_counting_visual.json'),
    JSON.stringify({
      nodeId: "fea1ba27-904d-4a1c-85d3-7e708a80727c",
      nodeName: "Money Counting",
      content: content,
      questions: []
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
        
        .coin-guide, .bill-guide {
            background: #f9f9f9;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        .coin-card, .bill-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .coin-card:hover, .bill-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        
        .coin-img {
            width: 100px;
            height: 100px;
            object-fit: contain;
            display: inline-block;
            margin: 10px;
            border: 2px solid #ddd;
            border-radius: 50%;
            padding: 5px;
            background: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .bill-img {
            width: 300px;
            height: auto;
            display: block;
            margin: 15px 0;
            border: 2px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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
        
        .coin-display, .money-display {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
            border: 2px dashed #ddd;
        }
        
        .coin-display .coin-img {
            width: 80px;
            height: 80px;
        }
        
        .money-display .bill-img {
            display: inline-block;
            width: 200px;
            margin: 10px;
        }
        
        .money-display .coin-img {
            width: 80px;
            height: 80px;
            vertical-align: middle;
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
        
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }
            
            .coin-img {
                width: 60px;
                height: 60px;
            }
            
            .bill-img {
                width: 100%;
                max-width: 250px;
            }
            
            h1 {
                font-size: 1.8em;
            }
            
            h2 {
                font-size: 1.4em;
            }
        }
        
        /* Animation for coins */
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        .coin-img:hover {
            animation: bounce 0.5s ease;
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
✅ Visual content created successfully!

Files saved:
1. JSON: ${path.join(outputDir, 'money_counting_visual.json')}
2. HTML: ${path.join(outputDir, 'money_counting_preview.html')}

The content includes:
- Images of all coins (penny, nickel, dime, quarter)
- Images of bills ($1, $5)
- Step-by-step counting examples with visual coin displays
- Interactive-looking design perfect for elementary students
`)
}

// Run the generator
createVisualPreview().catch(console.error)
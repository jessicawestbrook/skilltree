const { createClient } = require('@supabase/supabase-js')
const fs = require('fs')
const path = require('path')

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL || 'your-supabase-url'
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY || 'your-supabase-anon-key'

if (!supabaseUrl || !supabaseKey || supabaseUrl === 'your-supabase-url') {
  console.error('Please set REACT_APP_SUPABASE_URL and REACT_APP_SUPABASE_ANON_KEY environment variables')
  process.exit(1)
}

const supabase = createClient(supabaseUrl, supabaseKey)

async function generateSitemap() {
  try {
    console.log('Fetching skill tree nodes...')
    
    // Fetch all published skill tree nodes that should be indexed
    const { data: nodes, error } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, path, updated_at, level')
      .order('level', { ascending: true })
    
    if (error) {
      throw error
    }

    console.log(`Found ${nodes.length} skill tree nodes`)

    const currentDate = new Date().toISOString().split('T')[0]
    
    let sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
  
  <!-- Homepage -->
  <url>
    <loc>https://skilltree.app/</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  
  <!-- Main Pages -->
  <url>
    <loc>https://skilltree.app/learning-paths</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  
  <url>
    <loc>https://skilltree.app/intro-assessment</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  
  <!-- Test Pages -->
  <url>
    <loc>https://skilltree.app/standardized-tests</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  
  <url>
    <loc>https://skilltree.app/iq-test</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  
  <url>
    <loc>https://skilltree.app/test/sat</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  
  <url>
    <loc>https://skilltree.app/test/act</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  
  <url>
    <loc>https://skilltree.app/test/lsat</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  
  <!-- Learning Tools -->
  <url>
    <loc>https://skilltree.app/spelling-bee</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  
  <url>
    <loc>https://skilltree.app/vocabulary-trainer</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  
  <url>
    <loc>https://skilltree.app/language-trainer</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  
  <url>
    <loc>https://skilltree.app/reading-comprehension</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
`

    // Add category pages (levels 1-3 for better SEO)
    const categoryNodes = nodes.filter(node => node.level <= 3 && node.level > 0)
    
    for (const node of categoryNodes) {
      const lastmod = node.updated_at ? new Date(node.updated_at).toISOString().split('T')[0] : currentDate
      const priority = node.level === 1 ? '0.9' : node.level === 2 ? '0.8' : '0.7'
      const changefreq = node.level === 1 ? 'weekly' : node.level === 2 ? 'weekly' : 'monthly'
      
      // Create SEO-friendly URL from node name
      const slug = node.name
        .toLowerCase()
        .replace(/[^a-z0-9\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .trim()
      
      sitemap += `  
  <!-- ${node.name} -->
  <url>
    <loc>https://skilltree.app/category/${node.id}/${slug}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>${changefreq}</changefreq>
    <priority>${priority}</priority>
  </url>`
    }

    sitemap += `
  
  <!-- Auth Pages -->
  <url>
    <loc>https://skilltree.app/signup</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.6</priority>
  </url>
  
  <url>
    <loc>https://skilltree.app/login</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.5</priority>
  </url>
  
  <!-- Support Pages -->
  <url>
    <loc>https://skilltree.app/feedback</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.4</priority>
  </url>
  
</urlset>`

    // Write sitemap to public directory
    const outputPath = path.join(__dirname, '../public/sitemap.xml')
    fs.writeFileSync(outputPath, sitemap, 'utf8')
    
    console.log(`✓ Generated sitemap with ${categoryNodes.length} category pages`)
    console.log(`✓ Sitemap saved to: ${outputPath}`)
    
  } catch (error) {
    console.error('Error generating sitemap:', error)
    process.exit(1)
  }
}

if (require.main === module) {
  generateSitemap()
}

module.exports = { generateSitemap }
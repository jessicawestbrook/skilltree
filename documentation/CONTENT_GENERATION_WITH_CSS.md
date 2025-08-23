# Content Generation with Embedded CSS

## Overview
All learning content should be generated as HTML with embedded CSS styles to ensure proper formatting across the application. The CSS should be included directly in the content using `<style>` tags at the beginning of the HTML.

## CSS Template Location
The CSS template is stored in: `scripts/content_generation/templates/learning_content_css.js`

## Usage in Content Generation

### 1. Import the CSS Template
```javascript
const { wrapWithCSS } = require('./templates/learning_content_css');
```

### 2. Generate HTML Content
When using Claude API or any content generation method, generate the HTML content with proper semantic structure using the CSS classes defined in the template.

### 3. Wrap Content with CSS
```javascript
const htmlContent = generateYourHTMLContent(); // Your content generation logic
const contentWithCSS = wrapWithCSS(htmlContent);
```

### 4. Save to Database
Store the `contentWithCSS` in the `learning_content.content` field.

## CSS Classes Available

### Layout Sections
- `.intro-section` / `.mission-section` - Green gradient introduction boxes
- `.content-section` - White content boxes with border
- `.key-concepts` / `.important-box` - Yellow gradient highlight boxes
- `.example-section` / `.practice-section` - Purple gradient example areas
- `.summary-section` / `.recap-section` - Blue gradient summary boxes

### Typography
- Standard HTML headers (h1-h4) are pre-styled
- Paragraphs and lists have appropriate spacing

### Special Elements
- `.tip` / `.hint` - Blue tip boxes with lightbulb icon
- `.warning` / `.caution` - Red warning boxes with warning icon
- `.fun-fact` / `.did-you-know` - Pink fun fact boxes
- `.solution` - Purple solution boxes for practice problems
- `.code-block` / `.formula` - Gray boxes for code or formulas

### Interactive Elements
- `.cards-grid` - Responsive grid for card layouts
- `.card` - Individual card styling with hover effects
- `.timeline` - Timeline layout for historical content
- `.visualization` - Container for visual elements

## Example HTML Structure

```html
<h1>Your Topic Title</h1>

<div class="intro-section">
  <h2>🎯 Learning Objectives</h2>
  <p>What we'll learn today...</p>
</div>

<div class="content-section">
  <h2>Main Concept</h2>
  <p>Content explanation...</p>
</div>

<div class="key-concepts">
  <h2>Key Points to Remember</h2>
  <ul>
    <li>Point 1</li>
    <li>Point 2</li>
  </ul>
</div>

<div class="example-section">
  <h2>Practice Examples</h2>
  <div class="example">
    <h3>Example 1</h3>
    <p>Problem statement...</p>
    <div class="solution">
      <strong>Solution:</strong> Answer explanation...
    </div>
  </div>
</div>

<div class="tip">
  Remember this helpful tip...
</div>

<div class="summary-section">
  <h2>What We Learned</h2>
  <p>Summary of key concepts...</p>
</div>
```

## Content Generation Prompt Template

When using Claude API, include instructions like:

```
Generate HTML content for [TOPIC]. Use these CSS classes:
- .intro-section for introduction
- .content-section for main content blocks
- .key-concepts for important points
- .example-section with nested .example and .solution divs for practice
- .tip for helpful hints
- .summary-section for recap

Structure the content with proper HTML tags (h1, h2, h3, p, ul, li).
Make it engaging for [TARGET_AGE_GROUP].
Include storytelling elements about how the concept was discovered.
Add a "why this matters" section.
End with thought-provoking questions.
```

## Dark Mode Support
The CSS template includes automatic dark mode support using `@media (prefers-color-scheme: dark)`. No additional configuration needed.

## Responsive Design
The CSS is mobile-responsive with breakpoints at 768px. Content will adapt automatically to different screen sizes.

## Testing Generated Content
Use the preview function to test how content will look:

```javascript
const { createCompleteHTMLDocument } = require('./templates/learning_content_css');

const preview = createCompleteHTMLDocument('Title', yourHTMLContent);
await fs.writeFile('preview.html', preview);
// Open preview.html in browser
```

## Important Notes

1. **Always include CSS**: Never save HTML content without the embedded CSS
2. **Use semantic HTML**: Proper use of h1-h4, p, ul, etc.
3. **Test responsiveness**: Check on mobile viewport
4. **Verify dark mode**: Test with dark mode enabled
5. **Keep content structured**: Use the provided CSS classes for consistent styling

## Migration of Existing Content

For content already in the database without CSS:
1. Fetch the content
2. Wrap it with the CSS template
3. Update the database record

Example migration script available at: `scripts/update_html_with_css.js`
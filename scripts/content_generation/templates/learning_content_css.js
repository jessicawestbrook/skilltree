/**
 * CSS Template for Learning Content Generation
 * =============================================
 * 
 * This module provides CSS styles that should be embedded in all
 * generated learning content HTML to ensure proper formatting.
 */

const LEARNING_CONTENT_CSS = `
<style>
  /* Base Learning Content Styles */
  .learning-content {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: #1f2937;
  }
  
  /* Typography */
  h1 {
    color: #059669;
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
    text-align: center;
    font-weight: 700;
  }
  
  h2 {
    color: #047857;
    font-size: 2rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
    font-weight: 600;
  }
  
  h3 {
    color: #065f46;
    font-size: 1.5rem;
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
    font-weight: 600;
  }
  
  h4 {
    color: #064e3b;
    font-size: 1.25rem;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
    font-weight: 600;
  }
  
  p {
    margin-bottom: 1rem;
    color: #374151;
  }
  
  /* Introduction/Mission Section */
  .intro-section, .mission-section {
    background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    border-left: 4px solid #22c55e;
  }
  
  .intro-section h2, .mission-section h2 {
    color: #166534;
    margin-bottom: 0.5rem;
  }
  
  .intro-section p, .mission-section p {
    color: #15803d;
    font-size: 1.1rem;
    margin: 0;
  }
  
  /* Content Sections */
  .content-section {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }
  
  /* Key Concepts Box */
  .key-concepts, .important-box {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 2rem 0;
    border-left: 4px solid #f59e0b;
  }
  
  .key-concepts h2, .important-box h2 {
    color: #92400e;
    margin-bottom: 1rem;
  }
  
  .key-concepts ul, .important-box ul {
    color: #78350f;
  }
  
  /* Example/Practice Problems */
  .example-section, .practice-section {
    background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
    border-radius: 12px;
    padding: 2rem;
    margin: 2rem 0;
  }
  
  .example-section h2, .practice-section h2 {
    color: #6b21a8;
    margin-bottom: 1.5rem;
    text-align: center;
  }
  
  .example, .practice-problem {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .example h3, .practice-problem h3 {
    color: #6b21a8;
    margin-bottom: 1rem;
  }
  
  /* Solution Box */
  .solution {
    background: #f3e8ff;
    border-radius: 8px;
    padding: 1rem;
    margin-top: 1rem;
    border-left: 4px solid #a855f7;
  }
  
  .solution strong {
    color: #6b21a8;
  }
  
  /* Tips and Hints */
  .tip, .hint {
    background: #dbeafe;
    border-left: 4px solid #3b82f6;
    border-radius: 4px;
    padding: 1rem;
    margin: 1rem 0;
    color: #1e40af;
  }
  
  .tip::before, .hint::before {
    content: "💡 ";
    font-size: 1.25rem;
  }
  
  /* Warning/Caution Box */
  .warning, .caution {
    background: #fee2e2;
    border-left: 4px solid #ef4444;
    border-radius: 4px;
    padding: 1rem;
    margin: 1rem 0;
    color: #991b1b;
  }
  
  .warning::before, .caution::before {
    content: "⚠️ ";
    font-size: 1.25rem;
  }
  
  /* Fun Facts */
  .fun-fact, .did-you-know {
    background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 2rem 0;
    border-left: 4px solid #ec4899;
  }
  
  .fun-fact h3, .did-you-know h3 {
    color: #be185d;
    margin-bottom: 0.5rem;
  }
  
  .fun-fact p, .did-you-know p {
    color: #9f1239;
  }
  
  /* Summary Section */
  .summary-section, .recap-section {
    background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
    border-radius: 12px;
    padding: 2rem;
    margin: 2rem 0;
  }
  
  .summary-section h2, .recap-section h2 {
    color: #075985;
    margin-bottom: 1.5rem;
    text-align: center;
  }
  
  /* Timeline */
  .timeline {
    position: relative;
    padding: 2rem 0;
  }
  
  .timeline::before {
    content: '';
    position: absolute;
    left: 50%;
    top: 0;
    bottom: 0;
    width: 2px;
    background: #d1d5db;
  }
  
  .timeline-item {
    position: relative;
    padding: 1rem 2rem;
    margin-bottom: 2rem;
    width: calc(50% - 2rem);
  }
  
  .timeline-item:nth-child(odd) {
    margin-left: auto;
  }
  
  .timeline-item::before {
    content: '';
    position: absolute;
    width: 12px;
    height: 12px;
    background: #059669;
    border: 2px solid white;
    border-radius: 50%;
    top: 1.5rem;
  }
  
  .timeline-item:nth-child(odd)::before {
    left: -6px;
  }
  
  .timeline-item:nth-child(even)::before {
    right: -6px;
  }
  
  .timeline-content {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .timeline-date {
    color: #059669;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }
  
  /* Lists */
  ul, ol {
    margin-bottom: 1rem;
    padding-left: 1.5rem;
  }
  
  li {
    margin-bottom: 0.5rem;
  }
  
  /* Code/Formula Blocks */
  .code-block, .formula {
    background: #f3f4f6;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 1rem;
    margin: 1rem 0;
    font-family: 'Courier New', monospace;
    overflow-x: auto;
  }
  
  .formula {
    text-align: center;
    font-size: 1.25rem;
    background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
  }
  
  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
  }
  
  th {
    background: #059669;
    color: white;
    padding: 0.75rem;
    text-align: left;
    font-weight: 600;
  }
  
  td {
    padding: 0.75rem;
    border: 1px solid #e5e7eb;
  }
  
  tr:nth-child(even) {
    background: #f9fafb;
  }
  
  /* Interactive Elements */
  .interactive-element {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border: 2px dashed #3b82f6;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 2rem 0;
    text-align: center;
  }
  
  /* Visualization Container */
  .visualization {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 2rem 0;
    padding: 1rem;
    background: #f9fafb;
    border-radius: 12px;
  }
  
  /* Progress Indicators */
  .progress-indicator {
    background: #e5e7eb;
    height: 8px;
    border-radius: 4px;
    margin: 1rem 0;
    overflow: hidden;
  }
  
  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #10b981 0%, #059669 100%);
    border-radius: 4px;
    transition: width 0.3s ease;
  }
  
  /* Cards Grid */
  .cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
  }
  
  .card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
  }
  
  .card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  }
  
  /* Dark Mode Support */
  @media (prefers-color-scheme: dark) {
    .learning-content {
      color: #e5e7eb;
    }
    
    h1 { color: #34d399; }
    h2 { color: #6ee7b7; }
    h3 { color: #86efac; }
    h4 { color: #bbf7d0; }
    p { color: #d1d5db; }
    
    .content-section,
    .example,
    .practice-problem,
    .timeline-content,
    .card {
      background: #1f2937;
      border-color: #374151;
      color: #e5e7eb;
    }
    
    .intro-section, .mission-section {
      background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
    }
    
    .intro-section h2, .mission-section h2 { color: #34d399; }
    .intro-section p, .mission-section p { color: #6ee7b7; }
    
    .key-concepts, .important-box {
      background: linear-gradient(135deg, #78350f 0%, #92400e 100%);
    }
    
    .key-concepts h2, .important-box h2 { color: #fbbf24; }
    .key-concepts ul, .important-box ul { color: #fde68a; }
    
    .example-section, .practice-section {
      background: linear-gradient(135deg, #4c1d95 0%, #5b21b6 100%);
    }
    
    .solution {
      background: #4c1d95;
      color: #e9d5ff;
    }
    
    .tip, .hint {
      background: #1e3a8a;
      color: #93c5fd;
    }
    
    .warning, .caution {
      background: #7f1d1d;
      color: #fecaca;
    }
    
    .code-block, .formula {
      background: #111827;
      border-color: #374151;
      color: #e5e7eb;
    }
    
    th {
      background: #065f46;
    }
    
    td {
      border-color: #374151;
    }
    
    tr:nth-child(even) {
      background: #111827;
    }
  }
  
  /* Responsive Design */
  @media (max-width: 768px) {
    h1 { font-size: 2rem; }
    h2 { font-size: 1.5rem; }
    h3 { font-size: 1.25rem; }
    h4 { font-size: 1.1rem; }
    
    .timeline::before {
      left: 1rem;
    }
    
    .timeline-item {
      width: calc(100% - 3rem);
      margin-left: 3rem !important;
    }
    
    .timeline-item::before {
      left: -2rem !important;
    }
    
    .cards-grid {
      grid-template-columns: 1fr;
    }
  }
  
  /* Print Styles */
  @media print {
    .intro-section,
    .key-concepts,
    .example-section,
    .practice-section,
    .fun-fact,
    .summary-section {
      background: none !important;
      border: 1px solid #000;
      padding: 0.5rem;
    }
    
    .card {
      page-break-inside: avoid;
    }
  }
</style>
`;

/**
 * Function to wrap HTML content with the CSS template
 * @param {string} htmlContent - The HTML content to wrap
 * @returns {string} - HTML content with embedded CSS
 */
function wrapWithCSS(htmlContent) {
  return LEARNING_CONTENT_CSS + '\n' + htmlContent;
}

/**
 * Function to create a complete HTML document with CSS
 * @param {string} title - The title of the content
 * @param {string} htmlContent - The HTML content
 * @returns {string} - Complete HTML document
 */
function createCompleteHTMLDocument(title, htmlContent) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f9fafb;">
    ${wrapWithCSS(htmlContent)}
</body>
</html>`;
}

module.exports = {
  LEARNING_CONTENT_CSS,
  wrapWithCSS,
  createCompleteHTMLDocument
};
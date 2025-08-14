import { Node } from '../types';

// Constants for node positioning
const NODE_WIDTH = 120; // Actual node width including margins
const NODE_HEIGHT = 140; // Actual node height including extra elements
const MIN_SPACING_X = 40; // Minimum horizontal spacing between nodes
const MIN_SPACING_Y = 60; // Minimum vertical spacing between nodes
const CATEGORY_SPACING = 100; // Space between categories
const DOMAIN_SPACING = 200; // Space between domains
const SUBNODE_SPACING_X = 30; // Horizontal spacing for subnodes
const SUBNODE_SPACING_Y = 40; // Vertical spacing for subnodes

// Helper function to check if two rectangles overlap
const isOverlapping = (rect1: { x: number; y: number; width: number; height: number }, 
                      rect2: { x: number; y: number; width: number; height: number }): boolean => {
  return !(rect1.x + rect1.width < rect2.x || 
          rect2.x + rect2.width < rect1.x || 
          rect1.y + rect1.height < rect2.y || 
          rect2.y + rect2.height < rect1.y);
};

// Helper function to find next available position without collision
const findAvailablePosition = (
  proposedX: number, 
  proposedY: number, 
  existingNodes: Array<{ x: number; y: number; width: number; height: number }>,
  maxX = 1200
): { x: number; y: number } => {
  const nodeRect = { 
    x: proposedX, 
    y: proposedY, 
    width: NODE_WIDTH, 
    height: NODE_HEIGHT 
  };
  
  // Check for collisions
  while (existingNodes.some(existing => isOverlapping(nodeRect, existing))) {
    // Try moving right first
    nodeRect.x += NODE_WIDTH + MIN_SPACING_X;
    
    // If we've gone too far right, move to next row
    if (nodeRect.x > maxX) {
      nodeRect.x = proposedX;
      nodeRect.y += NODE_HEIGHT + MIN_SPACING_Y;
    }
  }
  
  return { x: nodeRect.x, y: nodeRect.y };
};

// Improved positioning algorithm with collision detection
export const layoutNodesWithCollisionDetection = (
  hierarchicalData: any,
  expandedNodes: Set<string> = new Set()
): { nodes: Node[] } => {
  try {
    const nodes: Node[] = [];
    const occupiedRects: Array<{ x: number; y: number; width: number; height: number }> = [];
    let index = 0;
    let globalY = 80; // Start with some padding from top
    
    
    // Validate input data
    if (!hierarchicalData || typeof hierarchicalData !== 'object') {
      console.warn('Invalid hierarchical data provided to layout engine');
      return { nodes: [] };
    }
    
    // Process each category
    Object.entries(hierarchicalData).forEach(([categoryName, domains]) => {
    let categoryMaxY = globalY;
    
    if (typeof domains === 'object' && !Array.isArray(domains) && domains !== null) {
      // Process each domain in the category
      let domainStartX = 50;
      
      Object.entries(domains).forEach(([, domainNodes], domainIndex) => {
        let domainMaxY = globalY;
        let domainMaxX = domainStartX;
        
        // Process nodes in this domain
        (domainNodes as Node[]).forEach((node, nodeIndex) => {
          // Calculate proposed position
          const proposedX = domainStartX + (nodeIndex % 3) * (NODE_WIDTH + MIN_SPACING_X);
          const proposedY = globalY + Math.floor(nodeIndex / 3) * (NODE_HEIGHT + MIN_SPACING_Y);
          
          // Find collision-free position
          const position = findAvailablePosition(proposedX, proposedY, occupiedRects);
          
          const processedNode = {
            ...node,
            index: index++,
            x: position.x,
            y: position.y
          };
          nodes.push(processedNode);
          
          // Track occupied space
          const nodeRect = {
            x: position.x,
            y: position.y,
            width: NODE_WIDTH,
            height: NODE_HEIGHT
          };
          occupiedRects.push(nodeRect);
          
          // Update domain boundaries
          domainMaxY = Math.max(domainMaxY, position.y + NODE_HEIGHT);
          domainMaxX = Math.max(domainMaxX, position.x + NODE_WIDTH);
          
          // If this is an expanded parent node, add its subnodes
          if (node.isParent && node.subnodes && expandedNodes.has(node.id)) {
            const subnodesPerRow = 4; // More subnodes per row for better layout
            const subnodeStartX = position.x + NODE_WIDTH + SUBNODE_SPACING_X;
            const subnodeStartY = position.y;
            
            node.subnodes.forEach((subnode, subIndex) => {
              const row = Math.floor(subIndex / subnodesPerRow);
              const col = subIndex % subnodesPerRow;
              
              const subnodeProposedX = subnodeStartX + col * (80 + SUBNODE_SPACING_X);
              const subnodeProposedY = subnodeStartY + row * (90 + SUBNODE_SPACING_Y);
              
              // Find collision-free position for subnode
              const subnodePosition = findAvailablePosition(
                subnodeProposedX, 
                subnodeProposedY, 
                occupiedRects,
                1400 // Allow subnodes to extend further right
              );
              
              const processedSubnode = {
                ...subnode,
                index: index++,
                x: subnodePosition.x,
                y: subnodePosition.y
              };
              nodes.push(processedSubnode);
              
              // Track occupied space for subnode (smaller size)
              const subnodeRect = {
                x: subnodePosition.x,
                y: subnodePosition.y,
                width: 80,
                height: 90
              };
              occupiedRects.push(subnodeRect);
              
              // Update domain boundaries
              domainMaxY = Math.max(domainMaxY, subnodePosition.y + 90);
              domainMaxX = Math.max(domainMaxX, subnodePosition.x + 80);
            });
          }
        });
        
        // Update category max Y and prepare for next domain
        categoryMaxY = Math.max(categoryMaxY, domainMaxY);
        domainStartX = domainMaxX + DOMAIN_SPACING; // Move next domain to the right
      });
    } else if (Array.isArray(domains)) {
      // Process mastery nodes (single array)
      let currentX = 50;
      (domains as Node[]).forEach((node, nodeIndex) => {
        // Find collision-free position for mastery nodes
        const position = findAvailablePosition(currentX, globalY, occupiedRects);
        
        const processedNode = {
          ...node,
          index: index++,
          x: position.x,
          y: position.y
        };
        nodes.push(processedNode);
        
        // Track occupied space
        occupiedRects.push({
          x: position.x,
          y: position.y,
          width: NODE_WIDTH,
          height: NODE_HEIGHT
        });
        
        categoryMaxY = Math.max(categoryMaxY, position.y + NODE_HEIGHT);
        currentX = position.x + NODE_WIDTH + MIN_SPACING_X;
      });
    }
    
    // Move to next category position
    globalY = categoryMaxY + CATEGORY_SPACING;
  });
  
  return { nodes };
  } catch (error) {
    console.error('Error in layout engine:', error);
    // Return fallback layout on error
    return { 
      nodes: [], 
 
    };
  }
};
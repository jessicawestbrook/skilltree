import { Node, Connection, NodeState } from '../types';

export const getNodeState = (nodeId: string, conqueredNodes: string[], allNodes: Node[]): NodeState => {
  if (conqueredNodes.includes(nodeId)) return 'completed';
  
  const node = allNodes.find(n => n.id === nodeId);
  if (!node) return 'locked';
  
  // Check if prerequisites are met
  if (!node.prereqs || node.prereqs.length === 0) return 'available';
  
  const prereqsMet = node.prereqs.every((prereq: string) => 
    conqueredNodes.includes(prereq)
  );
  
  return prereqsMet ? 'available' : 'locked';
};

export const createHierarchicalConnections = (allNodes: Node[]): Connection[] => {
  const connections: Connection[] = [];
  
  allNodes.forEach(node => {
    if (node.prereqs && node.prereqs.length > 0) {
      node.prereqs.forEach((prereqId: string) => {
        const fromNode = allNodes.find(n => n.id === prereqId);
        if (fromNode) {
          connections.push({ from: prereqId, to: node.id });
        }
      });
    }
    
    // Add connections from parent to subnodes
    if (node.parentId) {
      const parentNode = allNodes.find(n => n.id === node.parentId);
      if (parentNode) {
        connections.push({ from: node.parentId, to: node.id });
      }
    }
  });
  
  return connections;
};

export const filterHierarchicalNodes = (
  allNodes: Node[],
  activeFilters: string[],
  searchTerm: string,
  currentView: string,
  expandedNodes: Set<string>
): Node[] => {
  let nodes = [...allNodes];
  
  // Filter out subnodes of collapsed parent nodes
  nodes = nodes.filter(node => {
    if (node.parentId && !expandedNodes.has(node.parentId)) {
      return false;
    }
    return true;
  });
  
  // Filter by domain
  if (activeFilters.length > 0) {
    nodes = nodes.filter(node => activeFilters.includes(node.domain));
  }
  
  // Filter by search
  if (searchTerm) {
    nodes = nodes.filter(node => 
      node.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }
  
  // Filter by view (removed category filtering since categories are no longer used)
  // View filtering can be reimplemented based on other criteria if needed
  
  return nodes;
};

export const toggleNodeExpansion = (
  nodeId: string, 
  expandedNodes: Set<string>
): Set<string> => {
  const newExpandedNodes = new Set(expandedNodes);
  
  if (newExpandedNodes.has(nodeId)) {
    newExpandedNodes.delete(nodeId);
  } else {
    newExpandedNodes.add(nodeId);
  }
  
  return newExpandedNodes;
};

export const getVisibleNodes = (
  allNodes: Node[],
  expandedNodes: Set<string>
): Node[] => {
  return allNodes.filter(node => {
    // Always show top-level nodes
    if (!node.parentId) return true;
    
    // Only show subnodes if their parent is expanded
    return expandedNodes.has(node.parentId);
  });
};

export const calculateHierarchicalProgress = (
  allNodes: Node[],
  conqueredNodes: string[],
  expandedNodes: Set<string>
): number => {
  const visibleNodes = getVisibleNodes(allNodes, expandedNodes);
  const completedVisibleNodes = visibleNodes.filter(node => 
    conqueredNodes.includes(node.id)
  );
  
  if (visibleNodes.length === 0) return 0;
  return Math.round((completedVisibleNodes.length / visibleNodes.length) * 100);
};
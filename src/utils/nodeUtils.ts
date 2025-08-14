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

export const createConnections = (allNodes: Node[]): Connection[] => {
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
  });
  return connections;
};

export const filterNodes = (
  allNodes: Node[],
  activeFilters: string[],
  searchTerm: string,
  currentView: string
): Node[] => {
  let nodes = [...allNodes];
  
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
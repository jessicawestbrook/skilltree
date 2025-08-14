'use client';

import React, { useRef, useMemo, useState, Suspense } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { 
  OrbitControls, 
  Stars, 
  Text, 
  Sphere, 
  Line,
  PerspectiveCamera,
  Float,
  TrackballControls,
  useTexture,
  Environment,
  Sparkles
} from '@react-three/drei';
import * as THREE from 'three';
import { Node } from '@/types';

interface KnowledgeNodeProps {
  node: Node;
  position: [number, number, number];
  onClick: (node: Node) => void;
  isCompleted: boolean;
  isAvailable: boolean;
  isSelected: boolean;
  connections: Array<[number, number, number]>;
}

function KnowledgeNode3D({ node, position, onClick, isCompleted, isAvailable, isSelected, connections }: KnowledgeNodeProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);
  
  // Determine node color based on state
  const nodeColor = useMemo(() => {
    if (isCompleted) return '#10b981'; // green
    if (isAvailable) return '#3b82f6'; // blue
    if (isSelected) return '#f59e0b'; // orange
    return '#6b7280'; // gray for locked
  }, [isCompleted, isAvailable, isSelected]);

  // Determine emissive intensity
  const emissiveIntensity = hovered ? 0.8 : isCompleted ? 0.5 : 0.3;

  // Animation
  useFrame((state) => {
    if (!meshRef.current) return;
    
    // Gentle rotation
    meshRef.current.rotation.y += 0.005;
    
    // Pulsing effect for available nodes
    if (isAvailable && !isCompleted) {
      meshRef.current.scale.setScalar(
        1 + Math.sin(state.clock.elapsedTime * 2) * 0.05
      );
    }
    
    // Hovering effect
    if (hovered) {
      meshRef.current.scale.setScalar(1.2);
    } else if (!isAvailable || isCompleted) {
      meshRef.current.scale.setScalar(1);
    }
  });

  // Node size based on importance
  const nodeSize = node.level === 0 ? 0.8 : node.level === 1 ? 0.6 : 0.4;

  return (
    <group position={position}>
      {/* Connections to other nodes */}
      {connections.map((targetPos, idx) => (
        <Line
          key={idx}
          points={[[0, 0, 0], targetPos]}
          color={isCompleted ? '#10b981' : '#374151'}
          lineWidth={1}
          opacity={0.3}
          transparent
        />
      ))}
      
      {/* Main node sphere */}
      <Float
        speed={2}
        rotationIntensity={0.5}
        floatIntensity={0.3}
      >
        <mesh
          ref={meshRef}
          onClick={(e) => {
            e.stopPropagation();
            onClick(node);
          }}
          onPointerOver={() => setHovered(true)}
          onPointerOut={() => setHovered(false)}
        >
          <sphereGeometry args={[nodeSize, 32, 32]} />
          <meshStandardMaterial
            color={nodeColor}
            emissive={nodeColor}
            emissiveIntensity={emissiveIntensity}
            metalness={0.4}
            roughness={0.3}
          />
        </mesh>
      </Float>

      {/* Glow effect */}
      {(isAvailable || isCompleted) && (
        <Sphere args={[nodeSize * 1.5, 16, 16]}>
          <meshBasicMaterial
            color={nodeColor}
            transparent
            opacity={0.1}
            side={THREE.BackSide}
          />
        </Sphere>
      )}

      {/* Node label */}
      <Text
        position={[0, nodeSize + 0.3, 0]}
        fontSize={0.2}
        color="white"
        anchorX="center"
        anchorY="middle"
      >
        {node.name}
      </Text>

      {/* Status indicator */}
      {isCompleted && (
        <Text
          position={[0, -nodeSize - 0.2, 0]}
          fontSize={0.15}
          color="#10b981"
        >
          ✓
        </Text>
      )}
      {!isAvailable && !isCompleted && (
        <Text
          position={[0, -nodeSize - 0.2, 0]}
          fontSize={0.15}
          color="#ef4444"
        >
          🔒
        </Text>
      )}

      {/* Particle effects for completed nodes */}
      {isCompleted && (
        <Sparkles
          count={20}
          scale={2}
          size={2}
          speed={0.5}
          color="#10b981"
        />
      )}
    </group>
  );
}

interface UniverseSceneProps {
  nodes: Node[];
  completedNodes: Set<string>;
  onNodeClick: (node: Node) => void;
  selectedNode: Node | null;
}

function UniverseScene({ nodes, completedNodes, onNodeClick, selectedNode }: UniverseSceneProps) {
  const { camera } = useThree();
  
  // Calculate 3D positions for nodes in a galaxy-like formation
  const nodePositions = useMemo(() => {
    const positions = new Map<string, [number, number, number]>();
    const domainGroups = new Map<string, Node[]>();
    
    // Group nodes by domain
    nodes.forEach(node => {
      const domain = node.domain || 'general';
      if (!domainGroups.has(domain)) {
        domainGroups.set(domain, []);
      }
      domainGroups.get(domain)!.push(node);
    });
    
    // Create spiral galaxy layout
    let domainIndex = 0;
    const domainCount = domainGroups.size;
    
    domainGroups.forEach((domainNodes, domain) => {
      const angleOffset = (domainIndex / domainCount) * Math.PI * 2;
      const spiralRadius = 10 + domainIndex * 3;
      
      domainNodes.forEach((node, nodeIndex) => {
        const nodeAngle = angleOffset + (nodeIndex / domainNodes.length) * Math.PI / 3;
        const radius = spiralRadius + (node.level || 0) * 2 + Math.random() * 2;
        const height = (node.level || 0) * 2 + (Math.random() - 0.5) * 3;
        
        const x = Math.cos(nodeAngle) * radius;
        const z = Math.sin(nodeAngle) * radius;
        const y = height;
        
        positions.set(node.id, [x, y, z]);
      });
      
      domainIndex++;
    });
    
    return positions;
  }, [nodes]);

  // Calculate connections
  const connections = useMemo(() => {
    const conns = new Map<string, Array<[number, number, number]>>();
    
    nodes.forEach(node => {
      const nodePos = nodePositions.get(node.id);
      if (!nodePos) return;
      
      const nodeConns: Array<[number, number, number]> = [];
      
      // Connect to prerequisites
      if (node.prereqs) {
        node.prereqs.forEach(prereqId => {
          const prereqPos = nodePositions.get(prereqId);
          if (prereqPos) {
            const relativePos: [number, number, number] = [
              prereqPos[0] - nodePos[0],
              prereqPos[1] - nodePos[1],
              prereqPos[2] - nodePos[2]
            ];
            nodeConns.push(relativePos);
          }
        });
      }
      
      conns.set(node.id, nodeConns);
    });
    
    return conns;
  }, [nodes, nodePositions]);

  // Auto-rotate camera
  useFrame((state) => {
    if (!selectedNode) {
      state.camera.position.x = Math.cos(state.clock.elapsedTime * 0.1) * 30;
      state.camera.position.z = Math.sin(state.clock.elapsedTime * 0.1) * 30;
      state.camera.lookAt(0, 0, 0);
    }
  });

  return (
    <>
      {/* Ambient lighting */}
      <ambientLight intensity={0.2} />
      <pointLight position={[10, 10, 10]} intensity={0.5} />
      <pointLight position={[-10, -10, -10]} intensity={0.3} color="#3b82f6" />
      
      {/* Galaxy core light */}
      <pointLight position={[0, 0, 0]} intensity={1} color="#f59e0b" />
      
      {/* Render all nodes */}
      {nodes.map(node => {
        const position = nodePositions.get(node.id);
        if (!position) return null;
        
        return (
          <KnowledgeNode3D
            key={node.id}
            node={node}
            position={position}
            onClick={onNodeClick}
            isCompleted={completedNodes.has(node.id)}
            isAvailable={!node.prereqs || node.prereqs.every(p => completedNodes.has(p))}
            isSelected={selectedNode?.id === node.id}
            connections={connections.get(node.id) || []}
          />
        );
      })}
      
      {/* Galaxy center */}
      <Sphere args={[1, 32, 32]} position={[0, 0, 0]}>
        <meshStandardMaterial
          color="#f59e0b"
          emissive="#f59e0b"
          emissiveIntensity={0.5}
        />
      </Sphere>
      
      {/* Particle field */}
      <Sparkles
        count={200}
        scale={50}
        size={1}
        speed={0.2}
        color="#ffffff"
      />
    </>
  );
}

interface KnowledgeUniverseProps {
  nodes: Node[];
  completedNodes: Set<string>;
  onNodeClick: (node: Node) => void;
  selectedNode: Node | null;
}

export default function KnowledgeUniverse({ 
  nodes, 
  completedNodes, 
  onNodeClick, 
  selectedNode 
}: KnowledgeUniverseProps) {
  return (
    <div className="w-full h-full relative">
      <Canvas className="bg-black">
        <PerspectiveCamera makeDefault position={[20, 15, 20]} fov={60} />
        <Stars 
          radius={100} 
          depth={50} 
          count={5000} 
          factor={4} 
          saturation={0} 
          fade 
          speed={1}
        />
        
        <Suspense fallback={null}>
          <UniverseScene
            nodes={nodes}
            completedNodes={completedNodes}
            onNodeClick={onNodeClick}
            selectedNode={selectedNode}
          />
        </Suspense>
        
        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          zoomSpeed={0.6}
          panSpeed={0.5}
          rotateSpeed={0.4}
          minDistance={5}
          maxDistance={100}
        />
      </Canvas>
      
      {/* UI Overlay */}
      <div className="absolute top-4 left-4 text-white bg-black/50 backdrop-blur-md rounded-lg p-4">
        <h2 className="text-xl font-bold mb-2">Knowledge Universe</h2>
        <p className="text-sm opacity-80">
          Navigate with mouse • Scroll to zoom • Click nodes to explore
        </p>
        <div className="mt-2 space-y-1 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span>Completed</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
            <span>Available</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-gray-500 rounded-full"></div>
            <span>Locked</span>
          </div>
        </div>
      </div>
      
      {/* Selected Node Info */}
      {selectedNode && (
        <div className="absolute bottom-4 left-4 right-4 md:left-auto md:right-4 md:w-96 text-white bg-black/70 backdrop-blur-md rounded-lg p-4">
          <h3 className="text-lg font-bold">{selectedNode.name}</h3>
          <p className="text-sm opacity-80 mt-1">
            Domain: {selectedNode.domain} • Level: {selectedNode.level}
          </p>
          <p className="text-sm mt-2">
            {selectedNode.prereqs?.length 
              ? `Prerequisites: ${selectedNode.prereqs.length} nodes`
              : 'No prerequisites'}
          </p>
          <button 
            onClick={() => onNodeClick(selectedNode)}
            className="mt-3 px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg text-sm font-medium transition-colors"
          >
            Start Learning
          </button>
        </div>
      )}
    </div>
  );
}
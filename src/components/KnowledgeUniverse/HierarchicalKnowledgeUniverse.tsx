'use client';

import React, { useRef, useMemo, useState, Suspense, useCallback } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { 
  OrbitControls, 
  Stars, 
  Text, 
  Sphere, 
  Line,
  PerspectiveCamera,
  Float,
  Sparkles
} from '@react-three/drei';
import * as THREE from 'three';
import { Node } from '@/types';
import { 
  knowledgeStructure, 
  KnowledgeCategory
} from '@/data/comprehensiveKnowledgeStructure';

interface CategoryNodeProps {
  category: KnowledgeCategory;
  position: [number, number, number];
  onClick: (category: KnowledgeCategory) => void;
  depth: number;
  isExpanded: boolean;
  isHovered: boolean;
  onHover: (category: KnowledgeCategory | null) => void;
}

function CategoryNode3D({ 
  category, 
  position, 
  onClick, 
  depth, 
  isExpanded,
  isHovered,
  onHover 
}: CategoryNodeProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [localHovered, setLocalHovered] = useState(false);
  
  const nodeColor = category.color || '#3b82f6';
  const emissiveIntensity = localHovered || isHovered ? 0.8 : 0.3;
  const scale = 2 - (depth * 0.3);
  
  useFrame((state) => {
    if (!meshRef.current) return;
    
    meshRef.current.rotation.y += 0.003;
    
    if (localHovered || isHovered) {
      meshRef.current.scale.setScalar(scale * 1.1);
    } else {
      meshRef.current.scale.setScalar(scale);
    }
    
    if (isExpanded) {
      meshRef.current.rotation.x = Math.sin(state.clock.elapsedTime) * 0.05;
    }
  });

  const hasSubcategories = category.subcategories && category.subcategories.length > 0;
  const nodeCount = category.nodes?.length || 0;
  const subcategoryCount = category.subcategories?.length || 0;

  return (
    <group position={position}>
      <Float
        speed={2}
        rotationIntensity={0.3}
        floatIntensity={0.2}
      >
        <mesh
          ref={meshRef}
          onClick={(e) => {
            e.stopPropagation();
            onClick(category);
          }}
          onPointerOver={() => {
            setLocalHovered(true);
            onHover(category);
          }}
          onPointerOut={() => {
            setLocalHovered(false);
            onHover(null);
          }}
        >
          {hasSubcategories ? (
            <boxGeometry args={[scale, scale, scale]} />
          ) : nodeCount > 0 ? (
            <dodecahedronGeometry args={[scale * 0.6, 0]} />
          ) : (
            <sphereGeometry args={[scale * 0.5, 32, 32]} />
          )}
          <meshStandardMaterial
            color={nodeColor}
            emissive={nodeColor}
            emissiveIntensity={emissiveIntensity}
            metalness={0.4}
            roughness={0.3}
            opacity={0.9}
            transparent
          />
        </mesh>
      </Float>

      {(localHovered || isHovered) && (
        <Sphere args={[scale * 0.7, 16, 16]}>
          <meshBasicMaterial
            color={nodeColor}
            transparent
            opacity={0.2}
            side={THREE.BackSide}
          />
        </Sphere>
      )}

      <group position={[0, scale * 0.7, 0]}>
        <mesh position={[0, 0, -0.05]}>
          <planeGeometry args={[scale * 2.5, scale * 0.5]} />
          <meshBasicMaterial color="#000000" opacity={0.8} transparent />
        </mesh>
        <Text
          position={[0, 0, 0]}
          fontSize={0.4}
          color="#ffffff"
          anchorX="center"
          anchorY="middle"
          maxWidth={3}
        >
          {category.name}
        </Text>
      </group>

      {(nodeCount > 0 || subcategoryCount > 0) && (
        <group position={[0, -scale * 0.7, 0]}>
          <mesh position={[0, 0, -0.05]}>
            <planeGeometry args={[scale * 2, scale * 0.35]} />
            <meshBasicMaterial color="#000000" opacity={0.7} transparent />
          </mesh>
          <Text
            position={[0, 0, 0]}
            fontSize={0.3}
            color="#ffffff"
            anchorX="center"
            anchorY="middle"
          >
            {subcategoryCount > 0 && `${subcategoryCount} categories`}
            {subcategoryCount > 0 && nodeCount > 0 && ' • '}
            {nodeCount > 0 && `${nodeCount} nodes`}
          </Text>
        </group>
      )}

      {(hasSubcategories || nodeCount > 0) && (
        <Text
          position={[scale * 0.6, scale * 0.6, 0]}
          fontSize={0.4}
          color={isExpanded ? '#10b981' : '#fbbf24'}
          outlineWidth={0.05}
          outlineColor="#000000"
          outlineBlur={0.1}
          outlineOpacity={1}
        >
          {hasSubcategories ? (isExpanded ? '−' : '+') : '→'}
        </Text>
      )}

      {isExpanded && (
        <Sparkles
          count={30}
          scale={scale * 2}
          size={3}
          speed={0.5}
          color={nodeColor}
        />
      )}
    </group>
  );
}

interface LeafNodeProps {
  node: Node;
  position: [number, number, number];
  onClick: (node: Node) => void;
  isCompleted: boolean;
  isAvailable: boolean;
}

function LeafNode3D({ node, position, onClick, isCompleted, isAvailable }: LeafNodeProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);
  
  const nodeColor = useMemo(() => {
    if (isCompleted) return '#10b981';
    if (isAvailable) return '#3b82f6';
    return '#6b7280';
  }, [isCompleted, isAvailable]);

  useFrame(() => {
    if (!meshRef.current) return;
    
    meshRef.current.rotation.y += 0.01;
    
    if (hovered) {
      meshRef.current.scale.setScalar(0.6);
    } else {
      meshRef.current.scale.setScalar(0.5);
    }
  });

  return (
    <group position={position}>
      <mesh
        ref={meshRef}
        onClick={(e) => {
          e.stopPropagation();
          onClick(node);
        }}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <sphereGeometry args={[0.5, 24, 24]} />
        <meshStandardMaterial
          color={nodeColor}
          emissive={nodeColor}
          emissiveIntensity={hovered ? 0.6 : 0.3}
          metalness={0.3}
          roughness={0.4}
        />
      </mesh>

      <group position={[0, 0.8, 0]}>
        <mesh position={[0, 0, -0.05]}>
          <planeGeometry args={[1.5, 0.3]} />
          <meshBasicMaterial color="#000000" opacity={0.8} transparent />
        </mesh>
        <Text
          position={[0, 0, 0]}
          fontSize={0.25}
          color="#ffffff"
          anchorX="center"
          anchorY="middle"
        >
          {node.name}
        </Text>
      </group>

      {isCompleted && (
        <Text
          position={[0, -0.6, 0]}
          fontSize={0.15}
          color="#10b981"
        >
          ✓
        </Text>
      )}
    </group>
  );
}

interface UniverseSceneProps {
  currentCategory: KnowledgeCategory;
  expandedCategories: Set<string>;
  completedNodes: Set<string>;
  onCategoryClick: (category: KnowledgeCategory) => void;
  onNodeClick: (node: Node) => void;
  hoveredCategory: KnowledgeCategory | null;
  onHoverCategory: (category: KnowledgeCategory | null) => void;
}

function UniverseScene({ 
  currentCategory,
  expandedCategories,
  completedNodes,
  onCategoryClick,
  onNodeClick,
  hoveredCategory,
  onHoverCategory
}: UniverseSceneProps) {
  
  const positions = useMemo(() => {
    const pos = new Map<string, [number, number, number]>();
    const radius = 10;
    
    if (currentCategory.subcategories) {
      const count = currentCategory.subcategories.length;
      currentCategory.subcategories.forEach((subcat, index) => {
        const angle = (index / count) * Math.PI * 2;
        const x = Math.cos(angle) * radius;
        const z = Math.sin(angle) * radius;
        const y = 0;
        pos.set(subcat.id, [x, y, z]);
        
        if (expandedCategories.has(subcat.id) && subcat.subcategories) {
          const subRadius = 5;
          subcat.subcategories.forEach((subsubcat, subIndex) => {
            const subAngle = angle + (subIndex / subcat.subcategories!.length) * Math.PI / 2 - Math.PI / 4;
            const subX = x + Math.cos(subAngle) * subRadius;
            const subZ = z + Math.sin(subAngle) * subRadius;
            const subY = -3;
            pos.set(subsubcat.id, [subX, subY, subZ]);
          });
        }
      });
    }
    
    if (currentCategory.nodes) {
      const nodeRadius = currentCategory.subcategories ? 15 : 8;
      currentCategory.nodes.forEach((node, index) => {
        const angle = (index / currentCategory.nodes!.length) * Math.PI * 2;
        const x = Math.cos(angle) * nodeRadius;
        const z = Math.sin(angle) * nodeRadius;
        const y = currentCategory.subcategories ? -5 : 0;
        pos.set(node.id, [x, y, z]);
      });
    }
    
    return pos;
  }, [currentCategory, expandedCategories]);

  useFrame((state) => {
    if (!hoveredCategory) {
      state.camera.position.x = Math.cos(state.clock.elapsedTime * 0.05) * 25;
      state.camera.position.z = Math.sin(state.clock.elapsedTime * 0.05) * 25;
      state.camera.position.y = 10;
      state.camera.lookAt(0, 0, 0);
    }
  });

  return (
    <>
      <ambientLight intensity={0.3} />
      <pointLight position={[10, 10, 10]} intensity={0.5} />
      <pointLight position={[-10, -10, -10]} intensity={0.3} color="#3b82f6" />
      <pointLight position={[0, 0, 0]} intensity={0.8} color={currentCategory.color || '#f59e0b'} />
      
      {currentCategory.subcategories?.map(subcat => {
        const pos = positions.get(subcat.id);
        if (!pos) return null;
        
        return (
          <React.Fragment key={subcat.id}>
            <CategoryNode3D
              category={subcat}
              position={pos}
              onClick={onCategoryClick}
              depth={1}
              isExpanded={expandedCategories.has(subcat.id)}
              isHovered={hoveredCategory?.id === subcat.id}
              onHover={onHoverCategory}
            />
            
            {expandedCategories.has(subcat.id) && subcat.subcategories?.map(subsubcat => {
              const subPos = positions.get(subsubcat.id);
              if (!subPos) return null;
              
              return (
                <React.Fragment key={subsubcat.id}>
                  <Line
                    points={[pos, subPos]}
                    color={subcat.color || '#374151'}
                    lineWidth={1}
                    opacity={0.3}
                    transparent
                  />
                  <CategoryNode3D
                    category={subsubcat}
                    position={subPos}
                    onClick={onCategoryClick}
                    depth={2}
                    isExpanded={expandedCategories.has(subsubcat.id)}
                    isHovered={hoveredCategory?.id === subsubcat.id}
                    onHover={onHoverCategory}
                  />
                </React.Fragment>
              );
            })}
          </React.Fragment>
        );
      })}
      
      {currentCategory.nodes?.map(node => {
        const pos = positions.get(node.id);
        if (!pos) return null;
        
        return (
          <LeafNode3D
            key={node.id}
            node={node}
            position={pos}
            onClick={onNodeClick}
            isCompleted={completedNodes.has(node.id)}
            isAvailable={!node.prereqs || node.prereqs.every(p => completedNodes.has(p))}
          />
        );
      })}
      
      <Sphere args={[0.5, 32, 32]} position={[0, 0, 0]}>
        <meshStandardMaterial
          color={currentCategory.color || '#f59e0b'}
          emissive={currentCategory.color || '#f59e0b'}
          emissiveIntensity={0.5}
        />
      </Sphere>
      
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

interface HierarchicalKnowledgeUniverseProps {
  completedNodes: Set<string>;
  onNodeClick: (node: Node) => void;
  selectedNode: Node | null;
}

export default function HierarchicalKnowledgeUniverse({ 
  completedNodes, 
  onNodeClick, 
  selectedNode 
}: HierarchicalKnowledgeUniverseProps) {
  const [currentCategory, setCurrentCategory] = useState<KnowledgeCategory>(knowledgeStructure);
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set());
  const [navigationStack, setNavigationStack] = useState<KnowledgeCategory[]>([knowledgeStructure]);
  const [hoveredCategory, setHoveredCategory] = useState<KnowledgeCategory | null>(null);

  const handleCategoryClick = useCallback((category: KnowledgeCategory) => {
    if (category.subcategories && category.subcategories.length > 0) {
      if (expandedCategories.has(category.id)) {
        setExpandedCategories(prev => {
          const next = new Set(prev);
          next.delete(category.id);
          return next;
        });
      } else {
        setExpandedCategories(prev => new Set(prev).add(category.id));
      }
    } else if (category.nodes && category.nodes.length > 0) {
      setCurrentCategory(category);
      setNavigationStack(prev => [...prev, category]);
      setExpandedCategories(new Set());
    }
  }, [expandedCategories]);

  const handleBack = useCallback(() => {
    if (navigationStack.length > 1) {
      const newStack = [...navigationStack];
      newStack.pop();
      const previousCategory = newStack[newStack.length - 1];
      setCurrentCategory(previousCategory);
      setNavigationStack(newStack);
      setExpandedCategories(new Set());
    }
  }, [navigationStack]);

  const handleDrillDown = useCallback((category: KnowledgeCategory) => {
    setCurrentCategory(category);
    setNavigationStack(prev => [...prev, category]);
    setExpandedCategories(new Set());
  }, []);

  return (
    <div className="w-full h-full relative">
      <Canvas className="bg-black">
        <PerspectiveCamera makeDefault position={[20, 10, 20]} fov={60} />
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
            currentCategory={currentCategory}
            expandedCategories={expandedCategories}
            completedNodes={completedNodes}
            onCategoryClick={handleCategoryClick}
            onNodeClick={onNodeClick}
            hoveredCategory={hoveredCategory}
            onHoverCategory={setHoveredCategory}
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
      
      <div className="absolute top-4 left-4 text-white bg-black/70 backdrop-blur-md rounded-lg p-4 max-w-sm">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-xl font-bold">Knowledge Universe</h2>
          {navigationStack.length > 1 && (
            <button
              onClick={handleBack}
              className="px-3 py-1 bg-blue-500/20 hover:bg-blue-500/30 rounded text-sm transition-colors"
            >
              ← Back
            </button>
          )}
        </div>
        
        <div className="text-sm opacity-80 mb-3">
          {navigationStack.map((cat, index) => (
            <React.Fragment key={cat.id}>
              {index > 0 && <span className="mx-1">›</span>}
              <span 
                className={index === navigationStack.length - 1 ? 'text-blue-400' : 'cursor-pointer hover:text-blue-300'}
                onClick={() => {
                  if (index < navigationStack.length - 1) {
                    const newStack = navigationStack.slice(0, index + 1);
                    setCurrentCategory(newStack[newStack.length - 1]);
                    setNavigationStack(newStack);
                    setExpandedCategories(new Set());
                  }
                }}
              >
                {cat.name}
              </span>
            </React.Fragment>
          ))}
        </div>
        
        <p className="text-xs opacity-60 mb-3">
          {currentCategory.description}
        </p>
        
        <div className="space-y-1 text-xs">
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
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-yellow-500"></div>
            <span>Category (click to expand)</span>
          </div>
        </div>
        
        <div className="mt-3 pt-3 border-t border-white/20 text-xs opacity-60">
          <p>Click categories to expand/drill down</p>
          <p>Click nodes to start learning</p>
          <p>Scroll to zoom • Drag to rotate</p>
        </div>
      </div>
      
      {hoveredCategory && (
        <div className="absolute bottom-4 left-4 right-4 md:left-auto md:right-4 md:w-96 text-white bg-black/80 backdrop-blur-md rounded-lg p-4">
          <h3 className="text-lg font-bold" style={{ color: hoveredCategory.color }}>
            {hoveredCategory.name}
          </h3>
          <p className="text-sm opacity-80 mt-1">
            {hoveredCategory.description}
          </p>
          {hoveredCategory.subcategories && (
            <p className="text-sm mt-2">
              Contains {hoveredCategory.subcategories.length} subcategories
            </p>
          )}
          {hoveredCategory.nodes && (
            <p className="text-sm mt-1">
              Contains {hoveredCategory.nodes.length} learning nodes
            </p>
          )}
          <button 
            onClick={() => handleDrillDown(hoveredCategory)}
            className="mt-3 px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg text-sm font-medium transition-colors"
          >
            Explore {hoveredCategory.name}
          </button>
        </div>
      )}
      
      {selectedNode && (
        <div className="absolute bottom-4 right-4 w-96 text-white bg-black/80 backdrop-blur-md rounded-lg p-4">
          <h3 className="text-lg font-bold">{selectedNode.name}</h3>
          <p className="text-sm opacity-80 mt-1">
            Difficulty: {selectedNode.difficulty} • Points: {selectedNode.points}
          </p>
          <p className="text-sm mt-2">
            {selectedNode.prereqs?.length 
              ? `Prerequisites: ${selectedNode.prereqs.join(', ')}`
              : 'No prerequisites'}
          </p>
          <button 
            onClick={() => onNodeClick(selectedNode)}
            className="mt-3 px-4 py-2 bg-green-500 hover:bg-green-600 rounded-lg text-sm font-medium transition-colors"
          >
            Start Learning
          </button>
        </div>
      )}
    </div>
  );
}
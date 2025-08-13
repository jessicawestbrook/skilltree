'use client';

import React from 'react';
import { Node } from '../types';
import { Zap, Lock, CheckCircle, ChevronRight, Plus, Minus } from 'lucide-react';

interface KnowledgeGraphViewProps {
  nodes: Node[];
  connections: Array<{ from: string; to: string }>;
  selectedNode: Node | null;
  onNodeClick: (node: Node) => void;
  expandedNodes: Set<string>;
  toggleNodeExpansion: (nodeId: string) => void;
  getNodeState: (nodeId: string) => 'completed' | 'available' | 'locked';
}

export default function KnowledgeGraphView({
  nodes,
  connections,
  selectedNode,
  onNodeClick,
  expandedNodes,
  toggleNodeExpansion,
  getNodeState
}: KnowledgeGraphViewProps) {
  return (
    <div className="relative w-full h-full min-h-[800px] bg-gradient-to-br from-gray-50 to-white dark:from-gray-900 dark:to-gray-800 rounded-2xl p-8">
      {/* Connections */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none">
        <defs>
          <linearGradient id="connectionGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#9333ea" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.3" />
          </linearGradient>
        </defs>
        {connections.map((conn, index) => {
          const fromNode = nodes.find(n => n.id === conn.from);
          const toNode = nodes.find(n => n.id === conn.to);
          if (!fromNode || !toNode) return null;
          
          return (
            <line
              key={index}
              x1={(fromNode.x || 0) + 60}
              y1={(fromNode.y || 0) + 60}
              x2={(toNode.x || 0) + 60}
              y2={(toNode.y || 0) + 60}
              stroke="url(#connectionGradient)"
              strokeWidth="2"
              strokeDasharray="5,5"
              className="animate-pulse"
            />
          );
        })}
      </svg>

      {/* Nodes */}
      {nodes.map((node) => {
        const state = getNodeState(node.id);
        const isSelected = selectedNode?.id === node.id;
        const isExpanded = expandedNodes.has(node.id);
        
        return (
          <div
            key={node.id}
            className={`absolute transform -translate-x-1/2 -translate-y-1/2 transition-all duration-300 ${
              isSelected ? 'scale-110 z-20' : 'hover:scale-105 z-10'
            }`}
            style={{ left: node.x, top: node.y }}
          >
            <div
              onClick={() => onNodeClick(node)}
              className={`
                relative w-28 h-28 rounded-2xl cursor-pointer
                flex flex-col items-center justify-center p-3
                backdrop-blur-sm transition-all duration-300
                ${state === 'completed' 
                  ? 'bg-gradient-to-br from-green-500 to-emerald-600 text-white shadow-green-500/30' 
                  : state === 'available'
                  ? 'bg-gradient-to-br from-blue-500 to-cyan-600 text-white shadow-blue-500/30 animate-pulse'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400 opacity-75'
                }
                ${isSelected ? 'ring-4 ring-white ring-opacity-60' : ''}
                shadow-xl hover:shadow-2xl
              `}
            >
              {/* Status Icon */}
              <div className="absolute -top-2 -right-2 w-6 h-6 bg-white dark:bg-gray-800 rounded-full flex items-center justify-center shadow-md">
                {state === 'completed' ? (
                  <CheckCircle className="w-4 h-4 text-green-500" />
                ) : state === 'available' ? (
                  <Zap className="w-4 h-4 text-blue-500" />
                ) : (
                  <Lock className="w-4 h-4 text-gray-400" />
                )}
              </div>

              {/* Node Content */}
              <div className="text-center">
                <div className="text-2xl mb-1">{'🧠'}</div>
                <div className="text-xs font-bold leading-tight">{node.name}</div>
                <div className="text-xs opacity-80 mt-1">
                  +{node.points} pts
                </div>
              </div>

              {/* Expand/Collapse for Parent Nodes */}
              {node.isParent && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    toggleNodeExpansion(node.id);
                  }}
                  className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-6 h-6 bg-white dark:bg-gray-800 rounded-full flex items-center justify-center shadow-md"
                >
                  {isExpanded ? (
                    <Minus className="w-3 h-3 text-gray-600" />
                  ) : (
                    <Plus className="w-3 h-3 text-gray-600" />
                  )}
                </button>
              )}

              {/* Difficulty Stars */}
              <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 flex gap-0.5">
                {[...Array(5)].map((_, i) => (
                  <div
                    key={i}
                    className={`w-2 h-2 ${
                      i < node.difficulty
                        ? 'bg-yellow-400'
                        : 'bg-gray-300 dark:bg-gray-600'
                    } rounded-full`}
                  />
                ))}
              </div>
            </div>

            {/* Subnodes Preview */}
            {node.isParent && !isExpanded && node.subnodes && (
              <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 text-xs text-gray-500 dark:text-gray-400 whitespace-nowrap">
                {node.subnodes.length} topics
              </div>
            )}
          </div>
        );
      })}

      {/* Selected Node Info Panel */}
      {selectedNode && (
        <div className="absolute bottom-8 left-8 right-8 bg-white dark:bg-gray-800 rounded-xl shadow-2xl p-6 max-w-md mx-auto">
          <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100 mb-2">
            {selectedNode.name}
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
            {'Master this knowledge to unlock new paths.'}
          </p>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4 text-sm">
              <span className="text-gray-500">Difficulty: {'⭐'.repeat(selectedNode.difficulty)}</span>
              <span className="text-gray-500">+{selectedNode.points} points</span>
            </div>
            {getNodeState(selectedNode.id) === 'available' && (
              <button className="px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-medium text-sm hover:shadow-lg transition-all">
                Start Learning
                <ChevronRight className="inline w-4 h-4 ml-1" />
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
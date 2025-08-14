'use client';

import React, { useState, useMemo } from 'react';
import { ChevronDown, ChevronRight, BookOpen, Trophy, Star, Lock, CheckCircle } from 'lucide-react';
import { KnowledgeCategory, flattenKnowledgeStructure } from '@/data/comprehensiveKnowledgeStructure';
import { Node } from '@/types';
import { useUserStats } from '@/hooks/useUserStats';

interface HierarchicalCategoryMenuProps {
  category: KnowledgeCategory;
  onNodeClick: (node: Node) => void;
  selectedNode?: Node | null;
  level?: number;
}

interface CategoryItemProps {
  category: KnowledgeCategory;
  onNodeClick: (node: Node) => void;
  selectedNode?: Node | null;
  level: number;
  userStats: any;
}

function CategoryItem({ category, onNodeClick, selectedNode, level, userStats }: CategoryItemProps) {
  const [isExpanded, setIsExpanded] = useState(level < 2); // Auto-expand first two levels
  
  const categoryStats = useMemo(() => {
    const allNodes = flattenKnowledgeStructure(category, [], new Set());
    const completedNodes = new Set(userStats.conqueredNodes);
    const completed = allNodes.filter(n => completedNodes.has(n.id)).length;
    
    return {
      total: allNodes.length,
      completed,
      percentage: allNodes.length > 0 ? Math.round((completed / allNodes.length) * 100) : 0
    };
  }, [category, userStats.conqueredNodes]);

  const hasSubcategories = category.subcategories && category.subcategories.length > 0;
  const hasNodes = category.nodes && category.nodes.length > 0;
  const hasContent = hasSubcategories || hasNodes;

  const toggleExpanded = () => {
    if (hasContent) {
      setIsExpanded(!isExpanded);
    }
  };

  const getNodeStatus = (node: Node) => {
    const isCompleted = userStats.conqueredNodes.includes(node.id);
    const isAvailable = !node.prereqs || node.prereqs.every(p => userStats.conqueredNodes.includes(p));
    
    return { isCompleted, isAvailable };
  };

  return (
    <div className="w-full">
      {/* Category Header */}
      <div
        onClick={toggleExpanded}
        className={`
          flex items-center justify-between p-3 rounded-lg transition-all duration-200
          ${hasContent ? 'cursor-pointer hover:bg-gray-50' : 'cursor-default'}
          ${level === 0 ? 'bg-white shadow-sm border' : ''}
          ${level === 1 ? 'bg-gray-50 border-l-4' : ''}
          ${level >= 2 ? 'bg-gray-25' : ''}
        `}
        style={{
          marginLeft: `${Math.max(0, level - 1) * 20}px`,
          borderLeftColor: level === 1 ? category.color : undefined
        }}
      >
        <div className="flex items-center space-x-3 flex-1">
          {/* Expand/Collapse Icon */}
          {hasContent ? (
            isExpanded ? (
              <ChevronDown size={18} className="text-gray-600 flex-shrink-0" />
            ) : (
              <ChevronRight size={18} className="text-gray-600 flex-shrink-0" />
            )
          ) : (
            <div className="w-[18px]" /> // Spacer for alignment
          )}

          {/* Category Icon */}
          <div 
            className={`
              flex items-center justify-center text-white font-bold rounded-lg flex-shrink-0
              ${level === 0 ? 'w-10 h-10' : level === 1 ? 'w-8 h-8' : 'w-6 h-6'}
            `}
            style={{ backgroundColor: category.color }}
          >
            <BookOpen size={level === 0 ? 20 : level === 1 ? 16 : 12} />
          </div>

          {/* Category Info */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-2">
              <h3 className={`
                font-semibold text-gray-900 truncate
                ${level === 0 ? 'text-lg' : level === 1 ? 'text-base' : 'text-sm'}
              `}>
                {category.name}
              </h3>
              
              {categoryStats.total > 0 && (
                <span className={`
                  text-green-600 font-medium flex-shrink-0
                  ${level === 0 ? 'text-sm' : 'text-xs'}
                `}>
                  {categoryStats.completed}/{categoryStats.total}
                </span>
              )}
            </div>
            
            <p className={`
              text-gray-600 truncate
              ${level === 0 ? 'text-sm mt-1' : 'text-xs'}
            `}>
              {category.description}
            </p>
          </div>
        </div>

        {/* Progress Indicator */}
        {categoryStats.total > 0 && (
          <div className="flex items-center space-x-2 flex-shrink-0 ml-3">
            <div className={`
              bg-gray-200 rounded-full overflow-hidden
              ${level === 0 ? 'w-16 h-2' : 'w-12 h-1.5'}
            `}>
              <div 
                className="h-full bg-green-500 transition-all duration-300"
                style={{ width: `${categoryStats.percentage}%` }}
              />
            </div>
            <span className="text-xs text-gray-500 w-8 text-right">
              {categoryStats.percentage}%
            </span>
          </div>
        )}
      </div>

      {/* Expanded Content */}
      {isExpanded && hasContent && (
        <div className="mt-2 space-y-2">
          {/* Subcategories */}
          {hasSubcategories && category.subcategories!.map((subcategory) => (
            <CategoryItem
              key={subcategory.id}
              category={subcategory}
              onNodeClick={onNodeClick}
              selectedNode={selectedNode}
              level={level + 1}
              userStats={userStats}
            />
          ))}

          {/* Nodes */}
          {hasNodes && (
            <div 
              className="space-y-1"
              style={{ marginLeft: `${level * 20 + 20}px` }}
            >
              {category.nodes!.map((node) => {
                const { isCompleted, isAvailable } = getNodeStatus(node);
                
                return (
                  <div
                    key={node.id}
                    onClick={() => isAvailable && onNodeClick(node)}
                    className={`
                      flex items-center justify-between p-2 rounded-md transition-all cursor-pointer
                      ${isAvailable ? 'hover:bg-blue-50' : 'opacity-60 cursor-not-allowed'}
                      ${isCompleted ? 'bg-green-50 border border-green-200' : 'bg-white border border-gray-200'}
                      ${selectedNode?.id === node.id ? 'border-blue-500 bg-blue-50 shadow-sm' : ''}
                    `}
                  >
                    <div className="flex items-center space-x-3 flex-1 min-w-0">
                      {/* Status Icon */}
                      <div className="flex-shrink-0">
                        {isCompleted ? (
                          <CheckCircle size={16} className="text-green-500" />
                        ) : isAvailable ? (
                          <div className="w-4 h-4 rounded-full border-2 border-gray-300" />
                        ) : (
                          <Lock size={14} className="text-gray-400" />
                        )}
                      </div>

                      {/* Node Info */}
                      <div className="flex-1 min-w-0">
                        <h4 className="text-sm font-medium text-gray-900 truncate">
                          {node.name}
                        </h4>
                        {node.prereqs && node.prereqs.length > 0 && (
                          <p className="text-xs text-gray-500 truncate">
                            Requires: {node.prereqs.length} topic{node.prereqs.length !== 1 ? 's' : ''}
                          </p>
                        )}
                      </div>
                    </div>

                    {/* Node Stats */}
                    <div className="flex items-center space-x-3 flex-shrink-0 text-xs text-gray-600">
                      {/* Difficulty */}
                      <div className="flex items-center space-x-1">
                        {[...Array(node.difficulty || 1)].map((_, i) => (
                          <Star key={i} size={10} className="fill-yellow-400 text-yellow-400" />
                        ))}
                      </div>
                      
                      {/* Points */}
                      <span className="font-medium text-blue-600">
                        +{node.points}
                      </span>

                      {/* Completion Status */}
                      {isCompleted && (
                        <Trophy size={14} className="text-green-500" />
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function HierarchicalCategoryMenu({ 
  category, 
  onNodeClick, 
  selectedNode, 
  level = 0 
}: HierarchicalCategoryMenuProps) {
  const { userStats } = useUserStats();

  return (
    <div className="space-y-2">
      <CategoryItem
        category={category}
        onNodeClick={onNodeClick}
        selectedNode={selectedNode}
        level={level}
        userStats={userStats}
      />
    </div>
  );
}
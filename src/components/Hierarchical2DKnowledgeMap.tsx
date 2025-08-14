'use client';

import React, { useState, useMemo, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { 
  ChevronRight, 
  ChevronDown, 
  Lock, 
  CheckCircle, 
  Star,
  BookOpen,
  Brain,
  Beaker,
  Languages,
  Palette,
  Code,
  Users,
  Wrench,
  Heart,
  Compass,
  DollarSign,
  Folder,
  FolderOpen
} from 'lucide-react';
import { Node } from '@/types';
import { 
  knowledgeStructure, 
  KnowledgeCategory,
  flattenKnowledgeStructure 
} from '@/data/comprehensiveKnowledgeStructure';

interface CategoryCardProps {
  category: KnowledgeCategory;
  depth: number;
  completedNodes: Set<string>;
  onNodeClick: (node: Node) => void;
  selectedNode: Node | null;
  onCategoryClick: (categoryId: string) => void;
}

const categoryIcons: { [key: string]: any } = {
  mathematics: Brain,
  sciences: Beaker,
  languages: Languages,
  arts: Palette,
  technology: Code,
  history: Compass,
  'social-sciences': Users,
  'practical-skills': Wrench,
  'health-fitness': Heart,
  'philosophy-religion': BookOpen,
  business: DollarSign,
};

function CategoryCard({
  category,
  depth,
  completedNodes,
  onNodeClick,
  selectedNode,
  onCategoryClick
}: CategoryCardProps) {
  const hasSubcategories = category.subcategories && category.subcategories.length > 0;
  const hasNodes = category.nodes && category.nodes.length > 0;
  const Icon = categoryIcons[category.id] || BookOpen;
  
  // Calculate completion stats
  const stats = useMemo(() => {
    const allNodes = flattenKnowledgeStructure(category, [], new Set());
    const completed = allNodes.filter(n => completedNodes.has(n.id)).length;
    return {
      total: allNodes.length,
      completed,
      percentage: allNodes.length > 0 ? Math.round((completed / allNodes.length) * 100) : 0
    };
  }, [category, completedNodes]);
  
  return (
    <div
      className="group relative bg-white rounded-2xl border border-gray-200 p-6 transition-all duration-300 cursor-pointer hover:shadow-2xl hover:border-transparent hover:scale-105 overflow-hidden"
      onClick={() => onCategoryClick(category.id)}
    >
      {/* Background gradient overlay on hover */}
      <div 
        className="absolute inset-0 opacity-0 group-hover:opacity-5 transition-opacity duration-300"
        style={{ background: `linear-gradient(135deg, ${category.color}20, ${category.color}10)` }}
      />
      
      <div className="relative z-10">
        <div className="flex items-start justify-between mb-4">
          <div className="relative">
            <div 
              className="w-20 h-20 rounded-2xl flex items-center justify-center text-white shadow-lg transform group-hover:scale-110 transition-transform duration-300"
              style={{ 
                background: `linear-gradient(135deg, ${category.color}, ${category.color}dd)`
              }}
            >
              <Icon size={36} />
            </div>
            {/* Glowing effect on hover */}
            <div 
              className="absolute inset-0 w-20 h-20 rounded-2xl opacity-0 group-hover:opacity-30 transition-opacity duration-300 blur-md"
              style={{ backgroundColor: category.color }}
            />
          </div>
          
          <div className="flex flex-col items-end gap-2">
            {stats.percentage === 100 && (
              <div className="flex items-center gap-1 bg-green-100 px-2 py-1 rounded-full">
                <CheckCircle size={16} className="text-green-600" />
                <span className="text-xs font-semibold text-green-700">Complete</span>
              </div>
            )}
            {stats.percentage > 0 && stats.percentage < 100 && (
              <div className="flex items-center gap-1 bg-blue-100 px-2 py-1 rounded-full">
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
                <span className="text-xs font-semibold text-blue-700">In Progress</span>
              </div>
            )}
          </div>
        </div>
        
        <div className="space-y-4">
          <div>
            <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-gray-700 transition-colors">
              {category.name}
            </h3>
            <p className="text-sm text-gray-600 leading-relaxed h-10 overflow-hidden">
              {category.description.length > 85 
                ? `${category.description.substring(0, 85)}...` 
                : category.description
              }
            </p>
          </div>
          
          <div className="space-y-3">
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center gap-4 text-gray-500">
                {hasSubcategories && (
                  <div className="flex items-center gap-1">
                    <div className="w-2 h-2 rounded-full bg-blue-400" />
                    <span>{category.subcategories.length} categories</span>
                  </div>
                )}
                {hasNodes && (
                  <div className="flex items-center gap-1">
                    <div className="w-2 h-2 rounded-full bg-purple-400" />
                    <span>{category.nodes.length} topics</span>
                  </div>
                )}
              </div>
              {stats.total > 0 && (
                <span className={`font-bold px-2 py-1 rounded-full text-xs ${
                  stats.percentage === 0 
                    ? 'text-gray-600 bg-gray-100' 
                    : 'text-green-600 bg-green-50'
                }`}>
                  {stats.percentage === 0 ? 'Not Started' : `${stats.percentage}% complete`}
                </span>
              )}
            </div>
            
            {stats.total > 0 && (
              <div className="relative">
                <div className="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-green-400 to-green-600 transition-all duration-500 ease-out rounded-full shadow-sm"
                    style={{ width: `${stats.percentage}%` }}
                  />
                </div>
                {/* Progress bar glow effect */}
                {stats.percentage > 0 && (
                  <div 
                    className="absolute inset-0 h-3 bg-gradient-to-r from-green-400 to-green-600 rounded-full opacity-20 blur-sm transition-all duration-500"
                    style={{ width: `${stats.percentage}%` }}
                  />
                )}
              </div>
            )}
          </div>
        </div>
        
        {/* Subtle hover indicator */}
        <div className="absolute bottom-4 right-4 opacity-0 group-hover:opacity-60 transition-opacity duration-300">
          <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
            <ChevronRight size={16} className="text-gray-600" />
          </div>
        </div>
      </div>
    </div>
  );
}

interface Hierarchical2DKnowledgeMapProps {
  completedNodes: Set<string>;
  onNodeClick: (node: Node) => void;
  selectedNode: Node | null;
}

export default function Hierarchical2DKnowledgeMap({
  completedNodes,
  onNodeClick,
  selectedNode
}: Hierarchical2DKnowledgeMapProps) {
  const router = useRouter();
  
  const handleCategoryClick = useCallback((categoryId: string) => {
    router.push(`/category/${categoryId}`);
  }, [router]);
  
  // Calculate overall progress
  const overallStats = useMemo(() => {
    const allNodes = flattenKnowledgeStructure(knowledgeStructure, [], new Set());
    const completed = allNodes.filter(n => completedNodes.has(n.id)).length;
    return {
      total: allNodes.length,
      completed,
      percentage: allNodes.length > 0 ? Math.round((completed / allNodes.length) * 100) : 0
    };
  }, [completedNodes]);
  
  return (
    <div className="w-full bg-gray-50 rounded-xl p-6">
      {/* Header */}
      <div className="mb-6 bg-white rounded-lg p-4 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Knowledge Map</h2>
            <p className="text-gray-600">Click on categories to explore and learn</p>
          </div>
        </div>
        
        {/* Overall Progress */}
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Overall Progress</span>
            <span className="text-sm font-bold text-gray-900">
              {overallStats.completed} / {overallStats.total} topics completed
            </span>
          </div>
          <div className="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-blue-500 to-green-500 transition-all duration-500"
              style={{ width: `${overallStats.percentage}%` }}
            />
          </div>
          <div className="mt-2 text-xs text-gray-500 text-right">
            {overallStats.percentage}% Complete
          </div>
        </div>
      </div>
      
      {/* Categories Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {knowledgeStructure.subcategories?.map(category => (
          <CategoryCard
            key={category.id}
            category={category}
            depth={0}
            completedNodes={completedNodes}
            onNodeClick={onNodeClick}
            selectedNode={selectedNode}
            onCategoryClick={handleCategoryClick}
          />
        ))}
      </div>
      
      {/* Legend */}
      <div className="mt-8 bg-white rounded-lg p-4 shadow-sm">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">How to Use</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
          <div className="flex items-center gap-2">
            <CheckCircle size={16} className="text-green-500" />
            <span>Green checkmark indicates fully completed categories</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-2 bg-green-500 rounded-full"></div>
            <span>Progress bar shows completion percentage</span>
          </div>
        </div>
        <p className="text-xs text-gray-500 mt-3">
          Click on any category card to explore its subcategories and learning topics
        </p>
      </div>
    </div>
  );
}
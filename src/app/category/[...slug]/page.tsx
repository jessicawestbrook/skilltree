'use client';

import React, { useState, useMemo, use } from 'react';
import { ArrowLeft, ChevronRight, BookOpen, Users, Trophy, Star, Grid3X3, List } from 'lucide-react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { knowledgeStructure, KnowledgeCategory, flattenKnowledgeStructure } from '@/data/comprehensiveKnowledgeStructure';
import { useAuth } from '@/contexts/AuthContext';
import { useUserStats } from '@/hooks/useUserStats';
import { Node } from '@/types';
import HierarchicalCategoryMenu from '@/components/HierarchicalCategoryMenu';

interface CategoryPageProps {
  params: Promise<{
    slug: string[];
  }>;
}

function findCategoryByPath(structure: KnowledgeCategory, pathSegments: string[]): KnowledgeCategory | null {
  if (pathSegments.length === 0) return structure;
  
  const [currentSegment, ...remainingSegments] = pathSegments;
  
  // Check direct match
  if (structure.id === currentSegment) {
    if (remainingSegments.length === 0) return structure;
    // Continue searching in subcategories
    if (structure.subcategories) {
      for (const subcat of structure.subcategories) {
        const result = findCategoryByPath(subcat, remainingSegments);
        if (result) return result;
      }
    }
  }
  
  // Search in subcategories
  if (structure.subcategories) {
    for (const subcat of structure.subcategories) {
      const result = findCategoryByPath(subcat, pathSegments);
      if (result) return result;
    }
  }
  
  return null;
}

function getParentPath(pathSegments: string[]): string[] {
  return pathSegments.slice(0, -1);
}

function buildBreadcrumbs(pathSegments: string[]): Array<{name: string, path: string[]}> {
  const breadcrumbs = [{ name: 'Knowledge Universe', path: [] }];
  
  for (let i = 0; i < pathSegments.length; i++) {
    const currentPath = pathSegments.slice(0, i + 1);
    const category = findCategoryByPath(knowledgeStructure, currentPath);
    if (category) {
      breadcrumbs.push({
        name: category.name,
        path: currentPath
      });
    }
  }
  
  return breadcrumbs;
}

export default function CategoryPage({ params }: CategoryPageProps) {
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const { userStats } = useUserStats();
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [viewMode, setViewMode] = useState<'grid' | 'hierarchy'>('grid');
  
  // Unwrap the params Promise using React.use()
  const resolvedParams = use(params);
  const pathSegments = resolvedParams.slug || [];
  const category = findCategoryByPath(knowledgeStructure, pathSegments);
  const breadcrumbs = buildBreadcrumbs(pathSegments);
  const parentPath = getParentPath(pathSegments);
  
  const categoryStats = useMemo(() => {
    if (!category) return { total: 0, completed: 0, percentage: 0 };
    
    const allNodes = flattenKnowledgeStructure(category, [], new Set());
    const completedNodes = new Set(userStats.conqueredNodes);
    const completed = allNodes.filter(n => completedNodes.has(n.id)).length;
    
    return {
      total: allNodes.length,
      completed,
      percentage: allNodes.length > 0 ? Math.round((completed / allNodes.length) * 100) : 0
    };
  }, [category, userStats.conqueredNodes]);
  
  if (!category) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-800 mb-4">Category Not Found</h1>
          <Link href="/" className="text-blue-600 hover:text-blue-800">
            Return to Knowledge Universe
          </Link>
        </div>
      </div>
    );
  }
  
  const handleNodeClick = (node: Node) => {
    setSelectedNode(node);
    // Here you could trigger the quiz modal or navigate to a learning page
  };
  
  const handleSubcategoryClick = (subcategory: KnowledgeCategory) => {
    const newPath = [...pathSegments, subcategory.id];
    router.push(`/category/${newPath.join('/')}`);
  };
  
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-6">
          {/* Breadcrumbs */}
          <nav className="flex items-center space-x-2 text-sm text-gray-600 mb-4">
            {breadcrumbs.map((crumb, index) => (
              <React.Fragment key={index}>
                {index > 0 && <ChevronRight size={16} className="text-gray-400" />}
                {index === breadcrumbs.length - 1 ? (
                  <span className="text-gray-900 font-medium">{crumb.name}</span>
                ) : (
                  <Link 
                    href={crumb.path.length === 0 ? '/' : `/category/${crumb.path.join('/')}`}
                    className="hover:text-gray-900"
                  >
                    {crumb.name}
                  </Link>
                )}
              </React.Fragment>
            ))}
          </nav>
          
          {/* Category Header */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div 
                className="w-16 h-16 rounded-lg flex items-center justify-center text-white text-2xl font-bold"
                style={{ backgroundColor: category.color }}
              >
                <BookOpen size={32} />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">{category.name}</h1>
                <p className="text-lg text-gray-600 mt-1">{category.description}</p>
                <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                  {category.subcategories && (
                    <span>{category.subcategories.length} subcategories</span>
                  )}
                  {category.nodes && (
                    <span>{category.nodes.length} topics</span>
                  )}
                  {categoryStats.total > 0 && (
                    <span className="text-green-600 font-medium">
                      {categoryStats.completed}/{categoryStats.total} completed ({categoryStats.percentage}%)
                    </span>
                  )}
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              {/* View Toggle */}
              {(category.subcategories?.length || category.nodes?.length) && (
                <div className="flex items-center bg-gray-100 rounded-lg p-1">
                  <button
                    onClick={() => setViewMode('grid')}
                    className={`
                      flex items-center space-x-2 px-3 py-2 rounded-md transition-colors text-sm font-medium
                      ${viewMode === 'grid' 
                        ? 'bg-white text-gray-900 shadow-sm' 
                        : 'text-gray-600 hover:text-gray-900'
                      }
                    `}
                  >
                    <Grid3X3 size={16} />
                    <span>Grid</span>
                  </button>
                  <button
                    onClick={() => setViewMode('hierarchy')}
                    className={`
                      flex items-center space-x-2 px-3 py-2 rounded-md transition-colors text-sm font-medium
                      ${viewMode === 'hierarchy' 
                        ? 'bg-white text-gray-900 shadow-sm' 
                        : 'text-gray-600 hover:text-gray-900'
                      }
                    `}
                  >
                    <List size={16} />
                    <span>Tree</span>
                  </button>
                </div>
              )}
              
              {pathSegments.length > 0 && (
                <button
                  onClick={() => {
                    if (parentPath.length === 0) {
                      router.push('/');
                    } else {
                      router.push(`/category/${parentPath.join('/')}`);
                    }
                  }}
                  className="flex items-center space-x-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                >
                  <ArrowLeft size={20} />
                  <span>Back</span>
                </button>
              )}
            </div>
          </div>
          
          {/* Progress Bar */}
          {categoryStats.total > 0 && (
            <div className="mt-4">
              <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
                <span>Learning Progress</span>
                <span>{categoryStats.percentage}%</span>
              </div>
              <div className="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-blue-500 to-green-500 transition-all duration-500"
                  style={{ width: `${categoryStats.percentage}%` }}
                />
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {viewMode === 'hierarchy' ? (
          /* Hierarchical View */
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Content Structure</h2>
            <div className="bg-white rounded-lg border shadow-sm p-6">
              <HierarchicalCategoryMenu
                category={category}
                onNodeClick={handleNodeClick}
                selectedNode={selectedNode}
                level={0}
              />
            </div>
          </div>
        ) : (
          /* Grid View (Original) */
          <>
            {/* Subcategories */}
            {category.subcategories && category.subcategories.length > 0 && (
              <div className="mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Explore Subcategories</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {category.subcategories.map((subcategory) => {
                    const allNodes = flattenKnowledgeStructure(subcategory, [], new Set());
                    const completedNodes = new Set(userStats.conqueredNodes);
                    const completed = allNodes.filter(n => completedNodes.has(n.id)).length;
                    const subStats = {
                      total: allNodes.length,
                      completed,
                      percentage: allNodes.length > 0 ? Math.round((completed / allNodes.length) * 100) : 0
                    };
                    
                    return (
                      <div
                        key={subcategory.id}
                        onClick={() => handleSubcategoryClick(subcategory)}
                        className="bg-white rounded-xl shadow-sm border hover:shadow-md transition-all cursor-pointer p-6"
                      >
                        <div className="flex items-start justify-between mb-4">
                          <div 
                            className="w-12 h-12 rounded-lg flex items-center justify-center text-white"
                            style={{ backgroundColor: subcategory.color }}
                          >
                            <BookOpen size={24} />
                          </div>
                          <ChevronRight size={20} className="text-gray-400" />
                        </div>
                        
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">{subcategory.name}</h3>
                        <p className="text-sm text-gray-600 mb-4">{subcategory.description}</p>
                        
                        <div className="space-y-2">
                          <div className="flex items-center justify-between text-xs text-gray-500">
                            <div className="flex items-center space-x-3">
                              {subcategory.subcategories && (
                                <span>{subcategory.subcategories.length} categories</span>
                              )}
                              {subcategory.nodes && (
                                <span>{subcategory.nodes.length} topics</span>
                              )}
                            </div>
                            {subStats.total > 0 && (
                              <span className="text-green-600 font-medium">
                                {subStats.percentage}% complete
                              </span>
                            )}
                          </div>
                          
                          {subStats.total > 0 && (
                            <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                              <div 
                                className="h-full bg-green-500 transition-all duration-300"
                                style={{ width: `${subStats.percentage}%` }}
                              />
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
            
            {/* Learning Topics */}
            {category.nodes && category.nodes.length > 0 && (
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Learning Topics</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                  {category.nodes.map((node) => {
                    const isCompleted = userStats.conqueredNodes.includes(node.id);
                    const isAvailable = !node.prereqs || node.prereqs.every(p => userStats.conqueredNodes.includes(p));
                    
                    return (
                      <div
                        key={node.id}
                        onClick={() => isAvailable && handleNodeClick(node)}
                        className={`
                          bg-white rounded-lg border p-4 transition-all cursor-pointer
                          ${isAvailable ? 'hover:shadow-md' : 'opacity-60 cursor-not-allowed'}
                          ${isCompleted ? 'border-green-300 bg-green-50' : ''}
                          ${selectedNode?.id === node.id ? 'border-blue-500 bg-blue-50 shadow-lg' : ''}
                        `}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <h3 className="font-semibold text-gray-900 text-sm">{node.name}</h3>
                          {isCompleted && <Trophy size={16} className="text-green-500" />}
                        </div>
                        
                        <div className="flex items-center space-x-3 text-xs text-gray-600">
                          <div className="flex items-center space-x-1">
                            {[...Array(node.difficulty || 1)].map((_, i) => (
                              <Star key={i} size={10} className="fill-yellow-400 text-yellow-400" />
                            ))}
                          </div>
                          <span className="font-medium">+{node.points}pts</span>
                        </div>
                        
                        {node.prereqs && node.prereqs.length > 0 && (
                          <div className="mt-2 text-xs text-gray-500">
                            Requires: {node.prereqs.length} topics
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </>
        )}
        
        {/* Empty State */}
        {(!category.subcategories || category.subcategories.length === 0) && 
         (!category.nodes || category.nodes.length === 0) && (
          <div className="text-center py-12">
            <BookOpen size={48} className="text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Coming Soon</h3>
            <p className="text-gray-600">
              This category is being developed. Check back soon for learning content!
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
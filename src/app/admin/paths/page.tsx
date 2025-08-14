'use client';

import React, { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase-client';

const supabase = createClient();

interface LearningPath {
  id: string;
  name: string;
  description: string;
  difficulty: string;
  estimated_hours: number;
  category: string;
  icon: string;
  color: string;
  is_published: boolean;
  created_at: string;
  node_count?: number;
}

export default function PathsPage() {
  const [paths, setPaths] = useState<LearningPath[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');

  useEffect(() => {
    fetchPaths();
  }, []);

  const fetchPaths = async () => {
    try {
      const { data: pathsData, error: pathsError } = await supabase
        .from('learning_paths')
        .select('*')
        .order('created_at', { ascending: false });

      if (pathsError) throw pathsError;

      // Get node counts for each path
      const pathsWithCounts = await Promise.all(
        (pathsData || []).map(async (path) => {
          const { count } = await supabase
            .from('learning_path_nodes')
            .select('*', { count: 'exact', head: true })
            .eq('path_id', path.id);
          
          return { ...path, node_count: count || 0 };
        })
      );

      setPaths(pathsWithCounts);
    } catch (error) {
      console.error('Error fetching paths:', error);
    } finally {
      setLoading(false);
    }
  };

  const togglePublished = async (pathId: string, currentStatus: boolean) => {
    try {
      const { error } = await supabase
        .from('learning_paths')
        .update({ is_published: !currentStatus })
        .eq('id', pathId);

      if (error) throw error;
      
      setPaths(paths.map(p => 
        p.id === pathId ? { ...p, is_published: !currentStatus } : p
      ));
    } catch (error) {
      console.error('Error updating path:', error);
    }
  };

  const deletePath = async (pathId: string) => {
    if (!confirm('Are you sure you want to delete this learning path?')) return;

    try {
      const { error } = await supabase
        .from('learning_paths')
        .delete()
        .eq('id', pathId);

      if (error) throw error;
      
      setPaths(paths.filter(p => p.id !== pathId));
    } catch (error) {
      console.error('Error deleting path:', error);
    }
  };

  const filteredPaths = paths.filter(p => {
    const matchesSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         p.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = !selectedCategory || p.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const uniqueCategories = Array.from(new Set(paths.map(p => p.category))).sort();

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading paths...</div>;
  }

  return (
    <div>
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Learning Paths</h1>
          <p className="text-gray-600 mt-2">Manage learning paths and journeys</p>
        </div>
        <a
          href="/admin/paths/new"
          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
        >
          Create New Path
        </a>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="Search paths..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            <option value="">All Categories</option>
            {uniqueCategories.map((category, index) => (
              <option key={`category-${index}-${category}`} value={category}>{category}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Paths Table */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Path
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Category
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Difficulty
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Duration
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Nodes
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredPaths.map((path) => (
                <tr key={path.id}>
                  <td className="px-6 py-4">
                    <div className="flex items-center">
                      <span className="text-2xl mr-3">{path.icon}</span>
                      <div>
                        <div className="text-sm font-medium text-gray-900">{path.name}</div>
                        <div className="text-sm text-gray-500 max-w-xs truncate">
                          {path.description}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span 
                      className="px-2 py-1 text-xs rounded-full font-medium"
                      style={{ 
                        backgroundColor: `${path.color}20`,
                        color: path.color 
                      }}
                    >
                      {path.category}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 text-xs rounded-full font-medium ${
                      path.difficulty === 'beginner' ? 'bg-green-100 text-green-800' :
                      path.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {path.difficulty}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {path.estimated_hours}h
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {path.node_count || 0}
                  </td>
                  <td className="px-6 py-4">
                    <button
                      onClick={() => togglePublished(path.id, path.is_published)}
                      className={`px-3 py-1 rounded-full text-xs font-medium ${
                        path.is_published
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {path.is_published ? 'Published' : 'Draft'}
                    </button>
                  </td>
                  <td className="px-6 py-4 text-sm">
                    <div className="flex gap-2">
                      <a
                        href={`/admin/paths/${path.id}/edit`}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        Edit
                      </a>
                      <a
                        href={`/admin/paths/${path.id}/nodes`}
                        className="text-purple-600 hover:text-purple-900"
                      >
                        Nodes
                      </a>
                      <button
                        onClick={() => deletePath(path.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {filteredPaths.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            No learning paths found
          </div>
        )}
      </div>
    </div>
  );
}
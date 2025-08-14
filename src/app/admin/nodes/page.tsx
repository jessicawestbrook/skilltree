'use client';

import React, { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase-client';

interface KnowledgeNode {
  id: string;
  title: string;
  description: string;
  domain: string;
  difficulty: number;
  is_available: boolean;
  prerequisites: string[];
  position_x: number;
  position_y: number;
  icon: string;
  color: string;
  created_at: string;
}

export default function NodesPage() {
  const [nodes, setNodes] = useState<KnowledgeNode[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDomain, setSelectedDomain] = useState('');

  useEffect(() => {
    fetchNodes();
  }, []);

  const fetchNodes = async () => {
    try {
      const supabase = createClient();
      const { data, error } = await supabase
        .from('knowledge_nodes')
        .select('*')
        .order('domain', { ascending: true });

      if (error) throw error;
      setNodes(data || []);
    } catch (error) {
      console.error('Error fetching nodes:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleAvailability = async (nodeId: string, currentStatus: boolean) => {
    try {
      const supabase = createClient();
      const { error } = await supabase
        .from('knowledge_nodes')
        .update({ is_available: !currentStatus })
        .eq('id', nodeId);

      if (error) throw error;
      
      setNodes(nodes.map(n => 
        n.id === nodeId ? { ...n, is_available: !currentStatus } : n
      ));
    } catch (error) {
      console.error('Error updating node:', error);
    }
  };

  const filteredNodes = nodes.filter(n => {
    const matchesSearch = n.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         n.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDomain = !selectedDomain || n.domain === selectedDomain;
    return matchesSearch && matchesDomain;
  });

  const uniqueDomains = Array.from(new Set(nodes.map(n => n.domain))).sort();

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading nodes...</div>;
  }

  return (
    <div>
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Knowledge Nodes</h1>
          <p className="text-gray-600 mt-2">Manage knowledge graph nodes</p>
        </div>
        <a
          href="/admin/nodes/new"
          className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
        >
          Create New Node
        </a>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="Search nodes..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
          <select
            value={selectedDomain}
            onChange={(e) => setSelectedDomain(e.target.value)}
            className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="">All Domains</option>
            {uniqueDomains.map(domain => (
              <option key={domain} value={domain}>{domain}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Nodes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredNodes.map((node) => (
          <div
            key={node.id}
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <span className="text-2xl">{node.icon}</span>
                <div>
                  <h3 className="font-bold text-lg text-gray-800">{node.title}</h3>
                  <span className="text-sm text-gray-500">{node.id}</span>
                </div>
              </div>
              <button
                onClick={() => toggleAvailability(node.id, node.is_available)}
                className={`px-3 py-1 rounded-full text-xs font-medium ${
                  node.is_available
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                {node.is_available ? 'Available' : 'Locked'}
              </button>
            </div>

            <p className="text-gray-600 text-sm mb-4">{node.description}</p>

            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">Domain:</span>
                <span className="font-medium" style={{ color: node.color }}>
                  {node.domain}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Difficulty:</span>
                <div className="flex gap-1">
                  {[...Array(5)].map((_, i) => (
                    <span key={i} className={i < node.difficulty ? 'text-yellow-500' : 'text-gray-300'}>
                      ★
                    </span>
                  ))}
                </div>
              </div>
              {node.prerequisites.length > 0 && (
                <div>
                  <span className="text-gray-500">Prerequisites:</span>
                  <div className="mt-1 flex flex-wrap gap-1">
                    {node.prerequisites.map((prereq, i) => (
                      <span key={i} className="px-2 py-1 bg-gray-100 rounded text-xs">
                        {prereq}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="mt-4 pt-4 border-t flex gap-2">
              <a
                href={`/admin/nodes/${node.id}/edit`}
                className="flex-1 text-center px-3 py-1 bg-blue-50 text-blue-700 rounded hover:bg-blue-100"
              >
                Edit
              </a>
              <a
                href={`/admin/nodes/${node.id}/questions`}
                className="flex-1 text-center px-3 py-1 bg-purple-50 text-purple-700 rounded hover:bg-purple-100"
              >
                Questions
              </a>
            </div>
          </div>
        ))}
      </div>

      {filteredNodes.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          No nodes found
        </div>
      )}
    </div>
  );
}
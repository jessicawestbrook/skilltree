'use client';

import React, { useEffect, useState } from 'react';
import { CourseContentService } from '@/services/courseContentService';
import { BookOpen, Clock, Plus, Edit } from 'lucide-react';

interface ContentSummary {
  id: string;
  node_id: string;
  title: string;
  estimated_time: number;
  updated_at: string;
}

export default function ContentPage() {
  const [contents, setContents] = useState<ContentSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchContents();
  }, []);

  const fetchContents = async () => {
    setLoading(true);
    const data = await CourseContentService.getAllContentSummaries();
    setContents(data);
    setLoading(false);
  };

  const filteredContents = contents.filter(c =>
    c.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.node_id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading content...</div>;
  }

  return (
    <div>
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Course Content</h1>
          <p className="text-gray-600 mt-2">Manage learning materials for each knowledge node</p>
        </div>
        <a
          href="/admin/content/new"
          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
        >
          <Plus className="inline w-4 h-4 mr-2" />
          Create Content
        </a>
      </div>

      {/* Search */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <input
          type="text"
          placeholder="Search content..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
        />
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredContents.map((content) => (
          <div key={content.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <BookOpen className="w-8 h-8 text-green-600" />
                <div>
                  <h3 className="font-bold text-lg text-gray-800">{content.title}</h3>
                  <p className="text-sm text-gray-500">Node: {content.node_id}</p>
                </div>
              </div>
            </div>

            <div className="space-y-2 text-sm mb-4">
              <div className="flex items-center gap-2 text-gray-600">
                <Clock className="w-4 h-4" />
                <span>{content.estimated_time} minutes</span>
              </div>
              <div className="text-gray-500">
                Updated: {new Date(content.updated_at).toLocaleDateString()}
              </div>
            </div>

            <div className="flex gap-2">
              <a
                href={`/admin/content/${content.id}/edit`}
                className="flex-1 text-center px-3 py-2 bg-blue-50 text-blue-700 rounded hover:bg-blue-100"
              >
                <Edit className="inline w-4 h-4 mr-1" />
                Edit
              </a>
              <a
                href={`/admin/content/${content.id}/preview`}
                className="flex-1 text-center px-3 py-2 bg-green-50 text-green-700 rounded hover:bg-green-100"
              >
                Preview
              </a>
            </div>
          </div>
        ))}
      </div>

      {filteredContents.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          {searchTerm ? 'No content found matching your search' : 'No course content created yet'}
        </div>
      )}
    </div>
  );
}
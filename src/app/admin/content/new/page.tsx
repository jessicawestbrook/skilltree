'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { CourseContentService, CourseSection } from '@/services/courseContentService';
import { Plus, Trash2, GripVertical, Save, ArrowLeft } from 'lucide-react';
import { supabase } from '@/lib/supabase';

export default function NewContentPage() {
  const router = useRouter();
  const [nodeId, setNodeId] = useState('');
  const [title, setTitle] = useState('');
  const [overview, setOverview] = useState('');
  const [objectives, setObjectives] = useState<string[]>(['']);
  const [estimatedTime, setEstimatedTime] = useState(15);
  const [difficulty, setDifficulty] = useState('beginner');
  const [sections, setSections] = useState<Partial<CourseSection>[]>([
    {
      section_order: 0,
      section_type: 'introduction',
      title: '',
      content: ''
    }
  ]);
  const [saving, setSaving] = useState(false);

  const handleAddObjective = () => {
    setObjectives([...objectives, '']);
  };

  const handleObjectiveChange = (index: number, value: string) => {
    const newObjectives = [...objectives];
    newObjectives[index] = value;
    setObjectives(newObjectives);
  };

  const handleRemoveObjective = (index: number) => {
    setObjectives(objectives.filter((_, i) => i !== index));
  };

  const handleAddSection = () => {
    setSections([...sections, {
      section_order: sections.length,
      section_type: 'concept',
      title: '',
      content: ''
    }]);
  };

  const handleSectionChange = (index: number, field: string, value: any) => {
    const newSections = [...sections];
    newSections[index] = { ...newSections[index], [field]: value };
    setSections(newSections);
  };

  const handleRemoveSection = (index: number) => {
    setSections(sections.filter((_, i) => i !== index));
  };

  const handleSave = async () => {
    if (!nodeId || !title) {
      alert('Please fill in required fields');
      return;
    }

    setSaving(true);
    
    try {
      // First create the main content
      const { data: contentData, error: contentError } = await supabase
        .from('course_content')
        .insert({
          node_id: nodeId,
          title,
          overview,
          learning_objectives: objectives.filter(o => o.trim()),
          estimated_time: estimatedTime,
          difficulty_level: difficulty
        })
        .select()
        .single();

      if (contentError) throw contentError;

      // Then add sections
      if (contentData && sections.length > 0) {
        const sectionsToInsert = sections
          .filter(s => s.title && s.content)
          .map((s, index) => ({
            content_id: contentData.id,
            section_order: index,
            section_type: s.section_type,
            title: s.title,
            content: s.content,
            media_url: s.media_url,
            media_type: s.media_type
          }));

        if (sectionsToInsert.length > 0) {
          const { error: sectionsError } = await supabase
            .from('course_sections')
            .insert(sectionsToInsert);

          if (sectionsError) throw sectionsError;
        }
      }

      router.push('/admin/content');
    } catch (error) {
      console.error('Error saving content:', error);
      alert('Failed to save content');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6 flex items-center gap-4">
        <button
          onClick={() => router.push('/admin/content')}
          className="p-2 hover:bg-gray-100 rounded-lg"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Create Course Content</h1>
          <p className="text-gray-600 mt-1">Add learning materials for a knowledge node</p>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
        {/* Basic Info */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Node ID <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={nodeId}
              onChange={(e) => setNodeId(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="e.g., symbols-meaning"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Title <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="Course title"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Estimated Time (minutes)
            </label>
            <input
              type="number"
              value={estimatedTime}
              onChange={(e) => setEstimatedTime(parseInt(e.target.value))}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              min="5"
              max="120"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Difficulty Level
            </label>
            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>
        </div>

        {/* Overview */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Overview
          </label>
          <textarea
            value={overview}
            onChange={(e) => setOverview(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            rows={3}
            placeholder="Brief overview of what students will learn"
          />
        </div>

        {/* Learning Objectives */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Learning Objectives
          </label>
          <div className="space-y-2">
            {objectives.map((obj, index) => (
              <div key={index} className="flex gap-2">
                <input
                  type="text"
                  value={obj}
                  onChange={(e) => handleObjectiveChange(index, e.target.value)}
                  className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="Learning objective"
                />
                <button
                  onClick={() => handleRemoveObjective(index)}
                  className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
            <button
              onClick={handleAddObjective}
              className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
            >
              <Plus className="inline w-4 h-4 mr-2" />
              Add Objective
            </button>
          </div>
        </div>

        {/* Content Sections */}
        <div>
          <h3 className="text-lg font-semibold mb-4">Content Sections</h3>
          <div className="space-y-4">
            {sections.map((section, index) => (
              <div key={index} className="border rounded-lg p-4 bg-gray-50">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <GripVertical className="w-5 h-5 text-gray-400" />
                    <span className="font-medium">Section {index + 1}</span>
                  </div>
                  <button
                    onClick={() => handleRemoveSection(index)}
                    className="p-1 text-red-600 hover:bg-red-50 rounded"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Section Type
                    </label>
                    <select
                      value={section.section_type}
                      onChange={(e) => handleSectionChange(index, 'section_type', e.target.value)}
                      className="w-full px-3 py-2 border rounded-lg text-sm"
                    >
                      <option value="introduction">Introduction</option>
                      <option value="concept">Concept</option>
                      <option value="example">Example</option>
                      <option value="practice">Practice</option>
                      <option value="summary">Summary</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Section Title
                    </label>
                    <input
                      type="text"
                      value={section.title}
                      onChange={(e) => handleSectionChange(index, 'title', e.target.value)}
                      className="w-full px-3 py-2 border rounded-lg text-sm"
                      placeholder="Section title"
                    />
                  </div>
                </div>

                <div className="mt-3">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Content
                  </label>
                  <textarea
                    value={section.content}
                    onChange={(e) => handleSectionChange(index, 'content', e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg text-sm"
                    rows={4}
                    placeholder="Section content (supports markdown)"
                  />
                </div>

                <div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Media URL (optional)
                    </label>
                    <input
                      type="text"
                      value={section.media_url || ''}
                      onChange={(e) => handleSectionChange(index, 'media_url', e.target.value)}
                      className="w-full px-3 py-2 border rounded-lg text-sm"
                      placeholder="https://..."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Media Type
                    </label>
                    <select
                      value={section.media_type || ''}
                      onChange={(e) => handleSectionChange(index, 'media_type', e.target.value)}
                      className="w-full px-3 py-2 border rounded-lg text-sm"
                    >
                      <option value="">None</option>
                      <option value="image">Image</option>
                      <option value="video">Video</option>
                      <option value="diagram">Diagram</option>
                      <option value="code">Code</option>
                    </select>
                  </div>
                </div>
              </div>
            ))}

            <button
              onClick={handleAddSection}
              className="w-full px-4 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 border-2 border-dashed border-gray-300"
            >
              <Plus className="inline w-4 h-4 mr-2" />
              Add Section
            </button>
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-end gap-4 pt-6 border-t">
          <button
            onClick={() => router.push('/admin/content')}
            className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            disabled={saving}
            className={`px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-2 ${
              saving ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            <Save className="w-4 h-4" />
            {saving ? 'Saving...' : 'Save Content'}
          </button>
        </div>
      </div>
    </div>
  );
}
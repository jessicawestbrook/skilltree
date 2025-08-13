'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { QuizService } from '@/services/quizService';

export default function NewQuestionPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    nodeId: '',
    question: '',
    options: ['', '', '', ''],
    correct: 0,
    explanation: ''
  });
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.nodeId || !formData.question || formData.options.some(o => !o)) {
      alert('Please fill in all required fields');
      return;
    }

    setSaving(true);
    
    const success = await QuizService.addQuestion(formData.nodeId, {
      question: formData.question,
      options: formData.options,
      correct: formData.correct,
      explanation: formData.explanation
    });

    if (success) {
      router.push('/admin/questions');
    } else {
      alert('Failed to save question');
      setSaving(false);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Add New Question</h1>
        <p className="text-gray-600 mt-2">Create a new quiz question</p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 max-w-2xl">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Node ID <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={formData.nodeId}
              onChange={(e) => setFormData({...formData, nodeId: e.target.value})}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., symbols-meaning"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Question <span className="text-red-500">*</span>
            </label>
            <textarea
              value={formData.question}
              onChange={(e) => setFormData({...formData, question: e.target.value})}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
              placeholder="Enter the question text"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Options <span className="text-red-500">*</span>
            </label>
            <div className="space-y-2">
              {formData.options.map((option, index) => (
                <div key={index} className="flex items-center gap-2">
                  <input
                    type="radio"
                    name="correct"
                    checked={formData.correct === index}
                    onChange={() => setFormData({...formData, correct: index})}
                    className="flex-shrink-0"
                  />
                  <input
                    type="text"
                    value={option}
                    onChange={(e) => {
                      const newOptions = [...formData.options];
                      newOptions[index] = e.target.value;
                      setFormData({...formData, options: newOptions});
                    }}
                    className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder={`Option ${index + 1}`}
                    required
                  />
                </div>
              ))}
            </div>
            <p className="text-sm text-gray-500 mt-2">Select the radio button for the correct answer</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Explanation
            </label>
            <textarea
              value={formData.explanation}
              onChange={(e) => setFormData({...formData, explanation: e.target.value})}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
              placeholder="Explain why this is the correct answer (optional)"
            />
          </div>

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={saving}
              className={`px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 ${
                saving ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              {saving ? 'Saving...' : 'Save Question'}
            </button>
            <button
              type="button"
              onClick={() => router.push('/admin/questions')}
              className="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
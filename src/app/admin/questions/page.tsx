'use client';

import React, { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase-client';
import { QuizService, DatabaseQuizQuestion } from '@/services/quizService';

const supabase = createClient();

export default function QuestionsPage() {
  const [questions, setQuestions] = useState<DatabaseQuizQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedNode, setSelectedNode] = useState('');
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editForm, setEditForm] = useState({
    question: '',
    options: ['', '', '', ''],
    correct_answer: 0,
    explanation: ''
  });

  useEffect(() => {
    fetchQuestions();
  }, []);

  const fetchQuestions = async () => {
    try {
      const { data, error } = await supabase
        .from('quiz_questions')
        .select('*')
        .order('created_at', { ascending: false });

      if (error) throw error;
      setQuestions(data || []);
    } catch (error) {
      console.error('Error fetching questions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this question?')) return;

    const success = await QuizService.deleteQuestion(id);
    if (success) {
      setQuestions(questions.filter(q => q.id !== id));
    }
  };

  const handleEdit = (question: DatabaseQuizQuestion) => {
    setEditingId(question.id);
    setEditForm({
      question: question.question,
      options: question.options,
      correct_answer: question.correct_answer,
      explanation: question.explanation
    });
  };

  const handleSaveEdit = async () => {
    if (!editingId) return;

    const success = await QuizService.updateQuestion(editingId, {
      question: editForm.question,
      options: editForm.options,
      correct: editForm.correct_answer,
      explanation: editForm.explanation
    });

    if (success) {
      setQuestions(questions.map(q => 
        q.id === editingId 
          ? { ...q, ...editForm, correct_answer: editForm.correct_answer }
          : q
      ));
      setEditingId(null);
    }
  };

  const filteredQuestions = questions.filter(q => {
    const matchesSearch = q.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         q.node_id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesNode = !selectedNode || q.node_id === selectedNode;
    return matchesSearch && matchesNode;
  });

  const uniqueNodes = Array.from(new Set(questions.map(q => q.node_id))).sort();

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading questions...</div>;
  }

  return (
    <div>
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Questions Management</h1>
          <p className="text-gray-600 mt-2">Manage all quiz questions in the system</p>
        </div>
        <a
          href="/admin/questions/new"
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Add New Question
        </a>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="Search questions..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <select
            value={selectedNode}
            onChange={(e) => setSelectedNode(e.target.value)}
            className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Nodes</option>
            {uniqueNodes.map(node => (
              <option key={node} value={node}>{node}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Questions Table */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Node ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Question
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Options
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Correct
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredQuestions.map((q) => (
                <tr key={q.id}>
                  {editingId === q.id ? (
                    <>
                      <td className="px-6 py-4 text-sm text-gray-900">{q.node_id}</td>
                      <td className="px-6 py-4">
                        <input
                          type="text"
                          value={editForm.question}
                          onChange={(e) => setEditForm({...editForm, question: e.target.value})}
                          className="w-full px-2 py-1 border rounded"
                        />
                      </td>
                      <td className="px-6 py-4">
                        <div className="space-y-1">
                          {editForm.options.map((opt, i) => (
                            <input
                              key={i}
                              type="text"
                              value={opt}
                              onChange={(e) => {
                                const newOptions = [...editForm.options];
                                newOptions[i] = e.target.value;
                                setEditForm({...editForm, options: newOptions});
                              }}
                              className="w-full px-2 py-1 border rounded text-xs"
                            />
                          ))}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <select
                          value={editForm.correct_answer}
                          onChange={(e) => setEditForm({...editForm, correct_answer: parseInt(e.target.value)})}
                          className="px-2 py-1 border rounded"
                        >
                          {editForm.options.map((_, i) => (
                            <option key={i} value={i}>{i + 1}</option>
                          ))}
                        </select>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex gap-2">
                          <button
                            onClick={handleSaveEdit}
                            className="text-green-600 hover:text-green-900"
                          >
                            Save
                          </button>
                          <button
                            onClick={() => setEditingId(null)}
                            className="text-gray-600 hover:text-gray-900"
                          >
                            Cancel
                          </button>
                        </div>
                      </td>
                    </>
                  ) : (
                    <>
                      <td className="px-6 py-4 text-sm text-gray-900">{q.node_id}</td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        <div className="max-w-xs truncate" title={q.question}>
                          {q.question}
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500">
                        <ol className="list-decimal list-inside text-xs">
                          {q.options.map((opt, i) => (
                            <li key={i} className={i === q.correct_answer ? 'font-bold text-green-600' : ''}>
                              {opt}
                            </li>
                          ))}
                        </ol>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {q.correct_answer + 1}
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <div className="flex gap-2">
                          <button
                            onClick={() => handleEdit(q)}
                            className="text-blue-600 hover:text-blue-900"
                          >
                            Edit
                          </button>
                          <button
                            onClick={() => handleDelete(q.id)}
                            className="text-red-600 hover:text-red-900"
                          >
                            Delete
                          </button>
                        </div>
                      </td>
                    </>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {filteredQuestions.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            No questions found
          </div>
        )}
      </div>
    </div>
  );
}
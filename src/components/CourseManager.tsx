import React, { useState, useEffect } from 'react';
import { supabase } from '../services/supabase';
import {
  AcademicCapIcon,
  PlusIcon,
  PencilIcon,
  TrashIcon,
  BookOpenIcon,
  ChevronRightIcon,
  ChevronDownIcon,
  QuestionMarkCircleIcon,
  FolderIcon,
  FolderOpenIcon
} from '@heroicons/react/24/outline';

interface SkillNode {
  id: string;
  name: string;
  parent_id: string | null;
  description?: string;
  metadata?: any;
  display_order: number;
  is_hidden: boolean;
}

interface Course extends SkillNode {
  skillPath?: string;
  parentSkill?: SkillNode;
}

interface CourseModule {
  id: string;
  course_id: string;
  chapter_number: number;
  title: string;
  description: string;
  module_type: string;
  display_order: number;
  metadata?: any;
}

interface Question {
  id: string;
  question_text: string;
  question_type: string;
  difficulty: string;
  category: string;
  subcategory?: string;
  options?: any;
  correct_answer?: string;
  correct_answer_index?: number;
  explanation?: string;
}

interface GroupedCourses {
  [skillId: string]: {
    skill: SkillNode;
    courses: Course[];
  };
}

const CourseManager: React.FC = () => {
  const [groupedCourses, setGroupedCourses] = useState<GroupedCourses>({});
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [modules, setModules] = useState<CourseModule[]>([]);
  const [selectedModule, setSelectedModule] = useState<CourseModule | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(false);
  const [expandedCourse, setExpandedCourse] = useState<string | null>(null);
  const [expandedSkills, setExpandedSkills] = useState<Set<string>>(new Set());
  const [skillNodes, setSkillNodes] = useState<SkillNode[]>([]);
  
  // Form states
  const [showCourseForm, setShowCourseForm] = useState(false);
  const [showModuleForm, setShowModuleForm] = useState(false);
  const [showQuestionForm, setShowQuestionForm] = useState(false);
  const [editingCourse, setEditingCourse] = useState<Course | null>(null);
  const [editingModule, setEditingModule] = useState<CourseModule | null>(null);
  const [editingQuestion, setEditingQuestion] = useState<Question | null>(null);

  // Form data
  const [courseForm, setCourseForm] = useState({
    name: '',
    description: '',
    parent_id: '',
    metadata: {},
    display_order: 0
  });

  const [moduleForm, setModuleForm] = useState({
    title: '',
    description: '',
    chapter_number: 1,
    module_type: 'chapter',
    display_order: 1
  });

  const [questionForm, setQuestionForm] = useState({
    question_text: '',
    question_type: 'multiple_choice',
    difficulty: 'basic',
    category: '',
    subcategory: '',
    options: ['', '', '', ''],
    correct_answer_index: 0,
    explanation: ''
  });

  // Load courses and skills
  useEffect(() => {
    loadCoursesAndSkills();
  }, []);

  const loadCoursesAndSkills = async () => {
    setLoading(true);
    try {
      // Get all skill nodes first
      const { data: allNodes, error: nodesError } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .order('name');

      if (nodesError) throw nodesError;

      // Filter courses (nodes that look like courses)
      const courses = allNodes?.filter(node => 
        node.metadata?.textbook || 
        node.metadata?.year || 
        node.metadata?.course_type ||
        node.metadata?.chapters ||
        node.name.includes('Course') ||
        node.name.includes('Henle') ||
        node.name.includes('Module')
      ) || [];

      // Build hierarchy - group courses by their parent skill
      const grouped: GroupedCourses = {};
      const nodeMap = new Map(allNodes?.map(n => [n.id, n]) || []);

      for (const course of courses) {
        if (!course.parent_id) continue;

        const parentNode = nodeMap.get(course.parent_id);
        if (!parentNode) continue;

        // Build the skill path
        let skillPath = parentNode.name;
        let currentParent = parentNode.parent_id;
        const pathParts = [parentNode.name];

        while (currentParent) {
          const grandParent = nodeMap.get(currentParent);
          if (grandParent && grandParent.name !== 'Knowledge') {
            pathParts.unshift(grandParent.name);
          }
          currentParent = grandParent?.parent_id || null;
        }
        skillPath = pathParts.join(' > ');

        // Add to grouped structure
        if (!grouped[course.parent_id]) {
          grouped[course.parent_id] = {
            skill: parentNode,
            courses: []
          };
        }

        grouped[course.parent_id].courses.push({
          ...course,
          skillPath,
          parentSkill: parentNode
        });
      }

      // Sort courses within each group by display_order and name
      Object.values(grouped).forEach(group => {
        group.courses.sort((a, b) => {
          if (a.display_order !== b.display_order) {
            return (a.display_order || 999) - (b.display_order || 999);
          }
          return a.name.localeCompare(b.name);
        });
      });

      setGroupedCourses(grouped);
      setSkillNodes(allNodes || []);
    } catch (error) {
      console.error('Error loading courses:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadModules = async (courseId: string) => {
    try {
      const { data, error } = await supabase
        .from('course_modules')
        .select('*')
        .eq('course_id', courseId)
        .order('chapter_number');

      if (error) throw error;
      setModules(data || []);
    } catch (error) {
      console.error('Error loading modules:', error);
      setModules([]);
    }
  };

  const loadQuestions = async (category: string, subcategory?: string) => {
    try {
      let query = supabase
        .from('questions')
        .select('*')
        .eq('category', category);
      
      if (subcategory) {
        query = query.eq('subcategory', subcategory);
      }
      
      const { data, error } = await query.order('created_at', { ascending: false });

      if (error) throw error;
      setQuestions(data || []);
    } catch (error) {
      console.error('Error loading questions:', error);
      setQuestions([]);
    }
  };

  const handleToggleSkill = (skillId: string) => {
    const newExpanded = new Set(expandedSkills);
    if (newExpanded.has(skillId)) {
      newExpanded.delete(skillId);
    } else {
      newExpanded.add(skillId);
    }
    setExpandedSkills(newExpanded);
  };

  const handleCourseClick = async (course: Course) => {
    if (expandedCourse === course.id) {
      setExpandedCourse(null);
      setSelectedCourse(null);
      setModules([]);
    } else {
      setExpandedCourse(course.id);
      setSelectedCourse(course);
      await loadModules(course.id);
    }
  };

  const handleModuleClick = async (module: CourseModule) => {
    setSelectedModule(module);
    // Load questions for this module/chapter
    await loadQuestions(selectedCourse?.name || '', module.title);
  };

  // Course CRUD operations
  const handleSaveCourse = async () => {
    try {
      if (editingCourse) {
        // Update existing course
        const { error } = await supabase
          .from('skill_tree_nodes')
          .update({
            name: courseForm.name,
            description: courseForm.description,
            metadata: courseForm.metadata,
            display_order: courseForm.display_order,
            updated_at: new Date().toISOString()
          })
          .eq('id', editingCourse.id);

        if (error) throw error;
      } else {
        // Create new course
        const { error } = await supabase
          .from('skill_tree_nodes')
          .insert({
            name: courseForm.name,
            description: courseForm.description,
            parent_id: courseForm.parent_id,
            metadata: { ...courseForm.metadata, course_type: 'course' },
            display_order: courseForm.display_order,
            is_hidden: false
          });

        if (error) throw error;
      }

      setShowCourseForm(false);
      setEditingCourse(null);
      setCourseForm({ name: '', description: '', parent_id: '', metadata: {}, display_order: 0 });
      loadCoursesAndSkills();
    } catch (error) {
      console.error('Error saving course:', error);
      alert('Error saving course. Please try again.');
    }
  };

  const handleDeleteCourse = async (course: Course) => {
    if (!window.confirm(`Are you sure you want to delete "${course.name}"? This action cannot be undone.`)) {
      return;
    }

    try {
      const { error } = await supabase
        .from('skill_tree_nodes')
        .delete()
        .eq('id', course.id);

      if (error) throw error;
      loadCoursesAndSkills();
    } catch (error) {
      console.error('Error deleting course:', error);
      alert('Error deleting course. It may have dependent data.');
    }
  };

  // Module CRUD operations
  const handleSaveModule = async () => {
    if (!selectedCourse) return;

    try {
      if (editingModule) {
        // Update existing module
        const { error } = await supabase
          .from('course_modules')
          .update({
            title: moduleForm.title,
            description: moduleForm.description,
            chapter_number: moduleForm.chapter_number,
            module_type: moduleForm.module_type,
            display_order: moduleForm.display_order
          })
          .eq('id', editingModule.id);

        if (error) throw error;
      } else {
        // Create new module
        const { error } = await supabase
          .from('course_modules')
          .insert({
            course_id: selectedCourse.id,
            title: moduleForm.title,
            description: moduleForm.description,
            chapter_number: moduleForm.chapter_number,
            module_type: moduleForm.module_type,
            display_order: moduleForm.display_order
          });

        if (error) throw error;
      }

      setShowModuleForm(false);
      setEditingModule(null);
      setModuleForm({ title: '', description: '', chapter_number: 1, module_type: 'chapter', display_order: 1 });
      loadModules(selectedCourse.id);
    } catch (error) {
      console.error('Error saving module:', error);
      alert('Error saving module. Please try again.');
    }
  };

  const handleDeleteModule = async (module: CourseModule) => {
    if (!window.confirm(`Are you sure you want to delete "${module.title}"?`)) {
      return;
    }

    try {
      const { error } = await supabase
        .from('course_modules')
        .delete()
        .eq('id', module.id);

      if (error) throw error;
      if (selectedCourse) loadModules(selectedCourse.id);
    } catch (error) {
      console.error('Error deleting module:', error);
      alert('Error deleting module.');
    }
  };

  // Question CRUD operations
  const handleSaveQuestion = async () => {
    if (!selectedCourse) return;

    try {
      const questionData: any = {
        question_text: questionForm.question_text,
        question_type: questionForm.question_type,
        difficulty: questionForm.difficulty,
        category: selectedCourse.name,
        subcategory: selectedModule?.title || questionForm.subcategory,
        explanation: questionForm.explanation
      };

      // Handle different question types
      if (questionForm.question_type === 'multiple_choice') {
        questionData.options = questionForm.options.filter(o => o.trim());
        questionData.correct_answer_index = questionForm.correct_answer_index;
      } else if (questionForm.question_type === 'true_false') {
        questionData.options = ['True', 'False'];
        questionData.correct_answer = questionForm.correct_answer_index === 0 ? 'True' : 'False';
      }

      if (editingQuestion) {
        // Update existing question
        const { error } = await supabase
          .from('questions')
          .update(questionData)
          .eq('id', editingQuestion.id);

        if (error) throw error;
      } else {
        // Create new question
        const { error } = await supabase
          .from('questions')
          .insert(questionData);

        if (error) throw error;
      }

      setShowQuestionForm(false);
      setEditingQuestion(null);
      setQuestionForm({
        question_text: '',
        question_type: 'multiple_choice',
        difficulty: 'basic',
        category: '',
        subcategory: '',
        options: ['', '', '', ''],
        correct_answer_index: 0,
        explanation: ''
      });
      
      if (selectedModule) {
        loadQuestions(selectedCourse.name, selectedModule.title);
      }
    } catch (error) {
      console.error('Error saving question:', error);
      alert('Error saving question. Please try again.');
    }
  };

  const handleDeleteQuestion = async (question: Question) => {
    if (!window.confirm(`Are you sure you want to delete this question?`)) {
      return;
    }

    try {
      const { error } = await supabase
        .from('questions')
        .delete()
        .eq('id', question.id);

      if (error) throw error;
      if (selectedCourse && selectedModule) {
        loadQuestions(selectedCourse.name, selectedModule.title);
      }
    } catch (error) {
      console.error('Error deleting question:', error);
      alert('Error deleting question.');
    }
  };

  if (loading) {
    return <div className="p-4">Loading courses...</div>;
  }

  return (
    <div className="max-w-7xl mx-auto p-4">
      <div className="bg-white dark:bg-neutral-800 rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <AcademicCapIcon className="h-6 w-6" />
            Course Management
          </h2>
          <button
            onClick={() => {
              setEditingCourse(null);
              setCourseForm({ name: '', description: '', parent_id: '', metadata: {}, display_order: 0 });
              setShowCourseForm(true);
            }}
            className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
          >
            <PlusIcon className="h-5 w-5" />
            New Course
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Courses List - Grouped by Skill */}
          <div className="lg:col-span-1 border-r pr-4 overflow-y-auto max-h-[calc(100vh-300px)]">
            <h3 className="font-semibold mb-3">Courses by Skill</h3>
            <div className="space-y-2">
              {Object.entries(groupedCourses)
                .sort(([, a], [, b]) => {
                  // Sort by skill path
                  const pathA = a.courses[0]?.skillPath || a.skill.name;
                  const pathB = b.courses[0]?.skillPath || b.skill.name;
                  return pathA.localeCompare(pathB);
                })
                .map(([skillId, { skill, courses }]) => (
                <div key={skillId} className="border rounded-lg dark:border-neutral-700">
                  {/* Skill Header */}
                  <div
                    className="flex items-center justify-between p-3 bg-gray-50 dark:bg-neutral-800 cursor-pointer rounded-t-lg"
                    onClick={() => handleToggleSkill(skillId)}
                  >
                    <div className="flex items-center gap-2">
                      {expandedSkills.has(skillId) ? (
                        <FolderOpenIcon className="h-5 w-5 text-primary-600" />
                      ) : (
                        <FolderIcon className="h-5 w-5 text-gray-500" />
                      )}
                      <div>
                        <div className="font-medium text-gray-900 dark:text-white">
                          {skill.name}
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                          {courses[0]?.skillPath}
                        </div>
                      </div>
                    </div>
                    <span className="text-sm text-gray-600 dark:text-gray-400 bg-gray-200 dark:bg-neutral-700 px-2 py-0.5 rounded">
                      {courses.length} {courses.length === 1 ? 'course' : 'courses'}
                    </span>
                  </div>

                  {/* Courses within skill */}
                  {expandedSkills.has(skillId) && (
                    <div className="p-2 space-y-1">
                      {courses.map(course => (
                        <div key={course.id}>
                          <div
                            className={`flex items-center justify-between p-2 rounded cursor-pointer transition-colors ${
                              expandedCourse === course.id 
                                ? 'bg-primary-100 dark:bg-primary-900/30' 
                                : 'hover:bg-gray-100 dark:hover:bg-neutral-700'
                            }`}
                            onClick={() => handleCourseClick(course)}
                          >
                            <div className="flex items-center gap-2 ml-4">
                              {expandedCourse === course.id ? (
                                <ChevronDownIcon className="h-4 w-4" />
                              ) : (
                                <ChevronRightIcon className="h-4 w-4" />
                              )}
                              <BookOpenIcon className="h-4 w-4 text-gray-500" />
                              <span className="text-sm font-medium">{course.name}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  setEditingCourse(course);
                                  setCourseForm({
                                    name: course.name,
                                    description: course.description || '',
                                    parent_id: course.parent_id || '',
                                    metadata: course.metadata || {},
                                    display_order: course.display_order || 0
                                  });
                                  setShowCourseForm(true);
                                }}
                                className="p-1 hover:bg-gray-200 dark:hover:bg-neutral-600 rounded"
                              >
                                <PencilIcon className="h-3 w-3" />
                              </button>
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleDeleteCourse(course);
                                }}
                                className="p-1 hover:bg-red-100 dark:hover:bg-red-900/30 rounded text-red-600"
                              >
                                <TrashIcon className="h-3 w-3" />
                              </button>
                            </div>
                          </div>

                          {/* Modules for expanded course */}
                          {expandedCourse === course.id && (
                            <div className="ml-12 mt-2 space-y-1">
                              <div className="flex justify-between items-center mb-2">
                                <span className="text-xs text-gray-600 dark:text-gray-400">Modules</span>
                                <button
                                  onClick={() => {
                                    setEditingModule(null);
                                    setModuleForm({ 
                                      title: '', 
                                      description: '', 
                                      chapter_number: modules.length + 1, 
                                      module_type: 'chapter', 
                                      display_order: modules.length + 1 
                                    });
                                    setShowModuleForm(true);
                                  }}
                                  className="text-xs bg-gray-200 dark:bg-neutral-700 px-2 py-0.5 rounded hover:bg-gray-300 dark:hover:bg-neutral-600"
                                >
                                  <PlusIcon className="h-3 w-3 inline" /> Add
                                </button>
                              </div>
                              {modules.map(module => (
                                <div
                                  key={module.id}
                                  onClick={() => handleModuleClick(module)}
                                  className={`flex items-center justify-between p-1.5 rounded cursor-pointer text-xs ${
                                    selectedModule?.id === module.id
                                      ? 'bg-gray-200 dark:bg-neutral-700'
                                      : 'hover:bg-gray-100 dark:hover:bg-neutral-700/50'
                                  }`}
                                >
                                  <span>Ch {module.chapter_number}: {module.title}</span>
                                  <div className="flex gap-1">
                                    <button
                                      onClick={(e) => {
                                        e.stopPropagation();
                                        setEditingModule(module);
                                        setModuleForm({
                                          title: module.title,
                                          description: module.description || '',
                                          chapter_number: module.chapter_number,
                                          module_type: module.module_type,
                                          display_order: module.display_order
                                        });
                                        setShowModuleForm(true);
                                      }}
                                      className="p-0.5 hover:bg-gray-300 dark:hover:bg-neutral-600 rounded"
                                    >
                                      <PencilIcon className="h-3 w-3" />
                                    </button>
                                    <button
                                      onClick={(e) => {
                                        e.stopPropagation();
                                        handleDeleteModule(module);
                                      }}
                                      className="p-0.5 hover:bg-red-100 dark:hover:bg-red-900/30 rounded text-red-600"
                                    >
                                      <TrashIcon className="h-3 w-3" />
                                    </button>
                                  </div>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Questions List */}
          <div className="lg:col-span-2">
            {selectedModule && selectedCourse ? (
              <>
                <div className="flex justify-between items-center mb-3">
                  <h3 className="font-semibold">
                    Questions: {selectedCourse.name} - {selectedModule.title}
                  </h3>
                  <button
                    onClick={() => {
                      setEditingQuestion(null);
                      setQuestionForm({
                        question_text: '',
                        question_type: 'multiple_choice',
                        difficulty: 'basic',
                        category: selectedCourse.name,
                        subcategory: selectedModule.title,
                        options: ['', '', '', ''],
                        correct_answer_index: 0,
                        explanation: ''
                      });
                      setShowQuestionForm(true);
                    }}
                    className="flex items-center gap-2 bg-green-600 text-white px-3 py-1.5 rounded-lg hover:bg-green-700 text-sm"
                  >
                    <PlusIcon className="h-4 w-4" />
                    Add Question
                  </button>
                </div>
                
                <div className="space-y-3">
                  {questions.length > 0 ? (
                    questions.map(question => (
                      <div key={question.id} className="border rounded-lg p-3 dark:border-neutral-700">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <p className="font-medium">{question.question_text}</p>
                            <div className="flex gap-4 mt-2 text-sm text-gray-600 dark:text-gray-400">
                              <span>Type: {question.question_type}</span>
                              <span>Difficulty: {question.difficulty}</span>
                            </div>
                            {question.options && (
                              <div className="mt-2 text-sm">
                                <span className="font-medium">Options:</span>
                                <ol className="list-decimal list-inside ml-2">
                                  {(Array.isArray(question.options) ? question.options : []).map((opt, idx) => (
                                    <li key={idx} className={idx === question.correct_answer_index ? 'text-green-600 font-medium' : ''}>
                                      {opt}
                                    </li>
                                  ))}
                                </ol>
                              </div>
                            )}
                          </div>
                          <div className="flex gap-1">
                            <button
                              onClick={() => {
                                setEditingQuestion(question);
                                setQuestionForm({
                                  question_text: question.question_text,
                                  question_type: question.question_type,
                                  difficulty: question.difficulty,
                                  category: question.category,
                                  subcategory: question.subcategory || '',
                                  options: question.options || ['', '', '', ''],
                                  correct_answer_index: question.correct_answer_index || 0,
                                  explanation: question.explanation || ''
                                });
                                setShowQuestionForm(true);
                              }}
                              className="p-1 hover:bg-gray-200 dark:hover:bg-neutral-600 rounded"
                            >
                              <PencilIcon className="h-4 w-4" />
                            </button>
                            <button
                              onClick={() => handleDeleteQuestion(question)}
                              className="p-1 hover:bg-red-100 dark:hover:bg-red-900/30 rounded text-red-600"
                            >
                              <TrashIcon className="h-4 w-4" />
                            </button>
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="text-gray-500 text-center py-8">No questions yet for this module</p>
                  )}
                </div>
              </>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <QuestionMarkCircleIcon className="h-12 w-12 mx-auto mb-3 opacity-50" />
                <p>Select a course and module to view questions</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Course Form Modal */}
      {showCourseForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-neutral-800 rounded-lg shadow-xl p-6 max-w-md w-full">
            <h3 className="text-lg font-semibold mb-4">
              {editingCourse ? 'Edit Course' : 'Create New Course'}
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Course Name</label>
                <input
                  type="text"
                  value={courseForm.name}
                  onChange={(e) => setCourseForm({ ...courseForm, name: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg dark:bg-neutral-700 dark:border-neutral-600"
                  placeholder="e.g., Introduction to Python"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Description</label>
                <textarea
                  value={courseForm.description}
                  onChange={(e) => setCourseForm({ ...courseForm, description: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg dark:bg-neutral-700 dark:border-neutral-600"
                  rows={3}
                  placeholder="Course description..."
                />
              </div>
              {!editingCourse && (
                <div>
                  <label className="block text-sm font-medium mb-1">Parent Skill</label>
                  <select
                    value={courseForm.parent_id}
                    onChange={(e) => setCourseForm({ ...courseForm, parent_id: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg dark:bg-neutral-700 dark:border-neutral-600"
                    required
                  >
                    <option value="">Select a skill...</option>
                    {skillNodes
                      .filter(node => !node.metadata?.textbook && !node.metadata?.year && !node.name.includes('Henle'))
                      .sort((a, b) => a.name.localeCompare(b.name))
                      .map(skill => (
                        <option key={skill.id} value={skill.id}>
                          {skill.name}
                        </option>
                      ))}
                  </select>
                </div>
              )}
              <div>
                <label className="block text-sm font-medium mb-1">Display Order</label>
                <input
                  type="number"
                  value={courseForm.display_order}
                  onChange={(e) => setCourseForm({ ...courseForm, display_order: parseInt(e.target.value) || 0 })}
                  className="w-full px-3 py-2 border rounded-lg dark:bg-neutral-700 dark:border-neutral-600"
                />
              </div>
              <div className="flex justify-end gap-2 mt-6">
                <button
                  onClick={() => {
                    setShowCourseForm(false);
                    setEditingCourse(null);
                  }}
                  className="px-4 py-2 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-neutral-700 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSaveCourse}
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
                >
                  {editingCourse ? 'Update' : 'Create'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Module Form Modal */}
      {showModuleForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-neutral-800 rounded-lg shadow-xl p-6 max-w-md w-full">
            <h3 className="text-lg font-semibold mb-4">
              {editingModule ? 'Edit Module' : 'Create New Module'}
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Module Title</label>
                <input
                  type="text"
                  value={moduleForm.title}
                  onChange={(e) => setModuleForm({ ...moduleForm, title: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg dark:bg-neutral-700 dark:border-neutral-600"
                  placeholder="e.g., Introduction to Variables"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Description</label>
                <textarea
                  value={moduleForm.description}
                  onChange={(e) => setModuleForm({ ...moduleForm, description: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg dark:bg-neutral-700 dark:border-neutral-600"
                  rows={3}
                  placeholder="Module description..."
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Chapter Number</label>
                  <input
                    type="number"
                    value={moduleForm.chapter_number}
                    onChange={(e) => setModuleForm({ ...moduleForm, chapter_number: parseInt(e.target.value) || 1 })}
                    className="w-full px-3 py-2 border rounded-lg dark:bg-neutral-700 dark:border-neutral-600"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Type</label>
                  <select
                    value={moduleForm.module_type}
                    onChange={(e) => setModuleForm({ ...moduleForm, module_type: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg dark:bg-neutral-700 dark:border-neutral-600"
                  >
                    <option value="chapter">Chapter</option>
                    <option value="lesson">Lesson</option>
                    <option value="quiz">Quiz</option>
                    <option value="project">Project</option>
                  </select>
                </div>
              </div>
              <div className="flex justify-end gap-2 mt-6">
                <button
                  onClick={() => {
                    setShowModuleForm(false);
                    setEditingModule(null);
                  }}
                  className="px-4 py-2 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-neutral-700 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSaveModule}
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
                >
                  {editingModule ? 'Update' : 'Create'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Question Form Modal */}
      {showQuestionForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-neutral-800 rounded-lg shadow-xl p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <h3 className="text-lg font-semibold mb-4">
              {editingQuestion ? 'Edit Question' : 'Create New Question'}
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Question Text</label>
                <textarea
                  value={questionForm.question_text}
                  onChange={(e) => setQuestionForm({ ...questionForm, question_text: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg dark:bg-neutral-700 dark:border-neutral-600"
                  rows={3}
                  placeholder="Enter the question..."
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Question Type</label>
                  <select
                    value={questionForm.question_type}
                    onChange={(e) => setQuestionForm({ ...questionForm, question_type: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg dark:bg-neutral-700 dark:border-neutral-600"
                  >
                    <option value="multiple_choice">Multiple Choice</option>
                    <option value="true_false">True/False</option>
                    <option value="short_answer">Short Answer</option>
                    <option value="essay">Essay</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Difficulty</label>
                  <select
                    value={questionForm.difficulty}
                    onChange={(e) => setQuestionForm({ ...questionForm, difficulty: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg dark:bg-neutral-700 dark:border-neutral-600"
                  >
                    <option value="basic">Basic</option>
                    <option value="elementary">Elementary</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                    <option value="expert">Expert</option>
                  </select>
                </div>
              </div>

              {/* Options for multiple choice */}
              {questionForm.question_type === 'multiple_choice' && (
                <div>
                  <label className="block text-sm font-medium mb-1">Answer Options</label>
                  <div className="space-y-2">
                    {questionForm.options.map((option, index) => (
                      <div key={index} className="flex items-center gap-2">
                        <input
                          type="radio"
                          name="correct"
                          checked={questionForm.correct_answer_index === index}
                          onChange={() => setQuestionForm({ ...questionForm, correct_answer_index: index })}
                          className="flex-shrink-0"
                        />
                        <input
                          type="text"
                          value={option}
                          onChange={(e) => {
                            const newOptions = [...questionForm.options];
                            newOptions[index] = e.target.value;
                            setQuestionForm({ ...questionForm, options: newOptions });
                          }}
                          className="flex-1 px-3 py-2 border rounded-lg dark:bg-neutral-700 dark:border-neutral-600"
                          placeholder={`Option ${index + 1}`}
                        />
                      </div>
                    ))}
                  </div>
                  <button
                    onClick={() => setQuestionForm({ ...questionForm, options: [...questionForm.options, ''] })}
                    className="mt-2 text-sm text-primary-600 hover:text-primary-700"
                  >
                    + Add Option
                  </button>
                </div>
              )}

              {/* True/False options */}
              {questionForm.question_type === 'true_false' && (
                <div>
                  <label className="block text-sm font-medium mb-1">Correct Answer</label>
                  <div className="flex gap-4">
                    <label className="flex items-center">
                      <input
                        type="radio"
                        name="tf"
                        checked={questionForm.correct_answer_index === 0}
                        onChange={() => setQuestionForm({ ...questionForm, correct_answer_index: 0 })}
                        className="mr-2"
                      />
                      True
                    </label>
                    <label className="flex items-center">
                      <input
                        type="radio"
                        name="tf"
                        checked={questionForm.correct_answer_index === 1}
                        onChange={() => setQuestionForm({ ...questionForm, correct_answer_index: 1 })}
                        className="mr-2"
                      />
                      False
                    </label>
                  </div>
                </div>
              )}

              <div>
                <label className="block text-sm font-medium mb-1">Explanation (Optional)</label>
                <textarea
                  value={questionForm.explanation}
                  onChange={(e) => setQuestionForm({ ...questionForm, explanation: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg dark:bg-neutral-700 dark:border-neutral-600"
                  rows={2}
                  placeholder="Explain the correct answer..."
                />
              </div>

              <div className="flex justify-end gap-2 mt-6">
                <button
                  onClick={() => {
                    setShowQuestionForm(false);
                    setEditingQuestion(null);
                  }}
                  className="px-4 py-2 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-neutral-700 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSaveQuestion}
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
                >
                  {editingQuestion ? 'Update' : 'Create'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CourseManager;
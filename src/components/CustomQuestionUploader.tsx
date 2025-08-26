import React, { useState } from 'react'
import { 
  CloudArrowUpIcon, 
  XMarkIcon,
  CheckIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline'
import { useAuth } from '../contexts/AuthContext'
import { studyListService } from '../services/studyListService'

interface CustomQuestion {
  question: string
  answer: string
  options?: string[]
  category?: string
  difficulty?: string
  notes?: string
}

interface CustomQuestionUploaderProps {
  studyListId?: string
  onClose: () => void
  onSuccess: () => void
}

const CustomQuestionUploader: React.FC<CustomQuestionUploaderProps> = ({ 
  studyListId, 
  onClose, 
  onSuccess 
}) => {
  const { user } = useAuth()
  const [uploadMethod, setUploadMethod] = useState<'file' | 'manual'>('manual')
  const [questions, setQuestions] = useState<CustomQuestion[]>([])
  const [currentQuestion, setCurrentQuestion] = useState<CustomQuestion>({
    question: '',
    answer: '',
    options: ['', '', '', ''],
    category: '',
    difficulty: 'medium',
    notes: ''
  })
  const [parseError, setParseError] = useState('')
  const [isUploading, setIsUploading] = useState(false)

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = (e) => {
      const content = e.target?.result as string
      parseFileContent(content, file.name)
    }
    reader.readAsText(file)
  }

  const parseFileContent = (content: string, filename: string) => {
    setParseError('')
    const parsedQuestions: CustomQuestion[] = []

    try {
      // Try to parse as JSON first
      if (filename.endsWith('.json')) {
        const jsonData = JSON.parse(content)
        const items = Array.isArray(jsonData) ? jsonData : [jsonData]
        
        items.forEach(item => {
          if (item.question && item.answer) {
            parsedQuestions.push({
              question: item.question,
              answer: item.answer,
              options: item.options || [],
              category: item.category || '',
              difficulty: item.difficulty || 'medium',
              notes: item.notes || ''
            })
          }
        })
      } 
      // Parse as CSV
      else if (filename.endsWith('.csv')) {
        const lines = content.split('\n').filter(line => line.trim())
        const headers = lines[0].toLowerCase().split(',').map(h => h.trim())
        
        const questionIndex = headers.findIndex(h => h.includes('question'))
        const answerIndex = headers.findIndex(h => h.includes('answer'))
        
        if (questionIndex === -1 || answerIndex === -1) {
          throw new Error('CSV must have "question" and "answer" columns')
        }

        for (let i = 1; i < lines.length; i++) {
          const values = lines[i].split(',').map(v => v.trim().replace(/^"|"$/g, ''))
          if (values[questionIndex] && values[answerIndex]) {
            parsedQuestions.push({
              question: values[questionIndex],
              answer: values[answerIndex],
              category: values[headers.indexOf('category')] || '',
              difficulty: values[headers.indexOf('difficulty')] || 'medium',
              notes: values[headers.indexOf('notes')] || ''
            })
          }
        }
      }
      // Parse as tab-separated (Anki format)
      else if (filename.endsWith('.txt') || filename.endsWith('.tsv')) {
        const lines = content.split('\n').filter(line => line.trim())
        
        lines.forEach(line => {
          const parts = line.split('\t')
          if (parts.length >= 2) {
            parsedQuestions.push({
              question: parts[0].trim(),
              answer: parts[1].trim(),
              category: parts[2]?.trim() || '',
              notes: parts[3]?.trim() || ''
            })
          }
        })
      }
      else {
        throw new Error('Unsupported file format. Use .json, .csv, .txt, or .tsv')
      }

      if (parsedQuestions.length === 0) {
        throw new Error('No valid questions found in file')
      }

      setQuestions(parsedQuestions)
    } catch (error: any) {
      setParseError(error.message || 'Failed to parse file')
    }
  }

  const handleManualAdd = () => {
    if (!currentQuestion.question.trim() || !currentQuestion.answer.trim()) {
      alert('Please provide both question and answer')
      return
    }

    // Filter out empty options
    const filteredOptions = currentQuestion.options?.filter(opt => opt.trim()) || []

    setQuestions([...questions, {
      ...currentQuestion,
      options: filteredOptions.length > 0 ? filteredOptions : undefined
    }])

    // Reset form
    setCurrentQuestion({
      question: '',
      answer: '',
      options: ['', '', '', ''],
      category: '',
      difficulty: 'medium',
      notes: ''
    })
  }

  const removeQuestion = (index: number) => {
    setQuestions(questions.filter((_, i) => i !== index))
  }

  const handleUpload = async () => {
    if (!user || questions.length === 0) return

    setIsUploading(true)
    try {
      // Create custom questions in the database
      const uploadPromises = questions.map(async (q) => {
        // Store as a custom question type
        const questionData = {
          question_text: q.question,
          correct_answer: q.answer,
          options: q.options,
          category: q.category || 'Custom',
          difficulty: q.difficulty || 'medium',
          notes: q.notes,
          created_by: user.id,
          is_custom: true
        }

        // If a study list is selected, add directly to it
        if (studyListId) {
          await studyListService.addItemToStudyList(
            studyListId,
            'custom_question',
            `custom_${Date.now()}_${Math.random()}`,
            questionData
          )
        } else {
          // Otherwise, add to starred items
          await studyListService.starItem(
            user.id,
            'custom_question',
            `custom_${Date.now()}_${Math.random()}`,
            questionData
          )
        }
      })

      await Promise.all(uploadPromises)
      onSuccess()
      onClose()
    } catch (error) {
      console.error('Error uploading questions:', error)
      alert('Failed to upload questions. Please try again.')
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 overflow-y-auto">
      <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white dark:bg-neutral-800 border-b border-neutral-200 dark:border-neutral-700 p-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-neutral-900 dark:text-white">
              Upload Custom Questions
            </h2>
            <button
              onClick={onClose}
              className="p-2 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-lg transition-colors"
            >
              <XMarkIcon className="h-5 w-5" />
            </button>
          </div>

          {/* Method Toggle */}
          <div className="flex gap-2 mt-4">
            <button
              onClick={() => setUploadMethod('manual')}
              className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                uploadMethod === 'manual'
                  ? 'bg-primary-600 text-white'
                  : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300'
              }`}
            >
              Manual Entry
            </button>
            <button
              onClick={() => setUploadMethod('file')}
              className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                uploadMethod === 'file'
                  ? 'bg-primary-600 text-white'
                  : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300'
              }`}
            >
              File Upload
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          {uploadMethod === 'manual' ? (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
                  Question *
                </label>
                <textarea
                  value={currentQuestion.question}
                  onChange={(e) => setCurrentQuestion({ ...currentQuestion, question: e.target.value })}
                  className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-700 text-neutral-900 dark:text-white"
                  rows={2}
                  placeholder="Enter your question..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
                  Answer *
                </label>
                <textarea
                  value={currentQuestion.answer}
                  onChange={(e) => setCurrentQuestion({ ...currentQuestion, answer: e.target.value })}
                  className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-700 text-neutral-900 dark:text-white"
                  rows={2}
                  placeholder="Enter the answer..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
                  Multiple Choice Options (optional)
                </label>
                <div className="space-y-2">
                  {currentQuestion.options?.map((option, index) => (
                    <input
                      key={index}
                      type="text"
                      value={option}
                      onChange={(e) => {
                        const newOptions = [...(currentQuestion.options || [])]
                        newOptions[index] = e.target.value
                        setCurrentQuestion({ ...currentQuestion, options: newOptions })
                      }}
                      className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-700 text-neutral-900 dark:text-white"
                      placeholder={`Option ${index + 1}`}
                    />
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
                    Category
                  </label>
                  <input
                    type="text"
                    value={currentQuestion.category}
                    onChange={(e) => setCurrentQuestion({ ...currentQuestion, category: e.target.value })}
                    className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-700 text-neutral-900 dark:text-white"
                    placeholder="e.g., Math, Science, History"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
                    Difficulty
                  </label>
                  <select
                    value={currentQuestion.difficulty}
                    onChange={(e) => setCurrentQuestion({ ...currentQuestion, difficulty: e.target.value })}
                    className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-700 text-neutral-900 dark:text-white"
                  >
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
                  Notes (optional)
                </label>
                <input
                  type="text"
                  value={currentQuestion.notes}
                  onChange={(e) => setCurrentQuestion({ ...currentQuestion, notes: e.target.value })}
                  className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-700 text-neutral-900 dark:text-white"
                  placeholder="Additional notes or hints..."
                />
              </div>

              <button
                onClick={handleManualAdd}
                disabled={!currentQuestion.question.trim() || !currentQuestion.answer.trim()}
                className="w-full py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-neutral-400 disabled:cursor-not-allowed transition-colors"
              >
                Add Question to List
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {/* File Upload Area */}
              <div className="border-2 border-dashed border-neutral-300 dark:border-neutral-600 rounded-lg p-8">
                <input
                  type="file"
                  id="file-upload"
                  className="hidden"
                  accept=".json,.csv,.txt,.tsv"
                  onChange={handleFileUpload}
                />
                <label
                  htmlFor="file-upload"
                  className="flex flex-col items-center cursor-pointer"
                >
                  <CloudArrowUpIcon className="h-12 w-12 text-neutral-400 mb-4" />
                  <p className="text-lg font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                    Click to upload or drag and drop
                  </p>
                  <p className="text-sm text-neutral-500 dark:text-neutral-400">
                    Supported formats: JSON, CSV, TXT (tab-separated), TSV
                  </p>
                </label>
              </div>

              {/* File Format Help */}
              <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg p-4">
                <h4 className="font-medium text-neutral-900 dark:text-white mb-2">File Format Examples:</h4>
                <div className="space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
                  <div>
                    <strong>CSV:</strong> question, answer, category, difficulty
                  </div>
                  <div>
                    <strong>JSON:</strong> {`[{"question": "...", "answer": "...", "options": [...]}]`}
                  </div>
                  <div>
                    <strong>Tab-separated:</strong> question[TAB]answer[TAB]category
                  </div>
                </div>
              </div>

              {parseError && (
                <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                  <div className="flex items-start">
                    <ExclamationTriangleIcon className="h-5 w-5 text-red-500 mr-2 flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-red-700 dark:text-red-300">{parseError}</p>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Questions List */}
          {questions.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4">
                Questions to Upload ({questions.length})
              </h3>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {questions.map((q, index) => (
                  <div
                    key={index}
                    className="flex items-start justify-between p-3 bg-neutral-50 dark:bg-neutral-900 rounded-lg"
                  >
                    <div className="flex-1">
                      <p className="font-medium text-neutral-900 dark:text-white">
                        {q.question}
                      </p>
                      <p className="text-sm text-neutral-600 dark:text-neutral-400 mt-1">
                        Answer: {q.answer}
                      </p>
                      {q.category && (
                        <span className="inline-block mt-1 text-xs bg-neutral-200 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-400 px-2 py-1 rounded">
                          {q.category}
                        </span>
                      )}
                    </div>
                    <button
                      onClick={() => removeQuestion(index)}
                      className="ml-2 p-1 hover:bg-red-100 dark:hover:bg-red-900/30 rounded transition-colors"
                    >
                      <XMarkIcon className="h-4 w-4 text-red-500" />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-white dark:bg-neutral-800 border-t border-neutral-200 dark:border-neutral-700 p-6">
          <div className="flex items-center justify-between">
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              {questions.length} question{questions.length !== 1 ? 's' : ''} ready to upload
            </p>
            <div className="flex gap-3">
              <button
                onClick={onClose}
                className="px-4 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleUpload}
                disabled={questions.length === 0 || isUploading}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-neutral-400 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
              >
                {isUploading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    Uploading...
                  </>
                ) : (
                  <>
                    <CheckIcon className="h-5 w-5" />
                    Upload {questions.length} Question{questions.length !== 1 ? 's' : ''}
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CustomQuestionUploader
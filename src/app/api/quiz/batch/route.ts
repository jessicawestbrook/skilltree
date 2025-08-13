import { NextRequest, NextResponse } from 'next/server';
import { QuizService } from '@/services/quizService';

export async function POST(request: NextRequest) {
  try {
    const contentType = request.headers.get('content-type') || '';
    let result;

    if (contentType.includes('application/json')) {
      const data = await request.json();
      
      if (data.action === 'add') {
        result = await QuizService.batchAddQuestions(data.questions);
      } else if (data.action === 'update') {
        result = await QuizService.batchUpdateQuestions(data.updates);
      } else if (data.action === 'delete') {
        result = await QuizService.batchDeleteQuestions(data.questionIds);
      } else if (data.action === 'loadJSON') {
        result = await QuizService.loadQuestionsFromJSON(data.jsonData);
      } else {
        return NextResponse.json(
          { error: 'Invalid action. Use: add, update, delete, or loadJSON' },
          { status: 400 }
        );
      }
    } else if (contentType.includes('text/csv')) {
      const csvData = await request.text();
      result = await QuizService.loadQuestionsFromCSV(csvData);
    } else if (contentType.includes('multipart/form-data')) {
      const formData = await request.formData();
      const file = formData.get('file') as File;
      
      if (!file) {
        return NextResponse.json(
          { error: 'No file provided' },
          { status: 400 }
        );
      }

      const fileContent = await file.text();
      
      if (file.name.endsWith('.csv')) {
        result = await QuizService.loadQuestionsFromCSV(fileContent);
      } else if (file.name.endsWith('.json')) {
        const jsonData = JSON.parse(fileContent);
        result = await QuizService.loadQuestionsFromJSON(jsonData);
      } else {
        return NextResponse.json(
          { error: 'Unsupported file format. Use .csv or .json' },
          { status: 400 }
        );
      }
    } else {
      return NextResponse.json(
        { error: 'Unsupported content type' },
        { status: 400 }
      );
    }

    if (result.success) {
      return NextResponse.json(result, { status: 200 });
    } else {
      return NextResponse.json(result, { status: 400 });
    }
  } catch (error) {
    console.error('Batch operation error:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error occurred',
        errors: [error instanceof Error ? error.message : 'Unknown error occurred']
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'Quiz Batch API',
    endpoints: {
      POST: {
        description: 'Batch operations for quiz questions',
        contentTypes: {
          'application/json': {
            actions: {
              add: {
                description: 'Add multiple questions',
                body: {
                  action: 'add',
                  questions: [
                    {
                      nodeId: 'string',
                      question: {
                        question: 'string',
                        options: ['string[]'],
                        correct: 'number',
                        explanation: 'string'
                      }
                    }
                  ]
                }
              },
              update: {
                description: 'Update multiple questions',
                body: {
                  action: 'update',
                  updates: [
                    {
                      id: 'string',
                      updates: {
                        question: 'string?',
                        options: 'string[]?',
                        correct: 'number?',
                        explanation: 'string?'
                      }
                    }
                  ]
                }
              },
              delete: {
                description: 'Delete multiple questions',
                body: {
                  action: 'delete',
                  questionIds: ['string[]']
                }
              },
              loadJSON: {
                description: 'Load questions from JSON data',
                body: {
                  action: 'loadJSON',
                  jsonData: 'object | array'
                }
              }
            }
          },
          'text/csv': {
            description: 'Upload CSV file with questions',
            format: 'nodeId,question,option1,option2,option3,option4,correct,explanation'
          },
          'multipart/form-data': {
            description: 'Upload file (.csv or .json)',
            field: 'file'
          }
        }
      }
    }
  });
}
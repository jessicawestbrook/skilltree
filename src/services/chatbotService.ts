// Chatbot service for handling AI responses
// This is a simple implementation - in production, you'd integrate with OpenAI, Claude, or other AI services

export interface ChatContext {
  nodeId?: string;
  nodeTitle?: string;
  currentContent?: string;
  userLevel?: string;
  domain?: string;
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'bot';
  content: string;
  timestamp: Date;
}

export class ChatbotService {
  private static knowledgeBase = {
    // Computer Science topics
    'algorithm': {
      concepts: ['complexity', 'efficiency', 'data structures', 'sorting', 'searching'],
      examples: ['binary search', 'quicksort', 'merge sort', 'hash tables'],
      explanations: {
        'what': 'An algorithm is a step-by-step procedure for solving a problem or performing a computation.',
        'why': 'Algorithms help us solve problems efficiently and systematically.',
        'how': 'Algorithms work by breaking down complex problems into smaller, manageable steps.'
      }
    },
    'data-structures': {
      concepts: ['arrays', 'linked lists', 'trees', 'graphs', 'stacks', 'queues'],
      examples: ['binary tree', 'hash map', 'stack operations', 'queue implementation'],
      explanations: {
        'what': 'Data structures are ways of organizing and storing data to enable efficient access and modification.',
        'why': 'Good data structure choice can dramatically improve program performance.',
        'how': 'Data structures work by providing specific methods to store, access, and manipulate data.'
      }
    },
    'programming': {
      concepts: ['variables', 'functions', 'loops', 'conditions', 'objects', 'classes'],
      examples: ['for loop', 'if statement', 'function definition', 'class inheritance'],
      explanations: {
        'what': 'Programming is the process of creating instructions for computers to execute.',
        'why': 'Programming allows us to automate tasks and solve complex problems.',
        'how': 'Programming works by writing code in a specific language that computers can understand.'
      }
    },
    'machine-learning': {
      concepts: ['neural networks', 'supervised learning', 'unsupervised learning', 'deep learning'],
      examples: ['linear regression', 'decision trees', 'neural network training', 'image classification'],
      explanations: {
        'what': 'Machine learning is a method of data analysis that automates analytical model building.',
        'why': 'ML enables computers to learn and improve from experience without being explicitly programmed.',
        'how': 'ML algorithms build mathematical models based on training data to make predictions or decisions.'
      }
    }
  };

  private static getTopicKey(nodeTitle?: string): string {
    if (!nodeTitle) return 'programming';
    
    const title = nodeTitle.toLowerCase();
    if (title.includes('algorithm')) return 'algorithm';
    if (title.includes('data') || title.includes('structure')) return 'data-structures';
    if (title.includes('machine') || title.includes('learning') || title.includes('ml')) return 'machine-learning';
    return 'programming';
  }

  private static analyzeUserMessage(message: string): {
    intent: 'explanation' | 'example' | 'clarification' | 'general' | 'greeting';
    keywords: string[];
  } {
    const lowerMessage = message.toLowerCase();
    const keywords: string[] = [];
    
    // Extract potential keywords
    const words = lowerMessage.split(/\s+/);
    keywords.push(...words.filter(word => word.length > 3));

    // Determine intent
    let intent: 'explanation' | 'example' | 'clarification' | 'general' | 'greeting' = 'general';
    
    if (lowerMessage.includes('hello') || lowerMessage.includes('hi') || lowerMessage.includes('hey')) {
      intent = 'greeting';
    } else if (lowerMessage.includes('example') || lowerMessage.includes('show me') || lowerMessage.includes('demonstrate')) {
      intent = 'example';
    } else if (lowerMessage.includes('what') || lowerMessage.includes('define') || lowerMessage.includes('explain')) {
      intent = 'explanation';
    } else if (lowerMessage.includes('confused') || lowerMessage.includes('unclear') || lowerMessage.includes('clarify')) {
      intent = 'clarification';
    }

    return { intent, keywords };
  }

  static async generateResponse(
    userMessage: string,
    context: ChatContext,
    conversationHistory: ChatMessage[] = []
  ): Promise<string> {
    try {
      const { intent, keywords } = this.analyzeUserMessage(userMessage);
      const topicKey = this.getTopicKey(context.nodeTitle);
      const topic = this.knowledgeBase[topicKey as keyof typeof this.knowledgeBase];

      let response = '';

      switch (intent) {
        case 'greeting':
          response = this.generateGreeting(context);
          break;
        
        case 'explanation':
          response = this.generateExplanation(userMessage, topic, context);
          break;
        
        case 'example':
          response = this.generateExample(userMessage, topic, context);
          break;
        
        case 'clarification':
          response = this.generateClarification(userMessage, topic, context);
          break;
        
        default:
          response = this.generateGeneral(userMessage, topic, context, keywords);
      }

      // Add contextual information if available
      if (context.currentContent && response.length < 100) {
        response += ` Based on what you're currently studying, this directly relates to the concepts we're covering in "${context.nodeTitle}".`;
      }

      // Add encouragement
      const encouragements = [
        " Feel free to ask follow-up questions!",
        " I'm here to help you understand this better!",
        " Let me know if you need more clarification!",
        " Keep exploring these concepts!",
        " You're doing great with your learning!"
      ];
      
      response += encouragements[Math.floor(Math.random() * encouragements.length)];

      return response;
      
    } catch (error) {
      console.error('Error generating chatbot response:', error);
      return "I'm having trouble processing that right now. Could you please rephrase your question?";
    }
  }

  private static generateGreeting(context: ChatContext): string {
    const greetings = [
      `Hello! I'm here to help you learn about ${context.nodeTitle || 'this topic'}.`,
      `Hi there! Ready to explore ${context.nodeTitle || 'some interesting concepts'}?`,
      `Hey! I'm your learning assistant. What would you like to know about ${context.nodeTitle || 'this subject'}?`
    ];
    return greetings[Math.floor(Math.random() * greetings.length)];
  }

  private static generateExplanation(message: string, topic: any, context: ChatContext): string {
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('what')) {
      return `${topic.explanations.what} In the context of ${context.nodeTitle}, this is particularly important because it forms the foundation for understanding more advanced concepts.`;
    }
    
    if (lowerMessage.includes('why')) {
      return `${topic.explanations.why} When studying ${context.nodeTitle}, understanding the 'why' helps you see how everything connects together.`;
    }
    
    if (lowerMessage.includes('how')) {
      return `${topic.explanations.how} Let me break this down in the context of ${context.nodeTitle}...`;
    }

    // Default explanation
    return `Great question about ${context.nodeTitle}! ${topic.explanations.what} This concept is essential because ${topic.explanations.why.toLowerCase()}`;
  }

  private static generateExample(message: string, topic: any, context: ChatContext): string {
    const randomExample = topic.examples[Math.floor(Math.random() * topic.examples.length)];
    
    return `Here's a practical example related to ${context.nodeTitle}: Consider ${randomExample}. This demonstrates the key principles we're discussing because it shows how the concepts apply in real-world scenarios.`;
  }

  private static generateClarification(message: string, topic: any, context: ChatContext): string {
    return `I understand this part of ${context.nodeTitle} can be confusing. Let me clarify: The key thing to remember is that ${topic.explanations.what.toLowerCase()} The most important distinction to understand is how this relates to ${topic.concepts.slice(0, 2).join(' and ')}.`;
  }

  private static generateGeneral(message: string, topic: any, context: ChatContext, keywords: string[]): string {
    // Try to match keywords with topic concepts
    const matchedConcepts = topic.concepts.filter((concept: string) => 
      keywords.some(keyword => keyword.includes(concept) || concept.includes(keyword))
    );

    if (matchedConcepts.length > 0) {
      const concept = matchedConcepts[0];
      return `That's a great question about ${concept} in the context of ${context.nodeTitle}! This concept is fundamental because it connects to ${topic.concepts.filter((c: string) => c !== concept).slice(0, 2).join(' and ')}.`;
    }

    // Fallback response
    return `That's an interesting question about ${context.nodeTitle}! Based on what we're studying, this relates to the core concepts of ${topic.concepts.slice(0, 3).join(', ')}. Let me help you understand this better.`;
  }

  static getQuickSuggestions(context: ChatContext): string[] {
    const topicKey = this.getTopicKey(context.nodeTitle);
    const topic = this.knowledgeBase[topicKey as keyof typeof this.knowledgeBase];
    
    return [
      `What is ${context.nodeTitle}?`,
      `Can you give me an example?`,
      `How does this relate to ${topic.concepts[0]}?`,
      `Why is this important?`
    ];
  }
}
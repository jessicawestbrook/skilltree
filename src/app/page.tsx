import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { Brain, Trophy, Flame, Star, Lock, CheckCircle, TrendingUp, Globe, Calendar, BarChart3, BookOpen, Search, X, ChevronRight, Zap, Target, Users, Activity, Sparkles, Shield, Map, Compass, Award, Cpu, Menu, Home, User, Grid, Hammer, Leaf, Heart, Briefcase, Mountain, Palette } from 'lucide-react';
// Uncomment when you have the supabase file created:
// import { supabase } from './supabase';

const App = () => {
  // Responsive detection
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
  const [activeTab, setActiveTab] = useState('graph');
  const [showMobileMenu, setShowMobileMenu] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Comprehensive Knowledge Graph
  const knowledgeGraph = {
    foundation: {
      communication: [
        { id: 'symbols-meaning', name: 'Symbols & Meaning', prereqs: [], category: 'foundation', domain: 'communication', difficulty: 1, points: 50 },
        { id: 'sound-patterns', name: 'Sound Patterns', prereqs: [], category: 'foundation', domain: 'communication', difficulty: 1, points: 50 },
        { id: 'visual-literacy', name: 'Visual Literacy', prereqs: ['symbols-meaning'], category: 'foundation', domain: 'communication', difficulty: 1, points: 75 },
        { id: 'written-expression', name: 'Written Expression', prereqs: ['symbols-meaning'], category: 'foundation', domain: 'communication', difficulty: 2, points: 100 }
      ],
      quantitative: [
        { id: 'quantity-concept', name: 'Quantity & Counting', prereqs: [], category: 'foundation', domain: 'quantitative', difficulty: 1, points: 50 },
        { id: 'patterns-sequences', name: 'Pattern Recognition', prereqs: [], category: 'foundation', domain: 'quantitative', difficulty: 1, points: 50 },
        { id: 'spatial-reasoning', name: 'Spatial Reasoning', prereqs: [], category: 'foundation', domain: 'quantitative', difficulty: 2, points: 75 },
        { id: 'measurement-basics', name: 'Basic Measurement', prereqs: ['quantity-concept'], category: 'foundation', domain: 'quantitative', difficulty: 2, points: 75 }
      ],
      practical: [
        { id: 'self-care', name: 'Personal Care', prereqs: [], category: 'foundation', domain: 'practical', difficulty: 1, points: 25 },
        { id: 'tool-use-basic', name: 'Basic Tool Use', prereqs: [], category: 'foundation', domain: 'practical', difficulty: 1, points: 50 },
        { id: 'safety-awareness', name: 'Safety Awareness', prereqs: [], category: 'foundation', domain: 'practical', difficulty: 1, points: 50 }
      ]
    },
    fundamentals: {
      mathematics: [
        { id: 'number-systems', name: 'Number Systems', prereqs: ['quantity-concept'], category: 'fundamentals', domain: 'mathematics', difficulty: 2, points: 100 },
        { id: 'operations', name: 'Math Operations', prereqs: ['number-systems'], category: 'fundamentals', domain: 'mathematics', difficulty: 2, points: 100 },
        { id: 'algebra-thinking', name: 'Algebraic Thinking', prereqs: ['operations'], category: 'fundamentals', domain: 'mathematics', difficulty: 3, points: 150 },
        { id: 'geometric-thinking', name: 'Geometric Thinking', prereqs: ['spatial-reasoning'], category: 'fundamentals', domain: 'mathematics', difficulty: 3, points: 150 }
      ],
      science: [
        { id: 'scientific-method', name: 'Scientific Method', prereqs: [], category: 'fundamentals', domain: 'science', difficulty: 2, points: 100 },
        { id: 'matter-energy', name: 'Matter & Energy', prereqs: ['scientific-method'], category: 'fundamentals', domain: 'science', difficulty: 3, points: 150 },
        { id: 'living-systems', name: 'Living Systems', prereqs: ['scientific-method'], category: 'fundamentals', domain: 'science', difficulty: 3, points: 150 },
        { id: 'forces-motion', name: 'Forces & Motion', prereqs: ['matter-energy'], category: 'fundamentals', domain: 'science', difficulty: 3, points: 150 }
      ],
      practical_skills: [
        { id: 'cooking-fundamentals', name: 'Cooking Basics', prereqs: ['measurement-basics', 'safety-awareness'], category: 'fundamentals', domain: 'practical', difficulty: 2, points: 100 },
        { id: 'digital-literacy', name: 'Digital Literacy', prereqs: [], category: 'fundamentals', domain: 'practical', difficulty: 2, points: 100 },
        { id: 'money-management', name: 'Money Management', prereqs: ['operations'], category: 'fundamentals', domain: 'practical', difficulty: 2, points: 100 },
        { id: 'basic-repairs', name: 'Basic Repairs', prereqs: ['tool-use-basic'], category: 'fundamentals', domain: 'practical', difficulty: 2, points: 100 }
      ]
    },
    domains: {
      mathematics: [
        { id: 'calculus-concepts', name: 'Calculus', prereqs: ['algebra-thinking'], category: 'domains', domain: 'mathematics', difficulty: 4, points: 200 },
        { id: 'statistics-probability', name: 'Statistics', prereqs: ['algebra-thinking'], category: 'domains', domain: 'mathematics', difficulty: 3, points: 175 },
        { id: 'linear-systems', name: 'Linear Algebra', prereqs: ['algebra-thinking'], category: 'domains', domain: 'mathematics', difficulty: 4, points: 200 }
      ],
      physics: [
        { id: 'quantum-mechanics', name: 'Quantum Mechanics', prereqs: ['forces-motion', 'calculus-concepts'], category: 'domains', domain: 'physics', difficulty: 5, points: 300 },
        { id: 'thermodynamics', name: 'Thermodynamics', prereqs: ['matter-energy'], category: 'domains', domain: 'physics', difficulty: 4, points: 200 },
        { id: 'electromagnetism', name: 'Electromagnetism', prereqs: ['forces-motion'], category: 'domains', domain: 'physics', difficulty: 4, points: 200 }
      ],
      biology: [
        { id: 'cellular-processes', name: 'Cell Biology', prereqs: ['living-systems'], category: 'domains', domain: 'biology', difficulty: 3, points: 175 },
        { id: 'genetics', name: 'Genetics', prereqs: ['cellular-processes'], category: 'domains', domain: 'biology', difficulty: 4, points: 200 },
        { id: 'ecology', name: 'Ecology', prereqs: ['living-systems'], category: 'domains', domain: 'biology', difficulty: 3, points: 175 },
        { id: 'evolution', name: 'Evolution', prereqs: ['genetics', 'ecology'], category: 'domains', domain: 'biology', difficulty: 4, points: 200 }
      ],
      computer_science: [
        { id: 'programming-basics', name: 'Programming', prereqs: ['digital-literacy'], category: 'domains', domain: 'computer_science', difficulty: 3, points: 150 },
        { id: 'algorithms', name: 'Algorithms', prereqs: ['programming-basics'], category: 'domains', domain: 'computer_science', difficulty: 4, points: 200 },
        { id: 'machine-learning', name: 'Machine Learning', prereqs: ['algorithms', 'statistics-probability'], category: 'domains', domain: 'computer_science', difficulty: 5, points: 300 },
        { id: 'web-development', name: 'Web Development', prereqs: ['programming-basics'], category: 'domains', domain: 'computer_science', difficulty: 3, points: 150 }
      ],
      practical_living: [
        { id: 'gardening', name: 'Gardening', prereqs: ['living-systems'], category: 'domains', domain: 'practical', difficulty: 2, points: 125 },
        { id: 'home-maintenance', name: 'Home Maintenance', prereqs: ['basic-repairs'], category: 'domains', domain: 'practical', difficulty: 3, points: 150 },
        { id: 'woodworking', name: 'Woodworking', prereqs: ['tool-use-basic', 'geometric-thinking'], category: 'domains', domain: 'practical', difficulty: 3, points: 175 },
        { id: 'auto-mechanics', name: 'Auto Mechanics', prereqs: ['forces-motion', 'basic-repairs'], category: 'domains', domain: 'practical', difficulty: 4, points: 200 }
      ],
      health_wellness: [
        { id: 'nutrition', name: 'Nutrition Science', prereqs: ['cooking-fundamentals', 'cellular-processes'], category: 'domains', domain: 'health', difficulty: 3, points: 150 },
        { id: 'exercise-physiology', name: 'Exercise Science', prereqs: ['living-systems'], category: 'domains', domain: 'health', difficulty: 3, points: 150 },
        { id: 'mental-health', name: 'Mental Health', prereqs: [], category: 'domains', domain: 'health', difficulty: 3, points: 150 },
        { id: 'first-aid', name: 'First Aid', prereqs: ['safety-awareness'], category: 'domains', domain: 'health', difficulty: 2, points: 100 }
      ],
      business: [
        { id: 'entrepreneurship', name: 'Entrepreneurship', prereqs: ['money-management'], category: 'domains', domain: 'business', difficulty: 3, points: 175 },
        { id: 'marketing', name: 'Marketing', prereqs: ['written-expression'], category: 'domains', domain: 'business', difficulty: 3, points: 150 },
        { id: 'accounting', name: 'Accounting', prereqs: ['money-management'], category: 'domains', domain: 'business', difficulty: 3, points: 150 },
        { id: 'project-management', name: 'Project Management', prereqs: [], category: 'domains', domain: 'business', difficulty: 3, points: 150 }
      ],
      arts: [
        { id: 'visual-composition', name: 'Visual Arts', prereqs: ['visual-literacy'], category: 'domains', domain: 'arts', difficulty: 2, points: 125 },
        { id: 'music-theory', name: 'Music Theory', prereqs: ['sound-patterns'], category: 'domains', domain: 'arts', difficulty: 3, points: 150 },
        { id: 'creative-writing', name: 'Creative Writing', prereqs: ['written-expression'], category: 'domains', domain: 'arts', difficulty: 3, points: 150 },
        { id: 'photography', name: 'Photography', prereqs: ['visual-composition'], category: 'domains', domain: 'arts', difficulty: 2, points: 125 }
      ]
    },
    mastery: [
      { id: 'quantum-computing', name: 'Quantum Computing', prereqs: ['quantum-mechanics', 'algorithms'], category: 'mastery', domain: 'advanced', difficulty: 6, points: 500 },
      { id: 'artificial-general-intelligence', name: 'AGI', prereqs: ['machine-learning'], category: 'mastery', domain: 'advanced', difficulty: 6, points: 500 },
      { id: 'master-gardener', name: 'Master Gardener', prereqs: ['gardening', 'ecology'], category: 'mastery', domain: 'practical', difficulty: 5, points: 400 },
      { id: 'master-chef', name: 'Master Chef', prereqs: ['cooking-fundamentals', 'nutrition'], category: 'mastery', domain: 'practical', difficulty: 5, points: 400 }
    ]
  };

  // Flatten all nodes for easier access
  const allNodes = useMemo(() => {
    const nodes = [];
    let index = 0;
    
    // Process each category
    Object.entries(knowledgeGraph).forEach(([category, domains]) => {
      if (typeof domains === 'object' && !Array.isArray(domains)) {
        Object.entries(domains).forEach(([domain, domainNodes]) => {
          domainNodes.forEach(node => {
            nodes.push({
              ...node,
              index: index++,
              x: 100 + (index % 8) * 120,
              y: 100 + Math.floor(index / 8) * 120
            });
          });
        });
      } else if (Array.isArray(domains)) {
        domains.forEach(node => {
          nodes.push({
            ...node,
            index: index++,
            x: 100 + (index % 8) * 120,
            y: 100 + Math.floor(index / 8) * 120
          });
        });
      }
    });
    
    return nodes;
  }, []);

  // Create connections based on prerequisites
  const connections = useMemo(() => {
    const conns = [];
    allNodes.forEach(node => {
      if (node.prereqs && node.prereqs.length > 0) {
        node.prereqs.forEach(prereqId => {
          const fromNode = allNodes.find(n => n.id === prereqId);
          if (fromNode) {
            conns.push({ from: prereqId, to: node.id });
          }
        });
      }
    });
    return conns;
  }, [allNodes]);

  // State management
  const [selectedNode, setSelectedNode] = useState(null);
  const [userStats, setUserStats] = useState({
    pathfinderPoints: 2450,
    neuralLevel: 12,
    memoryCrystals: 8,
    synapticStreak: 7,
    conqueredNodes: ['symbols-meaning', 'quantity-concept', 'self-care', 'tool-use-basic'],
    neuralPower: 85,
    title: 'Knowledge Seeker'
  });

  // ====================
  // SUPABASE INTEGRATION
  // ====================
  
  // Load user data from Supabase
  const loadUserData = async () => {
    // Uncomment when Supabase is connected:
    /*
    try {
      setIsLoading(true);
      
      // Get current user
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return;
      
      setCurrentUser(user);
      
      // Load user stats
      const { data: userData, error } = await supabase
        .from('users')
        .select('*')
        .eq('id', user.id)
        .single();
      
      if (userData) {
        setUserStats({
          pathfinderPoints: userData.points || 0,
          neuralLevel: userData.neural_level || 1,
          memoryCrystals: userData.memory_crystals || 0,
          synapticStreak: userData.streak || 0,
          conqueredNodes: userData.conquered_nodes || [],
          neuralPower: userData.neural_power || 0,
          title: userData.title || 'Knowledge Seeker'
        });
      }
      
      // Load user progress
      const { data: progressData } = await supabase
        .from('user_progress')
        .select('node_id')
        .eq('user_id', user.id)
        .eq('completed', true);
      
      if (progressData) {
        const completedNodeIds = progressData.map(p => p.node_id);
        setUserStats(prev => ({
          ...prev,
          conqueredNodes: completedNodeIds
        }));
      }
    } catch (error) {
      console.error('Error loading user data:', error);
    } finally {
      setIsLoading(false);
    }
    */
  };

  // Save progress to Supabase
  const saveProgress = async (nodeId, score) => {
    // Uncomment when Supabase is connected:
    /*
    try {
      if (!currentUser) return;
      
      // Save to user_progress table
      const { error: progressError } = await supabase
        .from('user_progress')
        .upsert({
          user_id: currentUser.id,
          node_id: nodeId,
          completed: true,
          score: score,
          completed_at: new Date().toISOString()
        });
      
      if (progressError) throw progressError;
      
      // Update user stats
      const { error: userError } = await supabase
        .from('users')
        .update({
          points: userStats.pathfinderPoints,
          neural_level: userStats.neuralLevel,
          memory_crystals: userStats.memoryCrystals,
          streak: userStats.synapticStreak,
          conquered_nodes: userStats.conqueredNodes,
          title: userStats.title
        })
        .eq('id', currentUser.id);
      
      if (userError) throw userError;
      
      console.log('Progress saved successfully!');
    } catch (error) {
      console.error('Error saving progress:', error);
    }
    */
  };

  // Load nodes from Supabase (optional - if you want to store nodes in DB)
  const loadNodesFromDatabase = async () => {
    // Uncomment when Supabase is connected:
    /*
    try {
      const { data, error } = await supabase
        .from('nodes')
        .select('*')
        .order('category', { ascending: true });
      
      if (data && data.length > 0) {
        // Update your knowledge graph with database nodes
        console.log('Loaded nodes from database:', data);
      }
    } catch (error) {
      console.error('Error loading nodes:', error);
    }
    */
  };

  // Get leaderboard data
  const loadLeaderboard = async () => {
    // Uncomment when Supabase is connected:
    /*
    try {
      const { data, error } = await supabase
        .from('leaderboard')  // This is the view we created
        .select('*')
        .limit(10);
      
      if (data) {
        console.log('Leaderboard:', data);
        // Update your leaderboard display
      }
    } catch (error) {
      console.error('Error loading leaderboard:', error);
    }
    */
  };

  // Authentication functions
  const signUp = async (email, password) => {
    // Uncomment when Supabase is connected:
    /*
    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
      });
      
      if (error) throw error;
      
      if (data.user) {
        // Create user profile
        await supabase.from('users').insert({
          id: data.user.id,
          email: email,
          username: email.split('@')[0],
          points: 0,
          neural_level: 1,
          memory_crystals: 0,
          streak: 0,
          title: 'Knowledge Seeker'
        });
      }
      
      return { success: true, user: data.user };
    } catch (error) {
      console.error('Signup error:', error);
      return { success: false, error: error.message };
    }
    */
  };

  const signIn = async (email, password) => {
    // Uncomment when Supabase is connected:
    /*
    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });
      
      if (error) throw error;
      
      return { success: true, user: data.user };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: error.message };
    }
    */
  };

  const signOut = async () => {
    // Uncomment when Supabase is connected:
    /*
    try {
      await supabase.auth.signOut();
      setCurrentUser(null);
      setUserStats({
        pathfinderPoints: 0,
        neuralLevel: 1,
        memoryCrystals: 0,
        synapticStreak: 0,
        conqueredNodes: [],
        neuralPower: 0,
        title: 'Knowledge Seeker'
      });
    } catch (error) {
      console.error('Signout error:', error);
    }
    */
  };

  // Load data on component mount
  useEffect(() => {
    loadUserData();
    loadNodesFromDatabase();
    loadLeaderboard();
    
    // Set up auth listener
    // Uncomment when Supabase is connected:
    /*
    const { data: authListener } = supabase.auth.onAuthStateChange((event, session) => {
      if (event === 'SIGNED_IN') {
        loadUserData();
      }
      if (event === 'SIGNED_OUT') {
        setCurrentUser(null);
      }
    });

    return () => {
      authListener?.subscription?.unsubscribe();
    };
    */
  }, []);

  // Auto-save progress periodically
  useEffect(() => {
    const saveInterval = setInterval(() => {
      if (currentUser && userStats.conqueredNodes.length > 0) {
        // Auto-save user stats
        // Uncomment when Supabase is connected:
        /*
        supabase
          .from('users')
          .update({
            points: userStats.pathfinderPoints,
            neural_level: userStats.neuralLevel,
            memory_crystals: userStats.memoryCrystals,
            streak: userStats.synapticStreak,
            conquered_nodes: userStats.conqueredNodes,
            title: userStats.title,
            last_active: new Date().toISOString()
          })
          .eq('id', currentUser.id)
          .then(({ error }) => {
            if (error) console.error('Auto-save error:', error);
            else console.log('Auto-saved progress');
          });
        */
      }
    }, 30000); // Save every 30 seconds

    return () => clearInterval(saveInterval);
  }, [currentUser, userStats]);
  const [currentView, setCurrentView] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [activeFilters, setActiveFilters] = useState([]);
  const [showQuiz, setShowQuiz] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [showAchievement, setShowAchievement] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [answerFeedback, setAnswerFeedback] = useState(null);

  // Sample quiz questions
  const quizQuestions = {
    'symbols-meaning': [
      {
        question: "What is the primary purpose of symbols?",
        options: ["To represent ideas", "To look pretty", "To confuse", "To take up space"],
        correct: 0,
        explanation: "Symbols are visual representations of ideas, concepts, or objects"
      }
    ],
    'quantity-concept': [
      {
        question: "Which represents 'more'?",
        options: ["3 < 5", "5 > 3", "3 = 3", "None"],
        correct: 1,
        explanation: "The symbol > means 'greater than', so 5 > 3 means 5 is more than 3"
      }
    ],
    'cooking-fundamentals': [
      {
        question: "What happens to water at 100°C?",
        options: ["It freezes", "It boils", "Nothing", "It disappears"],
        correct: 1,
        explanation: "Water boils at 100°C (212°F) at sea level"
      }
    ]
  };

  // Domain icons mapping
  const domainIcons = {
    mathematics: BarChart3,
    science: Zap,
    practical: Hammer,
    biology: Leaf,
    physics: Activity,
    computer_science: Cpu,
    health: Heart,
    business: Briefcase,
    arts: Palette,
    advanced: Brain
  };

  // Get node state
  const getNodeState = useCallback((nodeId) => {
    if (userStats.conqueredNodes.includes(nodeId)) return 'completed';
    
    const node = allNodes.find(n => n.id === nodeId);
    if (!node) return 'locked';
    
    // Check if prerequisites are met
    if (!node.prereqs || node.prereqs.length === 0) return 'available';
    
    const prereqsMet = node.prereqs.every(prereq => 
      userStats.conqueredNodes.includes(prereq)
    );
    
    return prereqsMet ? 'available' : 'locked';
  }, [userStats.conqueredNodes, allNodes]);

  // Filter nodes based on view and search
  const filteredNodes = useMemo(() => {
    let nodes = [...allNodes];
    
    // Filter by domain
    if (activeFilters.length > 0) {
      nodes = nodes.filter(node => activeFilters.includes(node.domain));
    }
    
    // Filter by search
    if (searchTerm) {
      nodes = nodes.filter(node => 
        node.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    // Filter by view
    if (currentView !== 'all') {
      nodes = nodes.filter(node => node.category === currentView);
    }
    
    return nodes;
  }, [allNodes, activeFilters, searchTerm, currentView]);

  // Learning paths
  const learningPaths = {
    'self-sufficiency': {
      name: 'Self-Sufficient Living',
      icon: Home,
      nodes: ['cooking-fundamentals', 'gardening', 'basic-repairs', 'home-maintenance', 'first-aid'],
      description: 'Learn to be independent'
    },
    'digital-creator': {
      name: 'Digital Creator',
      icon: Cpu,
      nodes: ['digital-literacy', 'programming-basics', 'web-development', 'photography', 'creative-writing'],
      description: 'Create in the digital world'
    },
    'entrepreneur': {
      name: 'Entrepreneur Path',
      icon: Briefcase,
      nodes: ['money-management', 'entrepreneurship', 'marketing', 'accounting', 'project-management'],
      description: 'Start your business journey'
    },
    'maker': {
      name: 'Maker & Builder',
      icon: Hammer,
      nodes: ['tool-use-basic', 'woodworking', 'basic-repairs', 'home-maintenance'],
      description: 'Build and create with your hands'
    },
    'scholar': {
      name: 'Academic Scholar',
      icon: BookOpen,
      nodes: ['scientific-method', 'algebra-thinking', 'calculus-concepts', 'statistics-probability'],
      description: 'Deep theoretical knowledge'
    }
  };

  // Handle quiz answer
  const handleAnswer = (answerIndex) => {
    setSelectedAnswer(answerIndex);
    const questions = quizQuestions[selectedNode.id] || quizQuestions['symbols-meaning'];
    const question = questions[currentQuestion] || questions[0];
    const isCorrect = answerIndex === question.correct;
    
    setAnswerFeedback({
      isCorrect,
      explanation: question.explanation
    });
    
    if (isCorrect) {
      setUserStats(prev => ({
        ...prev,
        pathfinderPoints: prev.pathfinderPoints + selectedNode.points
      }));
    }
    
    setTimeout(() => {
      completeNode();
    }, 2000);
  };

  // Complete a node
  const completeNode = () => {
    if (!userStats.conqueredNodes.includes(selectedNode.id)) {
      const newConqueredNodes = [...userStats.conqueredNodes, selectedNode.id];
      const newPoints = userStats.pathfinderPoints + selectedNode.points;
      const newLevel = Math.floor(newConqueredNodes.length / 5) + 1;
      
      setUserStats(prev => ({
        ...prev,
        conqueredNodes: newConqueredNodes,
        pathfinderPoints: newPoints,
        memoryCrystals: prev.memoryCrystals + 1,
        neuralLevel: newLevel,
        title: newConqueredNodes.length > 20 ? 'Knowledge Master' : 
               newConqueredNodes.length > 10 ? 'Neural Explorer' : 'Knowledge Seeker'
      }));
      
      // Save to Supabase
      saveProgress(selectedNode.id, selectedNode.points);
      
      setShowAchievement(true);
      setTimeout(() => setShowAchievement(false), 3000);
    }
    
    setShowQuiz(false);
    setCurrentQuestion(0);
    setSelectedAnswer(null);
    setAnswerFeedback(null);
  };

  // Toggle filter
  const toggleFilter = (domain) => {
    setActiveFilters(prev => 
      prev.includes(domain) 
        ? prev.filter(f => f !== domain)
        : [...prev, domain]
    );
  };

  // Calculate progress
  const calculateProgress = () => {
    const totalNodes = allNodes.length;
    const completedNodes = userStats.conqueredNodes.length;
    return Math.round((completedNodes / totalNodes) * 100);
  };

  // Styles
  const styles = {
    container: {
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      fontFamily: 'system-ui, -apple-system, sans-serif',
      paddingBottom: isMobile ? '70px' : '0'
    },
    header: {
      background: 'rgba(255, 255, 255, 0.95)',
      backdropFilter: 'blur(10px)',
      borderRadius: isMobile ? '0 0 20px 20px' : '20px',
      padding: isMobile ? '15px' : '20px',
      margin: isMobile ? '0 0 15px 0' : '20px 20px 20px 20px',
      boxShadow: '0 10px 30px rgba(0,0,0,0.1)'
    },
    mainGrid: {
      display: isMobile ? 'block' : 'grid',
      gridTemplateColumns: isMobile ? '1fr' : '280px 1fr 300px',
      gap: '20px',
      maxWidth: '1400px',
      margin: '0 auto',
      padding: '0 20px'
    },
    panel: {
      background: 'rgba(255, 255, 255, 0.95)',
      backdropFilter: 'blur(10px)',
      borderRadius: '15px',
      padding: '20px',
      marginBottom: isMobile ? '15px' : '0',
      boxShadow: '0 5px 20px rgba(0,0,0,0.1)'
    },
    graphContainer: {
      background: 'rgba(255, 255, 255, 0.95)',
      backdropFilter: 'blur(10px)',
      borderRadius: '20px',
      padding: '20px',
      height: isMobile ? '500px' : '700px',
      position: 'relative',
      overflow: 'auto',
      boxShadow: '0 5px 20px rgba(0,0,0,0.1)'
    },
    node: {
      position: 'absolute',
      width: '90px',
      height: '90px',
      borderRadius: '15px',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
      fontSize: '11px',
      fontWeight: 'bold',
      textAlign: 'center',
      padding: '8px',
      border: '2px solid transparent'
    },
    nodeCompleted: {
      background: 'linear-gradient(135deg, #00c851, #00ff00)',
      color: 'white',
      boxShadow: '0 5px 15px rgba(0, 200, 81, 0.4)'
    },
    nodeAvailable: {
      background: 'linear-gradient(135deg, #2196F3, #00bcd4)',
      color: 'white',
      boxShadow: '0 5px 15px rgba(33, 150, 243, 0.4)',
      animation: 'pulse 2s infinite'
    },
    nodeLocked: {
      background: '#e0e0e0',
      color: '#999',
      opacity: 0.6
    }
  };

  // Mobile navigation
  const MobileNav = () => (
    <div style={{
      position: 'fixed',
      bottom: 0,
      left: 0,
      right: 0,
      background: 'white',
      borderTop: '1px solid #ddd',
      display: 'flex',
      justifyContent: 'space-around',
      padding: '10px 0',
      zIndex: 1000
    }}>
      <button onClick={() => setActiveTab('graph')} style={{ 
        background: 'none', 
        border: 'none', 
        padding: '5px',
        color: activeTab === 'graph' ? '#667eea' : '#999'
      }}>
        <Grid size={24} />
        <div style={{ fontSize: '10px' }}>Map</div>
      </button>
      <button onClick={() => setActiveTab('paths')} style={{ 
        background: 'none', 
        border: 'none', 
        padding: '5px',
        color: activeTab === 'paths' ? '#667eea' : '#999'
      }}>
        <Map size={24} />
        <div style={{ fontSize: '10px' }}>Paths</div>
      </button>
      <button onClick={() => setActiveTab('profile')} style={{ 
        background: 'none', 
        border: 'none', 
        padding: '5px',
        color: activeTab === 'profile' ? '#667eea' : '#999'
      }}>
        <User size={24} />
        <div style={{ fontSize: '10px' }}>Profile</div>
      </button>
    </div>
  );

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '15px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Brain size={36} color="#667eea" />
            <div>
              <h1 style={{ margin: 0, fontSize: isMobile ? '24px' : '28px', color: '#333' }}>NeuroQuest</h1>
              <p style={{ margin: 0, fontSize: '12px', color: '#666' }}>Master All Human Knowledge</p>
            </div>
          </div>
          
          <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
            <div style={{ 
              background: 'linear-gradient(135deg, #ff6b6b, #ffd93d)', 
              padding: '8px 15px', 
              borderRadius: '20px',
              color: 'white',
              fontWeight: 'bold',
              display: 'flex',
              alignItems: 'center',
              gap: '5px'
            }}>
              <Flame size={18} />
              {userStats.synapticStreak} Day Streak!
            </div>
            
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#667eea' }}>
                {userStats.pathfinderPoints.toLocaleString()}
              </div>
              <div style={{ fontSize: '10px', color: '#999' }}>POINTS</div>
            </div>
            
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#764ba2' }}>
                {userStats.neuralLevel}
              </div>
              <div style={{ fontSize: '10px', color: '#999' }}>LEVEL</div>
            </div>
          </div>
        </div>
        
        {/* Progress Bar */}
        <div style={{ marginTop: '15px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '5px' }}>
            <span>Overall Progress</span>
            <span>{calculateProgress()}%</span>
          </div>
          <div style={{ height: '8px', background: '#e0e0e0', borderRadius: '10px', overflow: 'hidden' }}>
            <div style={{
              width: `${calculateProgress()}%`,
              height: '100%',
              background: 'linear-gradient(90deg, #667eea, #764ba2)',
              transition: 'width 0.5s ease'
            }} />
          </div>
        </div>
      </div>

      <div style={styles.mainGrid}>
        {/* Left Sidebar - Filters */}
        {!isMobile && (
          <div>
            {/* Search */}
            <div style={styles.panel}>
              <input
                type="text"
                placeholder="Search knowledge..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{
                  width: '100%',
                  padding: '10px',
                  border: '2px solid #e0e0e0',
                  borderRadius: '10px',
                  fontSize: '14px'
                }}
              />
            </div>

            {/* Category Filter */}
            <div style={{ ...styles.panel, marginTop: '15px' }}>
              <h3 style={{ fontSize: '16px', marginBottom: '15px' }}>Knowledge Level</h3>
              {['all', 'foundation', 'fundamentals', 'domains', 'mastery'].map(view => (
                <button
                  key={view}
                  onClick={() => setCurrentView(view)}
                  style={{
                    width: '100%',
                    padding: '10px',
                    marginBottom: '8px',
                    border: 'none',
                    borderRadius: '8px',
                    background: currentView === view ? 'linear-gradient(135deg, #667eea, #764ba2)' : '#f0f0f0',
                    color: currentView === view ? 'white' : '#666',
                    cursor: 'pointer',
                    fontWeight: currentView === view ? 'bold' : 'normal',
                    transition: 'all 0.3s'
                  }}
                >
                  {view.charAt(0).toUpperCase() + view.slice(1)}
                </button>
              ))}
            </div>

            {/* Domain Filter */}
            <div style={{ ...styles.panel, marginTop: '15px' }}>
              <h3 style={{ fontSize: '16px', marginBottom: '15px' }}>Domains</h3>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {Object.keys(domainIcons).map(domain => {
                  const Icon = domainIcons[domain];
                  const isActive = activeFilters.includes(domain);
                  return (
                    <button
                      key={domain}
                      onClick={() => toggleFilter(domain)}
                      style={{
                        padding: '8px 12px',
                        border: 'none',
                        borderRadius: '20px',
                        background: isActive ? 'linear-gradient(135deg, #667eea, #764ba2)' : '#f0f0f0',
                        color: isActive ? 'white' : '#666',
                        cursor: 'pointer',
                        fontSize: '12px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}
                    >
                      <Icon size={14} />
                      {domain.replace('_', ' ')}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Learning Paths */}
            <div style={{ ...styles.panel, marginTop: '15px' }}>
              <h3 style={{ fontSize: '16px', marginBottom: '15px' }}>Learning Paths</h3>
              {Object.entries(learningPaths).slice(0, 3).map(([key, path]) => {
                const Icon = path.icon;
                return (
                  <div key={key} style={{
                    padding: '10px',
                    background: '#f8f8f8',
                    borderRadius: '8px',
                    marginBottom: '8px',
                    cursor: 'pointer'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <Icon size={20} color="#667eea" />
                      <div>
                        <div style={{ fontWeight: 'bold', fontSize: '13px' }}>{path.name}</div>
                        <div style={{ fontSize: '11px', color: '#666' }}>{path.description}</div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Knowledge Graph */}
        <div style={styles.graphContainer}>
          <svg style={{ position: 'absolute', width: '100%', height: '100%', top: 0, left: 0 }}>
            {connections.map((conn, idx) => {
              const fromNode = filteredNodes.find(n => n.id === conn.from);
              const toNode = filteredNodes.find(n => n.id === conn.to);
              
              if (!fromNode || !toNode) return null;
              
              const fromState = getNodeState(fromNode.id);
              const toState = getNodeState(toNode.id);
              const isActive = fromState === 'completed' && toState !== 'locked';
              
              return (
                <line
                  key={idx}
                  x1={fromNode.x + 45}
                  y1={fromNode.y + 45}
                  x2={toNode.x + 45}
                  y2={toNode.y + 45}
                  stroke={isActive ? '#667eea' : '#ddd'}
                  strokeWidth={isActive ? '2' : '1'}
                  strokeDasharray={!isActive ? '5,5' : '0'}
                  opacity={isActive ? 0.6 : 0.3}
                />
              );
            })}
          </svg>

          {filteredNodes.map(node => {
            const state = getNodeState(node.id);
            const Icon = domainIcons[node.domain] || Brain;
            
            return (
              <div
                key={node.id}
                style={{
                  ...styles.node,
                  ...(state === 'completed' ? styles.nodeCompleted :
                      state === 'available' ? styles.nodeAvailable :
                      styles.nodeLocked),
                  left: node.x,
                  top: node.y,
                  transform: selectedNode?.id === node.id ? 'scale(1.1)' : 'scale(1)'
                }}
                onClick={() => {
                  if (state !== 'locked') {
                    setSelectedNode(node);
                    if (state === 'available' && (quizQuestions[node.id] || quizQuestions['symbols-meaning'])) {
                      setShowQuiz(true);
                    }
                  }
                }}
                onMouseEnter={(e) => {
                  if (state !== 'locked') {
                    e.currentTarget.style.transform = 'scale(1.1)';
                  }
                }}
                onMouseLeave={(e) => {
                  if (selectedNode?.id !== node.id) {
                    e.currentTarget.style.transform = 'scale(1)';
                  }
                }}
              >
                <Icon size={24} />
                <div style={{ marginTop: '5px', fontSize: '10px', lineHeight: '1.2' }}>
                  {node.name}
                </div>
                <div style={{ fontSize: '9px', opacity: 0.8 }}>
                  +{node.points}
                </div>
                {state === 'locked' && <Lock size={16} style={{ position: 'absolute', top: '5px', right: '5px' }} />}
                {state === 'completed' && <CheckCircle size={16} style={{ position: 'absolute', top: '5px', right: '5px' }} />}
              </div>
            );
          })}

          {/* Node Details */}
          {selectedNode && !showQuiz && (
            <div style={{
              position: 'absolute',
              bottom: '20px',
              left: '20px',
              right: '20px',
              background: 'white',
              borderRadius: '15px',
              padding: '20px',
              boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
              zIndex: 10
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                <div>
                  <h3 style={{ margin: '0 0 10px 0' }}>{selectedNode.name}</h3>
                  <div style={{ display: 'flex', gap: '10px', fontSize: '12px', color: '#666' }}>
                    <span>Difficulty: {'⭐'.repeat(selectedNode.difficulty)}</span>
                    <span>+{selectedNode.points} points</span>
                  </div>
                  {selectedNode.prereqs && selectedNode.prereqs.length > 0 && (
                    <div style={{ marginTop: '10px', fontSize: '12px', color: '#999' }}>
                      Prerequisites: {selectedNode.prereqs.join(', ')}
                    </div>
                  )}
                </div>
                <button
                  onClick={() => setSelectedNode(null)}
                  style={{ background: 'none', border: 'none', cursor: 'pointer' }}
                >
                  <X size={20} />
                </button>
              </div>
              {getNodeState(selectedNode.id) === 'available' && (
                <button
                  onClick={() => setShowQuiz(true)}
                  style={{
                    marginTop: '15px',
                    padding: '10px 20px',
                    background: 'linear-gradient(135deg, #667eea, #764ba2)',
                    color: 'white',
                    border: 'none',
                    borderRadius: '10px',
                    cursor: 'pointer',
                    fontWeight: 'bold',
                    width: '100%'
                  }}
                >
                  Start Challenge <ChevronRight size={16} style={{ verticalAlign: 'middle' }} />
                </button>
              )}
            </div>
          )}
        </div>

        {/* Right Sidebar - Stats */}
        {!isMobile && (
          <div>
            {/* User Stats */}
            <div style={styles.panel}>
              <h3 style={{ fontSize: '16px', marginBottom: '15px' }}>Your Progress</h3>
              <div style={{ textAlign: 'center', marginBottom: '20px' }}>
                <div style={{ 
                  width: '80px', 
                  height: '80px', 
                  margin: '0 auto',
                  background: 'linear-gradient(135deg, #667eea, #764ba2)',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  marginBottom: '10px'
                }}>
                  <User size={40} color="white" />
                </div>
                <div style={{ fontWeight: 'bold', fontSize: '18px' }}>{userStats.title}</div>
                <div style={{ fontSize: '12px', color: '#999' }}>Level {userStats.neuralLevel}</div>
              </div>
              
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                <div style={{ background: '#f8f8f8', padding: '10px', borderRadius: '8px', textAlign: 'center' }}>
                  <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#667eea' }}>
                    {userStats.conqueredNodes.length}
                  </div>
                  <div style={{ fontSize: '10px', color: '#999' }}>CONQUERED</div>
                </div>
                <div style={{ background: '#f8f8f8', padding: '10px', borderRadius: '8px', textAlign: 'center' }}>
                  <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#764ba2' }}>
                    {userStats.memoryCrystals}
                  </div>
                  <div style={{ fontSize: '10px', color: '#999' }}>CRYSTALS</div>
                </div>
              </div>
            </div>

            {/* Recent Achievements */}
            <div style={{ ...styles.panel, marginTop: '15px' }}>
              <h3 style={{ fontSize: '16px', marginBottom: '15px' }}>Recent Achievements</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '10px', background: '#f8f8f8', borderRadius: '8px' }}>
                  <Trophy size={20} color="#ffd700" />
                  <div>
                    <div style={{ fontSize: '13px', fontWeight: 'bold' }}>First Steps</div>
                    <div style={{ fontSize: '11px', color: '#666' }}>Complete 5 nodes</div>
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '10px', background: '#f8f8f8', borderRadius: '8px' }}>
                  <Star size={20} color="#667eea" />
                  <div>
                    <div style={{ fontSize: '13px', fontWeight: 'bold' }}>Quick Learner</div>
                    <div style={{ fontSize: '11px', color: '#666' }}>Complete 3 nodes in one day</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Suggested Next */}
            <div style={{ ...styles.panel, marginTop: '15px' }}>
              <h3 style={{ fontSize: '16px', marginBottom: '15px' }}>Suggested Next</h3>
              {filteredNodes
                .filter(n => getNodeState(n.id) === 'available')
                .slice(0, 3)
                .map(node => {
                  const Icon = domainIcons[node.domain] || Brain;
                  return (
                    <div 
                      key={node.id}
                      style={{ 
                        padding: '10px', 
                        background: '#f8f8f8', 
                        borderRadius: '8px', 
                        marginBottom: '8px',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '10px'
                      }}
                      onClick={() => setSelectedNode(node)}
                    >
                      <Icon size={20} color="#667eea" />
                      <div>
                        <div style={{ fontSize: '13px', fontWeight: 'bold' }}>{node.name}</div>
                        <div style={{ fontSize: '11px', color: '#666' }}>+{node.points} points</div>
                      </div>
                    </div>
                  );
                })}
            </div>
          </div>
        )}
      </div>

      {/* Quiz Modal */}
      {showQuiz && selectedNode && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.8)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: '20px'
        }}>
          <div style={{
            background: 'white',
            borderRadius: '20px',
            padding: '30px',
            maxWidth: '500px',
            width: '100%'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2 style={{ margin: 0 }}>{selectedNode.name} Challenge</h2>
              <button
                onClick={() => {
                  setShowQuiz(false);
                  setCurrentQuestion(0);
                  setSelectedAnswer(null);
                  setAnswerFeedback(null);
                }}
                style={{ background: 'none', border: 'none', cursor: 'pointer' }}
              >
                <X size={24} />
              </button>
            </div>

            <div style={{ marginBottom: '20px' }}>
              <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>
                Question {currentQuestion + 1} of 1
              </div>
              <div style={{ height: '4px', background: '#e0e0e0', borderRadius: '2px' }}>
                <div style={{
                  width: '100%',
                  height: '100%',
                  background: 'linear-gradient(90deg, #667eea, #764ba2)',
                  borderRadius: '2px'
                }} />
              </div>
            </div>

            <div>
              <h3 style={{ marginBottom: '20px' }}>
                {(quizQuestions[selectedNode.id] || quizQuestions['symbols-meaning'])[0].question}
              </h3>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {(quizQuestions[selectedNode.id] || quizQuestions['symbols-meaning'])[0].options.map((option, idx) => (
                  <button
                    key={idx}
                    onClick={() => !answerFeedback && handleAnswer(idx)}
                    disabled={answerFeedback !== null}
                    style={{
                      padding: '15px',
                      border: '2px solid',
                      borderColor: answerFeedback && selectedAnswer === idx
                        ? answerFeedback.isCorrect ? '#00c851' : '#ff4444'
                        : '#e0e0e0',
                      borderRadius: '10px',
                      background: answerFeedback && selectedAnswer === idx
                        ? answerFeedback.isCorrect ? '#e8f5e9' : '#ffebee'
                        : 'white',
                      cursor: answerFeedback ? 'default' : 'pointer',
                      textAlign: 'left',
                      transition: 'all 0.3s'
                    }}
                  >
                    {option}
                  </button>
                ))}
              </div>

              {answerFeedback && (
                <div style={{
                  marginTop: '20px',
                  padding: '15px',
                  background: answerFeedback.isCorrect ? '#e8f5e9' : '#fff3e0',
                  borderRadius: '10px',
                  border: `1px solid ${answerFeedback.isCorrect ? '#00c851' : '#ff6f00'}`
                }}>
                  <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
                    {answerFeedback.isCorrect ? '✅ Correct!' : '💡 Not quite!'}
                  </div>
                  <div style={{ fontSize: '14px', color: '#666' }}>
                    {answerFeedback.explanation}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Achievement Popup */}
      {showAchievement && (
        <div style={{
          position: 'fixed',
          top: '20px',
          right: '20px',
          background: 'white',
          borderRadius: '15px',
          padding: '20px',
          boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
          zIndex: 1001,
          animation: 'slideIn 0.5s ease-out'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            <Trophy size={40} color="#ffd700" />
            <div>
              <div style={{ fontWeight: 'bold', fontSize: '16px' }}>Node Conquered!</div>
              <div style={{ fontSize: '14px', color: '#666' }}>
                {selectedNode?.name} completed
              </div>
              <div style={{ fontSize: '12px', color: '#667eea', marginTop: '5px' }}>
                +{selectedNode?.points} points earned!
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Mobile Navigation */}
      {isMobile && <MobileNav />}

      <style>{`
        @keyframes pulse {
          0%, 100% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.05); opacity: 0.9; }
        }
        @keyframes slideIn {
          from { transform: translateX(100%); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
      `}</style>
    </div>
  );
};

export default App;
'use client';

import React from 'react';
import { Trees, Sparkles, TrendingUp, Award, ChevronRight, Leaf, Target, BookOpen } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';

interface HomepageProps {
  onGetStarted: () => void;
}

export const Homepage: React.FC<HomepageProps> = ({ onGetStarted }) => {
  const { resolvedTheme } = useTheme();
  const isDark = resolvedTheme === 'dark';

  const features = [
    {
      icon: Trees,
      title: 'Skill Trees',
      description: 'Grow your abilities through branching learning paths'
    },
    {
      icon: Target,
      title: 'Goal-Oriented',
      description: 'Set and achieve learning milestones with gamified rewards'
    },
    {
      icon: Sparkles,
      title: 'Interactive Challenges',
      description: 'Engage with dynamic quizzes and real-world applications'
    },
    {
      icon: TrendingUp,
      title: 'Track Progress',
      description: 'Visualize your learning journey with detailed analytics'
    }
  ];

  const stats = [
    { value: '10K+', label: 'Active Students' },
    { value: '500+', label: 'Skills to Master' },
    { value: '95%', label: 'Success Rate' },
    { value: '4.9', label: 'User Rating' }
  ];

  return (
    <div className={`min-h-screen ${isDark ? 'bg-gray-900' : 'bg-gradient-to-br from-forest-50 via-cream-100 to-sky-50'}`}>
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-forest-600/10 to-sky-600/10" />
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-24">
          <div className="text-center">
            {/* Logo */}
            <div className="flex justify-center mb-8">
              <div className={`p-4 rounded-2xl ${isDark ? 'bg-forest-900/30' : 'bg-white'} shadow-xl`}>
                <Trees className="w-16 h-16 text-forest-600" />
              </div>
            </div>

            {/* Headline */}
            <h1 className={`text-5xl md:text-6xl font-bold mb-6 ${isDark ? 'text-white' : 'text-gray-900'}`}>
              <span className="bg-gradient-to-r from-forest-600 to-sky-600 bg-clip-text text-transparent">
                SkillTree
              </span>
            </h1>
            
            <p className={`text-xl md:text-2xl mb-8 max-w-2xl mx-auto ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>
              Grow Your Skills. Master Your Future.
              Plant the seeds of knowledge and watch your abilities bloom.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={onGetStarted}
                className="px-8 py-4 bg-gradient-to-r from-forest-600 to-sky-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 flex items-center justify-center gap-2"
              >
                Start Growing
                <ChevronRight className="w-5 h-5" />
              </button>
              
              <button
                onClick={onGetStarted}
                className={`px-8 py-4 ${isDark ? 'bg-gray-800 text-white' : 'bg-white text-gray-900'} font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200`}
              >
                Sign In
              </button>
            </div>
          </div>
        </div>

        {/* Floating Elements */}
        <div className="absolute top-20 left-10 animate-pulse">
          <Leaf className="w-8 h-8 text-forest-500 opacity-60" />
        </div>
        <div className="absolute top-40 right-20 animate-bounce">
          <Award className="w-10 h-10 text-sunset-500 opacity-60" />
        </div>
        <div className="absolute bottom-20 left-1/4 animate-pulse">
          <BookOpen className="w-8 h-8 text-sky-500 opacity-60" />
        </div>
      </div>

      {/* Stats Section */}
      <div className={`py-16 ${isDark ? 'bg-gray-800/50' : 'bg-white/80'} backdrop-blur-lg`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className={`text-3xl md:text-4xl font-bold mb-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  {stat.value}
                </div>
                <div className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className={`text-3xl md:text-4xl font-bold mb-4 ${isDark ? 'text-white' : 'text-gray-900'}`}>
              Why Choose NeuroQuest?
            </h2>
            <p className={`text-lg ${isDark ? 'text-gray-300' : 'text-gray-600'} max-w-2xl mx-auto`}>
              Experience learning like never before with our innovative features
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div
                  key={index}
                  className={`p-6 rounded-2xl ${
                    isDark ? 'bg-gray-800/50' : 'bg-white'
                  } shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200`}
                >
                  <div className="flex justify-center mb-4">
                    <div className="p-3 rounded-xl bg-gradient-to-br from-forest-500 to-sky-500">
                      <Icon className="w-8 h-8 text-white" />
                    </div>
                  </div>
                  <h3 className={`text-xl font-semibold mb-2 text-center ${isDark ? 'text-white' : 'text-gray-900'}`}>
                    {feature.title}
                  </h3>
                  <p className={`text-center ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                    {feature.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Bottom CTA Section */}
      <div className="py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className={`text-3xl md:text-4xl font-bold mb-6 ${isDark ? 'text-white' : 'text-gray-900'}`}>
            Ready to Begin Your Learning Adventure?
          </h2>
          <p className={`text-lg mb-8 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>
            Join thousands of learners who are already expanding their knowledge horizons
          </p>
          <button
            onClick={onGetStarted}
            className="px-10 py-4 bg-gradient-to-r from-forest-600 to-sky-600 text-white text-lg font-semibold rounded-xl shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-200 flex items-center justify-center gap-2 mx-auto"
          >
            Get Started Free
            <ChevronRight className="w-6 h-6" />
          </button>
        </div>
      </div>

      {/* Footer */}
      <footer className={`py-8 border-t ${isDark ? 'border-gray-800 bg-gray-900' : 'border-gray-200 bg-gray-50'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center gap-2 mb-4 md:mb-0">
              <Trees className="w-6 h-6 text-forest-600" />
              <span className={`font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                SkillTree
              </span>
            </div>
            <div className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
              © 2025 SkillTree. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};
# SkillTree - Interactive Learning Platform

An engaging, gamified learning platform designed for homeschooling, supplemental learning, and lifelong education. Built with React, TypeScript, and Supabase.

## 🎮 Features

### Core Learning System
- **Interactive Skill Tree**: D3.js-powered radial tree visualization with 5,700+ learning nodes
- **Learning Paths**: Structured paths with prerequisites for systematic learning
- **Progress Tracking**: Visual indicators (green=completed, gold=in-progress, gray=not started)
- **Mastery Tests**: Pre-quizzes and post-tests with 100% pass requirement
- **Smart Recommendations**: AI-powered content recommendations based on progress

### Assessment & Testing
- **Intro Skill Assessment**: Diagnostic test to evaluate initial competency
- **IQ Testing**: Timed tests with scoring and progress tracking
- **Standardized Tests**: SAT, ACT, LSAT preparation modules
- **Reading Comprehension**: Multiple questions per passage with timing
- **Spelling Bee**: Text-to-speech pronunciation with etymology

### User Experience
- **Responsive Design**: Mobile-friendly interface
- **Dark Mode**: System-wide dark theme support
- **Multiple Views**: Tree visualization, list view, and text-only mode
- **Mega Menu**: Quick access to top categories
- **Random Questions**: Sidebar for continuous practice
- **Career Guidance**: Career paths linked to skill requirements

### Administrative
- **Feedback System**: User feedback with admin response capability
- **Content Management**: Flag and manage learning content
- **User Analytics**: Track progress and performance metrics
- **Settings Panel**: Customize appearance and preferences

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Supabase account
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/skilltree2.git
cd skilltree2
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
Create a `.env.local` file with:
```env
REACT_APP_SUPABASE_URL=your_supabase_url
REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key
```

4. Start the development server:
```bash
npm start
```

The app will open at [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

```
skilltree2/
├── src/
│   ├── components/      # Reusable React components
│   ├── contexts/        # React context providers
│   ├── pages/          # Page components
│   ├── services/       # API and service integrations
│   ├── types/          # TypeScript definitions
│   └── utils/          # Utility functions
├── public/             # Static assets
├── CLAUDE.md          # AI assistant instructions
├── PROJECT_IMPROVEMENTS.md  # Feature roadmap
└── THEORETICAL_FOUNDATIONS.md  # Educational theory
```

## 🛠️ Available Scripts

- `npm start` - Run development server
- `npm run build` - Build for production
- `npm test` - Run test suite
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Auto-fix linting issues
- `npm run typecheck` - TypeScript type checking
- `npm run check-all` - Run all checks

## 🎨 Tech Stack

- **Frontend**: React 19, TypeScript 4.9
- **Styling**: Tailwind CSS
- **Data Visualization**: D3.js
- **Backend**: Supabase (PostgreSQL + Auth)
- **Routing**: React Router v7
- **UI Components**: Headless UI, Heroicons
- **State Management**: React Context API

## 📊 Database Schema

The application uses Supabase with the following key tables:
- `skill_tree_nodes` - Learning module hierarchy (5,700+ nodes)
- `questions` - Question bank with embedded options
- `user_progress` - Track user learning progress
- `user_ratings` - Competency ratings
- `starred_categories` - User bookmarks
- `feedback` - User feedback and bug reports

## 🎯 Key Features Implementation

### Tree Visualization
- Radial layout using D3.js
- Limited depth display for performance
- Synchronized with list view
- Touch and mouse navigation

### Learning System
- Pre-assessment before content
- Structured learning materials
- Mastery tests requiring 100% pass
- Progress persistence across sessions

### Authentication
- Email/password authentication
- Password reset functionality
- Protected routes for premium content
- Guest access with limitations

## 🚢 Deployment

### Vercel Deployment
```bash
npm run build
vercel --prod
```

### Environment Variables
Set these in your deployment platform:
- `REACT_APP_SUPABASE_URL`
- `REACT_APP_SUPABASE_ANON_KEY`

## 📈 Performance Optimizations

- Pagination for large datasets (1000 rows at a time)
- 5-minute cache for database queries
- Lazy loading of components
- Optimized D3.js rendering
- Code splitting for smaller bundles

## 🔐 Security

- Row Level Security (RLS) in Supabase
- Authenticated API access
- Input validation and sanitization
- Protected admin routes
- Secure password requirements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is proprietary software. All rights reserved.

## 👥 Team

- Development: [Your Name]
- Design: Green and gold nature-inspired theme
- Target Audience: K-12 students, lifelong learners

## 📮 Support

For issues and feature requests, please use the in-app feedback system or create an issue on GitHub.

## 🎮 Gamification

The platform uses game-like elements to increase engagement:
- Progress indicators and completion percentages
- Achievement system (coming soon)
- Skill ratings and competency levels
- Learning paths with prerequisites
- Visual progression through the skill tree

## 📚 Educational Philosophy

Based on research-backed learning principles:
- Mastery-based progression
- Spaced repetition
- Active recall through testing
- Visual learning with tree metaphor
- Personalized learning paths

See `THEORETICAL_FOUNDATIONS.md` for detailed educational theory.

## 🔄 Version History

- v1.0.0 - Initial release with all core features
- See `PROJECT_IMPROVEMENTS.md` for roadmap

---

Built with ❤️ for learners everywhere
# 🧠 NeuroQuest

An interactive knowledge learning platform that gamifies education across all domains of human knowledge. Master subjects from fundamental concepts to advanced topics through an engaging visual knowledge graph.

![NeuroQuest](https://img.shields.io/badge/version-0.5.0-blue)
![Next.js](https://img.shields.io/badge/Next.js-15.4.6-black)
![React](https://img.shields.io/badge/React-19.1.0-61dafb)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4.0-38B2AC)
![Supabase](https://img.shields.io/badge/Supabase-2.55.0-green)

## ✨ Features

### 🎮 Gamified Learning Experience
- **Visual Knowledge Graph**: Interactive node-based learning map with 100+ topics
- **Hierarchical Learning Paths**: Progress from foundations to mastery
- **Achievement System**: Earn points, levels, badges, and maintain learning streaks
- **Quiz Challenges**: Test your knowledge with interactive quizzes
- **Expandable Parent Nodes**: Drill down into subtopics (Calculus, Statistics, Algorithms, Languages)

### 👥 Social Features
- **Friend System**: Connect with fellow learners and track their progress
- **Study Groups**: Create or join groups for collaborative learning
- **Activity Feed**: Real-time updates on community achievements
- **Group Challenges**: Compete with your study group in knowledge challenges
- **Friend Suggestions**: Discover learners with similar interests
- **Private & Public Groups**: Control who can join your study sessions

### 📚 Comprehensive Knowledge Domains
- **Foundation**: Communication, Quantitative Reasoning, Practical Skills
- **Fundamentals**: Mathematics, Science, Digital Literacy
- **Specialized Domains**: 
  - Mathematics (Calculus, Statistics, Linear Algebra)
  - Computer Science (Algorithms, Data Structures)
  - World Languages (Spanish, French, German, Chinese, Japanese)
  - Sciences (Biology, Chemistry, Physics)
  - Practical Skills (Cooking, Money Management, Repairs)

### 🔄 Dynamic Features
- **Expandable Knowledge Nodes**: Click parent nodes to reveal detailed subtopics
- **Real-time Progress Tracking**: Visual progress bars and statistics
- **Prerequisite System**: Unlock advanced topics by mastering fundamentals
- **User Profiles**: Track achievements, neural level, and learning streaks
- **Leaderboard**: Compete with other learners
- **Learning Paths**: 7 curated paths for different learning goals
- **Course Content System**: Rich learning materials with sections, resources, and tips
- **Learning Modal**: Integrated content delivery with quiz challenges
- **Dark Mode Support**: Full theme support across the application

### 🏠 Landing Page
- **Modern Homepage**: Beautiful landing page for non-authenticated users
- **Feature Highlights**: Showcase platform capabilities
- **Call-to-Action**: Easy signup/signin flow
- **Responsive Design**: Mobile-first approach with Tailwind CSS

### 🛠️ Admin Interface
- **Dashboard**: Real-time statistics and quick actions
- **Question Management**: CRUD operations, inline editing, search and filter
- **Batch Upload**: Import questions via CSV/JSON files or web interface
- **Knowledge Nodes**: Manage nodes, prerequisites, and availability
- **Learning Paths**: Configure paths, manage nodes, and publication status
- **User Management**: View user profiles, progress, and activity
- **Settings Panel**: System configuration and maintenance tools

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Supabase account (free tier works)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jessicawestbrook/neuroquest.git
   cd neuroquest
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env.local` file in the root directory:
   ```env
   # Supabase Configuration
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
   
   # Email Service Configuration (Resend)
   RESEND_API_KEY=your_resend_api_key
   
   # Application Configuration
   NEXT_PUBLIC_APP_URL=http://localhost:3000
   
   # Optional: Error Tracking (Sentry)
   NEXT_PUBLIC_SENTRY_DSN=your_sentry_dsn_here
   NEXT_PUBLIC_SENTRY_ENVIRONMENT=development
   NEXT_PUBLIC_SENTRY_RELEASE=1.0.0
   
   # Optional: PWA Configuration
   NEXT_PUBLIC_PWA_ENABLED=true
   ```

4. **Set up the database**
   
   Run these SQL scripts in your Supabase SQL editor in order:
   
   ```sql
   -- Run each script in the Supabase SQL editor:
   scripts/create-social-tables.sql   # Creates all social feature tables (friends, groups, activity feed)
   
   -- Or run individual migration scripts:
   00-prepare-for-migration.sql      # Disables RLS for migration
   01-create-core-tables.sql          # Core tables
   02-create-dependent-tables.sql     # Dependent tables
   03-create-user-tables.sql          # User profile tables
   04-create-views-and-functions.sql  # Views and triggers
   ```
   
   **Important**: The `create-social-tables.sql` script creates all necessary tables for social features including:
   - Friends and friend requests tables
   - User profiles table
   - Study groups and members tables
   - Activity feed table
   - Friend suggestions function
   - All necessary RLS policies

5. **Migrate the data**
   ```bash
   npm run migrate:all
   ```
   
   This will populate:
   - 100+ knowledge nodes
   - 50+ prerequisite relationships
   - 7 learning paths
   - Quiz questions for various topics

6. **Re-enable security**
   ```sql
   -- Run in Supabase SQL editor:
   05-enable-security.sql
   ```

7. **Start the development server**
   ```bash
   npm run dev
   ```

   Open [http://localhost:3000](http://localhost:3000) to see the app.

8. **Access the admin interface**
   ```
   http://localhost:3000/admin
   ```

## 📖 Usage

### Navigation
- **Click nodes** to view details and start challenges
- **Click parent nodes** (with +/- icons) to expand/collapse subnodes
- **Complete prerequisites** to unlock new topics (locked nodes show 🔒)
- **Use the sidebar** to:
  - Search for specific topics
  - Filter by domain
  - Select learning paths
  - View your profile stats

### Learning Flow
1. Start with foundation topics (unlocked by default)
2. Complete quizzes to earn points and unlock prerequisites
3. Progress through fundamentals to specialized domains
4. Expand parent nodes to explore detailed subtopics
5. Achieve mastery by completing advanced topics

### Game Elements
- **Points**: Earn 25-300 points per completed topic
- **Neural Level**: Level up every 500 points
- **Memory Crystals**: Special rewards for achievements
- **Synaptic Streak**: Maintain daily learning habits
- **Achievements**: Unlock 8 different badges

## 🛠️ Tech Stack

- **Frontend Framework**: [Next.js 15](https://nextjs.org/) with App Router
- **UI Library**: [React 19](https://react.dev/)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Database**: [Supabase](https://supabase.com/) (PostgreSQL)
- **Styling**: CSS-in-JS with inline styles
- **Icons**: [Lucide React](https://lucide.dev/)
- **Authentication**: Supabase Auth (ready for integration)

## 📁 Project Structure

```
neuroquest/
├── src/
│   ├── app/              # Next.js app router pages
│   │   ├── page.tsx      # Main knowledge graph view
│   │   ├── admin/        # Admin dashboard
│   │   └── social/       # Social features dashboard
│   ├── components/       # React components
│   │   ├── Header.tsx    # Top navigation with stats
│   │   ├── Sidebar.tsx   # Domain filters and paths
│   │   ├── AuthModal.tsx # Login/signup modal
│   │   └── social/       # Social feature components
│   │       ├── FriendsPanel.tsx
│   │       ├── StudyGroupsPanel.tsx
│   │       └── ActivityFeed.tsx
│   ├── contexts/         # React contexts
│   ├── data/            # Static data files
│   ├── hooks/           # Custom React hooks
│   ├── services/        # API services (Supabase)
│   ├── types/           # TypeScript definitions
│   └── utils/           # Utility functions
├── scripts/             # Database setup and migrations
│   ├── 00-05*.sql      # Step-by-step schema setup
│   └── migrate-*.js    # Data migration scripts
├── public/              # Static assets
└── docs/               # Documentation
    ├── STEP_BY_STEP_SETUP.md    # Detailed setup guide
    └── SUPABASE_SETUP_GUIDE.md  # Database setup guide
```

## 🗄️ Database Schema

### Core Tables
- `knowledge_nodes` - All learning topics with hierarchy
- `node_prerequisites` - Prerequisite relationships
- `quiz_questions` - Questions for each node
- `learning_paths` - Curated learning sequences
- `learning_path_nodes` - Nodes in each path

### User Tables
- `user_profiles` - Extended user profiles with stats
- `user_progress` - Tracks completed nodes
- `achievements` - Available achievements
- `user_achievements` - Earned achievements

### Social Tables
- `friend_requests` - Pending friend connections
- `friends` - Established friendships
- `study_groups` - Collaborative learning groups
- `study_group_members` - Group membership
- `study_group_messages` - Group chat messages
- `study_group_challenges` - Group competitions
- `activity_feed` - User activity tracking

## 📝 Available Scripts

```bash
npm run dev                # Start development server
npm run build             # Build for production
npm run lint              # Run ESLint
npm run type-check        # Run TypeScript compiler
npm run start             # Start production server
npm run lint              # Run ESLint
npm run migrate:all       # Run all data migrations
npm run migrate:knowledge # Migrate knowledge nodes
npm run migrate:paths     # Migrate learning paths
npm run migrate:questions # Migrate quiz questions
```

## 🎨 Customization

### Adding New Knowledge Nodes
Edit `scripts/migrate-knowledge-graph.js` to add new topics:
```javascript
{
  id: 'your-topic-id',
  name: 'Your Topic Name',
  prereqs: ['prerequisite-id'],
  category: 'fundamentals',
  domain: 'your-domain',
  difficulty: 3,
  points: 150,
  level: 0,
  isParent: false
}
```

### Adding Quiz Questions

#### Method 1: Admin Interface
1. Navigate to `/admin/questions/new` to add individual questions
2. Use `/admin/upload` for batch uploading via CSV or JSON

#### Method 2: Batch Upload Script
```bash
# Generate sample files
node scripts/batch-load-questions.js --generate-sample

# Load from file
node scripts/batch-load-questions.js sample-questions.json
node scripts/batch-load-questions.js sample-questions.csv
```

#### Method 3: Direct Database Edit
Edit `scripts/migrate-questions.js` to add questions:
```javascript
'your-topic-id': [
  {
    question: "Your question?",
    options: ["Option 1", "Option 2", "Option 3", "Option 4"],
    correct: 0,
    explanation: "Explanation here"
  }
]
```

### Creating Learning Paths
Edit `scripts/migrate-learning-paths.js`:
```javascript
{
  name: 'Path Name',
  icon: 'IconName',
  description: 'Path description',
  nodes: ['node-1', 'node-2', 'node-3']
}
```

## 🚧 Roadmap

- [x] User authentication and profiles
- [x] Production deployment infrastructure
- [x] Push notifications system
- [x] Health monitoring and observability
- [x] Social features (friends, study groups)
- [ ] More quiz question types (multiple select, fill-in-blank)
- [ ] Progress certificates
- [ ] Mobile app version
- [ ] Content creator tools
- [ ] AI-powered learning recommendations
- [ ] Multiplayer real-time challenges

## 🏗️ Build Status

✅ **Production Ready**: Application builds successfully without errors  
✅ **TypeScript**: All type errors resolved  
✅ **ESLint**: Code quality standards enforced  
✅ **Environment**: Lazy initialization prevents build-time API key errors  

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t neuroquest .
docker run -p 3000:3000 --env-file .env.local neuroquest
```

### GitHub Actions CI/CD
The repository includes automated deployment workflows:
- **PR Checks**: Runs on pull requests (lint, type-check, tests)
- **Main Deploy**: Deploys to production on merge to main
- **Manual Deploy**: Trigger deployment manually from Actions tab

### Environment Variables for Production
Ensure these environment variables are set in your deployment platform:

**Required:**
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` 
- `SUPABASE_SERVICE_ROLE_KEY`
- `RESEND_API_KEY`
- `DATABASE_URL` (PostgreSQL connection string)

**Push Notifications:**
- `NEXT_PUBLIC_VAPID_PUBLIC_KEY`
- `VAPID_PRIVATE_KEY`
- `VAPID_SUBJECT`

**Optional:**
- `NEXT_PUBLIC_SENTRY_DSN` (Error tracking)
- `NEXT_PUBLIC_PWA_ENABLED` (Progressive Web App features)
- `OTEL_EXPORTER_OTLP_ENDPOINT` (OpenTelemetry endpoint)

### Build Commands
```bash
npm run build       # Creates optimized production build
npm run start       # Serves production build
npm run lint        # Validates code quality
npm run typecheck   # TypeScript type checking
npm test           # Run test suite
npm run prisma:generate  # Generate Prisma client
npm run prisma:migrate   # Run database migrations
```

## 📊 Recent Updates (v0.5.0)

### 👥 Social Features & Community (NEW)
- ✅ **Friend System**: Send/accept friend requests, manage connections
- ✅ **Study Groups**: Create, join, and manage collaborative learning groups
- ✅ **Activity Feed**: Track your and your friends' learning progress
- ✅ **Group Challenges**: Compete in knowledge challenges within groups
- ✅ **Social Dashboard**: Centralized hub for all social interactions
- ✅ **Privacy Controls**: Manage visibility of your activities
- ✅ **Join Codes**: Share private group access with unique codes
- ✅ **Member Management**: Role-based permissions for group admins

### 🚀 Production Deployment & Infrastructure (v0.4.0)
- ✅ **GitHub Actions CI/CD**: Automated deployment pipeline with build, test, and deploy stages
- ✅ **Docker Support**: Containerized application with multi-stage builds for optimized images
- ✅ **Health Monitoring**: Health check endpoints and readiness probes for production
- ✅ **Rate Limiting**: API rate limiting to prevent abuse and ensure fair usage
- ✅ **Push Notifications**: Web push notification system with VAPID keys
- ✅ **Observability Stack**: OpenTelemetry integration with Prometheus and Grafana
- ✅ **Database Migrations**: Prisma ORM for database schema management
- ✅ **Security Enhancements**: CSP headers, XSS protection, and secure cookies

### 🐛 Bug Fixes & Improvements (v0.3.1)
- ✅ **Onboarding Modal**: Fixed scrolling issues for welcome modal content visibility
- ✅ **Navigation Fix**: Resolved Next button functionality in onboarding flow
- ✅ **UI Polish**: Added proper z-index and positioning for interactive elements
- ✅ **Debug Logging**: Enhanced debugging capabilities for onboarding process

### 🔧 Build & Infrastructure (v0.3.0)
- ✅ **Production Build**: Fixed all TypeScript compilation errors
- ✅ **Environment Management**: Implemented lazy initialization for API clients
- ✅ **Code Quality**: Resolved 50+ ESLint warnings and errors
- ✅ **Type Safety**: Enhanced TypeScript definitions throughout
- ✅ **Error Handling**: Improved API error boundaries

### 🆕 New Features  
- 📧 **Email Verification**: Complete email verification system with Resend
- 🔐 **Authentication Flow**: Enhanced user registration and verification
- 📱 **PWA Support**: Progressive Web App capabilities with offline functionality
- 📊 **Analytics Integration**: User behavior tracking and performance monitoring
- 🎨 **Modern UI**: Improved components with better accessibility
- 🎯 **Onboarding System**: Interactive multi-step onboarding for new users

### 🏠 Homepage & Landing
- 🏠 **Landing Page**: Beautiful homepage for non-authenticated users
- 🎨 **Modern UI Components**: Redesigned header, sidebar, and layout
- 📚 **Course Content System**: Rich learning materials integrated with quiz system
- 🌙 **Dark Mode**: Full theme support with ThemeContext
- 📱 **Responsive Design**: Mobile-first approach with Tailwind CSS v3

### 🛠️ Developer Experience
- ✅ **Error-Free Build**: Production-ready compilation
- ✅ **Type Safety**: Comprehensive TypeScript coverage
- ✅ **Code Quality**: ESLint rules enforced consistently
- ✅ **Performance**: Optimized bundle size and load times
- ✅ **Testing**: Unit tests with Jest and React Testing Library

### 🔄 Tech Stack Updates
- **Next.js 15.4.6**: Latest App Router with enhanced performance
- **React 19**: Modern React features and concurrent rendering
- **TypeScript 5.0**: Enhanced type checking and inference
- **Sentry Integration**: Error tracking and performance monitoring
- **PWA Framework**: Service worker and offline capabilities

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Icons by [Lucide](https://lucide.dev/)
- Database by [Supabase](https://supabase.com/)
- Framework by [Next.js](https://nextjs.org/)
- UI inspiration from skill trees in RPG games

## 📧 Contact

Jessica Westbrook - [GitHub](https://github.com/jessicawestbrook)

Project Link: [https://github.com/jessicawestbrook/neuroquest](https://github.com/jessicawestbrook/neuroquest)

---

Built with ❤️ and 🧠 to make learning an adventure!
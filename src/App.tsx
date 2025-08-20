import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { ThemeProvider } from './contexts/ThemeContext'
import { SpellingBeeProvider } from './contexts/SpellingBeeContext'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import SkillTreePage from './pages/SkillTreePage'
import TextOnlySkillTreePage from './pages/TextOnlySkillTreePage'
import SimpleLearningPage from './pages/SimpleLearningPage'
import ProfilePage from './pages/ProfilePage'
import LoginPage from './pages/LoginPage'
import SignUpPage from './pages/SignUpPage'
import PasswordResetPage from './pages/PasswordResetPage'
import UpdatePasswordPage from './pages/UpdatePasswordPage'
import EmailVerificationPage from './pages/EmailVerificationPage'
import CategoryPage from './pages/CategoryPage'
import FeedbackPage from './pages/FeedbackPage'
import DiagnosticPage from './pages/DiagnosticPage'
import AdminPage from './pages/AdminPage'
import SettingsPage from './pages/SettingsPage'
import SearchPage from './pages/SearchPage'
import ContentManagementPage from './pages/ContentManagementPage'
import SpellingBeePage from './pages/SpellingBeePage'
import ReadingComprehensionPage from './pages/ReadingComprehensionPage'
import IntroAssessmentPage from './pages/IntroAssessmentPage'
import IQTestPage from './pages/IQTestPage'
import StandardizedTestsPage from './pages/StandardizedTestsPage'
import CareerAdvancementPage from './pages/CareerAdvancementPage'
import LearningPathsPage from './pages/LearningPathsPage'
import AdminSpellingBeePage from './pages/AdminSpellingBeePage'
import SpellingBeeSetupPage from './pages/SpellingBeeSetupPage'
import VocabularyTrainerPage from './pages/VocabularyTrainerPage'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <SpellingBeeProvider>
          <Router>
            <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignUpPage />} />
            <Route path="/password-reset" element={<PasswordResetPage />} />
            <Route path="/reset-password" element={<UpdatePasswordPage />} />
            <Route path="/verify-email" element={<EmailVerificationPage />} />
            <Route path="/" element={<Layout />}>
              <Route index element={<HomePage />} />
              <Route path="skill-tree" element={<SkillTreePage />} />
              <Route path="text-tree" element={<TextOnlySkillTreePage />} />
              <Route path="category/:categoryId" element={<CategoryPage />} />
              <Route
                path="learning/:contentId?"
                element={
                  <ProtectedRoute>
                    <SimpleLearningPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="profile"
                element={
                  <ProtectedRoute>
                    <ProfilePage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="feedback"
                element={
                  <ProtectedRoute>
                    <FeedbackPage />
                  </ProtectedRoute>
                }
              />
              <Route path="diagnostics" element={<DiagnosticPage />} />
              <Route path="settings" element={<SettingsPage />} />
              <Route path="search" element={<SearchPage />} />
              <Route path="spelling-bee" element={<SpellingBeePage />} />
              <Route path="spelling-bee-setup" element={<SpellingBeeSetupPage />} />
              <Route path="vocabulary-trainer" element={<VocabularyTrainerPage />} />
              <Route path="reading-comprehension" element={<ReadingComprehensionPage />} />
              <Route path="intro-assessment" element={<IntroAssessmentPage />} />
              <Route path="iq-test" element={<IQTestPage />} />
              <Route path="standardized-tests" element={<StandardizedTestsPage />} />
              <Route path="career-advancement" element={<CareerAdvancementPage />} />
              <Route path="learning-paths" element={<LearningPathsPage />} />
              <Route
                path="admin"
                element={
                  <ProtectedRoute>
                    <AdminPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="admin/spelling-bee"
                element={
                  <ProtectedRoute>
                    <AdminSpellingBeePage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="content-management"
                element={
                  <ProtectedRoute>
                    <ContentManagementPage />
                  </ProtectedRoute>
                }
              />
            </Route>
          </Routes>
        </Router>
        </SpellingBeeProvider>
      </AuthProvider>
    </ThemeProvider>
  )
}

export default App
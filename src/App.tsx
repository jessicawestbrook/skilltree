import React, { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { initializeChromeErrorHandler } from './utils/chromeErrorHandler'
import { HelmetProvider } from 'react-helmet-async'
import { AuthProvider } from './contexts/AuthContext'
import { ThemeProvider } from './contexts/ThemeContext'
import { SpellingProvider } from './contexts/SpellingContext'
import { NotificationProvider } from './contexts/NotificationContext'
import { AchievementProvider } from './contexts/AchievementContext'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
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
import ReadingComprehensionPage from './pages/ReadingComprehensionPage'
import IntroAssessmentPage from './pages/IntroAssessmentPage'
import IQTestPage from './pages/IQTestPage'
import VisualMatrixDemoPage from './pages/VisualMatrixDemoPage'
import VisualMatrixTestPage from './pages/VisualMatrixTestPage'
import StandardizedTestsPage from './pages/StandardizedTestsPage'
import LearningPathsPage from './pages/LearningPathsPage'
import AdminSpellingPage from './pages/AdminSpellingPage'
import SpellingSetupPage from './pages/SpellingSetupPage'
import SpellingVocabularyPage from './pages/SpellingVocabularyPage'
import LanguageTrainerPage from './pages/LanguageTrainerPage'
import StudyListsPage from './pages/StudyListsPage'
import TestPage from './pages/TestPage'
import NotificationsPage from './pages/NotificationsPage'
import { NotificationSettingsPage } from './pages/NotificationSettingsPage'
import AboutPage from './pages/AboutPage'
import ReviewFlashcardsPage from './pages/ReviewFlashcardsPage'
import StudyListReviewPage from './pages/StudyListReviewPage'
import ProtectedRoute from './components/ProtectedRoute'
import AdminRoute from './components/AdminRoute'

function App() {
  useEffect(() => {
    // Initialize Chrome error handler to suppress extension errors
    initializeChromeErrorHandler()
  }, [])

  return (
    <HelmetProvider>
      <ThemeProvider>
      <AuthProvider>
        <NotificationProvider>
          <AchievementProvider>
            <SpellingProvider>
            <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
              <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route path="/signup" element={<SignUpPage />} />
                <Route path="/password-reset" element={<PasswordResetPage />} />
                <Route path="/reset-password" element={<UpdatePasswordPage />} />
                <Route path="/verify-email" element={<EmailVerificationPage />} />
                <Route path="/" element={<Layout />}>
              <Route index element={<HomePage />} />
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
              <Route path="notification-settings" element={<NotificationSettingsPage />} />
              <Route path="search" element={<SearchPage />} />
              <Route path="about" element={<AboutPage />} />
              <Route
                path="notifications"
                element={
                  <ProtectedRoute>
                    <NotificationsPage />
                  </ProtectedRoute>
                }
              />
              <Route path="spelling-bee" element={<SpellingVocabularyPage />} />
              <Route path="spelling-bee-setup" element={<SpellingSetupPage />} />
              <Route path="vocabulary-trainer" element={<SpellingVocabularyPage />} />
              <Route path="spelling-vocabulary" element={<SpellingVocabularyPage />} />
              <Route path="language-trainer" element={<LanguageTrainerPage />} />
              <Route
                path="study-lists"
                element={
                  <ProtectedRoute>
                    <StudyListsPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="study-lists/:listSlug"
                element={
                  <ProtectedRoute>
                    <StudyListsPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="study-list-review"
                element={
                  <ProtectedRoute>
                    <StudyListReviewPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="review"
                element={
                  <ProtectedRoute>
                    <ReviewFlashcardsPage />
                  </ProtectedRoute>
                }
              />
              <Route path="reading-comprehension" element={<ReadingComprehensionPage />} />
              <Route path="intro-assessment" element={<IntroAssessmentPage />} />
              <Route path="iq-test" element={<IQTestPage />} />
              <Route path="visual-matrix-demo" element={<VisualMatrixDemoPage />} />
              <Route path="visual-matrix-test" element={<VisualMatrixTestPage />} />
              <Route path="standardized-tests" element={<StandardizedTestsPage />} />
              <Route path="test/:testId" element={<TestPage />} />
              <Route path="learning-paths" element={<LearningPathsPage />} />
              <Route
                path="admin"
                element={
                  <AdminRoute>
                    <AdminPage />
                  </AdminRoute>
                }
              />
              <Route
                path="admin/spelling-bee"
                element={
                  <AdminRoute>
                    <AdminSpellingPage />
                  </AdminRoute>
                }
              />
              <Route
                path="content-management"
                element={
                  <AdminRoute>
                    <ContentManagementPage />
                  </AdminRoute>
                }
              />
              {/* Hierarchical category paths */}
              <Route path=":segment1/:segment2?/:segment3?/:segment4?" element={<CategoryPage />} />
              </Route>
              </Routes>
            </Router>
            </SpellingProvider>
          </AchievementProvider>
        </NotificationProvider>
      </AuthProvider>
    </ThemeProvider>
    </HelmetProvider>
  )
}

export default App
import React, { useState, useEffect } from 'react'
import { ChevronLeftIcon, ChevronRightIcon, BookOpenIcon, ClockIcon, TrophyIcon, CheckCircleIcon, PlayIcon, PauseIcon, SpeakerWaveIcon } from '@heroicons/react/24/outline'
import { CheckCircleIcon as CheckCircleSolidIcon } from '@heroicons/react/24/solid'
import { extractTextForSpeech, estimateReadingTime } from '../utils/textExtractor'

interface LearningContentViewerProps {
  htmlContent: string
  nodeId: string
  nodeName: string
  onComplete?: () => void
  onProgress?: (progress: number) => void
}

const LearningContentViewer: React.FC<LearningContentViewerProps> = ({
  htmlContent,
  nodeId,
  nodeName,
  onComplete,
  onProgress
}) => {
  const [currentSection, setCurrentSection] = useState(0)
  const [completedSections, setCompletedSections] = useState<Set<number>>(new Set())
  const [isPlaying, setIsPlaying] = useState(false)
  const [readingTime, setReadingTime] = useState(0)
  const [sections, setSections] = useState<{ title: string; content: string; id: string }[]>([])
  const [showTableOfContents, setShowTableOfContents] = useState(false)

  // Parse HTML content into sections
  useEffect(() => {
    const parser = new DOMParser()
    const doc = parser.parseFromString(htmlContent, 'text/html')
    
    // Extract sections based on h2 tags
    const sectionElements = doc.querySelectorAll('section')
    const parsedSections: { title: string; content: string; id: string }[] = []
    
    if (sectionElements.length > 0) {
      sectionElements.forEach((section, index) => {
        const heading = section.querySelector('h2')
        const title = heading?.textContent || `Section ${index + 1}`
        const id = section.id || `section-${index}`
        
        // Clone section and add styling classes
        const sectionClone = section.cloneNode(true) as HTMLElement
        sectionClone.className = 'learning-section-content'
        
        parsedSections.push({
          title,
          content: sectionClone.outerHTML,
          id
        })
      })
    } else {
      // Fallback: treat entire content as one section
      parsedSections.push({
        title: nodeName,
        content: htmlContent,
        id: 'main-content'
      })
    }
    
    setSections(parsedSections)
    
    // Calculate estimated reading time
    setReadingTime(estimateReadingTime(htmlContent))
  }, [htmlContent, nodeName])

  // Mark section as completed
  const markSectionComplete = (sectionIndex: number) => {
    const newCompleted = new Set(completedSections)
    newCompleted.add(sectionIndex)
    setCompletedSections(newCompleted)
    
    // Report progress
    const progress = (newCompleted.size / sections.length) * 100
    onProgress?.(progress)
    
    // Save progress to localStorage
    localStorage.setItem(`learning-progress-${nodeId}`, JSON.stringify({
      completedSections: Array.from(newCompleted),
      currentSection: sectionIndex,
      timestamp: new Date().toISOString()
    }))
    
    // Check if all sections completed
    if (newCompleted.size === sections.length) {
      onComplete?.()
    }
  }

  // Load saved progress
  useEffect(() => {
    const savedProgress = localStorage.getItem(`learning-progress-${nodeId}`)
    if (savedProgress) {
      try {
        const { completedSections: saved, currentSection: savedSection } = JSON.parse(savedProgress)
        setCompletedSections(new Set(saved))
        setCurrentSection(savedSection || 0)
      } catch (error) {
        console.error('Error loading progress:', error)
      }
    }
  }, [nodeId])

  // Navigation handlers
  const goToSection = (index: number) => {
    setCurrentSection(index)
    setShowTableOfContents(false)
  }

  const goToNextSection = () => {
    if (currentSection < sections.length - 1) {
      markSectionComplete(currentSection)
      setCurrentSection(currentSection + 1)
    }
  }

  const goToPreviousSection = () => {
    if (currentSection > 0) {
      setCurrentSection(currentSection - 1)
    }
  }

  // Text-to-speech functionality
  const togglePlayPause = () => {
    if (isPlaying) {
      window.speechSynthesis.cancel()
      setIsPlaying(false)
    } else {
      const currentSectionData = sections[currentSection]
      if (!currentSectionData) return
      
      // Extract clean text using utility function
      const textToRead = extractTextForSpeech(
        currentSectionData.content,
        currentSectionData.title
      )
      
      if (textToRead) {
        const utterance = new SpeechSynthesisUtterance(textToRead)
        utterance.rate = 0.9 // Slightly slower for better comprehension
        utterance.pitch = 1.0
        utterance.volume = 1.0
        
        // Add event handlers
        utterance.onend = () => {
          setIsPlaying(false)
          // Optionally move to next section
          if (currentSection < sections.length - 1) {
            // You could auto-advance here if desired
            // goToNextSection()
          }
        }
        
        utterance.onerror = (event) => {
          console.error('Speech synthesis error:', event)
          setIsPlaying(false)
        }
        
        utterance.onpause = () => setIsPlaying(false)
        utterance.onresume = () => setIsPlaying(true)
        
        // Start speaking
        window.speechSynthesis.cancel() // Cancel any existing speech
        window.speechSynthesis.speak(utterance)
        setIsPlaying(true)
      } else {
        console.warn('No text content to read')
      }
    }
  }

  if (sections.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const currentSectionData = sections[currentSection]
  const progressPercentage = (completedSections.size / sections.length) * 100

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-50 to-secondary-50 dark:from-primary-900/20 dark:to-secondary-900/20 rounded-2xl p-6 mb-8">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-3xl font-bold text-neutral-800 dark:text-neutral-100">
            {nodeName}
          </h1>
          <div className="flex items-center gap-4">
            <button
              onClick={togglePlayPause}
              className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-neutral-800 rounded-lg shadow-sm hover:shadow-md transition-all"
              title={isPlaying ? 'Pause reading' : 'Read aloud'}
            >
              {isPlaying ? (
                <>
                  <PauseIcon className="h-5 w-5 text-primary-600" />
                  <span className="text-sm font-medium">Pause</span>
                  <div className="ml-2">
                    <div className="flex space-x-1">
                      <div className="w-1 h-3 bg-primary-600 animate-pulse" />
                      <div className="w-1 h-3 bg-primary-600 animate-pulse" style={{ animationDelay: '0.2s' }} />
                      <div className="w-1 h-3 bg-primary-600 animate-pulse" style={{ animationDelay: '0.4s' }} />
                    </div>
                  </div>
                </>
              ) : (
                <>
                  <SpeakerWaveIcon className="h-5 w-5 text-primary-600" />
                  <span className="text-sm font-medium">Read Aloud</span>
                </>
              )}
            </button>
            <div className="flex items-center gap-2 text-neutral-600 dark:text-neutral-400">
              <ClockIcon className="h-5 w-5" />
              <span className="text-sm">{readingTime} min read</span>
            </div>
          </div>
        </div>
        
        {/* Progress Bar */}
        <div className="relative">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-neutral-600 dark:text-neutral-400">
              Progress: {completedSections.size} of {sections.length} sections
            </span>
            <span className="text-sm font-medium text-primary-600">
              {Math.round(progressPercentage)}%
            </span>
          </div>
          <div className="h-3 bg-neutral-200 dark:bg-neutral-700 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-primary-500 to-primary-600 transition-all duration-500 ease-out"
              style={{ width: `${progressPercentage}%` }}
            />
          </div>
        </div>
      </div>

      {/* Table of Contents Toggle */}
      <div className="mb-6">
        <button
          onClick={() => setShowTableOfContents(!showTableOfContents)}
          className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-neutral-800 rounded-lg shadow-sm hover:shadow-md transition-all"
        >
          <BookOpenIcon className="h-5 w-5 text-primary-600" />
          <span className="font-medium">Table of Contents</span>
          <ChevronRightIcon className={`h-4 w-4 transition-transform ${showTableOfContents ? 'rotate-90' : ''}`} />
        </button>
        
        {/* Table of Contents */}
        {showTableOfContents && (
          <div className="mt-4 bg-white dark:bg-neutral-800 rounded-lg shadow-lg p-4">
            <div className="space-y-2">
              {sections.map((section, index) => (
                <button
                  key={section.id}
                  onClick={() => goToSection(index)}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-all flex items-center gap-3
                    ${currentSection === index 
                      ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400' 
                      : 'hover:bg-neutral-100 dark:hover:bg-neutral-700'
                    }`}
                >
                  {completedSections.has(index) ? (
                    <CheckCircleSolidIcon className="h-5 w-5 text-green-500 flex-shrink-0" />
                  ) : currentSection === index ? (
                    <div className="h-5 w-5 rounded-full border-2 border-primary-500 flex-shrink-0" />
                  ) : (
                    <div className="h-5 w-5 rounded-full border-2 border-neutral-300 dark:border-neutral-600 flex-shrink-0" />
                  )}
                  <span className="font-medium">{section.title}</span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Main Content Area */}
      <div className="bg-white dark:bg-neutral-800 rounded-2xl shadow-xl overflow-hidden">
        {/* Section Header */}
        <div className="bg-gradient-to-r from-primary-100 to-secondary-100 dark:from-primary-900/20 dark:to-secondary-900/20 px-8 py-4 border-b border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-neutral-800 dark:text-neutral-100 flex items-center gap-2">
              {completedSections.has(currentSection) && (
                <CheckCircleSolidIcon className="h-6 w-6 text-green-500" />
              )}
              {currentSectionData.title}
            </h2>
            <span className="text-sm text-neutral-600 dark:text-neutral-400">
              Section {currentSection + 1} of {sections.length}
            </span>
          </div>
        </div>

        {/* Content */}
        <div className="p-8">
          <div 
            className="learning-content-styled prose prose-lg dark:prose-invert max-w-none"
            dangerouslySetInnerHTML={{ __html: currentSectionData.content }}
          />
        </div>

        {/* Navigation Footer */}
        <div className="px-8 py-6 bg-neutral-50 dark:bg-neutral-900/50 border-t border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center justify-between">
            <button
              onClick={goToPreviousSection}
              disabled={currentSection === 0}
              className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all
                ${currentSection === 0 
                  ? 'bg-neutral-200 dark:bg-neutral-700 text-neutral-400 dark:text-neutral-500 cursor-not-allowed' 
                  : 'bg-white dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 hover:shadow-md'
                }`}
            >
              <ChevronLeftIcon className="h-5 w-5" />
              Previous
            </button>

            {/* Section Dots */}
            <div className="flex gap-2">
              {sections.map((_, index) => (
                <button
                  key={index}
                  onClick={() => goToSection(index)}
                  className={`h-2 w-2 rounded-full transition-all
                    ${currentSection === index 
                      ? 'w-8 bg-primary-600' 
                      : completedSections.has(index)
                        ? 'bg-green-500'
                        : 'bg-neutral-300 dark:bg-neutral-600 hover:bg-neutral-400'
                    }`}
                  title={`Go to ${sections[index].title}`}
                />
              ))}
            </div>

            {currentSection === sections.length - 1 ? (
              <button
                onClick={() => {
                  markSectionComplete(currentSection)
                  onComplete?.()
                }}
                className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg font-medium hover:shadow-lg transition-all"
              >
                <TrophyIcon className="h-5 w-5" />
                Complete Module
              </button>
            ) : (
              <button
                onClick={goToNextSection}
                className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-lg font-medium hover:shadow-lg transition-all"
              >
                Next
                <ChevronRightIcon className="h-5 w-5" />
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
        <button className="flex items-center justify-center gap-2 px-4 py-3 bg-white dark:bg-neutral-800 rounded-lg shadow-sm hover:shadow-md transition-all">
          <BookOpenIcon className="h-5 w-5 text-primary-600" />
          <span className="font-medium">Take Notes</span>
        </button>
        <button className="flex items-center justify-center gap-2 px-4 py-3 bg-white dark:bg-neutral-800 rounded-lg shadow-sm hover:shadow-md transition-all">
          <CheckCircleIcon className="h-5 w-5 text-primary-600" />
          <span className="font-medium">Practice Quiz</span>
        </button>
        <button className="flex items-center justify-center gap-2 px-4 py-3 bg-white dark:bg-neutral-800 rounded-lg shadow-sm hover:shadow-md transition-all">
          <TrophyIcon className="h-5 w-5 text-primary-600" />
          <span className="font-medium">View Achievements</span>
        </button>
      </div>
    </div>
  )
}

export default LearningContentViewer
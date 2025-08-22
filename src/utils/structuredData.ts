export const createCourseStructuredData = (category: any) => {
  const baseUrl = 'https://skilltree.app'
  
  return {
    "@context": "https://schema.org",
    "@type": "Course",
    "name": category.name,
    "description": category.description || `Learn ${category.name} with interactive lessons and assessments`,
    "provider": {
      "@type": "EducationalOrganization",
      "name": "SkillTree",
      "url": baseUrl
    },
    "url": `${baseUrl}/category/${category.id}`,
    "courseCode": category.id,
    "educationalLevel": category.level === 1 ? "Beginner" : category.level === 2 ? "Intermediate" : "Advanced",
    "teaches": category.name,
    "audience": {
      "@type": "EducationalAudience",
      "educationalRole": "student"
    },
    "availableLanguage": "en",
    "isAccessibleForFree": true,
    "learningResourceType": "Course",
    "interactivityType": "active",
    "educationalUse": "instruction"
  }
}

export const createLearningPathStructuredData = (categories: any[]) => {
  return {
    "@context": "https://schema.org",
    "@type": "LearningResource",
    "name": "SkillTree Learning Paths",
    "description": "Comprehensive learning paths with gamified skill trees covering mathematics, science, languages, and more",
    "url": "https://skilltree.app/learning-paths",
    "provider": {
      "@type": "EducationalOrganization",
      "name": "SkillTree",
      "url": "https://skilltree.app"
    },
    "hasPart": categories.map(category => ({
      "@type": "Course",
      "name": category.name,
      "url": `https://skilltree.app/category/${category.id}`,
      "description": category.description
    })),
    "isAccessibleForFree": true,
    "learningResourceType": "LearningPath",
    "interactivityType": "active",
    "educationalUse": "instruction"
  }
}

export const createTestStructuredData = (testName: string, testType: 'standardized' | 'iq' | 'assessment') => {
  const baseTypes = {
    standardized: "ExaminationTest",
    iq: "Assessment", 
    assessment: "EducationalTest"
  }
  
  return {
    "@context": "https://schema.org",
    "@type": baseTypes[testType],
    "name": testName,
    "description": `Practice ${testName} test with detailed explanations and scoring`,
    "url": `https://skilltree.app/test/${testName.toLowerCase().replace(/\s+/g, '-')}`,
    "provider": {
      "@type": "EducationalOrganization",
      "name": "SkillTree",
      "url": "https://skilltree.app"
    },
    "isAccessibleForFree": true,
    "educationalUse": "assessment",
    "interactivityType": "active"
  }
}

export const createBreadcrumbStructuredData = (breadcrumbs: Array<{name: string, url: string}>) => {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": breadcrumbs.map((item, index) => ({
      "@type": "ListItem",
      "position": index + 1,
      "name": item.name,
      "item": item.url
    }))
  }
}

export const createQuestionStructuredData = (question: any) => {
  return {
    "@context": "https://schema.org",
    "@type": "Question",
    "name": question.question_text,
    "text": question.question_text,
    "answerCount": question.options?.length || 0,
    "acceptedAnswer": {
      "@type": "Answer",
      "text": question.explanation || "Detailed explanation provided after answering"
    },
    "educationalLevel": question.difficulty || "intermediate",
    "learningResourceType": "Question"
  }
}

export const createOrganizationStructuredData = () => {
  return {
    "@context": "https://schema.org",
    "@type": "EducationalOrganization",
    "name": "SkillTree",
    "url": "https://skilltree.app",
    "logo": "https://skilltree.app/logo512.png",
    "description": "Interactive learning platform with gamified skill trees for homeschooling, test preparation, and lifelong learning",
    "sameAs": [
      "https://twitter.com/skilltreeapp",
      "https://github.com/skilltree"
    ],
    "contactPoint": {
      "@type": "ContactPoint",
      "contactType": "customer service",
      "url": "https://skilltree.app/feedback"
    },
    "offers": {
      "@type": "Offer",
      "category": "Education",
      "availability": "https://schema.org/InStock",
      "price": "0",
      "priceCurrency": "USD"
    },
    "areaServed": "Worldwide",
    "availableLanguage": ["en"],
    "foundingDate": "2025",
    "knowsAbout": [
      "Mathematics",
      "Science", 
      "Language Learning",
      "Test Preparation",
      "Educational Assessment",
      "Skill Development"
    ]
  }
}
import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "../contexts/AuthContext";
import { OnboardingProvider } from "../contexts/OnboardingContext";
import { ThemeProvider } from "../contexts/ThemeContext";
import ErrorBoundary from "../components/ErrorBoundary";
import PWAProvider from "../components/PWAProvider";
import Analytics from "../components/seo/Analytics";
import { ApiDebugger } from "../components/ApiDebugger";
import { generateWebsiteStructuredData, generateOrganizationStructuredData } from "../utils/seo/structuredData";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'),
  title: "SkillTree - Grow Your Skills. Master Your Future.",
  description: "A nature-themed homeschooling and supplemental learning platform that helps students grow their skills through interactive learning paths",
  keywords: "homeschool, supplemental learning, education, skills, learning paths, interactive, gamified learning, K-12",
  authors: [{ name: "SkillTree Team" }],
  creator: "SkillTree",
  publisher: "SkillTree",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  icons: {
    icon: '/favicon.svg',
    apple: '/apple-touch-icon.png',
    shortcut: '/favicon.ico',
  },
  manifest: '/manifest.json',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'SkillTree',
  },
  openGraph: {
    type: 'website',
    siteName: 'SkillTree',
    title: 'SkillTree - Grow Your Skills. Master Your Future.',
    description: 'A nature-themed homeschooling and supplemental learning platform that helps students grow their skills through interactive learning paths',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'SkillTree - Grow Your Skills. Master Your Future.',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'SkillTree - Grow Your Skills. Master Your Future.',
    description: 'A nature-themed homeschooling and supplemental learning platform that helps students grow their skills through interactive learning paths',
    images: ['/og-image.png'],
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const websiteStructuredData = generateWebsiteStructuredData();
  const organizationStructuredData = generateOrganizationStructuredData();

  return (
    <html lang="en">
      <head>
        {/* Structured Data */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(websiteStructuredData, null, 2)
          }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(organizationStructuredData, null, 2)
          }}
        />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        suppressHydrationWarning
      >
        <ErrorBoundary>
          <PWAProvider>
            <AuthProvider>
              <OnboardingProvider>
                <ThemeProvider>
                  <Analytics />
                  {children}
                  {process.env.NODE_ENV === 'development' && <ApiDebugger />}
                </ThemeProvider>
              </OnboardingProvider>
            </AuthProvider>
          </PWAProvider>
        </ErrorBoundary>
      </body>
    </html>
  );
}

import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "../contexts/AuthContext";
import { OnboardingProvider } from "../contexts/OnboardingContext";
import { ThemeProvider } from "../contexts/ThemeContext";
import ErrorBoundary from "../components/ErrorBoundary";
import PWAProvider from "../components/PWAProvider";
import Analytics from "../components/seo/Analytics";
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
  title: "NeuroQuest - Master All Human Knowledge",
  description: "An interactive learning platform to master knowledge across all domains with offline capability",
  keywords: "learning, education, knowledge, PWA, offline, study, courses, interactive",
  authors: [{ name: "NeuroQuest Team" }],
  creator: "NeuroQuest",
  publisher: "NeuroQuest",
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
    title: 'NeuroQuest',
  },
  openGraph: {
    type: 'website',
    siteName: 'NeuroQuest',
    title: 'NeuroQuest - Master All Human Knowledge',
    description: 'An interactive learning platform to master knowledge across all domains with offline capability',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'NeuroQuest - Master All Human Knowledge',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'NeuroQuest - Master All Human Knowledge',
    description: 'An interactive learning platform to master knowledge across all domains with offline capability',
    images: ['/og-image.png'],
  },
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 1,
    userScalable: false,
  },
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
                </ThemeProvider>
              </OnboardingProvider>
            </AuthProvider>
          </PWAProvider>
        </ErrorBoundary>
      </body>
    </html>
  );
}

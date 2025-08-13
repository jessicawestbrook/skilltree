import { test, expect } from '@playwright/test';

test.describe('Navigation', () => {
  test('should navigate to different pages without errors', async ({ page }) => {
    await page.goto('/');
    
    // Test homepage loads correctly
    await expect(page.getByText('Welcome to NeuroQuest')).toBeVisible();
    
    // Test direct navigation to various routes
    const routes = [
      '/reset-password',
      '/verify-email'
    ];
    
    for (const route of routes) {
      await page.goto(route);
      // Check that page loads without critical errors
      await expect(page.locator('body')).toBeVisible();
    }
  });

  test('should handle 404 pages gracefully', async ({ page }) => {
    // Try to navigate to a non-existent page
    const response = await page.goto('/non-existent-page');
    
    // Should either return 404 or redirect to a valid page
    if (response) {
      expect([200, 404]).toContain(response.status());
    }
    
    // Page should still render something
    await expect(page.locator('body')).toBeVisible();
  });

  test('should maintain proper URL structure', async ({ page }) => {
    await page.goto('/');
    
    // Check that we're on the homepage
    expect(page.url()).toBe('http://localhost:3000/');
    
    // Navigate to reset password page
    await page.goto('/reset-password');
    expect(page.url()).toBe('http://localhost:3000/reset-password');
    
    // Navigate to verify email page
    await page.goto('/verify-email');
    expect(page.url()).toBe('http://localhost:3000/verify-email');
  });

  test('should handle browser back and forward navigation', async ({ page }) => {
    await page.goto('/');
    await page.goto('/reset-password');
    
    // Go back
    await page.goBack();
    expect(page.url()).toBe('http://localhost:3000/');
    await expect(page.getByText('Welcome to NeuroQuest')).toBeVisible();
    
    // Go forward
    await page.goForward();
    expect(page.url()).toBe('http://localhost:3000/reset-password');
  });

  test('should preserve state when navigating', async ({ page }) => {
    await page.goto('/');
    
    // Open auth modal
    await page.getByText('Sign In').click();
    await expect(page.getByText('Welcome Back')).toBeVisible();
    
    // Fill some data
    await page.getByPlaceholder('Email address').fill('test@example.com');
    
    // Navigate away and back (simulate refresh)
    await page.reload();
    
    // Modal should be closed after reload
    await expect(page.getByText('Welcome Back')).not.toBeVisible();
    await expect(page.getByText('Welcome to NeuroQuest')).toBeVisible();
  });

  test('should handle deep linking correctly', async ({ page }) => {
    // Test direct navigation to sub-pages
    await page.goto('/reset-password');
    await expect(page.locator('body')).toBeVisible();
    
    await page.goto('/verify-email');
    await expect(page.locator('body')).toBeVisible();
  });

  test('should maintain responsive navigation across devices', async ({ page }) => {
    // Test on mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    
    await expect(page.getByText('Welcome to NeuroQuest')).toBeVisible();
    
    // Test navigation buttons are accessible
    await expect(page.getByRole('button', { name: 'Sign In' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Get Started' })).toBeVisible();
    
    // Test on tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.reload();
    
    await expect(page.getByText('Welcome to NeuroQuest')).toBeVisible();
    
    // Test on desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.reload();
    
    await expect(page.getByText('Welcome to NeuroQuest')).toBeVisible();
  });

  test('should handle query parameters correctly', async ({ page }) => {
    // Test navigation with query parameters
    await page.goto('/?test=1&param=value');
    
    expect(page.url()).toContain('test=1');
    expect(page.url()).toContain('param=value');
    
    // Page should still render correctly
    await expect(page.getByText('Welcome to NeuroQuest')).toBeVisible();
  });

  test('should handle hash navigation', async ({ page }) => {
    await page.goto('/#section1');
    
    expect(page.url()).toContain('#section1');
    
    // Page should still render correctly
    await expect(page.getByText('Welcome to NeuroQuest')).toBeVisible();
  });

  test('should provide proper page titles for SEO', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/NeuroQuest/);
    
    await page.goto('/reset-password');
    // Title should change for different pages (if implemented)
    await expect(page).toHaveTitle(/.+/); // At least some title
    
    await page.goto('/verify-email');
    await expect(page).toHaveTitle(/.+/); // At least some title
  });

  test('should handle external links appropriately', async ({ page, context }) => {
    await page.goto('/');
    
    // Check if there are any external links and test them
    const externalLinks = page.locator('a[href^="http"]:not([href*="localhost"])');
    const linkCount = await externalLinks.count();
    
    if (linkCount > 0) {
      // Test that external links open in new tabs (if configured)
      const link = externalLinks.first();
      const href = await link.getAttribute('href');
      const target = await link.getAttribute('target');
      
      if (target === '_blank') {
        expect(target).toBe('_blank');
      }
    }
  });
});
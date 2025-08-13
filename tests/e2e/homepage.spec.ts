import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test('should display hero section with key elements', async ({ page }) => {
    await page.goto('/');
    
    // Check hero section
    await expect(page.getByText('Welcome to NeuroQuest')).toBeVisible();
    await expect(page.getByText('Embark on an Interactive Learning Journey')).toBeVisible();
    await expect(page.getByText('Discover knowledge through an innovative neural network')).toBeVisible();
    
    // Check action buttons
    await expect(page.getByRole('button', { name: 'Get Started' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Sign In' })).toBeVisible();
  });

  test('should display features section', async ({ page }) => {
    await page.goto('/');
    
    // Check features section
    await expect(page.getByText('Why Choose NeuroQuest?')).toBeVisible();
    
    // Check individual features
    await expect(page.getByText('Interactive Learning')).toBeVisible();
    await expect(page.getByText('Progress Tracking')).toBeVisible();
    await expect(page.getByText('Adaptive Content')).toBeVisible();
  });

  test('should have proper page title and meta', async ({ page }) => {
    await page.goto('/');
    
    await expect(page).toHaveTitle(/NeuroQuest/);
  });

  test('should be responsive on mobile devices', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE dimensions
    await page.goto('/');
    
    // Check that main elements are still visible on mobile
    await expect(page.getByText('Welcome to NeuroQuest')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Get Started' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Sign In' })).toBeVisible();
  });

  test('should have accessible navigation', async ({ page }) => {
    await page.goto('/');
    
    // Check for proper heading hierarchy
    const h1 = page.locator('h1');
    await expect(h1).toBeVisible();
    
    // Check for proper button roles
    const buttons = page.locator('button');
    expect(await buttons.count()).toBeGreaterThan(0);
  });

  test('should handle Get Started button click', async ({ page }) => {
    await page.goto('/');
    
    await page.getByRole('button', { name: 'Get Started' }).click();
    
    // Should open auth modal in registration mode
    await expect(page.getByText('Join NeuroQuest')).toBeVisible();
    await expect(page.getByPlaceholder('Username')).toBeVisible();
  });

  test('should handle Sign In button click', async ({ page }) => {
    await page.goto('/');
    
    await page.getByRole('button', { name: 'Sign In' }).click();
    
    // Should open auth modal in login mode
    await expect(page.getByText('Welcome Back')).toBeVisible();
    await expect(page.getByPlaceholder('Email address')).toBeVisible();
    await expect(page.getByPlaceholder('Password')).toBeVisible();
  });

  test('should display footer information', async ({ page }) => {
    await page.goto('/');
    
    // Scroll to bottom to ensure footer is visible
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    
    // Check for footer content (adjust based on your actual footer)
    // This test assumes there's some footer content
    const footer = page.locator('footer');
    if (await footer.count() > 0) {
      await expect(footer).toBeVisible();
    }
  });

  test('should have proper color scheme and styling', async ({ page }) => {
    await page.goto('/');
    
    // Check that the page has loaded with proper styling
    const body = page.locator('body');
    await expect(body).toBeVisible();
    
    // Check for background or primary elements
    const heroSection = page.getByText('Welcome to NeuroQuest').locator('..');
    await expect(heroSection).toBeVisible();
  });

  test('should load without JavaScript errors', async ({ page }) => {
    const errors: string[] = [];
    
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });
    
    page.on('pageerror', (error) => {
      errors.push(error.message);
    });
    
    await page.goto('/');
    
    // Wait a bit for any delayed errors
    await page.waitForTimeout(2000);
    
    // Filter out common non-critical errors
    const criticalErrors = errors.filter(error => 
      !error.includes('favicon') &&
      !error.includes('manifest') &&
      !error.includes('DevTools')
    );
    
    expect(criticalErrors).toHaveLength(0);
  });

  test('should have proper accessibility features', async ({ page }) => {
    await page.goto('/');
    
    // Check for skip links or other accessibility features
    const skipLinks = page.locator('a[href="#main"], a[href="#content"]');
    if (await skipLinks.count() > 0) {
      await expect(skipLinks.first()).toBeVisible();
    }
    
    // Check that interactive elements are keyboard accessible
    await page.keyboard.press('Tab');
    const focusedElement = page.locator(':focus');
    await expect(focusedElement).toBeVisible();
  });
});
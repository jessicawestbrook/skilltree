import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display homepage for non-authenticated users', async ({ page }) => {
    await expect(page.getByText('Welcome to NeuroQuest')).toBeVisible();
    await expect(page.getByText('Sign In')).toBeVisible();
    await expect(page.getByText('Get Started')).toBeVisible();
  });

  test('should open auth modal when clicking Sign In', async ({ page }) => {
    await page.getByText('Sign In').click();
    
    await expect(page.getByText('Welcome Back')).toBeVisible();
    await expect(page.getByPlaceholder('Email address')).toBeVisible();
    await expect(page.getByPlaceholder('Password')).toBeVisible();
  });

  test('should switch between login and registration forms', async ({ page }) => {
    await page.getByText('Sign In').click();
    
    // Initially on login form
    await expect(page.getByText('Welcome Back')).toBeVisible();
    
    // Switch to registration
    await page.getByText('Sign up').click();
    await expect(page.getByText('Join NeuroQuest')).toBeVisible();
    await expect(page.getByPlaceholder('Username')).toBeVisible();
    
    // Switch back to login
    await page.getByText('Sign in').click();
    await expect(page.getByText('Welcome Back')).toBeVisible();
  });

  test('should show forgot password form', async ({ page }) => {
    await page.getByText('Sign In').click();
    await page.getByText('Forgot password?').click();
    
    await expect(page.getByText('Reset Password')).toBeVisible();
    await expect(page.getByText('Enter your email address')).toBeVisible();
    await expect(page.getByRole('button', { name: /send reset email/i })).toBeVisible();
  });

  test('should validate required fields in login form', async ({ page }) => {
    await page.getByText('Sign In').click();
    
    // Try to submit empty form
    await page.getByRole('button', { name: /sign in/i }).click();
    
    // Check for HTML5 validation (required fields)
    const emailInput = page.getByPlaceholder('Email address');
    const passwordInput = page.getByPlaceholder('Password');
    
    await expect(emailInput).toHaveAttribute('required');
    await expect(passwordInput).toHaveAttribute('required');
  });

  test('should validate required fields in registration form', async ({ page }) => {
    await page.getByText('Sign In').click();
    await page.getByText('Sign up').click();
    
    // Try to submit empty form
    await page.getByRole('button', { name: /create account/i }).click();
    
    // Check for HTML5 validation (required fields)
    const emailInput = page.getByPlaceholder('Email address');
    const usernameInput = page.getByPlaceholder('Username');
    const passwordInput = page.getByPlaceholder('Password');
    
    await expect(emailInput).toHaveAttribute('required');
    await expect(usernameInput).toHaveAttribute('required');
    await expect(passwordInput).toHaveAttribute('required');
  });

  test('should close modal when clicking close button', async ({ page }) => {
    await page.getByText('Sign In').click();
    
    // Modal should be visible
    await expect(page.getByText('Welcome Back')).toBeVisible();
    
    // Close modal
    await page.locator('button').filter({ hasText: '×' }).click();
    
    // Modal should be closed
    await expect(page.getByText('Welcome Back')).not.toBeVisible();
  });

  test('should toggle password visibility', async ({ page }) => {
    await page.getByText('Sign In').click();
    
    const passwordInput = page.getByPlaceholder('Password');
    const toggleButton = page.locator('button[type="button"]').filter({ has: page.locator('svg') }).first();
    
    // Initially password type
    await expect(passwordInput).toHaveAttribute('type', 'password');
    
    // Click toggle to show password
    await toggleButton.click();
    await expect(passwordInput).toHaveAttribute('type', 'text');
    
    // Click toggle to hide password
    await toggleButton.click();
    await expect(passwordInput).toHaveAttribute('type', 'password');
  });

  test('should handle form input correctly', async ({ page }) => {
    await page.getByText('Sign In').click();
    
    const emailInput = page.getByPlaceholder('Email address');
    const passwordInput = page.getByPlaceholder('Password');
    
    await emailInput.fill('test@example.com');
    await passwordInput.fill('password123');
    
    await expect(emailInput).toHaveValue('test@example.com');
    await expect(passwordInput).toHaveValue('password123');
  });

  test('should clear form when switching modes', async ({ page }) => {
    await page.getByText('Sign In').click();
    
    // Fill login form
    await page.getByPlaceholder('Email address').fill('test@example.com');
    await page.getByPlaceholder('Password').fill('password123');
    
    // Switch to registration
    await page.getByText('Sign up').click();
    
    // Check that form is cleared
    await expect(page.getByPlaceholder('Email address')).toHaveValue('');
    await expect(page.getByPlaceholder('Password')).toHaveValue('');
    await expect(page.getByPlaceholder('Username')).toHaveValue('');
  });
});
import React from 'react';
import { render, screen, act } from '@testing-library/react';
import { ThemeProvider, useTheme } from '../../contexts/ThemeContext';

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
};
global.localStorage = localStorageMock as any;

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Test component that uses theme context
const TestComponent = () => {
  const { theme, setTheme, resolvedTheme } = useTheme();
  
  return (
    <div>
      <div data-testid="current-theme">{theme}</div>
      <div data-testid="resolved-theme">{resolvedTheme}</div>
      <button 
        data-testid="toggle-theme" 
        onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
      >
        Toggle Theme
      </button>
      <button 
        data-testid="set-light" 
        onClick={() => setTheme('light')}
      >
        Set Light
      </button>
      <button 
        data-testid="set-dark" 
        onClick={() => setTheme('dark')}
      >
        Set Dark
      </button>
      <button 
        data-testid="set-system" 
        onClick={() => setTheme('system')}
      >
        Set System
      </button>
    </div>
  );
};

describe('ThemeContext', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorageMock.getItem.mockReturnValue(null);
    
    // Reset document classes
    document.documentElement.classList.remove('dark');
  });

  describe('ThemeProvider', () => {
    it('should provide default theme context', () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      expect(screen.getByTestId('current-theme')).toHaveTextContent('system');
      expect(screen.getByTestId('resolved-theme')).toHaveTextContent('light');
    });

    it('should load theme from localStorage', () => {
      localStorageMock.getItem.mockReturnValue('dark');

      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      expect(screen.getByTestId('current-theme')).toHaveTextContent('dark');
      expect(screen.getByTestId('resolved-theme')).toHaveTextContent('dark');
    });

    it('should handle invalid theme from localStorage', () => {
      localStorageMock.getItem.mockReturnValue('invalid-theme');

      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      expect(screen.getByTestId('current-theme')).toHaveTextContent('system');
    });
  });

  describe('theme switching', () => {
    it('should switch to light theme', () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      act(() => {
        screen.getByTestId('set-light').click();
      });

      expect(screen.getByTestId('current-theme')).toHaveTextContent('light');
      expect(screen.getByTestId('resolved-theme')).toHaveTextContent('light');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('theme', 'light');
      expect(document.documentElement.classList.contains('dark')).toBe(false);
    });

    it('should switch to dark theme', () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      act(() => {
        screen.getByTestId('set-dark').click();
      });

      expect(screen.getByTestId('current-theme')).toHaveTextContent('dark');
      expect(screen.getByTestId('resolved-theme')).toHaveTextContent('dark');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('theme', 'dark');
      expect(document.documentElement.classList.contains('dark')).toBe(true);
    });

    it('should switch to system theme', () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      act(() => {
        screen.getByTestId('set-system').click();
      });

      expect(screen.getByTestId('current-theme')).toHaveTextContent('system');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('theme', 'system');
    });

    it('should toggle between themes', () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      // Start with system, toggle should go to light
      act(() => {
        screen.getByTestId('toggle-theme').click();
      });
      expect(screen.getByTestId('current-theme')).toHaveTextContent('light');

      // Toggle to dark
      act(() => {
        screen.getByTestId('toggle-theme').click();
      });
      expect(screen.getByTestId('current-theme')).toHaveTextContent('dark');

      // Toggle back to light
      act(() => {
        screen.getByTestId('toggle-theme').click();
      });
      expect(screen.getByTestId('current-theme')).toHaveTextContent('light');
    });
  });

  describe('system theme detection', () => {
    it('should detect system dark theme preference', () => {
      // Mock system preference for dark theme
      window.matchMedia = jest.fn().mockImplementation(query => ({
        matches: query === '(prefers-color-scheme: dark)',
        media: query,
        onchange: null,
        addListener: jest.fn(),
        removeListener: jest.fn(),
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
      }));

      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      act(() => {
        screen.getByTestId('set-system').click();
      });

      expect(screen.getByTestId('current-theme')).toHaveTextContent('system');
      expect(screen.getByTestId('resolved-theme')).toHaveTextContent('dark');
      expect(document.documentElement.classList.contains('dark')).toBe(true);
    });

    it('should detect system light theme preference', () => {
      // Mock system preference for light theme
      window.matchMedia = jest.fn().mockImplementation(query => ({
        matches: query !== '(prefers-color-scheme: dark)',
        media: query,
        onchange: null,
        addListener: jest.fn(),
        removeListener: jest.fn(),
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
      }));

      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      act(() => {
        screen.getByTestId('set-system').click();
      });

      expect(screen.getByTestId('current-theme')).toHaveTextContent('system');
      expect(screen.getByTestId('resolved-theme')).toHaveTextContent('light');
      expect(document.documentElement.classList.contains('dark')).toBe(false);
    });
  });

  describe('error handling', () => {
    it('should handle localStorage errors gracefully', () => {
      const originalSetItem = localStorageMock.setItem;
      localStorageMock.setItem.mockImplementation(() => {
        throw new Error('Storage error');
      });

      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      expect(() => {
        act(() => {
          screen.getByTestId('set-dark').click();
        });
      }).not.toThrow();
      
      // Restore the original mock
      localStorageMock.setItem = originalSetItem;
    });

    it('should handle matchMedia not available', () => {
      delete (window as any).matchMedia;

      expect(() => {
        render(
          <ThemeProvider>
            <TestComponent />
          </ThemeProvider>
        );
      }).not.toThrow();
    });
  });

  describe('useTheme hook', () => {
    it('should throw error when used outside provider', () => {
      // Suppress console.error for this test
      const originalError = console.error;
      console.error = jest.fn();

      expect(() => {
        render(<TestComponent />);
      }).toThrow('useTheme must be used within a ThemeProvider');

      console.error = originalError;
    });
  });

  describe('theme persistence', () => {
    it('should persist theme changes to localStorage', () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      act(() => {
        screen.getByTestId('set-dark').click();
      });

      expect(localStorageMock.setItem).toHaveBeenCalledWith('theme', 'dark');

      act(() => {
        screen.getByTestId('set-light').click();
      });

      expect(localStorageMock.setItem).toHaveBeenCalledWith('theme', 'light');
    });

    it('should apply theme to document element', () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      // Test dark theme application
      act(() => {
        screen.getByTestId('set-dark').click();
      });
      expect(document.documentElement.classList.contains('dark')).toBe(true);

      // Test light theme application
      act(() => {
        screen.getByTestId('set-light').click();
      });
      expect(document.documentElement.classList.contains('dark')).toBe(false);
    });
  });
});
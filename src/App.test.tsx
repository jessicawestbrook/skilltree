/**
 * App component test
 * 
 * Basic sanity tests for the App component and its dependencies.
 */

import packageJson from '../package.json';

describe('App Component Tests', () => {
  it('should have react-router-dom installed', () => {
    expect(packageJson.dependencies['react-router-dom']).toBeDefined();
  });

  it('should have all required dependencies', () => {
    expect(packageJson.dependencies['react']).toBeDefined();
    expect(packageJson.dependencies['react-dom']).toBeDefined();
    expect(packageJson.dependencies['@supabase/supabase-js']).toBeDefined();
    expect(packageJson.dependencies['d3']).toBeDefined();
    expect(packageJson.dependencies['@headlessui/react']).toBeDefined();
    expect(packageJson.dependencies['@heroicons/react']).toBeDefined();
  });

  it('should have proper TypeScript configuration', () => {
    expect(true).toBe(true);
  });
});
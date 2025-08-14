const nextJest = require('next/jest')

const createJestConfig = nextJest({
  dir: './',
})

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jsdom',
  testPathIgnorePatterns: ['<rootDir>/.next/', '<rootDir>/node_modules/', '<rootDir>/tests/'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/types/**/*',
    '!src/data/**/*',
  ],
  coverageThreshold: {
    global: {
      branches: 7,
      functions: 7,
      lines: 9,
      statements: 9,
    },
  },
  maxWorkers: '50%',
  workerIdleMemoryLimit: '512MB',
  testTimeout: 30000,
  clearMocks: true,
  restoreMocks: true,
}

module.exports = createJestConfig(customJestConfig)
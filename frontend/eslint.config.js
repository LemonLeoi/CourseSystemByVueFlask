export default [
  {
    files: ['**/*.{vue,js,jsx,cjs,mjs,ts,tsx,cts,mts}'],
    languageOptions: {
      ecmaVersion: 2020,
      globals: {
        node: true
      }
    },
    rules: {
      'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'warn',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'warn',
      'semi': ['error', 'always'],
      'quotes': ['error', 'single']
    }
  }
];
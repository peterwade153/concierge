import parser from "@typescript-eslint/parser";
import reactPlugin from "eslint-plugin-react";
import reactHooksPlugin from "eslint-plugin-react-hooks";
import tsEslintPlugin from "@typescript-eslint/eslint-plugin";
import globals from "globals";

export default [
  {
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      parser,
      parserOptions: {
        ecmaVersion: 2020,
        sourceType: "module",
        ecmaFeatures: { jsx: true },
      },
      globals: {
        ...globals.browser,
        React: "readonly",
      },
    },
    plugins: {
      react: reactPlugin,
      "react-hooks": reactHooksPlugin,
      "@typescript-eslint": tsEslintPlugin,
    },
    rules: {
      // React
      "react/react-in-jsx-scope": "off",
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",

      // TypeScript-adjacent (mirrors the recommended rulesets without extending them)
      "@typescript-eslint/no-unused-vars": "error",
      "no-undef": "error",
      "no-const-assign": "off",
      "no-dupe-args": "off",
      "no-dupe-class-members": "off",
      "no-dupe-keys": "off",
      "no-func-assign": "off",
      "no-import-assign": "off",
      "no-redeclare": "off",
      "no-setter-return": "off",
      "no-this-before-super": "off",
      "no-var": "error",
      "prefer-const": "error",
      "prefer-rest-params": "error",
      "prefer-spread": "error",

      // Project style
      "@typescript-eslint/no-explicit-any": "warn",
    },
  },
];
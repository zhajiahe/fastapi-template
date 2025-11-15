import type { Config } from "tailwindcss";
import typography from '@tailwindcss/typography';

const config: Config = {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx,js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#3B82F6",
          foreground: "#FFFFFF",
        },
        secondary: {
          DEFAULT: "#6B7280",
          foreground: "#FFFFFF",
        },
      },
    },
  },
  plugins: [
    typography,
  ],
};

export default config;

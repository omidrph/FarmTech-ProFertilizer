/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Vazirmatn', 'Samim', 'Sahel', 'system-ui', 'sans-serif'],
        'vazir': ['Vazirmatn', 'sans-serif'],
        'samim': ['Samim', 'sans-serif'],
        'sahel': ['Sahel', 'sans-serif'],
        'yekan': ['Yekan', 'sans-serif'],
        'neda': ['Mj Neda', 'sans-serif'],
        'tehran': ['Mj Tehran', 'sans-serif'],
      },
      fontWeight: {
        'normal': '400',
        'medium': '500',
        'semibold': '600',
        'bold': '700',
        'black': '900',
      }
    },
  },
  plugins: [],
}
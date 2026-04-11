/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './themes/brownbaglunch/layouts/**/*.html',
    './layouts/**/*.html',
    './content/**/*.md',
  ],
  theme: {
    extend: {
      colors: {
        terracotta: '#e07b39',
        cream: '#fdf6ee',
        'warm-brown': '#3d2b1f',
        'warm-border': '#f0e4d0',
        'warm-light': '#fff8f0',
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
}

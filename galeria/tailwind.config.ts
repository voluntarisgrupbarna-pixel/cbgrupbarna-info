import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        club: {
          red: '#E4002B',        // --barna-red  · Vermell Clot
          'red-dark': '#A4001F', // --red-700    · pressed state
          'red-light': '#C30024',// --red-600    · hover state
          black: '#121212',      // --barna-black · brand ink
          'gray-1': '#1E1E1E',   // --ink-800    · raised surface on black
          'gray-2': '#2B2B2B',   // --ink-700    · hairlines on black
          cream: '#F2EFE9',      // --bone       · warm paper surface
        },
      },
      fontFamily: {
        display: ['Anton', 'sans-serif'],              // primary display — uppercase protagonist
        heading: ['Archivo Black', 'sans-serif'],      // heavy blocky alt display
        body: ['Archivo', 'sans-serif'],               // functional text + UI
        mono: ['Barlow Condensed', 'sans-serif'],      // scoreboard, labels, tags
      },
    },
  },
  plugins: [],
}
export default config

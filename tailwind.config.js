export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        radio: {
          green: '#00B94F',
          greenBright: '#00E060',
          greenDeep: '#007A33',
          yellow: '#FFDF00',
          blue: '#0033A0',
          red: '#E30000',
          gold: '#FFD700',
          dark: '#04120A',
          card: '#0A1F12',
          border: '#14432A',
        }
      },
      fontFamily: {
        display: ['Oswald', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
      },
      animation: {
        pulse2: 'pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        wave: 'wave 1.2s ease-in-out infinite',
      },
      keyframes: {
        wave: {
          '0%, 100%': { transform: 'scaleY(0.5)' },
          '50%': { transform: 'scaleY(1.5)' },
        }
      }
    },
  },
  plugins: [],
}

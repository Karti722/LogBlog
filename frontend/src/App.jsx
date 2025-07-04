import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="text-center">
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="h-24 p-6 transition-all duration-300 hover:drop-shadow-[0_0_2em_#646cffaa] inline-block" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="h-24 p-6 transition-all duration-300 hover:drop-shadow-[0_0_2em_#61dafbaa] animate-spin-slow inline-block" alt="React logo" />
        </a>
      </div>
      <div className="bg-blue-4000 text-black">
        Hello Tailwind!
      </div>
      <div className="p-8">
        <button 
          className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg transition-colors duration-200"
          onClick={() => setCount((count) => count + 1)}
        >
          count is {count}
        </button>
        <p className="mt-4 text-gray-600">
          Edit <code className="bg-gray-100 px-2 py-1 rounded text-sm font-mono">src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="text-gray-500">
        Click on the Vite and React logos to learn more
      </p>
    </div>
  )
}

export default App

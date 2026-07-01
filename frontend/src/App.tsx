import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4">
          <h1 className="text-3xl font-bold text-gray-900">ReleaseRank</h1>
          <p className="text-gray-600 mt-2">Compare audio files for YouTube and Spotify success</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 p-4">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Upload Audio Files</h2>
            <p className="text-gray-600">Placeholder for audio uploader component</p>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
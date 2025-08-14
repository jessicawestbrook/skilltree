export default function Loading() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-forest-50 via-cream-100 to-sky-50 flex items-center justify-center">
      <div className="text-center">
        <div className="relative inline-flex">
          <div className="w-24 h-24 bg-forest-200 rounded-full animate-ping"></div>
          <div 
            className="w-24 h-24 bg-forest-300 rounded-full animate-ping absolute top-0 left-0"
            style={{ animationDelay: '0.2s' }}
          ></div>
          <div 
            className="w-24 h-24 bg-forest-400 rounded-full animate-ping absolute top-0 left-0"
            style={{ animationDelay: '0.4s' }}
          ></div>
          <div className="absolute top-0 left-0 w-24 h-24 flex items-center justify-center">
            <span className="text-5xl">🌳</span>
          </div>
        </div>
        <h2 className="mt-8 text-2xl font-semibold text-gray-800">Growing Your Skills...</h2>
        <p className="mt-2 text-gray-600">Preparing your learning environment</p>
      </div>
    </div>
  );
}
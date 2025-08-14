export default function AdminLoading() {
  return (
    <div className="flex items-center justify-center min-h-[400px]">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-forest-600"></div>
        <p className="mt-4 text-gray-600">Loading admin panel...</p>
      </div>
    </div>
  );
}
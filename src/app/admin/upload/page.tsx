import QuestionBatchUpload from '@/components/QuestionBatchUpload';

export default function UploadPage() {
  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Batch Upload</h1>
        <p className="text-gray-600 mt-2">Upload multiple questions at once using CSV or JSON files</p>
      </div>
      <QuestionBatchUpload />
    </div>
  );
}
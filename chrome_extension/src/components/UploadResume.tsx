import React, { useState } from 'react';
import DescriptionIcon from '@mui/icons-material/Description';

function UploadResume() {
  const [resume, setResume] = useState<File | null>(null);
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setResume(e.target.files[0]);
    }
  };

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    setSuccess(false);
    if (!resume || !email) {
      setError('Please provide both your email and resume file.');
      return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append('resume', resume);
    formData.append('email', email);

    try {
      const response = await fetch('/upload-resume', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed.');
      }
      setSuccess(true);
      setResume(null);
      setEmail('');
    } catch (err) {
      setError('An error occurred while uploading. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center space-y-6 pt-12">
      <DescriptionIcon className="w-64 h-64 text-gray-400" />
      <div className="text-center space-y-2">
        <h1 className="text-xl font-semibold text-gray-900">
          Upload your resume.
        </h1>
        <p className="text-gray-600">
          By uploading your resume, we can tailor your results to your work history.
        </p>
      </div>
      <form onSubmit={handleSubmit} className="w-full max-w-md space-y-4">
        <div>
          <label className="block text-gray-700">Email</label>
          <input
            type="email"
            value={email}
            onChange={handleEmailChange}
            placeholder="you@example.com"
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>
        <div>
          <label className="block text-gray-700">Resume</label>
          <input
            type="file"
            onChange={handleFileChange}
            className="mt-1 block w-full text-gray-700"
            accept=".pdf,.doc,.docx"
            required
          />
        </div>
        {error && <p className="text-red-500">{error}</p>}
        {success && <p className="text-green-500">Resume uploaded successfully!</p>}
        <button
          type="submit"
          className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
          disabled={loading}
        >
          {loading ? 'Uploading...' : 'Upload Resume'}
        </button>
      </form>
    </div>
  );
}

export default UploadResume;

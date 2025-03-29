import { Send } from '@mui/icons-material';
import LinkIcon from '@mui/icons-material/Link';
import { Button } from '@mui/material';
import { useState } from 'react';



function UploadJobLink() {
    const [inputValue, setInputValue] = useState('');
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        console.log('Submitted:', inputValue);
        setInputValue('');
    };

    return (
        <div className="flex flex-col items-center justify-center space-y-6 pt-12">
          <LinkIcon className="w-64 h-64 text-gray-400" />
          <div className="text-center space-y-2">
            <h1 className="text-xl font-semibold text-gray-900">
              Upload a Job Link
            </h1>
            <p className="text-gray-600">
              By upload a job link, we will scrape the job descriptions and craft personalized interview guidance.
            </p>
          </div>

          <div className="w-full max-w-md">
                <form onSubmit={handleSubmit} className="flex gap-2">
                <div className="flex-1 relative">
                    <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                    placeholder="Input Job posting URL..."
                    />
                </div>
                <Button
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg"
                    endIcon={<Send />}
                >
                    <span>Upload</span>
                </Button>
                </form>
            </div>
        </div>
    );
}

export default UploadJobLink;

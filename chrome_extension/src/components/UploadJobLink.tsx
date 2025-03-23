import LinkIcon from '@mui/icons-material/Link';

function UploadJobLink() {
    return (
        <div className="flex flex-col items-center justify-center space-y-6 pt-12">
          <LinkIcon className="w-64 h-64 text-gray-400" />
          <div className="text-center space-y-2">
            <h1 className="text-xl font-semibold text-gray-900">
              Upload a Job Link
            </h1>
            <p className="text-gray-600">
              By upload a job link, we will scape the job descriptions and craft personalized interview guidance.
            </p>
          </div>
        </div>
    );
}

export default UploadJobLink;

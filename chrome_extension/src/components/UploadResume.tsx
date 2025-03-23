import DescriptionIcon from '@mui/icons-material/Description';

function UploadResume() {
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
        </div>
    );
}

export default UploadResume;

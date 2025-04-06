import { Button } from "@mui/material";
import AddIcon from '@mui/icons-material/Add';
import ContentPasteSearchIcon from '@mui/icons-material/ContentPasteSearch';
import { useRootContext } from "../context/RootContext";

function Overview() {

  const userInfo = useRootContext();

  return (
    <div className="min-h-screen bg-gray-50 p-6 w-full">
      <div className="flex flex-col items-center justify-center space-y-6 pt-12">
        {/* Icon and books illustration */}
        <ContentPasteSearchIcon className="w-64 h-64 text-gray-400" />

        {/* Text content */}
        <div className="text-center space-y-2">
          <h1 className="text-xl font-semibold text-gray-900">
            Welcome to JobHunter
          </h1>
          <p className="text-gray-600">
            Get started by going to your Job Sheet, uploading your resume, or uploading a job link.
          </p>
        </div>

        {/* Button that links to job spreadsheet */}
        <div className="flex flex-col items-start gap-2">
        {userInfo &&
          <>
            <a href={`https://docs.google.com/spreadsheets/d/${userInfo.excel_id}/edit?gid=0#gid=0`} 
            target="_blank"
            
            >
                <Button 
                    variant="outlined" 
                    className="flex items-center gap-2 px-6 py-3 bg-gray-200 text-gray-600 rounded-md hover:bg-gray-300 transition-colors" 
                    startIcon={<AddIcon className="w-5 h-5" />}
                >
                    <span>Go to my Job Sheet</span>
                </Button>
            </a>
            <span className="flex text-sm text-gray-500 italic">
                This will create a new Job Sheet if you haven't logged in before.
            </span>
          </> 
        }
        </div>
      </div>
    </div>
  );
}

export default Overview;

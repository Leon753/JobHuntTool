import { useState } from 'react';
import FormatListBulletedIcon from '@mui/icons-material/FormatListBulleted';
import DescriptionIcon from '@mui/icons-material/Description';
import LinkIcon from '@mui/icons-material/Link';
import Overview from './Overview';
import UploadResume from './UploadResume';
import UploadJobLink from './UploadJobLink';

function App() {
  const [activeTab, setActiveTab] = useState('overview');

  const tabs = [
    { id: 'overview', label: 'Overview', icon: FormatListBulletedIcon },
    { id: 'upload_resume', label: 'Upload Resume', icon: DescriptionIcon },
    { id: 'upload_job_link', label: 'Job Link', icon: LinkIcon },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'overview':
        return <Overview />;
      case 'upload_resume':
        return <UploadResume />;
      case 'upload_job_link':
        return <UploadJobLink />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 w-full relative">
      {/* Tab Navigation */}
      <div className="flex border-b">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex-1 flex items-center justify-center gap-2 py-4 px-4 transition-colors ${
                activeTab === tab.id
                  ? 'text-blue-600 border-b-2 border-blue-600 bg-white'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span className="text-sm font-medium">{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Content Area */}
      <div className="p-6">
        {renderContent()}
      </div>
    </div>
  );
}

export default App;

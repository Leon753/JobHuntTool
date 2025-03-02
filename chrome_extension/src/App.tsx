import MainFrame from './components/MainFrame'
import "./App.css";

function App() {
  
  return (
    <div className="App">
      <h1 className="flex flex-center grow w-max text-center text-xl font-bold mt-10 mx-auto">Welcome to Job Hunter</h1>
      <div className="py-8">
         <MainFrame />
      </div>
    </div>
  );
}

export default App;

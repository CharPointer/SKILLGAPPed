import NavBar from "./NavBar.jsx";
import ShowPlot from "./ShowPlot.jsx";
import UploadFile from "./UploadFile.jsx";
import React,{useEffect} from 'react';
import YourFiles from './YourFiles.jsx';
function App() {
  useEffect(()=>{
    document.title="skillGAPped";
  },[]);

  return(
    <>
      <div className="App-background">
        <NavBar/>
        <YourFiles/>
        <div>
          <ShowPlot/>
          <div className="UltraCoolButtons">
            <UploadFile/>
          </div>
        </div>
      </div>
    </>

  );
  }

export default App

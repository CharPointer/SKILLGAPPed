import NavBar from "./NavBar.jsx";
import ShowPlot from "./ShowPlot.jsx";
import UploadFile from "./UploadFile.jsx";
import React,{useEffect, useState} from 'react';
import YourFiles from './YourFiles.jsx';

function App() {

  const [htmlContent, setHtmlContent] = useState("");

  useEffect(()=>{
    document.title="skillGAPped";
  },[]);

  return(
    <>
      <div className="App-background">
        <NavBar/>
       <YourFiles setHtmlContent={setHtmlContent} />
        <div>
          <ShowPlot htmlContent={htmlContent} />
          <div className="UltraCoolButtons">
            <UploadFile/>
          </div>
        </div>
      </div>
    </>

  );
  }

export default App

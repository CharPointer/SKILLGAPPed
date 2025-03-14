import NavBar from "./NavBar.jsx";
import ShowPlot from "./ShowPlot.jsx";
import UploadFile from "./UploadFile.jsx";
import React,{useEffect, useState} from 'react';
import YourFiles from './YourFiles.jsx';

function App() {

  const [HtmlContent, SetHtmlContent] = useState("");

  useEffect(()=>{
    document.title="skillGAPped";
  },[]);


  useEffect(()=>{
    document.title="skillGAPped";
  },[]);
  return(
    <>
      <div className="App-background">
        <NavBar/>
       <YourFiles SetHtmlContent={SetHtmlContent} />
        <div>
          <ShowPlot HtmlContent={HtmlContent} />
          <div className="UltraCoolButtons">
            <UploadFile/>
          </div>
        </div>
      </div>
    </>

  );
  }

export default App

import NavBar from "./NavBar.jsx";
import ShowPlot from "./ShowPlot.jsx";
import UploadFile from "./UploadFile.jsx";
import React,{useEffect} from 'react';

function App() {
  useEffect(()=>{
    document.title="skillGAPped";
  },[]);

  return(
    <div className="App-background">
          <NavBar/>
          <ShowPlot/>
          <div className="UltraCoolButtons">
            <UploadFile/>
          </div>
    </div>
  );
  }

export default App

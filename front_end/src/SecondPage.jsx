import NavBar from "./NavBar.jsx";
import ShowPlot from "./ShowPlot.jsx";
import UploadFile from "./UploadFile.jsx";
import GeneratePlot from "./GeneratePlot.jsx"
import React,{useEffect} from 'react';
import { useNavigate } from "react-router-dom";


const MainPage = () => {
    const navigate = useNavigate();

    useEffect(()=>{
      document.title="skillGAPped";
    },[]);
  
    return(
      <div className="App-background">
            <NavBar/>
            <ShowPlot/>
            <div className="UltraCoolButtons">
              <UploadFile/>
              <GeneratePlot/>
            </div>
      </div>
    );
    }
  
  export default MainPage;
  
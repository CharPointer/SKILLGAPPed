import React, { useState, useEffect } from "react";
import ShowPlot from "./ShowPlot.jsx";

function YourFiles() {
    const [files, setFiles] = useState([]); 
    const [htmlContent, setHtmlContent]=useState("");
    async function fetchData() {
        try {
            const res = await (await fetch('http://localhost:3000/getFilesNames')).json();
            let data = res.Files;
            setFiles(prevFiles => Array.from(new Set([...prevFiles, ...data]))); 
        } catch (error) {
            console.log("Failed to get file names from API");
        }
    }

    async function GiveMEMYGRAAAAAPH(name) {
        try {
            const res = await fetch('http://localhost:3000/getHTMLFile');
    
            if (!res.ok) {
                throw new Error(`Server responded with status: ${res.status}`);
            }
    
            const html = await res.text(); 
            setHtmlContent(html);

            ShowPlot(htmlContent);
        } 
        catch (error) {
            console.error("Failed to fetch HTML file:", error);
        }

    }
    

    useEffect(() => {
        fetchData(); 
    }, []);

    return (
        <div className="YourFiles">
            <h1>Your Files</h1>
            <hr />
            <div className="YourFiles-Container">
                <div className="YourFiles-Buttons">
                    {files.length > 0 ? (
                        files.map(name => (
                            <button key={name} className="GetFileNames-btn" onClick={()=>GiveMEMYGRAAAAAPH(name)}>{name}</button>
                        ))
                    ) : (
                        <p>Loading files...</p>
                    )}
                </div>
            </div>
            <ShowPlot htmlContent={htmlContent} />
        </div>
    );
}

export default YourFiles;

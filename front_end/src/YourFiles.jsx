import React, { useState, useEffect } from "react";
import ShowPlot from "./ShowPlot.jsx";

function YourFiles({ setHtmlContent }) {

    const [files, setFiles] = useState([]); 

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
            const data=
            {
                "FileName": name, // example1.html is REQUIRED file to be fetched from BACKEND to CLIENT
                "Location": "" //PASS empty string
            }
            
            const res = await fetch('http://localhost:3000/getFileData',{
                method: 'POST',  // Use POST to send data in the body
                headers: {
                  'Content-Type': 'application/json',  // Specify the content type as JSON
                },
                body: JSON.stringify(data),  // Convert the JavaScript object to a JSON string
              });

            if (!res.ok) {
                throw new Error(`Server responded with status: ${res.status}`);
            }
    
            const html = await res.text(); 
            setHtmlContent(html);
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
                        <p></p>
                    )}
                </div>
            </div>
        </div>
    );
}

export default YourFiles;

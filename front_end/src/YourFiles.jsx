import React, { useState, useEffect } from "react";

function YourFiles() {
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
            const data = {
                "FileName": name,
                "Location": ""
            };
            const res = await fetch('http://localhost:3000/getFileData', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json" // Important for JSON data
                },
                body: JSON.stringify(data)
            });
    
            if (!res.ok) {
                throw new Error(`Server responded with status: ${res.status}`);
            }
    
            const responseData = await res.json(); // Assuming the server returns JSON
            console.log("Response:", responseData);
            return responseData;
    
        } catch (error) {
            console.error("Failed to get file data from API:", error);
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
                            <button key={name} className="GetFileNames-btn" onClick={()=>GiveMEMYGRAAAAAPH({name})}>{name}</button>
                        ))
                    ) : (
                        <p>Loading files...</p>
                    )}
                </div>
            </div>
        </div>
    );
}

export default YourFiles;

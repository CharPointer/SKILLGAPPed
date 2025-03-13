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
                            <button key={name} className="GetFileNames-btn">{name}</button>
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

import React, { useState, useEffect } from "react";

function YourFiles() {

    const [files, setFiles] = useState([]);

    async function fetchData() {
        try {
            const res = await (await fetch('http://localhost:3000/getFiledata')).json();
            let data = res.Files;
            setFiles(prevFiles => [...prevFiles, ...data]); 
        } catch (error) {
            console.log("Failed to get files from API");
        }
    }

    useEffect(() => {

        fetchData();
    });

    return (
        <div className="YourFiles">
            <h1>Your Files</h1>
            <hr />
            <div className="YourFiles-Container">
                <div className="YourFiles-Buttons">
                    
                        {files.length > 0 && files.map((name) => (
                        <button key={name} className="GetFileNames-btn">{name}</button>
                        ))}

                    <button className="GetFileNames-btn">Test.html</button>
                    <button className="GetFileNames-btn">Test.html</button>
                    <button className="GetFileNames-btn">Test.html</button>
                </div>
            </div>
        </div>
    );
}

export default YourFiles;

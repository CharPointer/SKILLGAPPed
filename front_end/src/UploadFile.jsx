import uploadPicture from './assets/uploadImg.png';
import React, {useRef, useState, useEffect} from 'react'
import FileInfoPopup from './FileInfoPopup.jsx';

function UploadFile(){

    const fileInputRef=useRef(null);
    const [file, setFile] = useState(null);
    const [status, setStatus]=useState("idle");
    const [uploadProgress, setUploadProgress] = useState(0);
    const [buttonPopUp,setButtonPopUp]=useState(false);
    const [upload, setUpload]=useState(false);

    //opens file input, because its invis and i stupid
    function UploadThatBoi(){
        if(fileInputRef.current){
            fileInputRef.current.click();
        }
    }

    //checks the file type
    async function HandleFileChange(e)
    {
        if(e.target.files)
        {
            const uploadedFile=e.target.files[0];
            const fileType =uploadedFile.name.split('.').pop().toLowerCase();

            if (fileType === 'json' || fileType === 'csv') {
                setFile(uploadedFile);
                setStatus("uploading");
                setUploadProgress(0);
                setButtonPopUp(true);
            } else {
                setFile(null); 
                setStatus("error");
                //Padaryti, kad issoktu kazkokia lentele 
            }
        }
    }

    //the function which AACTUALLY UPLOADS THE FUCKING FAIL
    async function handleFileUpload(uploadedFile){
        const formData = new FormData();
        formData.append("filetoupload", uploadedFile); // Must match the field name in Express
        console.log()
        try {
            const response = await fetch("http://localhost:3000/fileupload", {
                method: "POST",
                body: formData, // ✅ Send FormData directly
            });
    
            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }
    
            setStatus("success");
            setUploadProgress(100);
            console.log("File uploaded successfully");
        } catch (error) {
            setStatus("error");
            setUploadProgress(0);
        }
        
    }
    useEffect(() => {
        if (upload && file) {
            handleFileUpload(file);
        }
    }, [upload]);
    useEffect(() => {
        if (status==="success") {
            
        }
    }, [status]);

    return(
        <div>
            <div className="File-Information">

                {file&&buttonPopUp&& (
                    <FileInfoPopup 
                    trigger={buttonPopUp} 
                    name={file.name} 
                    size={(file.size / 1024).toFixed(2)} 
                    type={file.type}
                    setTrigger={setButtonPopUp}
                    setUpload={setUpload}
                />
                )}
                {file&&status==="error"&&(
                    <p>ERRROOORRAS</p>
                )}
                {file&&status==="success"&&(
                    <p>pavyko</p>
                )}
                    {file&&status==="uploading"&&(
                    <p>krauna</p>
                )}
                
            </div>
            <div className="Container-UploadFile" onClick={UploadThatBoi}>

                <p className="UploadFileText">Upload your file! </p>
                <img src={uploadPicture} alt="UploadImg"></img>
                <input title="" placeholder="" type="file"ref={fileInputRef}style={{display: "none"}} onChange={HandleFileChange}></input>
            </div>

        </div>
    );
}

export default UploadFile
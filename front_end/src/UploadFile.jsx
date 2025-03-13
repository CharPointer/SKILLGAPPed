import uploadPicture from './assets/uploadImg.png';
import React, {useRef, useState, useEffect} from 'react'
import FileInfoPopup from './FileInfoPopup.jsx';
import OtherPopups from './OtherPopups.jsx';

function UploadFile(){

    // console.log("he1lp")

    const fileInputRef=useRef(null); //mygtukas susiaktyvuoja (ignore)
    const [file, setFile] = useState(null); //failas

    const [status, setStatus]=useState("idle"); //idle,uploading, success,error


    const [buttonPopUp,setButtonPopUp]=useState(false);
    const [upload, setUpload]=useState(false);

    /*FOR POPUPS DONT CHECK IT */
    const [errorConst, setErrorConst] = useState(false);
    const [successConst, setSuccessConst] = useState(false)
    const [uploadingConst, setUploadingConst] = useState(false)



    const supportedFileType =["json", "csv", "txt", "xls", "xlsx",
                                "tsv", "parquet", "xml", "html", "h5", "feather",
                                "orc", "dta", "sav"];

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

            if (supportedFileType.includes(fileType)) {

                setStatus("idle"); // Reset status before setting the new file
                setErrorConst(false); // Hide error popup immediately
                setSuccessConst(false);
                setFile(uploadedFile);

                setButtonPopUp(true);
                setUploadingConst(true);
            }
        }
    }

    //the function which AACTUALLY UPLOADS THE FUCKING FAIL
    async function handleFileUpload(uploadedFile){
        const formData = new FormData();
        formData.append("filetoupload", uploadedFile); // Must match the field name in Express
        try {
            const response = await fetch("http://localhost:3000/fileupload", {
                method: "POST",
                body: formData, // ✅ Send FormData directly
                
            });
    
            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }
    
            setStatus("success");
            setUploadingConst(false);
            setSuccessConst(true);
            
            fileInputRef.current.value = "";
            setUpload(false);

            console.log("File uploaded successfully");

        } catch (error) 
        {
            setUpload(false);
            setStatus("error");

            setFile(null);
            fileInputRef.current.value = "";
            setErrorConst(true);
            console.log("bloke");
        }
        
    }
    useEffect(() => {
        if (upload && file) {
            handleFileUpload(file);
        }
    }, [upload]);

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
                    setStatus={setStatus}
                    />
                )}
                {status==="error"&&(
                    <OtherPopups trigger={errorConst} setTrigger={setErrorConst} setStatus={setStatus} Type="error"/>
                )}
                {status==="success"&&(
                    <OtherPopups trigger={successConst} setTrigger={setSuccessConst}setStatus={setStatus} Type="success"/>
                )}
                {status==="uploading"&&(
                    <OtherPopups trigger={uploadingConst} setTrigger={setUploadingConst} setStatus={setStatus} Type="uploading"/>
                )}
                
            </div>
            <div className="Container-UploadFile" onClick={UploadThatBoi}>

                <p className="UploadFileText">Upload your file! </p>
                <img src={uploadPicture} alt="UploadImg"></img>
                <input title="" placeholder="" type="file"ref={fileInputRef}style={{display: "none"}} onChange={HandleFileChange}></input>

                {console.log(status)}
            </div>

        </div>
    );
}

export default UploadFile
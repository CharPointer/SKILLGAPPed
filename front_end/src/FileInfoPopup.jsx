
function FileInfoPopup(props){
    return (props.trigger) ? (
        <div className="popup">
            <div className="popup-inner">
                <h1>Confirm upload?</h1>
                <p>File name: {props.name}</p>
                <p>Size: {props.size} KB</p>
                <p>Type: {props.type}</p>
                <div className="popup-Buttons">
                    <button className="upload-btn" onClick={()=>{
                                                                 props.setUpload(true)
                                                                 props.setTrigger(false)}}>Upload!</button>
                    <button className="close-btn" onClick={() => {
                                                                  props.setTrigger(false)
                                                                  props.setUpload(false)}}>Cancel</button>

                </div>

                {props.children}
            </div>
        </div>
    ) : "";
}

export default FileInfoPopup
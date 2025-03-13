import pictureLoading from "./assets/loading.gif";

function OtherPopups(props){
    return (props.trigger) ? (
        <div className="popup">
            <div className="popup-inner">
                <div className="popup-Buttons">

                    {props.Type === "error" || props.Type === "success" ? (
                        <div>
                            {props.Type==="error" ? (
                                <h2>Error 404</h2>
                            ):
                            (<h2>Success</h2>)}
                            
                            <button className="close-btn" onClick={() => {
                            props.setTrigger(false)
                            props.setStatus("idle")}}>Cancel</button>
                        </div>
                    ) : (
                        <div>
                            <img src={pictureLoading} alt="loading..."/>
                        </div>
                    )}

                </div>
                {props.children}
            </div>
        </div>
    ) : "";
}

export default OtherPopups;
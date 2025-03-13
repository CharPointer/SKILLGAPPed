
function ShowPlot({ htmlContent }){

    return(
        <div className="ShowPlot-body">
            <h1>Your data</h1>
            <hr></hr>
            <div>
                {htmlContent && <div dangerouslySetInnerHTML={{ __html: htmlContent }} />}
            </div>
        </div>
    );
}

export default ShowPlot

function ShowPlot(props){

    return(
        <div className="ShowPlot-body">
            <h1>Your data</h1>
            <hr></hr>
            <div>
                {props&&props}
                <div dangerouslySetInnerHTML={{ __html: props.htmlContent }} />
            </div>
        </div>
    );
}

export default ShowPlot
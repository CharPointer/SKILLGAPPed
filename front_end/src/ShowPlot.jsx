function ShowPlot({ HtmlContent }){

    return(
        <div className="ShowPlot-body">
            <h1>Your data</h1>
            <hr></hr>
            <div>
                <iframe
                    title="Plotly Plot"
                    style={{ width: "100%", height: "500px", border: "none" }}
                    srcDoc={HtmlContent} // Use srcDoc to insert the HTML
                />
                
            </div>
        </div>
    );
}

export default ShowPlot
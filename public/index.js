alert("Test")
const currentUrl = window.location.href;

function SendJson() {
    FileName = "Test.py"
    FileLocation = "UploadedFiles"

    data = {
        "FileName": FileName,
        "Location": FileLocation
    }

    fetch(currentUrl + "getFileData", {
        method: 'POST',  // Use POST to send data in the body
        headers: {
          'Content-Type': 'application/json',  // Specify the content type as JSON
        },
        body: JSON.stringify(data),  // Convert the JavaScript object to a JSON string
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to download file');
          }
          return response.blob();  
        })  // Parse the JSON response
        .then(blob => {
          // Create a link element to download the file
          const link = document.createElement('a');
          link.href = URL.createObjectURL(blob);  // Create a URL for the Blob
          link.download = 'example.txt';  // The filename the user will see when downloading
          link.click();  // Programmatically trigger a click to download the file
        })
        .catch(error => {
          console.error('Error:', error);
        });
}
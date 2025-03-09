const formidable = require("formidable");
const fs = require("fs");
const path = require("path")
const spawn = require("child_process").spawn;
const express = require("express");
const app = express();

const UploadPath = path.resolve(__dirname, 'UploadedFiles'); // ON GAWDS LIFE USE path.resolve for paths, cuz we dont know if we are going to use Windows pc or Linux pc for deployment
const port = 3000;

app.set("view engine", "ejs");
app.use(express.static("public"));

app.get("/", (req, res) => {
    res.render("index.ejs");
}) 

app.get("/getFilesNames", (req, res) => {
    fs.readdir(UploadPath, (err,files) => {
        if (err) throw err;
        var Json = {
            "Files": files
        }
        console.log(Json);
        res.json(Json);
        res.end();
    })
})

app.get("/runPython", (req, res) => {
    var Name = "Test.py" // need for this to be able to read json file/data from req and and do shit

    const pythonProcess = spawn('python',[path.resolve(UploadPath, Name)]);
    pythonProcess.stdout.setEncoding('utf8');
    pythonProcess.stdout.on('data', (data) => {
        console.log(data)
        // res.sendStatus(200);
        res.json({
            "Data": data
        });

        res.end();
    });
})

app.get("/getFileData", (req, res) => {
    // here will be the data for the vizualization to be sent to the client
    res.sendStatus(200);
    res.end();
}) 

app.post("/fileupload", (req,res) => {
    var form = new formidable.IncomingForm();
    form.parse(req, function (err, fields, files) {
        var oldpath = files.filetoupload[0].filepath;
        var oldName = files.filetoupload[0].originalFilename;
        console.log(files.filetoupload[0].filepath)
        var newpath = path.resolve(UploadPath,oldName);
        fs.copyFile(oldpath, newpath, fs.constants.COPYFILE_EXCL, function (err) {
          if (err) throw err;
          res.write('File uploaded and moved!');
          res.end();
        });
    });
})

app.listen(port);
console.log(`Open on port: ${port}`);
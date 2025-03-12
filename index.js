const formidable = require("formidable");
const fs = require("fs");
const path = require("path")
const spawn = require("child_process").spawn;
const express = require("express");
const bodyParser = require('body-parser');
const app = express();

const UploadPath = path.resolve(__dirname, 'UploadedFiles'); // ON GAWDS LIFE USE path.resolve for paths, cuz we dont know if we are going to use Windows pc or Linux pc for deployment
const port = 3000;

app.set("view engine", "ejs");
app.use(express.static("public"));
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());
  

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
    var Name = "./Ai/PythonRunAi.py" // need for this to be able to read json file/data from req and and do shit

    console.log("started")
    const pythonProcess = spawn(path.resolve(__dirname, './Aivenv/bin/python'),[path.resolve(__dirname, Name)]);
    console.log("start")
    pythonProcess.stdout.setEncoding('utf8');
    
    pythonProcess.stdout.on('data', (data) => {
        console.log(data)
        // res.sendStatus(200);
        res.json({
            "Data": data
        });

        res.end();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
})

app.post("/getFileData", (req, res) => {
    var data = req.body;
    console.log(data["Location"] + "/" + data["FileName"]);

    var filePath = path.resolve(__dirname, data["Location"]);
    filePath = path.resolve(filePath, data["FileName"]);

    res.sendFile(filePath, (err) => {
        if (err) {
            console.error("Error sending the file", err);
            res.status(500).send('error sending file');
        }
    })
}) 

app.post("/fileupload", (req,res) => {
    var form = new formidable.IncomingForm();
    console.log(req.body)
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
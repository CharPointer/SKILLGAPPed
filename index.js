const formidable = require("formidable");
const fs = require("fs");
const path = require("path")
const spawn = require("child_process").spawn;
const express = require("express");
const bodyParser = require('body-parser');
const { getMaxListeners } = require("events");
const { Console } = require("console");
const { name } = require("ejs");
const app = express();

const UploadPath = path.resolve(__dirname, 'UploadedFiles'); // ON GAWDS LIFE USE path.resolve for paths, cuz we dont know if we are going to use Windows pc or Linux pc for deployment :((((
const port = 3000;

app.set("view engine", "ejs");
app.use(express.static(path.join(__dirname, 'front_end', 'dist')));
app.use(express.static("public"));
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());

app.use(function (req, res, next) {

    // Website you wish to allow to connect
    res.setHeader('Access-Control-Allow-Origin', '*');

    // Request methods you wish to allow
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');

    // Request headers you wish to allow
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');

    // Set to true if you need the website to include cookies in the requests sent
    // to the API (e.g. in case you use sessions)
    res.setHeader('Access-Control-Allow-Credentials', true);

    // Pass to next layer of middleware
    next();
});

var IsProcessRunning = false;
var ConversionQueue = [];

function RunScript(file) {
    var Name = "./Ai/SuperGlue.py" // need for this to be able to read json file/data from req and and do shit

    console.log("started on " + file + " convertion!")
    const pythonProcess = spawn(path.resolve(__dirname, './Aivenv/bin/python'),[path.resolve(__dirname, Name), file]);
    pythonProcess.stdout.setEncoding('utf8');
    
    pythonProcess.stdout.on('data', (data) => {
        console.log(data)
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
        console.log(file + " exited unsussesfull");
        return 0;
    });

    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
        console.log(file + " success");
        return 1;
    });
}
async function RunScriptTest(file) {
    return new Promise((resolve, reject) => {
        var Name = "./Ai/SuperGlue.py" // need for this to be able to read json file/data from req and and do shit

        console.log("started on " + file + " convertion! IsProcessRunning:" + IsProcessRunning)
        const pythonProcess = spawn(path.resolve(__dirname, './Aivenv/bin/python'),[path.resolve(__dirname, Name), file]);
        pythonProcess.stdout.setEncoding('utf8');
        
        pythonProcess.stdout.on('data', (data) => {
            console.log(data)
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`stderr: ${data}`);
            console.log(file + " exited unsussesfull");
            resolve(0);
        });

        pythonProcess.on('close', (code) => {
            console.log(`Child process exited with code ${code}`);
            if (code === 0) {
                console.log(file + " success");
                resolve(1); // Resolve when successful2
            } else {
                console.log(file + " failed with code " + code);
                resolve(0); // Reject if exit code is non-zero
            }
        });
    });
}

function AddToQueue(Name) {
    Obj = {
        "Name": Name,
        "TriesLeft": 5,
    } 
    ConversionQueue.push(Obj);
    // console.log(ConversionQueue)
    if (IsProcessRunning == false) {
        QueueRunner();
        console.log("starting QueueRunner()");
    };
}

async function QueueRunner(){
    IsProcessRunning = true;
    where = 0;
    while (ConversionQueue.length != 0) {
        Obj = ConversionQueue[0];

        Name = Obj["Name"]

        try {
            console.log(ConversionQueue);
            const result = await RunScriptTest(Name);

            // console.log("asssssssssssssssssssssss"+ result)

            if (result === 0) {
                console.warn("NOT FINISHED, AKA THERE WAS ERROR IN PIPELINE");
                Obj["TriesLeft"] = Obj["TriesLeft"] - 1;
                if (Obj["TriesLeft"] <= 0) {
                    // Pop THAT SHIT OUT
                    ConversionQueue.splice(0, 1);
                }
            } else if (result === 1) {
                console.log("Everything's OK");
                // BRO edged hard
                ConversionQueue.splice(0, 1);
            } else {
                console.warn("THERE WAS UNEXPECTED RETURN WHICH SHOULD NOT HAVE HAPPENED");
            }
        } catch (error) {
            console.error("Error running script:", error);
            // HANDLE THE FUCK
        }

    }
    IsProcessRunning = false
}

app.get("/old", (req, res) => {
    res.render("index.ejs");
}) 

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'front_end', 'dist', 'index.html'));
});

app.get("/getFilesNames", (req, res) => {
    fs.readdir(path.resolve(__dirname, "Ai/VizualizationFiles"), (err,files) => {
        HtmlFiles = [];
        files.forEach(element => {
            var split = element.split(".");
            if (split[1] == "html") {
                HtmlFiles.push(element);
            }
        });

        if (err) throw err;
        var Json = {
            "Files": HtmlFiles
        }
        console.log(Json);
        res.json(Json);
        res.end();
    })
})

let test = 0;
app.get("/Add", (req,res) => {
    console.log("added")
    AddToQueue(`${test}`);
    test += 1;
    res.status(200);
})

app.post("/getFileData", (req, res) => {
    console.log("tried")
    var data = req.body;
    console.log(data["Location"] + "/" + data["FileName"]);
    
    var filePath = "";
    if (data["Location"] == ""){
        filePath = path.resolve(__dirname, "Ai/VizualizationFiles");
    } else {
        filePath = path.resolve(__dirname, data["Location"]);
    }

    filePath = path.resolve(filePath, data["FileName"]);

    res.sendFile(filePath, (err) => {
        if (err) {
            console.error("Error sending the file", err);
            res.status(500).send('error sending file');
        }
    })
}) 

app.post("/fileupload", (req,res) => {
    console.log("tried to upload")
    var form = new formidable.IncomingForm();
    console.log(req.body)
    try{
        form.parse(req, function (err, fields, files) {
            var oldpath = files.filetoupload[0].filepath;
            var oldName = files.filetoupload[0].originalFilename;
            console.log(files.filetoupload[0].filepath)
            var newpath = path.resolve(UploadPath,oldName);
            fs.copyFile(oldpath, newpath, fs.constants.COPYFILE_EXCL, function (err) {
              if (err) {
                console.log("Same file egzist");
                res.status(400).send("error same file exists");
              } else {
                res.write('File uploaded and moved!');
                res.end();
                let Name = files.filetoupload[0].originalFilename;
                //   console.log(Name)
                Name = Name.split(".");
                //   console.log(Name)
                Name = Name[0]
                //   console.log(Name)
                AddToQueue(Name);
              };
            });
        });
    } catch(err){
        console.log("FILE ERRORRRRR UPLOOOOOOAAAAADDDDEEEEE " + err)
        res.status(400);
        res.end();
    }
})

app.listen(port);
console.log(`Open on port: ${port}`);
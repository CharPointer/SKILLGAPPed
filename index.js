const formidable = require("formidable");
const fs = require("fs");
const path = require("path")
const express = require("express");
const app = express();

const UploadPath = path.resolve(__dirname, 'UploadedFiles');
const port = 3000;

app.set("view engine", "ejs");
app.use(express.static("public"));

app.get("/", (req, res) => {
    res.render("index.ejs");
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
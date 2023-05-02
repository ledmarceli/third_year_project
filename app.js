const express = require('express');
const cors = require('cors');
const path = require('path');
const app = express();
app.use(cors());
app.use(express.json());

//Handling FEN
app.post('/api', (req, res) => {
    const position = req.body.position;
    const move = req.body.move;
    var out = ""
    const { spawn } = require('child_process');

     //Spawn a child process to run the Python script
    const pythonProcess = spawn('python', ['server/backend_fen.py',position,move]);
  
     //Listen for data from the Python script
     pythonProcess.stdout.on('data', (data) => {
      console.log('Received data from Python script: ' + (data));
     out = (data);
     res.statusCode = 200;
     res.setHeader('Content-Type', 'application/json');
     res.end(JSON.stringify({output: data.toString()}));
    });
  
    //Listen for error output from the Python script
     pythonProcess.stderr.on('data', (data) => {
       console.error('Error output from Python script: ' + data.toString());
       res.statusCode = 500;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({error: data.toString()}));
    });
  
     //Listen for the Python script to exit
     pythonProcess.on('close', (code) => {
      console.log('Python script exited with code ' + code);
      });
    });
app.listen(8080, () => {
  console.log('Server listening on port 8080');
});


//Handling PGN
const multer  = require('multer');
const fs = require('fs');
const upload = multer({ dest: 'uploads/' });

app.post('/upload', upload.single('file'), (req, res) => {
  const filepath = req.file.path;
  const player = req.body.text
  const { spawn } = require('child_process');

    //Spawn a child process
    const pythonProcess = spawn('python', ['server/backend_pgn.py',filepath,player]);
  
     //Listen for data from the Python script
     pythonProcess.stdout.on('data', (data) => {
      console.log('Received data from Python script: ' + (data));
     out = (data);
     res.statusCode = 200;
     res.setHeader('Content-Type', 'application/json');
     res.end(JSON.stringify({output: data.toString()}));
     //Remove File
     fs.unlink(filepath, (err) => {
      if (err) {
        console.error(err);
      }
    });
    });
  
    //Listen for error output from the Python script
     pythonProcess.stderr.on('data', (data) => {
       console.error('Error output from Python script: ' + data.toString());
       res.statusCode = 500;
      //res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({error: data.toString()}));
    });
  
     //Listen for the Python script to exit
     pythonProcess.on('close', (code) => {
      console.log('Python script exited with code ' + code);
      });
    });
app.listen(3000, () => {
  console.log('Server started on port 3000');
});
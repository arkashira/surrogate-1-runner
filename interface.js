   app.post('/shell', express.json(), async (req, res) => {
     const { command } = req.body;
     try {
       const { stdout, stderr } = await execPromise(command);
       res.json({ output: stdout + stderr });
     } catch (err) {
       res.status(500).json({ output: err.message });
     }
   });
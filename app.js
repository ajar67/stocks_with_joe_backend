const express = require("express");
const cors = require("cors");
const { exec, spawn } = require("child_process");

const { PORT = 3003 } = process.env;
const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());

app.post("/api/login", (req, res) => {
  const apiKey = req.body.apiKey;
  if (!apiKey) {
    return res.status(400).json({ error: "No API key provided" });
  }

  const pythonProcess = spawn("python", ["testApiKey.py", apiKey]);

  pythonProcess.stdout.on("data", (data) => {
    console.log(`stdout: ${data}`);
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on("close", (code) => {
    console.log(`child process exited with code ${code}`);
    if (code === 0) {
      res.status(200).json({ message: "API key received and processed" });
    } else {
      res.status(500).json({ error: "Error processing API key" });
    }
  });
});

app.post("/run-script", (req, res) => {
  exec("python test.py", (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({ error: error.message });
    }
    if (stderr) {
      return res.status(500).json({ error: stderr });
    }
    res.status(200).json({ output: stdout });
  });
});

app.post("/get-info", (req, res) => {
  exec("python info.py", (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({ error: error.message });
    }
    if (stderr) {
      return res.status(500).json({ error: stderr });
    }
    res.status(200).json({ output: stdout });
  });
});

app.post("/kill-script", (req, res) => {
  exec("python terminate.py", (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({ error: error.message });
    }
    if (stderr) {
      return res.status(500).json({ error: stderr });
    }
    res.status(200).json({ output: stdout });
  });
});

app.use((req, res, next) => {
  res.status(404).send(`Route ${req.url} not found!`);
});

app.listen(PORT, () => {
  console.log(`Server is listening on ${PORT}`);
});

const express = require("express");
const cors = require("cors");
const { exec } = require("child_process");

const { PORT = 3003 } = process.env;
const app = express();
app.use(express.json());
app.use(cors());

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

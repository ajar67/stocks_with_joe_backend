const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const filePath = path.join(__dirname, "api_key.txt");
const { exec } = require("child_process");

const { PORT = 3003 } = process.env;
const app = express();
app.use(express.json());
app.use(cors());

app.post("/store-api-key", (req, res) => {
  console.log(req.body);
  const { apiKey } = req.body;
  if (!apiKey) {
    return res.status(400).json({ error: "API key is required" });
  }
  console.log(apiKey);
  fs.writeFileSync(filePath, apiKey, "utf8");
  console.log("created file");
  res.status(200).json({ message: "API key saved successfully" });
});

app.post("/logout", (req, res) => {
  const filePath = path.join(__dirname, "api_key.txt");
  if (fs.existsSync(filePath)) {
    fs.unlinkSync(filePath);
    console.log("API key file deleted");
  }
  res.status(200).json({ message: "Logged out successfully" });
});

app.post("/run-script", (req, res) => {
  exec("python3 test.py", (error, stdout, stderr) => {
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
  exec("python3 info.py", (error, stdout, stderr) => {
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
  exec("python3 terminate.py", (error, stdout, stderr) => {
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

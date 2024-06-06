const express = require("express");
const cors = require("cors");

const { PORT = 3003 } = process.env;
const app = express();
app.use(express.json());
app.use(cors());

server.use((req, res, next) => {
  res.status(404).send(`Route ${req.url} not found!`);
});

app.listen(PORT, () => {
  console.log(`Server is listening on ${PORT}`);
});

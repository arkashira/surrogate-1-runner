import express from "express";
import http from "http";
import { initSocket } from "./sync/socket";

const app = express();
app.use(express.json());

// Simple health check endpoint
app.get("/health", (_req, res) => res.send("ok"));

const server = http.createServer(app);
initSocket(server);

const PORT = process.env.PORT ?? 3000;
server.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
import { Server as HttpServer } from "http";
import { Server as SocketIOServer, Socket } from "socket.io";
import { InventoryItem } from "../models/inventory";
import { InventoryService } from "../services/inventoryService";

/**
 * Initializes a Socket.IO server on the given HTTP server.
 *
 * The socket.io instance listens for `inventory:update` events from clients.
 * When an update is received, the server:
 *   1. Persists the change via InventoryService.
 *   2. Emits an `inventory:ack` event back to the originating client.
 *   3. Broadcasts the updated item to all connected clients via `inventory:changed`.
 *
 * Conflict detection is performed by InventoryService. If a conflict is
 * detected, the server emits `inventory:conflict` to the originating client
 * with both the local and remote versions.
 *
 * @param httpServer The HTTP server to attach Socket.IO to.
 * @returns The Socket.IO server instance.
 */
export function initSocket(httpServer: HttpServer): SocketIOServer {
  const io = new SocketIOServer(httpServer, {
    cors: {
      origin: "*",
      methods: ["GET", "POST"],
    },
  });

  const inventoryService = new InventoryService();

  io.on("connection", (socket: Socket) => {
    console.log(`Socket connected: ${socket.id}`);

    // Handle optimistic updates from clients
    socket.on(
      "inventory:update",
      async (payload: { id: string; data: Partial<InventoryItem> }) => {
        try {
          const { id, data } = payload;
          const result = await inventoryService.updateItem(id, data);

          // Send ACK to the originating client
          socket.emit("inventory:ack", { id, status: "ok" });

          // Broadcast the change to all other clients
          socket.broadcast.emit("inventory:changed", { id, data: result });

          // If a conflict was detected, notify the originating client
          if (result.conflict) {
            socket.emit("inventory:conflict", {
              id,
              local: data,
              remote: result.remote,
            });
          }
        } catch (err) {
          console.error("Error processing inventory:update:", err);
          socket.emit("inventory:error", {
            id: payload.id,
            message: (err as Error).message,
          });
        }
      }
    );

    socket.on("disconnect", () => {
      console.log(`Socket disconnected: ${socket.id}`);
    });
  });

  return io;
}
package com.axentx.surrogate1;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;

/**
 * Manages a real‑time TCP connection used for interactive shell sessions.
 *
 * <p>The implementation guarantees:
 *
 * <ul>
 *   <li>Connection establishment within {@code CONNECTION_TIMEOUT_MS} (1 second).</li>
 *   <li>Keep‑alive is enabled so the socket stays open for extended periods.</li>
 *   <li>Explicit termination when the user logs out.</li>
 * </ul>
 *
 * <p>This class is deliberately lightweight and does not embed any protocol
 * logic – callers are responsible for reading/writing to {@link #getSocket()}.
 */
public class RealtimeConnection {

    /** Connection timeout in milliseconds – matches the acceptance criterion. */
    private static final int CONNECTION_TIMEOUT_MS = 1_000;

    private final String host;
    private final int port;

    private Socket socket;

    /**
     * Creates a new {@code RealtimeConnection} targeting the given host and port.
     *
     * @param host the remote host (e.g. {@code "localhost"}).
     * @param port the remote port where the shell service listens.
     */
    public RealtimeConnection(String host, int port) {
        this.host = host;
        this.port = port;
    }

    /**
     * Establishes the TCP connection. If a connection is already active,
     * this method is a no‑op.
     *
     * @throws IOException if the connection cannot be established within the
     *                     timeout or an I/O error occurs.
     */
    public synchronized void establish() throws IOException {
        if (isActive()) {
            return;
        }

        SocketAddress address = new InetSocketAddress(host, port);
        Socket s = new Socket();
        // Enforce the 1‑second connection window.
        s.connect(address, CONNECTION_TIMEOUT_MS);
        // Enable TCP keep‑alive to keep the connection alive for long periods.
        s.setKeepAlive(true);
        this.socket = s;
    }

    /**
     * Terminates the connection promptly. If no connection exists, this method
     * does nothing.
     *
     * @throws IOException if an error occurs while closing the socket.
     */
    public synchronized void terminate() throws IOException {
        if (socket != null) {
            try {
                socket.close();
            } finally {
                socket = null;
            }
        }
    }

    /**
     * Returns {@code true} if a live, connected socket exists.
     *
     * @return {@code true} if the connection is active; {@code false} otherwise.
     */
    public synchronized boolean isActive() {
        return socket != null && socket.isConnected() && !socket.isClosed();
    }

    /**
     * Provides access to the underlying {@link Socket}. Callers may read from
     * or write to the socket streams. The socket is guaranteed to be non‑null
     * only when {@link #isActive()} returns {@code true}.
     *
     * @return the active socket, or {@code null} if no connection is established.
     */
    public synchronized Socket getSocket() {
        return socket;
    }
}
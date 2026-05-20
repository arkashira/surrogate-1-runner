package com.axentx.surrogate1;

import com.jcraft.jsch.JSch;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.Session;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.security.GeneralSecurityException;
import java.util.Properties;
import java.util.concurrent.*;

/**
 * Utility for establishing an SSH connection that automatically terminates after a configurable idle timeout.
 */
public class SecureShell {

    private final JSch jsch;
    private final int idleTimeoutSeconds;
    private final ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();

    private Session session;
    private ScheduledFuture<?> idleFuture;

    /**
     * Creates a SecureShell instance with a new JSch instance.
     *
     * @param idleTimeoutSeconds idle timeout in seconds after which the connection is closed automatically
     */
    public SecureShell(int idleTimeoutSeconds) {
        this(new JSch(), idleTimeoutSeconds);
    }

    /**
     * Creates a SecureShell instance with a supplied JSch (useful for testing).
     *
     * @param jsch                JSch instance
     * @param idleTimeoutSeconds idle timeout in seconds after which the connection is closed automatically
     */
    public SecureShell(JSch jsch, int idleTimeoutSeconds) {
        this.jsch = jsch;
        this.idleTimeoutSeconds = idleTimeoutSeconds;
    }

    /**
     * Establishes an SSH connection using a private key.
     *
     * @param host       remote host
     * @param port       remote SSH port
     * @param username   SSH username
     * @param privateKey PEM‑encoded private key string
     * @throws JSchException          if the SSH connection cannot be established
     * @throws GeneralSecurityException if the private key cannot be parsed
     */
    public synchronized void connect(String host, int port, String username, String privateKey)
            throws JSchException, GeneralSecurityException {

        if (session != null && session.isConnected()) {
            throw new IllegalStateException("Already connected");
        }

        // Load private key from the supplied string
        byte[] keyBytes = privateKey.getBytes(StandardCharsets.UTF_8);
        jsch.addIdentity(username, keyBytes, null, null);

        session = jsch.getSession(username, host, port);
        // Disable strict host key checking for test environments; production should use known hosts.
        Properties config = new Properties();
        config.put("StrictHostKeyChecking", "no");
        session.setConfig(config);

        // Connect with a reasonable timeout (10 seconds)
        session.connect(10_000);

        scheduleIdleTermination();
    }

    /**
     * Returns true if the underlying SSH session is currently connected.
     */
    public synchronized boolean isConnected() {
        return session != null && session.isConnected();
    }

    /**
     * Terminates the SSH connection immediately.
     */
    public synchronized void disconnect() {
        cancelIdleTask();
        if (session != null && session.isConnected()) {
            session.disconnect();
        }
        session = null;
    }

    private void scheduleIdleTermination() {
        cancelIdleTask(); // ensure no previous task is running
        idleFuture = scheduler.schedule(this::disconnect, idleTimeoutSeconds, TimeUnit.SECONDS);
    }

    private void cancelIdleTask() {
        if (idleFuture != null && !idleFuture.isDone()) {
            idleFuture.cancel(true);
        }
    }

    /**
     * Shuts down internal resources. Should be called when the application terminates.
     */
    public void shutdown() {
        scheduler.shutdownNow();
    }
}
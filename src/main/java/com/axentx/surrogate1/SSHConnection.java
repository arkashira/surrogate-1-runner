package com.axentx.surrogate1;

import com.jcraft.jsch.*;

public class SSHConnection {
    private static final String HOST = "surrogate-1";
    private static final int PORT = 22;
    private static final String USERNAME = "admin";
    private static final int TIMEOUT = 5000; // 5 seconds

    private Session session;
    private Channel channel;

    public void connect() throws JSchException {
        JSch jsch = new JSch();
        session = jsch.getSession(USERNAME, HOST, PORT);
        session.setConfig("PreferredAuthentications", "publickey");
        session.setConfig("StrictHostKeyChecking", "no");
        session.connect(TIMEOUT);

        channel = session.openChannel("shell");
        channel.connect();
    }

    public void disconnect() {
        if (channel != null && channel.isConnected()) {
            channel.disconnect();
        }
        if (session != null && session.isConnected()) {
            session.disconnect();
        }
    }

    public Channel getChannel() {
        return channel;
    }
}
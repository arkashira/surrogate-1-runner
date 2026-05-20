package com.axentx.surrogate1;

import com.jcraft.jsch.*;

public class SSHAuthenticator {
    private static final String PRIVATE_KEY_PATH = "/path/to/private/key";
    private static final String PASSPHRASE = "your_passphrase";

    public void authenticate(Session session) throws JSchException {
        JSch jsch = new JSch();
        jsch.addIdentity(PRIVATE_KEY_PATH, PASSPHRASE);
        session.setConfig("PreferredAuthentications", "publickey");
    }
}
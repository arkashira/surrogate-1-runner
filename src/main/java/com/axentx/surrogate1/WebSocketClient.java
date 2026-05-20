package com.axentx.surrogate1;

import java.net.URI;
import javax.websocket.ContainerProvider;
import javax.websocket.Session;
import javax.websocket.WebSocketContainer;

public class WebSocketClient {

    private static final String WEBSOCKET_URI = "ws://localhost:8080/shell";

    public static void main(String[] args) {
        try {
            WebSocketContainer container = ContainerProvider.getWebSocketContainer();
            Session session = container.connectToServer(ClientEndpoint.class, URI.create(WEBSOCKET_URI));
            session.getBasicRemote().sendText("Hello from client");
            session.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @javax.websocket.ClientEndpoint
    public static class ClientEndpoint {
        @javax.websocket.OnMessage
        public void onMessage(String message) {
            System.out.println("Received message from server: " + message);
        }
    }
}
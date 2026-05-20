package com.axentx.surrogate.freerouter;

import org.freerouting.routing.Routing;

public class Main {
    public static void main(String[] args) {
        // Initialize FreeRouter with the updated version
        Routing router = new Routing();
        
        // Example usage of FreeRouter
        router.setup();
        router.run();
        
        System.out.println("FreeRouter initialized and running successfully.");
    }
}
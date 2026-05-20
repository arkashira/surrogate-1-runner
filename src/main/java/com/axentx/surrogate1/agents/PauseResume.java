package com.axentx.surrogate1.agents;

import java.util.concurrent.atomic.AtomicBoolean;

public class PauseResume {
    private AtomicBoolean paused = new AtomicBoolean(false);

    public void pause() {
        paused.set(true);
    }

    public void resume() {
        paused.set(false);
    }

    public boolean isPaused() {
        return paused.get();
    }
}
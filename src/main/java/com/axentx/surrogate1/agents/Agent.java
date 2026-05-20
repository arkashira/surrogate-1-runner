package com.axentx.surrogate1.agents;

public abstract class Agent {
    private PauseResume pauseResume = new PauseResume();

    public void pause() {
        pauseResume.pause();
    }

    public void resume() {
        pauseResume.resume();
    }

    public boolean isPaused() {
        return pauseResume.isPaused();
    }

    public abstract void run();
}
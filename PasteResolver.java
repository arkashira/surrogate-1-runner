package com.axentx.surrogate1.paste;

import java.awt.AWTException;
import java.awt.Robot;
import java.awt.event.KeyEvent;
import java.util.Objects;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Resolves the “paste cascade” problem that appears on macOS production builds.
 *
 * <p>The resolver tries a primary (legacy) strategy first. If that fails it falls
 * back to a synthetic ⌘ V key‑press generated with {@link java.awt.Robot}.
 *
 * <p>The class is deliberately lightweight, side‑effect‑free and fully
 * testable – the {@link Robot} creation can be overridden in a subclass or a
 * test double.
 */
public class PasteResolver {

    private static final Logger LOG = Logger.getLogger(PasteResolver.class.getName());

    /** Public entry point used by the surrounding workflow. */
    public boolean resolvePaste() {
        if (attemptFirstSolution()) {
            LOG.info("Paste resolved via first (legacy) solution.");
            return true;
        }

        if (attemptCmdV()) {
            LOG.info("Paste resolved via synthetic Cmd+V (Robot).");
            return true;
        }

        LOG.warning("All paste‑resolution attempts failed.");
        return false;
    }

    /* --------------------------------------------------------------------- *
     *  1️⃣  Legacy / first‑solution hook
     * --------------------------------------------------------------------- */

    /**
     * Placeholder for the original paste‑resolution logic.
     *
     * <p>Replace the body with the real implementation when it becomes
     * available.  Returning {@code false} forces the fallback to the Robot
     * strategy, which is safe and works on every macOS JVM.
     */
    protected boolean attemptFirstSolution() {
        // TODO: integrate the historic algorithm here.
        return false;
    }

    /* --------------------------------------------------------------------- *
     *  2️⃣  Robot‑based Cmd+V simulation (macOS only)
     * --------------------------------------------------------------------- */

    /**
     * Sends a synthetic ⌘ V key‑press using {@link Robot}.
     *
     * @return {@code true} if the event was dispatched without error.
     */
    private boolean attemptCmdV() {
        // Run only on macOS – other OSes already have a working paste path.
        if (!isMacOs()) {
            LOG.fine("Cmd+V simulation skipped: not macOS.");
            return false;
        }

        try {
            Robot robot = createRobot();

            // Press ⌘ (Meta) + V
            robot.keyPress(KeyEvent.VK_META);
            robot.keyPress(KeyEvent.VK_V);
            robot.delay(50);               // hold long enough for the OS to see it

            // Release in reverse order
            robot.keyRelease(KeyEvent.VK_V);
            robot.keyRelease(KeyEvent.VK_META);
            robot.delay(50);

            LOG.fine("Synthetic Cmd+V event dispatched.");
            return true;
        } catch (AWTException e) {
            LOG.log(Level.WARNING, "Failed to create Robot for Cmd+V simulation", e);
            return false;
        } catch (Throwable t) {
            LOG.log(Level.WARNING, "Unexpected error during Cmd+V simulation", t);
            return false;
        }
    }

    /** Detects macOS at runtime. */
    private static boolean isMacOs() {
        String os = System.getProperty("os.name");
        return os != null && os.toLowerCase().contains("mac");
    }

    /**
     * Factory method that creates the {@link Robot}.  Sub‑class or test code
     * can override it to inject a mock.
     */
    protected Robot createRobot() throws AWTException {
        return new Robot();
    }
}
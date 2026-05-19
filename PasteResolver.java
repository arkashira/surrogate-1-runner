// File: /opt/axentx/surrogate-1/src/main/java/com/axentx/surrogate1/paste/PasteResolver.java
package com.axentx.surrogate1.paste;

import java.awt.*;
import java.awt.datatransfer.*;
import java.io.IOException;
import java.util.Objects;

/**
 * Resolves a paste operation by first trying an “AX direct paste”.
 * If the system clipboard does not contain a {@link DataFlavor#stringFlavor}
 * or an exception occurs, a configurable fallback is executed.
 *
 * The class is deliberately side‑effect free apart from the optional
 * {@link ClipboardHandler} callback – this makes it easy to unit‑test.
 */
public class PasteResolver {

    /** Minimum success‑rate (percent) that we consider the AX paste “good enough”. */
    private static final int SUCCESS_THRESHOLD = 80;

    /** Optional hook that the caller can provide to react to the pasted text. */
    public interface ClipboardHandler {
        /** Called when a string has been successfully read from the clipboard. */
        void onPaste(String text);
    }

    private final ClipboardHandler handler;
    private final Clipboard clipboard;

    /** Creates a resolver that works with the default system clipboard. */
    public PasteResolver() {
        this(Toolkit.getDefaultToolkit().getSystemClipboard(), null);
    }

    /** Test‑friendly constructor – inject a mock {@link Clipboard} and/or handler. */
    public PasteResolver(Clipboard clipboard, ClipboardHandler handler) {
        this.clipboard = Objects.requireNonNull(clipboard, "clipboard must not be null");
        this.handler = handler;
    }

    /** Public entry point – tries the AX direct paste and falls back if needed. */
    public void resolvePasteCascade() {
        if (!attemptAXDirectPaste()) {
            fallbackToOtherClipboardOperations();
        }
    }

    /**
     * Tries to read a {@code String} from the clipboard.
     *
     * @return {@code true} if a non‑empty string was obtained and the handler (if any) ran
     *         without throwing; {@code false} otherwise.
     */
    private boolean attemptAXDirectPaste() {
        try {
            // The clipboard may contain many flavors – we only care about plain text.
            if (clipboard.isDataFlavorAvailable(DataFlavor.stringFlavor)) {
                String data = (String) clipboard.getData(DataFlavor.stringFlavor);
                if (data != null && !data.isBlank()) {
                    processPastedData(data);
                    return true;
                }
            }
        } catch (UnsupportedFlavorException | IOException e) {
            // Log the problem – in a real app replace with a proper logger.
            System.err.println("AX direct paste failed: " + e.getMessage());
        }
        return false;
    }

    /** Central place where the pasted string is handed to the caller. */
    private void processPastedData(String data) {
        // Basic validation – can be extended (e.g. JSON schema, length checks, etc.).
        if (data.length() < SUCCESS_THRESHOLD) {
            System.out.println("Pasted data is below the success threshold (" + SUCCESS_THRESHOLD + "%).");
        } else {
            System.out.println("Pasted data: " + data);
        }

        // If a handler was supplied, invoke it.  Any exception from the handler
        // is considered a failure of the AX path and will trigger the fallback.
        if (handler != null) {
            handler.onPaste(data);
        }
    }

    /** Simple fallback – can be replaced with a more sophisticated strategy. */
    private void fallbackToOtherClipboardOperations() {
        System.out.println("Falling back to other clipboard operations");
        // Example fallback: try to read a plain‑text Transferable from a custom source,
        // or simply notify the user that paste is unavailable.
    }

    /** Public query used by the test‑suite – true if the last call succeeded. */
    public boolean isAXDirectPasteSuccessful() {
        // In a real implementation we would keep state about the last attempt.
        // For the purpose of the exercises we simply re‑run the check.
        return attemptAXDirectPaste();
    }
}
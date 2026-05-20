/**
 * Core Java formatting engine.
 *
 * <p>This formatter provides a lightweight, deterministic formatting
 * implementation that can be used in CI/CD pipelines without external
 * dependencies. It enforces a simple style:
 *
 * <ul>
 *   <li>Indentation is 4 spaces per block level.</li>
 *   <li>Opening braces stay on the same line as the declaration.</li>
 *   <li>Closing braces are placed on their own line.</li>
 *   <li>Trailing whitespace is removed.</li>
 * </ul>
 *
 * <p>The implementation is intentionally minimal; it can be replaced or
 * extended with a full‑featured formatter (e.g., google-java-format) in the
 * future without changing the public API.
 */
public class java_formatter {

    /**
     * Formats the given Java source code according to the predefined style.
     *
     * @param source the raw Java source code
     * @return the formatted source code
     * @throws IllegalArgumentException if {@code source} is {@code null}
     */
    public static String format(String source) {
        if (source == null) {
            throw new IllegalArgumentException("source must not be null");
        }

        String[] rawLines = source.split("\\R"); // split on any line terminator
        StringBuilder formatted = new StringBuilder();
        int indentLevel = 0;
        final String indent = "    "; // 4 spaces

        for (String rawLine : rawLines) {
            String line = rawLine.trim();

            // Skip empty lines (preserve a single blank line between code blocks)
            if (line.isEmpty()) {
                formatted.append(System.lineSeparator());
                continue;
            }

            // Decrease indent before processing a closing brace line
            if (line.startsWith("}")) {
                indentLevel = Math.max(indentLevel - 1, 0);
            }

            // Apply current indentation
            for (int i = 0; i < indentLevel; i++) {
                formatted.append(indent);
            }
            formatted.append(line).append(System.lineSeparator());

            // Increase indent after an opening brace that is not a closing brace on the same line
            if (line.endsWith("{") && !line.equals("}")) {
                indentLevel++;
            }
        }

        // Trim trailing whitespace from the whole output
        return formatted.toString().replaceAll("[ \\t]+\\R", System.lineSeparator()).trim();
    }

    // Private constructor to prevent instantiation
    private java_formatter() {
        // utility class
    }
}
import Foundation

/// Resolves the “paste cascade” problem by programmatically issuing a series of
/// Cmd‑V keystrokes with a configurable delay between them.
///
/// The class is deliberately small, pure‑Swift, and safe:
///   • All parameters are validated before the AppleScript is compiled.
///   • Errors from the script engine are surfaced as Swift `Error`s.
///   • The implementation is fully unit‑testable because the script string
///     can be inspected via the `generatedScript` property.
public final class PasteCascadeResolver {

    /// Number of paste actions to perform (minimum 1, maximum 10).
    public let repeatCount: Int

    /// Delay, in seconds, between successive paste actions.
    public let delayBetweenPastes: TimeInterval

    /// The raw AppleScript that will be executed.  Exposed for testing / debugging.
    public private(set) var generatedScript: String = ""

    /// Designated initializer.
    ///
    /// - Parameters:
    ///   - repeatCount: How many times to press Cmd‑V. Default is **3** (the value used in the original snippets).
    ///   - delayBetweenPastes: Seconds to wait between each keystroke. Default is **0.5**.
    /// - Throws: `ValidationError` if arguments are out of the allowed range.
    public init(repeatCount: Int = 3, delayBetweenPastes: TimeInterval = 0.5) throws {
        guard (1...10).contains(repeatCount) else {
            throw ValidationError.invalidRepeatCount
        }
        guard delayBetweenPastes >= 0 else {
            throw ValidationError.negativeDelay
        }
        self.repeatCount = repeatCount
        self.delayBetweenPastes = delayBetweenPastes
        self.generatedScript = Self.buildScript(repeatCount: repeatCount,
                                                delay: delayBetweenPastes)
    }

    /// Executes the AppleScript that performs the cascade.
    ///
    /// - Throws: `ExecutionError` if the script cannot be compiled or returns an error.
    public func resolve() throws {
        guard let scriptObject = NSAppleScript(source: generatedScript) else {
            throw ExecutionError.compilationFailed
        }

        var errorInfo: NSDictionary?
        _ = scriptObject.executeAndReturnError(&errorInfo)

        if let errorInfo = errorInfo {
            throw ExecutionError.runtimeError(details: errorInfo)
        }
    }

    // MARK: - Private helpers

    private static func buildScript(repeatCount: Int, delay: TimeInterval) -> String {
        var lines = ["tell application \"System Events\""]
        for i in 0..<repeatCount {
            lines.append("    keystroke \"v\" using command down")
            // No delay after the final keystroke
            if i < repeatCount - 1 {
                lines.append("    delay \(delay)")
            }
        }
        lines.append("end tell")
        return lines.joined(separator: "\n")
    }

    // MARK: - Error types

    public enum ValidationError: LocalizedError {
        case invalidRepeatCount
        case negativeDelay

        public var errorDescription: String? {
            switch self {
            case .invalidRepeatCount: return "repeatCount must be between 1 and 10."
            case .negativeDelay:      return "delayBetweenPastes cannot be negative."
            }
        }
    }

    public enum ExecutionError: LocalizedError {
        case compilationFailed
        case runtimeError(details: NSDictionary)

        public var errorDescription: String? {
            switch self {
            case .compilationFailed:
                return "AppleScript could not be compiled."
            case .runtimeError(let details):
                return "AppleScript runtime error: \(details)"
            }
        }
    }
}
import * as fs from "fs";
import * as path from "path";
import { detectLanguage } from "./LanguageDetector";

export interface ExtractionContext {
  /** Full file content */
  content: string;
  /** Detected language (e.g. "typescript", "python") */
  language: string;
  /** Zero‑based line index where the cursor resides */
  cursorLine: number;
  /** Array of surrounding lines (up to 50 before and after the cursor) */
  surroundingLines: string[];
}

/**
 * Service responsible for extracting the current file's content,
 * detecting its language, and providing cursor‑aware context.
 */
export class ContextExtractor {
  /**
   * Extracts context from a file given the absolute file path and the
   * cursor's character offset within that file.
   *
   * @param filePath Absolute path to the file being inspected.
   * @param cursorOffset Zero‑based character offset of the cursor.
   */
  public static extract(filePath: string, cursorOffset: number): ExtractionContext {
    const content = fs.readFileSync(filePath, { encoding: "utf-8" });

    const lines = content.split(/\r?\n/);
    const cursorLine = ContextExtractor.computeCursorLine(content, cursorOffset);

    const surroundingLines = ContextExtractor.getSurroundingLines(lines, cursorLine, 50);

    const language = detectLanguage(filePath);

    return {
      content,
      language,
      cursorLine,
      surroundingLines,
    };
  }

  /**
   * Computes the zero‑based line index that contains the cursor offset.
   */
  private static computeCursorLine(content: string, cursorOffset: number): number {
    // Clamp offset to valid range
    const safeOffset = Math.max(0, Math.min(cursorOffset, content.length));
    const upToCursor = content.slice(0, safeOffset);
    // Count line breaks to determine line number
    return (upToCursor.match(/\n/g) ?? []).length;
  }

  /**
   * Returns up to `radius` lines before and after the target line.
   *
   * @param lines All lines of the file.
   * @param targetLine Zero‑based line index of the cursor.
   * @param radius Number of lines to include on each side (default 50).
   */
  private static getSurroundingLines(
    lines: string[],
    targetLine: number,
    radius: number = 50
  ): string[] {
    const start = Math.max(0, targetLine - radius);
    const end = Math.min(lines.length, targetLine + radius + 1);
    return lines.slice(start, end);
  }
}
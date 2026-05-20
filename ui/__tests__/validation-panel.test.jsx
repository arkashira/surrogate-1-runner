import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import ValidationPanel from "../validation-panel";

describe("ValidationPanel", () => {
  test("renders textarea with sample manifest", () => {
    render(<ValidationPanel />);
    const textarea = screen.getByPlaceholderText(
      /paste your kubernetes yaml manifest/i
    );
    expect(textarea).toBeInTheDocument();
    expect(textarea.value).toContain("apiVersion: apps/v1");
  });

  test("shows error on invalid yaml", () => {
    render(<ValidationPanel />);
    const textarea = screen.getByPlaceholderText(
      /paste your kubernetes yaml manifest/i
    );
    fireEvent.change(textarea, { target: { value: "invalid: [unbalanced" } });
    const error = screen.getByText(/error:/i);
    expect(error).toBeInTheDocument();
    expect(error.textContent.toLowerCase()).toContain("unexpected");
  });

  test("shows parsed JSON on valid yaml", () => {
    render(<ValidationPanel />);
    const textarea = screen.getByPlaceholderText(
      /paste your kubernetes yaml manifest/i
    );
    // Use a tiny valid manifest
    const validYaml = `apiVersion: v1\nkind: Pod\nmetadata:\n  name: test-pod\nspec:\n  containers:\n    - name: busybox\n      image: busybox`;
    fireEvent.change(textarea, { target: { value: validYaml } });
    const parsed = screen.getByText(/parsed manifest/i);
    expect(parsed).toBeInTheDocument();
    expect(parsed.textContent).toContain('"kind": "Pod"');
  });
});
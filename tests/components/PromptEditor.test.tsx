import React from "react";
import { render, fireEvent, screen } from "@testing-library/react";
import PromptEditor from "../../src/components/PromptEditor";

describe("PromptEditor", () => {
  it("renders the prompt editor and displays the estimated cost", () => {
    render(<PromptEditor initialPrompt="Hello, world!" modelName="gpt-3.5-turbo" />);
    expect(screen.getByDisplayValue("Hello, world!")).toBeInTheDocument();
    expect(screen.getByText(/Estimated cost:/)).toBeInTheDocument();
  });

  it("updates the estimated cost when the prompt changes", () => {
    render(<PromptEditor initialPrompt="Hello, world!" modelName="gpt-3.5-turbo" />);
    const textarea = screen.getByDisplayValue("Hello, world!");
    fireEvent.change(textarea, { target: { value: "Hello, world! How are you?" } });
    expect(screen.getByText(/Estimated cost:/)).toBeInTheDocument();
  });
});
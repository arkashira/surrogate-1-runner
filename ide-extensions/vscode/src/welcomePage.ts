import * as vscode from 'vscode';

export function showWelcomePage() {
    const welcomeMessage = `
    Welcome to the Surrogate-1 VS Code Extension!

    Quickstart Guide:
    1. Open a JavaScript or TypeScript file.
    2. Start typing and get AI suggestions.
    3. Enjoy coding with AI assistance!

    For more details, visit our documentation.
    `;
    vscode.window.showInformationMessage(welcomeMessage);
}
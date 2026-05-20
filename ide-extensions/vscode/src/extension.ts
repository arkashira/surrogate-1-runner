import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    console.log('Congratulations, your extension "surrogate-1-vscode-extension" is now active!');

    const disposable = vscode.commands.registerCommand('extension.showWelcomePage', () => {
        vscode.window.showInformationMessage('Welcome to the Surrogate-1 VS Code Extension!');
        // Here you can add more detailed quickstart guide or open a welcome page
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}
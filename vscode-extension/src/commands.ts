import * as vscode from 'vscode';
import { exec } from 'child_process';

export function activate(context: vscode.ExtensionContext) {
    const disposable = vscode.commands.registerCommand('extension.installMissingImport', async (uri: vscode.Uri) => {
        const document = await vscode.workspace.openTextDocument(uri);
        const editor = vscode.window.activeTextEditor;

        if (!editor || !document) {
            return;
        }

        const selectedText = editor.document.getText(editor.selection);
        const packageName = selectedText.trim();

        if (packageName) {
            vscode.window.showInformationMessage(`Installing ${packageName}...`);
            exec(`npm install ${packageName}`, (error, stdout, stderr) => {
                if (error) {
                    vscode.window.showErrorMessage(`Failed to install ${packageName}: ${error.message}`);
                    return;
                }
                vscode.window.showInformationMessage(`Successfully installed ${packageName}`);
            });
        } else {
            vscode.window.showErrorMessage('No package name selected');
        }
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}
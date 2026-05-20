import * as vscode from 'vscode';
import { activate as commandsActivate, deactivate as commandsDeactivate } from './commands';
import { registerDiagnosticProvider } from './diagnosticProvider';

export function activate(context: vscode.ExtensionContext) {
    // Register diagnostic provider for .js and .ts files
    registerDiagnosticProvider(context);

    // Activate commands
    commandsActivate(context);
}

export function deactivate() {
    commandsDeactivate();
}
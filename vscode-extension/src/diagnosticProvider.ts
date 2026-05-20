import * as vscode from 'vscode';
import { TextDocument, Diagnostic, DiagnosticSeverity, Range } from 'vscode';

let diagnosticCollection: vscode.DiagnosticCollection;

export function registerDiagnosticProvider(context: vscode.ExtensionContext) {
    diagnosticCollection = vscode.languages.createDiagnosticCollection('missing-imports');
    context.subscriptions.push(diagnosticCollection);

    vscode.workspace.onDidOpenTextDocument(checkDocument);
    vscode.workspace.onDidChangeTextDocument(checkDocument);
}

function checkDocument(document: TextDocument) {
    const diagnostics: Diagnostic[] = [];

    // Dummy logic to simulate checking for missing imports
    if (document.languageId === 'javascript' || document.languageId === 'typescript') {
        const text = document.getText();
        if (text.includes('import') && !text.includes('from')) {
            const range = new Range(0, 0, 0, 10); // Adjust range based on actual logic
            diagnostics.push({
                severity: DiagnosticSeverity.Warning,
                range,
                message: 'Missing import statement',
                source: 'missing-imports'
            });
        }
    }

    diagnosticCollection.set(document.uri, diagnostics);
}
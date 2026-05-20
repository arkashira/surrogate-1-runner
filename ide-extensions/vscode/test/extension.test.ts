import * as vscode from 'vscode';
import { activate } from '../src/extension';

suite('Extension Tests', () => {
    test('should activate the extension', async () => {
        await activate(new vscode.ExtensionContext({}));
        // Add more tests as needed
    });
});
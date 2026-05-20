import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
	console.log('Congratulations, your extension "surrogate-1" is now active!');

	const disposable = vscode.commands.registerCommand('surrogate-1.showPrompt', () => {
		vscode.window.showInformationMessage('Daily conversation prompt: Practice your English skills with a short dialogue!', 'Start Session')
			.then(selection => {
				if (selection === 'Start Session') {
					// In a real implementation, this would start a session
					vscode.window.showInformationMessage('Starting conversation session...');
				}
			});
	});

	context.subscriptions.push(disposable);
}

export function deactivate() {}
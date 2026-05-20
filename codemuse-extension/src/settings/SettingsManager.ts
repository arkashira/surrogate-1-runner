import * as vscode from 'vscode';

export class SettingsManager {
  private static instance: SettingsManager;

  private constructor() {}

  public static getInstance(): SettingsManager {
    if (!SettingsManager.instance) {
      SettingsManager.instance = new SettingsManager();
    }
    return SettingsManager.instance;
  }

  public getEndpointUrl(): string {
    return vscode.workspace.getConfiguration('codemuse').get('endpointUrl', '');
  }

  public getSuggestionDepth(): string {
    return vscode.workspace.getConfiguration('codemuse').get('suggestionDepth', 'quick');
  }

  public saveSettings(settings: { endpointUrl: string; suggestionDepth: string }): void {
    vscode.workspace.getConfiguration('codemuse').update('endpointUrl', settings.endpointUrl, vscode.ConfigurationTarget.Global);
    vscode.workspace.getConfiguration('codemuse').update('suggestionDepth', settings.suggestionDepth, vscode.ConfigurationTarget.Global);
  }
}
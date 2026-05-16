const { contextBridge, ipcRenderer } = require('electron');

function readArgument(name) {
  const prefix = `--${name}=`;
  const match = process.argv.find((argument) => argument.startsWith(prefix));
  return match ? match.slice(prefix.length) : undefined;
}

contextBridge.exposeInMainWorld('llbDesktop', {
  apiBaseUrl: readArgument('llb-api-base-url') || 'http://localhost:8000',
  providerCredentials: {
    save: (credentials) => ipcRenderer.invoke('provider-credentials:save', credentials),
  },
});

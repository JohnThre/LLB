const { app, BrowserWindow, ipcMain, safeStorage } = require('electron');
const childProcess = require('node:child_process');
const fs = require('node:fs');
const http = require('node:http');
const net = require('node:net');
const path = require('node:path');

const {
  createControlToken,
  resolveBackendCommand,
  resolveFrontendEntry,
} = require('./backend-utils');

let backendProcess = null;
let backendBaseUrl = null;
let desktopControlToken = null;

function findOpenPort() {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    server.once('error', reject);
    server.listen(0, '127.0.0.1', () => {
      const address = server.address();
      server.close(() => resolve(address.port));
    });
  });
}

function waitForBackend(baseUrl, timeoutMs = 30000) {
  const startedAt = Date.now();
  return new Promise((resolve, reject) => {
    const poll = () => {
      http
        .get(`${baseUrl}/api/v1/health`, (response) => {
          response.resume();
          if (response.statusCode && response.statusCode < 500) {
            resolve();
            return;
          }
          retry();
        })
        .on('error', retry);
    };

    const retry = () => {
      if (Date.now() - startedAt > timeoutMs) {
        reject(new Error('Timed out waiting for backend'));
        return;
      }
      setTimeout(poll, 250);
    };

    poll();
  });
}

async function startBackend() {
  const appRoot = path.resolve(__dirname, '..', '..');
  const port = await findOpenPort();
  desktopControlToken = createControlToken();
  backendBaseUrl = `http://127.0.0.1:${port}`;
  const command = resolveBackendCommand({
    appRoot,
    resourcesPath: process.resourcesPath,
    isPackaged: app.isPackaged,
    platform: process.platform,
  });

  backendProcess = childProcess.spawn(command.command, [...command.args, '--port', String(port)], {
    cwd: command.cwd,
    env: {
      ...process.env,
      LLB_DESKTOP_CONTROL_TOKEN: desktopControlToken,
    },
    stdio: 'ignore',
  });

  backendProcess.once('exit', () => {
    backendProcess = null;
  });

  await waitForBackend(backendBaseUrl);
}

function encryptedCredentialsPath() {
  return path.join(app.getPath('userData'), 'provider-credentials.json');
}

function loadStoredCredentials() {
  const filePath = encryptedCredentialsPath();
  if (!safeStorage.isEncryptionAvailable() || !fs.existsSync(filePath)) {
    return {};
  }
  const encrypted = Buffer.from(fs.readFileSync(filePath, 'utf8'), 'base64');
  return JSON.parse(safeStorage.decryptString(encrypted));
}

function saveStoredCredentials(credentials) {
  if (!safeStorage.isEncryptionAvailable()) {
    throw new Error('OS credential encryption is unavailable');
  }
  const encrypted = safeStorage.encryptString(JSON.stringify(credentials));
  fs.writeFileSync(encryptedCredentialsPath(), encrypted.toString('base64'), {
    mode: 0o600,
  });
}

async function sendCredentialsToBackend(credentials) {
  const response = await fetch(`${backendBaseUrl}/api/v1/desktop/provider-credentials`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-llb-desktop-token': desktopControlToken,
    },
    body: JSON.stringify({ credentials }),
  });
  if (!response.ok) {
    throw new Error(`Backend rejected provider credentials: ${response.status}`);
  }
}

async function createMainWindow() {
  const mainWindow = new BrowserWindow({
    width: 1280,
    height: 860,
    minWidth: 960,
    minHeight: 640,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      additionalArguments: [`--llb-api-base-url=${backendBaseUrl}`],
    },
  });

  await mainWindow.loadFile(
    resolveFrontendEntry({
      appRoot: path.resolve(__dirname, '..', '..'),
      resourcesPath: process.resourcesPath,
      isPackaged: app.isPackaged,
    }),
  );
}

ipcMain.handle('provider-credentials:save', async (_event, credentials) => {
  const storedCredentials = {
    ...loadStoredCredentials(),
    ...credentials,
  };
  saveStoredCredentials(storedCredentials);
  await sendCredentialsToBackend(storedCredentials);
});

app.whenReady().then(async () => {
  await startBackend();
  await sendCredentialsToBackend(loadStoredCredentials());
  await createMainWindow();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  if (backendProcess) {
    backendProcess.kill();
    backendProcess = null;
  }
});

const crypto = require('node:crypto');
const path = require('node:path');

function createControlToken() {
  return crypto.randomBytes(32).toString('base64url');
}

function resolveBackendCommand(options) {
  const platform = options.platform || process.platform;
  if (options.isPackaged) {
    const executableName = platform === 'win32' ? 'llb-backend.exe' : 'llb-backend';
    return {
      command: path.join(options.resourcesPath, 'backend', executableName),
      args: [],
      cwd: path.join(options.resourcesPath, 'backend'),
    };
  }

  const pythonName = platform === 'win32' ? 'python.exe' : 'python';
  const pythonPath =
    platform === 'win32'
      ? path.join(options.appRoot, 'backend', 'llb-env', 'Scripts', pythonName)
      : path.join(options.appRoot, 'backend', 'llb-env', 'bin', pythonName);

  return {
    command: pythonPath,
    args: ['-m', 'uvicorn', 'app.desktop_main:app', '--host', '127.0.0.1'],
    cwd: path.join(options.appRoot, 'backend'),
  };
}

function resolveFrontendEntry(options) {
  if (options.isPackaged) {
    return path.join(options.resourcesPath, 'frontend', 'dist', 'index.html');
  }
  return path.join(options.appRoot, 'frontend', 'dist', 'index.html');
}

module.exports = {
  createControlToken,
  resolveBackendCommand,
  resolveFrontendEntry,
};

const assert = require('node:assert/strict');
const path = require('node:path');
const test = require('node:test');

const {
  createControlToken,
  resolveBackendCommand,
  resolveFrontendEntry,
} = require('../src/backend-utils');

test('createControlToken returns a high-entropy URL-safe token', () => {
  const token = createControlToken();

  assert.equal(typeof token, 'string');
  assert.ok(token.length >= 32);
  assert.match(token, /^[A-Za-z0-9_-]+$/);
});

test('resolveBackendCommand uses the dev Python backend outside packaged mode', () => {
  const command = resolveBackendCommand({
    appRoot: '/repo',
    isPackaged: false,
    platform: 'darwin',
  });

  assert.equal(command.command, path.join('/repo', 'backend', 'llb-env', 'bin', 'python'));
  assert.deepEqual(command.args, [
    '-m',
    'uvicorn',
    'app.desktop_main:app',
    '--host',
    '127.0.0.1',
  ]);
  assert.equal(command.cwd, path.join('/repo', 'backend'));
});

test('resolveBackendCommand uses bundled backend executable in packaged mode', () => {
  const command = resolveBackendCommand({
    resourcesPath: '/app/resources',
    isPackaged: true,
    platform: 'win32',
  });

  assert.equal(command.command, path.join('/app/resources', 'backend', 'llb-backend.exe'));
  assert.deepEqual(command.args, []);
});

test('resolveFrontendEntry points at the development Vite build entry', () => {
  assert.equal(
    resolveFrontendEntry({
      appRoot: '/repo',
      isPackaged: false,
    }),
    path.join('/repo', 'frontend', 'dist', 'index.html'),
  );
});

test('resolveFrontendEntry points at bundled frontend in packaged mode', () => {
  assert.equal(
    resolveFrontendEntry({
      resourcesPath: '/app/resources',
      isPackaged: true,
    }),
    path.join('/app/resources', 'frontend', 'dist', 'index.html'),
  );
});

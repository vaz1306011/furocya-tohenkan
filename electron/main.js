const { app, BrowserWindow } = require("electron");
const http = require("http");
const path = require("path");

function waitForServer(url, timeoutMs = 15000) {
  const start = Date.now();
  return new Promise((resolve, reject) => {
    const timer = setInterval(() => {
      http
        .get(url, (res) => {
          if (res.statusCode && res.statusCode >= 200) {
            clearInterval(timer);
            resolve();
          }
        })
        .on("error", () => {
          if (Date.now() - start > timeoutMs) {
            clearInterval(timer);
            reject(new Error("API server did not start in time"));
          }
        });
    }, 400);
  });
}

async function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  const url = process.env.API_URL || "http://127.0.0.1:8000/";
  try {
    await waitForServer(url);
    await win.loadURL(url);
  } catch (err) {
    await win.loadURL(
      `data:text/html,` +
        encodeURIComponent(
          `<h2>API server failed to start</h2><pre>${err.message}</pre>`
        )
    );
  }
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

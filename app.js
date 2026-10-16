"use strict";

const DB_NAME = "securify-local-vault";
const DB_VERSION = 1;
const PBKDF2_ITERATIONS = 600_000;
const MAX_FILE_BYTES = 25 * 1024 * 1024;
const VERIFIER_TEXT = "Securify local vault verifier v1";
const IDLE_LOCK_MS = 5 * 60 * 1000;
const encoder = new TextEncoder();
const decoder = new TextDecoder();

const CHECKLIST = [
  {
    id: "screen-lock",
    title: "Use a strong screen lock",
    detail: "In Android Settings → Security & privacy → Screen lock, use a strong PIN, password or supported biometric unlock. Avoid swipe-only access."
  },
  {
    id: "play-protect",
    title: "Keep Google Play Protect on",
    detail: "Open Play Store → your profile → Play Protect → Settings, and confirm app scanning is enabled. Play Protect is provided by Google, not Securify."
  },
  {
    id: "updates",
    title: "Install Android and security updates",
    detail: "Check Settings → System → Software update, and look for a Google Play system update under Security & privacy."
  },
  {
    id: "find-device",
    title: "Set up Google's lost-device service",
    detail: "Find My Device / Find Hub can help locate, secure or erase a compatible phone. Turn on location and confirm the device appears in your Google account."
  },
  {
    id: "backup",
    title: "Back up files you cannot replace",
    detail: "Keep a separate backup in a trusted location. Securify's vault is stored in this app's browser storage and can be erased if app data is cleared."
  }
];

const ICONS = {
  arrow: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"></path><path d="m13 6 6 6-6 6"></path></svg>',
  arrowUpRight: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7"></path><path d="M8 7h9v9"></path></svg>',
  lock: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="3"></rect><path d="M8 10V7a4 4 0 0 1 8 0v3"></path><path d="M12 14v3"></path></svg>',
  unlock: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="3"></rect><path d="M8 10V7a4 4 0 0 1 7.6-1.7"></path><path d="M12 14v3"></path></svg>',
  shield: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.5 19 6v5.2c0 4.4-2.8 7.5-7 9.3-4.2-1.8-7-4.9-7-9.3V6l7-2.5Z"></path><path d="m9 12 2 2 4-4"></path></svg>',
  file: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V10Z"></path><path d="M13 3v7h7"></path><path d="M8 14h8M8 17h6"></path></svg>',
  download: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12"></path><path d="m7 10 5 5 5-5"></path><path d="M5 19h14"></path></svg>',
  trash: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16"></path><path d="M10 11v6M14 11v6"></path><path d="m6 7 1 13h10l1-13M9 7V4h6v3"></path></svg>',
  eye: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2.5 12s3.4-6 9.5-6 9.5 6 9.5 6-3.4 6-9.5 6-9.5-6-9.5-6Z"></path><circle cx="12" cy="12" r="2.5"></circle></svg>',
  eyeOff: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m3 3 18 18"></path><path d="M10.6 6.2A10.8 10.8 0 0 1 12 6c6.1 0 9.5 6 9.5 6a16 16 0 0 1-3 3.6M6.2 6.4C3.8 8 2.5 12 2.5 12s3.4 6 9.5 6a10 10 0 0 0 3-.5"></path><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"></path></svg>',
  key: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="8" cy="15" r="4"></circle><path d="m11 12 8-8 2 2-2 2 2 2-3 3-2-2-2 2"></path></svg>',
  device: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="2.5" width="14" height="19" rx="3"></rect><path d="M10 18.5h4"></path><path d="m9 9 2 2 4-4"></path></svg>',
  phone: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="2.5" width="12" height="19" rx="2.5"></rect><path d="M10 18.5h4"></path></svg>',
  alert: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10.3 4.5 2.8 18a2 2 0 0 0 1.8 3h14.8a2 2 0 0 0 1.8-3L13.7 4.5a2 2 0 0 0-3.4 0Z"></path><path d="M12 9v4M12 17h.01"></path></svg>',
  check: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12 4 4L19 6"></path></svg>',
  external: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 4h6v6"></path><path d="m20 4-9 9"></path><path d="M18 13v5a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h5"></path></svg>',
  storage: '<svg viewBox="0 0 24 24" aria-hidden="true"><ellipse cx="12" cy="5" rx="8" ry="3"></ellipse><path d="M4 5v7c0 1.7 3.6 3 8 3 1.2 0 2.3-.1 3.3-.3M4 12v7c0 1.7 3.6 3 8 3 2.1 0 4-.4 5.7-1M20 12v2"></path><circle cx="18" cy="17" r="3"></circle></svg>',
  app: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="4"></rect><path d="M8 8h8M8 12h8M8 16h5"></path></svg>',
  cloud: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7.5 18.5H6a4 4 0 0 1-.2-8A6.5 6.5 0 0 1 18.5 9a4.8 4.8 0 0 1-.5 9.5h-1"></path><path d="M12 12v9m-3-3 3 3 3-3"></path></svg>',
  sparkle: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 3 1.4 5.6L19 10l-5.6 1.4L12 17l-1.4-5.6L5 10l5.6-1.4L12 3Z"></path><path d="m19 16 .7 2.3L22 19l-2.3.7L19 22l-.7-2.3L16 19l2.3-.7L19 16Z"></path></svg>'
};

const state = {
  page: "overview",
  db: null,
  dbError: "",
  vaultMeta: null,
  vaultKey: null,
  files: [],
  checks: {},
  busy: false,
  progress: "",
  installPrompt: null,
  idleTimer: null,
  persistentStorage: null
};

function icon(name) {
  return ICONS[name] || ICONS.file;
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  })[character]);
}

function isNativeAndroidApp() {
  return Boolean(window.SecurifyAndroid && typeof window.SecurifyAndroid.saveBase64 === "function");
}

function canUseCrypto() {
  return Boolean(window.isSecureContext && window.crypto && window.crypto.subtle && window.indexedDB);
}

function formatBytes(bytes) {
  const value = Number(bytes) || 0;
  if (value < 1024) return `${value} B`;
  if (value < 1024 * 1024) return `${(value / 1024).toFixed(value < 10 * 1024 ? 1 : 0)} KB`;
  if (value < 1024 * 1024 * 1024) return `${(value / (1024 * 1024)).toFixed(value < 10 * 1024 * 1024 ? 1 : 0)} MB`;
  return `${(value / (1024 * 1024 * 1024)).toFixed(1)} GB`;
}

function formatDate(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Date unavailable";
  return new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric", year: "numeric" }).format(date);
}

function sanitizeDownloadName(value) {
  const name = String(value || "protected-file").replace(/[\\/\u0000-\u001f\u007f]/g, "_").trim();
  return name || "protected-file";
}

function safeMimeType(value) {
  const mime = String(value || "application/octet-stream");
  return /^[a-z0-9!#$&^_.+-]+\/[a-z0-9!#$&^_.+-]+$/i.test(mime) ? mime : "application/octet-stream";
}

function showToast(message, kind = "success") {
  const region = document.getElementById("toast-region");
  const toast = document.createElement("div");
  toast.className = kind === "error" ? "toast is-error" : "toast";
  toast.setAttribute("role", kind === "error" ? "alert" : "status");
  toast.textContent = message;
  region.appendChild(toast);
  window.setTimeout(() => toast.remove(), 4800);
}

function setFormMessage(id, message, kind = "") {
  const element = document.getElementById(id);
  if (!element) return;
  element.textContent = message;
  element.classList.toggle("is-error", kind === "error");
  element.classList.toggle("is-success", kind === "success");
}

function openDatabase() {
  return new Promise((resolve, reject) => {
    if (!window.indexedDB) {
      reject(new Error("This browser does not support local storage required by Securify."));
      return;
    }
    const request = window.indexedDB.open(DB_NAME, DB_VERSION);
    request.onupgradeneeded = () => {
      const database = request.result;
      if (!database.objectStoreNames.contains("meta")) database.createObjectStore("meta", { keyPath: "key" });
      if (!database.objectStoreNames.contains("files")) database.createObjectStore("files", { keyPath: "id" });
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error || new Error("Could not open local vault storage."));
    request.onblocked = () => reject(new Error("Close other Securify tabs and try again."));
  });
}

function databaseRequest(storeName, mode, action) {
  return new Promise((resolve, reject) => {
    if (!state.db) {
      reject(new Error("Local vault storage is not available."));
      return;
    }
    const transaction = state.db.transaction(storeName, mode);
    const store = transaction.objectStore(storeName);
    let request;
    try {
      request = action(store);
    } catch (error) {
      reject(error);
      return;
    }
    let result;
    if (request) {
      request.onsuccess = () => { result = request.result; };
      request.onerror = () => reject(request.error || new Error("Local storage request failed."));
    }
    transaction.oncomplete = () => resolve(result);
    transaction.onerror = () => reject(transaction.error || new Error("Could not update local storage."));
    transaction.onabort = () => reject(transaction.error || new Error("Local storage update was interrupted."));
  });
}

function getRecord(storeName, key) {
  return databaseRequest(storeName, "readonly", (store) => store.get(key));
}

function getAllRecords(storeName) {
  return databaseRequest(storeName, "readonly", (store) => store.getAll());
}

function putRecord(storeName, record) {
  return databaseRequest(storeName, "readwrite", (store) => store.put(record));
}

function deleteRecord(storeName, key) {
  return databaseRequest(storeName, "readwrite", (store) => store.delete(key));
}

function bytesToBase64(bytes) {
  let binary = "";
  const chunkSize = 0x8000;
  for (let offset = 0; offset < bytes.length; offset += chunkSize) {
    binary += String.fromCharCode(...bytes.subarray(offset, offset + chunkSize));
  }
  return window.btoa(binary);
}

function base64ToBytes(value) {
  const binary = window.atob(String(value));
  const bytes = new Uint8Array(binary.length);
  for (let index = 0; index < binary.length; index += 1) bytes[index] = binary.charCodeAt(index);
  return bytes;
}

async function deriveVaultKey(passphrase, salt, iterations = PBKDF2_ITERATIONS) {
  const material = await window.crypto.subtle.importKey("raw", encoder.encode(passphrase), "PBKDF2", false, ["deriveKey"]);
  return window.crypto.subtle.deriveKey(
    { name: "PBKDF2", salt, iterations, hash: "SHA-256" },
    material,
    { name: "AES-GCM", length: 256 },
    false,
    ["encrypt", "decrypt"]
  );
}

function renderHeader() {
  const names = {
    overview: "Overview",
    vault: "Secure vault",
    checkup: "Device checkup",
    settings: "Settings & help"
  };
  const current = document.getElementById("topbar-current");
  if (current) current.textContent = names[state.page] || "Overview";
  document.querySelectorAll("[data-nav]").forEach((button) => {
    const active = button.dataset.nav === state.page;
    button.classList.toggle("is-active", active);
    if (active) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  });
  const lockButton = document.getElementById("header-lock-button");
  if (lockButton) lockButton.hidden = !state.vaultKey || state.busy;
  const installButton = document.getElementById("install-button");
  if (installButton) installButton.hidden = !state.installPrompt;
  const count = document.getElementById("nav-vault-count");
  if (count) {
    count.hidden = !state.vaultKey;
    count.textContent = String(state.files.length);
  }
}

function renderApp() {
  renderHeader();
  const main = document.getElementById("main-content");
  if (state.dbError) {
    main.innerHTML = renderFatal();
    return;
  }
  const renderers = {
    overview: renderOverview,
    vault: renderVault,
    checkup: renderCheckup,
    settings: renderSettings
  };
  main.innerHTML = (renderers[state.page] || renderOverview)();
  if (state.page === "settings") updateStorageEstimate();
}

function renderFatal() {
  return `<section class="fatal-panel">
    <div class="panel-icon">${icon("storage")}</div>
    <p class="eyebrow">LOCAL STORAGE UNAVAILABLE</p>
    <h1>We couldn't open Securify's private storage.</h1>
    <p class="intro">${escapeHtml(state.dbError)} Try the latest version of Chrome or another up-to-date browser. Your files are never sent to a server by this app.</p>
    <button class="button" type="button" data-action="reload">Try again ${icon("arrow")}</button>
  </section>`;
}

function renderOverview() {
  const done = Object.values(state.checks).filter(Boolean).length;
  const vaultStatus = state.vaultKey ? "Vault open" : state.vaultMeta ? "Vault locked" : "Not set up";
  const vaultDetail = state.vaultKey ? "Your passphrase is active in this session" : state.vaultMeta ? "Unlock to view protected items" : "Create a passphrase to get started";
  const protectedCount = state.vaultKey ? state.files.length : state.vaultMeta ? "Locked" : "0 files";
  const primaryLabel = state.vaultMeta ? "Open your vault" : "Create your vault";
  const vaultLinkLabel = state.vaultMeta ? "Open the secure vault" : "Set up the secure vault";
  const vaultDetailCard = state.vaultMeta
    ? "Unlock your vault to add, download or remove encrypted copies."
    : "Encrypt selected files with a passphrase only you know.";

  return `<section aria-labelledby="home-title">
    <div class="page-heading">
      <div class="page-heading-copy">
        <p class="eyebrow"><span class="eyebrow-dot"></span>YOUR PERSONAL SECURITY SPACE</p>
        <h1 id="home-title">More control. More peace of mind.</h1>
        <p class="intro">Protect the files you choose with an encrypted on-device vault, and build good Android security habits with a practical checklist.</p>
      </div>
    </div>

    <section class="hero-card" aria-label="Securify private file vault">
      <div class="hero-copy">
        <p class="hero-eyebrow"><span class="online-dot"></span> YOUR PRIVATE FILE SPACE</p>
        <h2>Keep sensitive files <span>close. Keep them private.</span></h2>
        <p class="hero-description">Securify encrypts copies of the files you select, right on this device. No account, no uploads — just a private space opened with your passphrase.</p>
        <div class="hero-actions">
          <button class="button button-primary" type="button" data-nav="vault">${escapeHtml(primaryLabel)} ${icon("arrow")}</button>
          <button class="button button-light" type="button" data-nav="checkup">Security checklist ${icon("arrowUpRight")}</button>
        </div>
        <p class="hero-proof">${icon("shield")} AES-256-GCM file encryption · passphrase never stored</p>
      </div>
      <div class="hero-art" aria-hidden="true">
        <span class="orbit orbit-one"></span><span class="orbit orbit-two"></span><span class="orbit orbit-three"></span>
        <span class="hero-glow"></span><span class="art-spark art-spark-one"></span><span class="art-spark art-spark-two"></span><span class="art-spark art-spark-three"></span>
        <span class="hero-shield"><img src="./icons/securify.svg" alt=""></span>
        <span class="art-status"><span class="online-dot"></span> ENCRYPTED ON THIS DEVICE</span>
      </div>
    </section>

    <div class="section-title-row">
      <div><h2>Your security at a glance</h2><p>A clear view of what Securify is doing for you.</p></div>
    </div>
    <section class="metrics-grid" aria-label="Security summary">
      <article class="metric-card"><span class="metric-icon">${icon("lock")}</span><div class="metric-copy"><p class="metric-label">Vault status</p><strong>${escapeHtml(vaultStatus)}</strong><span class="metric-detail">${escapeHtml(vaultDetail)}</span></div></article>
      <article class="metric-card"><span class="metric-icon">${icon("file")}</span><div class="metric-copy"><p class="metric-label">Files in your vault</p><strong>${escapeHtml(protectedCount)}</strong><span class="metric-detail">Only files you add are included</span></div></article>
      <article class="metric-card"><span class="metric-icon">${icon("device")}</span><div class="metric-copy"><p class="metric-label">Guided checkup</p><strong>${done} of ${CHECKLIST.length} complete</strong><span class="metric-detail">A checklist, not an automatic scan</span></div></article>
    </section>

    <div class="section-title-row">
      <div><h2>Make Securify work for you</h2><p>Start with the essentials, at your own pace.</p></div>
    </div>
    <section class="feature-grid" aria-label="Securify features">
      <article class="feature-card">
        <div class="feature-card-top"><span class="metric-icon">${icon("key")}</span><span class="feature-arrow">${icon("arrowUpRight")}</span></div>
        <h3>Private file vault</h3><p>${escapeHtml(vaultDetailCard)}</p>
        <button class="text-link" type="button" data-nav="vault">${escapeHtml(vaultLinkLabel)} ${icon("arrow")}</button>
      </article>
      <article class="feature-card">
        <div class="feature-card-top"><span class="metric-icon">${icon("shield")}</span><span class="feature-arrow">${icon("arrowUpRight")}</span></div>
        <h3>Android security checkup</h3><p>Review screen lock, Play Protect, updates, backups and Google's lost-device settings.</p>
        <button class="text-link" type="button" data-nav="checkup">Review the checklist ${icon("arrow")}</button>
      </article>
    </section>

    <aside class="boundary-note" aria-label="Important scope note">${icon("alert")}<p><strong>A clear promise, not an antivirus claim.</strong>Securify protects only the files you manually add to its vault. It cannot scan all Android files, block malware or hacks across the phone, or remotely locate or erase a stolen device. Use Android security features and Google Play Protect too. <button type="button" data-nav="settings">See what Securify can and can't do.</button></p></aside>
  </section>`;
}

function renderVault() {
  if (!canUseCrypto()) return renderVaultCryptoUnavailable();
  if (!state.vaultMeta) return renderVaultSetup();
  if (!state.vaultKey) return renderVaultUnlock();
  return renderVaultOpen();
}

function renderVaultCryptoUnavailable() {
  return `<section aria-labelledby="vault-title">
    <div class="page-heading"><div class="page-heading-copy"><p class="eyebrow"><span class="eyebrow-dot"></span>PRIVATE FILE VAULT</p><h1 id="vault-title">A private place for your files.</h1><p class="intro">Securify encrypts only the files you select. Encryption requires a secure browser connection and local storage support.</p></div></div>
    <div class="limit-note">${icon("alert")}<p><strong>Secure connection required</strong>Open Securify on HTTPS, or use localhost for development, in an up-to-date browser. The vault uses the browser's Web Crypto API and IndexedDB; it does not upload files.</p></div>
  </section>`;
}

function vaultSidePanel() {
  return `<aside class="vault-side-panel">
    <h3>What happens to your files?</h3>
    <p>Your passphrase derives an encryption key on this device. The key stays in memory only while the vault is unlocked.</p>
    <div class="security-feature"><span class="security-feature-icon">${icon("key")}</span><div><strong>A key only you know</strong><span>PBKDF2-SHA-256 derives an AES-256-GCM key from your passphrase.</span></div></div>
    <div class="security-feature"><span class="security-feature-icon">${icon("cloud")}</span><div><strong>No server or account</strong><span>File contents and names are encrypted before they enter local app storage.</span></div></div>
    <div class="security-feature"><span class="security-feature-icon">${icon("alert")}</span><div><strong>No password reset</strong><span>If you forget your passphrase, Securify cannot recover your vault.</span></div></div>
  </aside>`;
}

function renderVaultSetup() {
  return `<section aria-labelledby="vault-title">
    <div class="page-heading"><div class="page-heading-copy"><p class="eyebrow"><span class="eyebrow-dot"></span>PRIVATE FILE VAULT</p><h1 id="vault-title">A private place for your files.</h1><p class="intro">Create a passphrase to encrypt selected files on this device. Your files are not uploaded, and Securify cannot recover a forgotten passphrase.</p></div></div>
    <div class="vault-layout">
      <section class="panel vault-main-panel">
        <span class="panel-icon">${icon("lock")}</span>
        <h2 class="panel-title">Create your encrypted vault</h2>
        <p class="panel-description">Choose a long, memorable passphrase that you do not use anywhere else. It is never saved by Securify; you will need it each time you unlock the vault.</p>
        <form class="form-stack" id="vault-setup-form" novalidate>
          <div class="field-group"><label class="form-label" for="setup-passphrase">Passphrase</label>
            <span class="field-wrap"><input class="form-input" id="setup-passphrase" name="passphrase" type="password" minlength="12" maxlength="256" autocomplete="new-password" placeholder="At least 12 characters" required><button class="password-toggle" type="button" data-action="toggle-password" data-target="setup-passphrase" aria-label="Show passphrase">${icon("eye")}</button></span>
          </div>
          <p class="field-hint">Use 12 or more characters. A few unrelated words are easier to remember than a short, reused password.</p>
          <div class="field-group"><label class="form-label" for="setup-confirm">Confirm passphrase</label>
            <span class="field-wrap"><input class="form-input" id="setup-confirm" name="confirm" type="password" minlength="12" maxlength="256" autocomplete="new-password" placeholder="Enter it again" required><button class="password-toggle" type="button" data-action="toggle-password" data-target="setup-confirm" aria-label="Show confirmation">${icon("eye")}</button></span>
          </div>
          <label class="form-consent"><input id="setup-acknowledge" type="checkbox" required><span>I understand that forgetting this passphrase means the encrypted files cannot be recovered, and that clearing this app's data can delete the vault.</span></label>
          <p class="form-message" id="setup-message" role="status" aria-live="polite"></p>
          <button class="button form-submit" id="setup-submit" type="submit">Create my vault ${icon("arrow")}</button>
        </form>
      </section>
      ${vaultSidePanel()}
    </div>
  </section>`;
}

function renderVaultUnlock() {
  return `<section aria-labelledby="vault-title">
    <div class="page-heading"><div class="page-heading-copy"><p class="eyebrow"><span class="eyebrow-dot"></span>PRIVATE FILE VAULT</p><h1 id="vault-title">Your files are waiting.</h1><p class="intro">Enter your passphrase to unlock your encrypted vault on this device.</p></div></div>
    <div class="vault-layout">
      <section class="panel vault-main-panel">
        <div class="locked-state">
          <span class="panel-icon">${icon("lock")}</span>
          <h2 class="panel-title">Vault locked</h2>
          <p class="panel-description">Your encrypted files stay in local app storage while the vault is locked. Your passphrase is not stored.</p>
          <form class="form-stack" id="vault-unlock-form" novalidate>
            <div class="field-group"><label class="form-label" for="unlock-passphrase">Vault passphrase</label>
              <span class="field-wrap"><input class="form-input" id="unlock-passphrase" name="passphrase" type="password" maxlength="256" autocomplete="current-password" placeholder="Enter your passphrase" required><button class="password-toggle" type="button" data-action="toggle-password" data-target="unlock-passphrase" aria-label="Show passphrase">${icon("eye")}</button></span>
            </div>
            <p class="form-message" id="unlock-message" role="status" aria-live="polite"></p>
            <button class="button form-submit" id="unlock-submit" type="submit">Unlock vault ${icon("arrow")}</button>
          </form>
        </div>
      </section>
      ${vaultSidePanel()}
    </div>
  </section>`;
}

function fileRow(file) {
  const name = file.error ? "Protected item — details unavailable" : file.name;
  const meta = file.error
    ? `<span>This item could not be read</span>`
    : `<span>${formatBytes(file.size)}</span><span>${escapeHtml(formatDate(file.addedAt))}</span>`;
  return `<article class="file-row">
    <span class="file-type-icon">${icon("file")}</span>
    <div class="file-info"><p class="file-name" title="${escapeHtml(name)}">${escapeHtml(name)}</p><div class="file-meta">${meta}</div></div>
    <div class="file-actions">
      ${file.error ? "" : `<button class="icon-button" type="button" data-action="download-file" data-id="${escapeHtml(file.id)}" aria-label="Download ${escapeHtml(file.name)}" title="Download a decrypted copy" ${state.busy ? "disabled" : ""}>${icon("download")}</button>`}
      <button class="icon-button icon-button-danger" type="button" data-action="delete-file" data-id="${escapeHtml(file.id)}" aria-label="Delete ${escapeHtml(name)} from the vault" title="Delete encrypted copy" ${state.busy ? "disabled" : ""}>${icon("trash")}</button>
    </div>
  </article>`;
}

function renderVaultOpen() {
  const countLabel = `${state.files.length} ${state.files.length === 1 ? "item" : "items"} protected`;
  const fileMarkup = state.files.length
    ? state.files.map(fileRow).join("")
    : `<div class="empty-vault"><span class="empty-vault-icon">${icon("file")}</span><h3>Your vault is ready for its first file</h3><p>Add a copy from your device. Securify encrypts it here; the original stays where it is.</p></div>`;
  return `<section aria-labelledby="vault-title">
    <div class="page-heading-row">
      <div class="page-heading"><div class="page-heading-copy"><p class="eyebrow"><span class="eyebrow-dot"></span>PRIVATE FILE VAULT</p><h1 id="vault-title">Your private space.</h1><p class="intro">Only files you manually add are protected here. Add an encrypted copy, then keep the original or delete it yourself.</p></div></div>
      <button class="button button-outline button-lock" type="button" data-action="lock" ${state.busy ? "disabled" : ""}>${icon("lock")} Lock vault</button>
    </div>
    <div class="vault-layout">
      <section class="panel vault-open-panel" aria-label="Encrypted files">
        <div class="vault-open-head">
          <div class="vault-open-identity"><span class="panel-icon">${icon("lock")}</span><div><h2>Securify vault</h2><p>${escapeHtml(countLabel)} · AES-256-GCM</p></div></div>
          <span class="status-tag"><span class="online-dot"></span> Unlocked</span>
        </div>
        <div class="vault-toolbar"><div><h3>Protected items</h3><p>Each file is encrypted separately. Maximum 25 MB per file.</p></div><button class="button" type="button" data-action="choose-files" ${state.busy ? "disabled" : ""}>${icon("arrow")} Add files</button></div>
        <input class="file-input" id="file-picker" type="file" multiple tabindex="-1" aria-label="Choose files to add to the vault">
        <div class="progress-line" id="vault-progress" ${state.busy ? "" : "hidden"}>${icon("sparkle")}<span>${escapeHtml(state.progress || "Working securely…")}</span></div>
        <div class="file-list" aria-live="polite">${fileMarkup}</div>
        <div class="vault-disclaimer">${icon("alert")}<span>Adding a file creates an encrypted copy; it does not remove the original. Downloading makes a decrypted copy. Keep a separate backup and never forget your passphrase.</span></div>
      </section>
      <aside class="vault-side-panel">
        <h3>Vault safety notes</h3>
        <p>These protections apply to this vault only. Your Android files outside it remain under the usual Android app permissions.</p>
        <div class="security-feature"><span class="security-feature-icon">${icon("key")}</span><div><strong>Passphrase-derived key</strong><span>The AES-256 key is created locally and held in memory only while unlocked.</span></div></div>
        <div class="security-feature"><span class="security-feature-icon">${icon("cloud")}</span><div><strong>Local browser storage</strong><span>Files are not uploaded. Clearing app data or uninstalling can erase this vault.</span></div></div>
        <div class="security-feature"><span class="security-feature-icon">${icon("alert")}</span><div><strong>Auto-lock after inactivity</strong><span>Securify locks after five minutes without activity. You can also lock it now.</span></div></div>
      </aside>
    </div>
  </section>`;
}

function renderCheckup() {
  const complete = CHECKLIST.filter((item) => state.checks[item.id]).length;
  const percent = Math.round((complete / CHECKLIST.length) * 100);
  const checkRows = CHECKLIST.map((item) => `<label class="check-row">
    <input type="checkbox" name="check-item" value="${escapeHtml(item.id)}" ${state.checks[item.id] ? "checked" : ""}>
    <span class="check-copy"><strong>${escapeHtml(item.title)}</strong><span>${escapeHtml(item.detail)}</span></span>
  </label>`).join("");
  const lostDeviceLink = isNativeAndroidApp()
    ? `<button class="button button-primary" type="button" data-action="open-find-device">Open Find My Device ${icon("external")}</button>`
    : `<a class="button button-primary" href="https://www.google.com/android/find/" target="_blank" rel="noopener noreferrer">Open Find My Device ${icon("external")}</a>`;

  return `<section aria-labelledby="checkup-title">
    <div class="page-heading"><div class="page-heading-copy"><p class="eyebrow"><span class="eyebrow-dot"></span>GUIDED DEVICE CHECKUP</p><h1 id="checkup-title">Small checks. Stronger habits.</h1><p class="intro">Use this practical guide to review Android's built-in protections. Mark an item only after checking it on your phone.</p></div></div>
    <div class="checkup-summary"><span class="progress-ring" aria-label="${percent}% complete">${percent}%</span><div><h2>${complete === CHECKLIST.length ? "Your checklist is complete" : `${complete} of ${CHECKLIST.length} checks completed`}</h2><p>${complete === CHECKLIST.length ? "Nice work. Keep your phone and apps up to date." : "Your progress is saved on this device, not sent to Securify."}</p></div><span class="summary-status">${complete === CHECKLIST.length ? "UP TO DATE" : "SELF-CHECK"}</span></div>
    <div class="checkup-layout">
      <section class="panel checklist-panel" aria-label="Android security checklist">
        <div class="panel-section-heading"><div><h2>Android essentials</h2><p>These steps use settings provided by Android and Google.</p></div></div>
        ${checkRows}
      </section>
      <aside class="guide-side">
        <section class="guide-card lost-phone-card">
          <h3>If your phone goes missing</h3>
          <p>Use Google's official lost-device service from another trusted device to try to locate, secure or erase your phone. Availability depends on your settings and device.</p>
          ${lostDeviceLink}
          <p class="small-note">Remote erase is permanent. Use it only if you have decided recovery is not possible.</p>
        </section>
        <div class="limit-note">${icon("alert")}<p><strong>This is a guide, not a scan.</strong>Securify cannot inspect Android settings, detect malware, block network attacks, or remotely locate or wipe your phone. Google Play Protect and Android's own security updates remain important.</p></div>
        <section class="guide-card"><h3>Keep a recovery plan</h3><p>Know how to reach your Google account from another device, save your carrier's support number, and keep backups of irreplaceable files in a separate trusted place.</p></section>
      </aside>
    </div>
  </section>`;
}

function renderSettings() {
  const vaultStatus = state.vaultKey ? "Unlocked" : state.vaultMeta ? "Locked" : "Not set up";
  const storageMessage = "Checking browser storage…";
  const nativeApp = isNativeAndroidApp();
  const installMode = nativeApp ? "Installed Android app" : isInstalled() ? "Installed app mode" : "Installable web app (PWA)";
  const installInstructions = nativeApp
    ? "Securify is installed as an Android app. Its private vault is stored locally on this device."
    : isInstalled()
      ? "Securify is running as an installed web app on this device."
      : "This project is an installable web app (PWA), not an APK or Play Store listing. Install it from an HTTPS address in Chrome.";
  const installSteps = nativeApp ? "" : `<div class="install-instructions">
          <div class="install-step"><span class="install-step-number">1</span><p><strong>Open the secure address</strong><br>Visit this app over HTTPS in Chrome on your Android phone.</p></div>
          <div class="install-step"><span class="install-step-number">2</span><p><strong>Use Chrome's menu</strong><br>Tap ⋮ → Install app, or Add to Home screen, then confirm.</p></div>
        </div>`;
  const installAction = nativeApp ? "" : `<div class="settings-actions"><button class="button button-outline" type="button" data-action="install">${icon("arrowUpRight")} ${state.installPrompt ? "Install Securify" : "Show install help"}</button></div>`;
  return `<section aria-labelledby="settings-title">
    <div class="page-heading"><div class="page-heading-copy"><p class="eyebrow"><span class="eyebrow-dot"></span>YOUR APP, YOUR CHOICES</p><h1 id="settings-title">Settings &amp; help.</h1><p class="intro">Understand how the vault works, install Securify on Android, and know exactly what this app can and cannot protect.</p></div></div>
    <div class="settings-grid">
      <section class="settings-card">
        <div class="settings-card-heading"><span class="metric-icon">${icon("lock")}</span><div><h2>Vault &amp; storage</h2><p>Your encrypted files stay in this browser's app storage.</p></div></div>
        <div class="settings-line"><div class="settings-line-copy"><strong>Vault status</strong><span>Passphrase is never saved by Securify.</span></div><span class="settings-value">${escapeHtml(vaultStatus)}</span></div>
        <div class="settings-line"><div class="settings-line-copy"><strong>App storage on this origin</strong><span>This estimate may include other Securify app data.</span></div><span class="settings-value storage-value" id="storage-value">${storageMessage}</span></div>
        <div class="settings-actions"><button class="button button-outline" type="button" data-nav="vault">${state.vaultKey ? "Manage vault" : state.vaultMeta ? "Unlock vault" : "Create a vault"} ${icon("arrow")}</button>${state.vaultKey ? `<button class="button button-outline" type="button" data-action="lock">${icon("lock")} Lock now</button>` : ""}</div>
      </section>

      <section class="settings-card">
        <div class="settings-card-heading"><span class="metric-icon">${icon("device")}</span><div><h2>Install on Android</h2><p>${escapeHtml(installMode)}</p></div></div>
        <p class="field-hint">${escapeHtml(installInstructions)}</p>
        ${installSteps}
        ${installAction}
      </section>

      <section class="settings-card settings-card-wide">
        <div class="settings-card-heading"><span class="metric-icon">${icon("shield")}</span><div><h2>What Securify protects — and what it doesn't</h2><p>Honest boundaries are part of safer security software.</p></div></div>
        <ul class="privacy-bullets">
          <li>${icon("check")}<span><strong>Protects:</strong> file copies you manually select, using AES-256-GCM encryption derived from your passphrase. File contents and names are encrypted; someone inspecting browser storage may still infer the number of items and their approximate sizes.</span></li>
          <li>${icon("check")}<span><strong>Does not protect:</strong> the rest of your phone's storage, apps, messages, network traffic or Android system. Securify is not an antivirus, malware scanner, firewall or remote anti-theft service.</span></li>
          <li>${icon("check")}<span><strong>Runs locally:</strong> the app has no account or file-upload feature. The checklist is saved in local browser storage. No analytics or third-party scripts are included.</span></li>
          <li>${icon("alert")}<span><strong>Recovery matters:</strong> forgetting the passphrase makes the vault unrecoverable. Clearing browser/app data or uninstalling may delete encrypted files. Keep separate backups.</span></li>
        </ul>
        <a class="text-link" href="./privacy.html">Read the full privacy policy ${icon("arrowUpRight")}</a>
      </section>

      <section class="settings-card settings-card-wide">
        <div class="settings-card-heading"><span class="metric-icon">${icon("app")}</span><div><h2>About Securify</h2><p>App information</p></div></div>
        <div class="settings-line"><div class="settings-line-copy"><strong>App name</strong><span>Personal file vault and Android security guide</span></div><span class="settings-value">Securify</span></div>
        <div class="settings-line"><div class="settings-line-copy"><strong>Developer</strong><span>Privacy-first personal security app</span></div><span class="settings-value">Securify</span></div>
        <div class="settings-line"><div class="settings-line-copy"><strong>Version</strong><span>${nativeApp ? "Android app" : "Web app"}</span></div><span class="settings-value">1.0.0</span></div>
      </section>
    </div>
  </section>`;
}

function isInstalled() {
  return Boolean(isNativeAndroidApp() || (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches) || window.navigator.standalone === true);
}

async function updateStorageEstimate() {
  const target = document.getElementById("storage-value");
  if (!target) return;
  if (!navigator.storage || typeof navigator.storage.estimate !== "function") {
    target.textContent = "Not available";
    return;
  }
  try {
    const estimate = await navigator.storage.estimate();
    if (!document.getElementById("storage-value")) return;
    const used = Number(estimate.usage || 0);
    const total = Number(estimate.quota || 0);
    target.textContent = total ? `${formatBytes(used)} used of ${formatBytes(total)} quota` : `${formatBytes(used)} used`;
  } catch {
    target.textContent = "Not available";
  }
}

function loadChecklist() {
  try {
    const stored = JSON.parse(window.localStorage.getItem("securify-checklist-v1") || "{}");
    const validIds = new Set(CHECKLIST.map((item) => item.id));
    for (const [key, value] of Object.entries(stored)) {
      if (validIds.has(key)) state.checks[key] = Boolean(value);
    }
  } catch {
    state.checks = {};
  }
}

function saveChecklist() {
  try {
    window.localStorage.setItem("securify-checklist-v1", JSON.stringify(state.checks));
  } catch {
    showToast("This browser could not save checklist progress. The vault is separate.", "error");
  }
}

async function requestPersistentStorage() {
  if (!navigator.storage || typeof navigator.storage.persist !== "function") return;
  try {
    state.persistentStorage = await navigator.storage.persist();
  } catch {
    state.persistentStorage = false;
  }
}

async function handleVaultSetup(form) {
  if (!canUseCrypto()) {
    setFormMessage("setup-message", "Open Securify on a secure connection to create your vault.", "error");
    return;
  }
  const passphrase = document.getElementById("setup-passphrase").value;
  const confirmation = document.getElementById("setup-confirm").value;
  const submit = document.getElementById("setup-submit");
  if (passphrase.length < 12) {
    setFormMessage("setup-message", "Choose a passphrase with at least 12 characters.", "error");
    return;
  }
  if (passphrase !== confirmation) {
    setFormMessage("setup-message", "The passphrases do not match. Please try again.", "error");
    return;
  }
  if (!document.getElementById("setup-acknowledge").checked) {
    setFormMessage("setup-message", "Please confirm that you understand how passphrase and app-data recovery work.", "error");
    return;
  }

  submit.disabled = true;
  submit.textContent = "Creating vault…";
  setFormMessage("setup-message", "Deriving your encryption key on this device. This may take a moment.");
  try {
    const salt = window.crypto.getRandomValues(new Uint8Array(16));
    const key = await deriveVaultKey(passphrase, salt);
    const verifierIv = window.crypto.getRandomValues(new Uint8Array(12));
    const verifier = await window.crypto.subtle.encrypt({ name: "AES-GCM", iv: verifierIv }, key, encoder.encode(VERIFIER_TEXT));
    const record = {
      key: "vault",
      version: 1,
      kdf: "PBKDF2-SHA-256",
      iterations: PBKDF2_ITERATIONS,
      salt: bytesToBase64(salt),
      verifierIv: bytesToBase64(verifierIv),
      verifier,
      createdAt: new Date().toISOString()
    };
    await putRecord("meta", record);
    state.vaultMeta = record;
    state.vaultKey = key;
    state.files = [];
    state.busy = false;
    form.reset();
    await requestPersistentStorage();
    startIdleLock();
    state.page = "vault";
    renderApp();
    showToast("Your vault is ready. Add the files you want to protect.");
  } catch (error) {
    submit.disabled = false;
    submit.innerHTML = `Create my vault ${icon("arrow")}`;
    setFormMessage("setup-message", error && error.name === "QuotaExceededError" ? "There is not enough browser storage to create the vault." : "Securify could not create local vault storage. Check available device storage and try again.", "error");
  }
}

async function handleVaultUnlock(form) {
  if (!canUseCrypto() || !state.vaultMeta) return;
  const passphraseInput = document.getElementById("unlock-passphrase");
  const passphrase = passphraseInput.value;
  const submit = document.getElementById("unlock-submit");
  if (!passphrase) {
    setFormMessage("unlock-message", "Enter your vault passphrase to continue.", "error");
    return;
  }
  submit.disabled = true;
  submit.textContent = "Unlocking…";
  setFormMessage("unlock-message", "Checking your passphrase on this device.");
  try {
    if (state.vaultMeta.version !== 1 || state.vaultMeta.kdf !== "PBKDF2-SHA-256") throw new Error("Unsupported vault format.");
    const iterations = Number(state.vaultMeta.iterations);
    if (!Number.isInteger(iterations) || iterations < 100_000 || iterations > 1_000_000) throw new Error("Invalid vault key parameters.");
    const salt = base64ToBytes(state.vaultMeta.salt);
    const key = await deriveVaultKey(passphrase, salt, iterations);
    const verifierBytes = await window.crypto.subtle.decrypt(
      { name: "AES-GCM", iv: base64ToBytes(state.vaultMeta.verifierIv) },
      key,
      state.vaultMeta.verifier
    );
    const verifier = decoder.decode(verifierBytes);
    new Uint8Array(verifierBytes).fill(0);
    if (verifier !== VERIFIER_TEXT) throw new Error("Passphrase did not match.");
    state.vaultKey = key;
    state.busy = true;
    state.progress = "Opening your encrypted items…";
    await loadVaultFiles();
    state.busy = false;
    state.progress = "";
    form.reset();
    startIdleLock();
    renderApp();
    showToast("Vault unlocked on this device.");
  } catch {
    state.vaultKey = null;
    state.files = [];
    state.busy = false;
    state.progress = "";
    submit.disabled = false;
    submit.innerHTML = `Unlock vault ${icon("arrow")}`;
    setFormMessage("unlock-message", "That passphrase did not unlock the vault. Try again. Your encrypted files have not changed.", "error");
    passphraseInput.focus();
  }
}

async function loadVaultFiles() {
  const records = await getAllRecords("files");
  const files = [];
  for (const record of records) {
    try {
      const decryptedMetadata = await window.crypto.subtle.decrypt(
        { name: "AES-GCM", iv: base64ToBytes(record.metaIv), additionalData: encoder.encode(`securify-file-v1:${record.id}:metadata`) },
        state.vaultKey,
        record.metadataCiphertext
      );
      const metadata = JSON.parse(decoder.decode(decryptedMetadata));
      new Uint8Array(decryptedMetadata).fill(0);
      if (typeof metadata.name !== "string" || !Number.isFinite(Number(metadata.size))) throw new Error("Invalid metadata.");
      files.push({
        id: record.id,
        name: metadata.name,
        type: safeMimeType(metadata.type),
        size: Number(metadata.size),
        addedAt: metadata.addedAt
      });
    } catch {
      files.push({ id: record.id, name: "Protected item", size: 0, addedAt: "", error: true });
    }
  }
  files.sort((first, second) => new Date(second.addedAt || 0).getTime() - new Date(first.addedAt || 0).getTime());
  state.files = files;
}

function startIdleLock() {
  if (state.idleTimer) window.clearTimeout(state.idleTimer);
  if (!state.vaultKey) return;
  state.idleTimer = window.setTimeout(() => lockVault(true), IDLE_LOCK_MS);
}

function resetIdleLock() {
  if (state.vaultKey) startIdleLock();
}

function lockVault(notify = false) {
  if (!state.vaultKey) return;
  if (state.busy) {
    startIdleLock();
    return;
  }
  if (state.idleTimer) window.clearTimeout(state.idleTimer);
  state.idleTimer = null;
  state.vaultKey = null;
  state.files = [];
  state.busy = false;
  state.progress = "";
  renderApp();
  if (notify) showToast("Vault locked. Your files remain encrypted in local storage.");
}

async function estimateSpaceForFile(size) {
  if (!navigator.storage || typeof navigator.storage.estimate !== "function") return true;
  try {
    const estimate = await navigator.storage.estimate();
    if (Number.isFinite(estimate.quota) && Number.isFinite(estimate.usage)) {
      return size + 1024 * 1024 < Math.max(0, estimate.quota - estimate.usage);
    }
  } catch {
    return true;
  }
  return true;
}

async function handleAddFiles(fileList) {
  if (!state.vaultKey || state.busy || !fileList || fileList.length === 0) return;
  const files = Array.from(fileList);
  state.busy = true;
  state.progress = "Preparing encrypted copies…";
  renderApp();
  let added = 0;
  let skipped = 0;
  try {
    await requestPersistentStorage();
    for (let index = 0; index < files.length; index += 1) {
      const file = files[index];
      state.progress = `Encrypting item ${index + 1} of ${files.length}…`;
      renderApp();
      if (file.size > MAX_FILE_BYTES) {
        skipped += 1;
        continue;
      }
      if (!(await estimateSpaceForFile(file.size))) {
        skipped += 1;
        showToast(`Not enough estimated browser storage for “${file.name}”.`, "error");
        continue;
      }
      const id = window.crypto.randomUUID ? window.crypto.randomUUID() : `${Date.now()}-${bytesToBase64(window.crypto.getRandomValues(new Uint8Array(16))).replace(/[+/=]/g, "")}`;
      const addedAt = new Date().toISOString();
      const metadata = {
        name: file.name,
        type: safeMimeType(file.type),
        size: file.size,
        lastModified: file.lastModified || 0,
        addedAt
      };
      const metadataBytes = encoder.encode(JSON.stringify(metadata));
      const fileBytes = new Uint8Array(await file.arrayBuffer());
      const fileIv = window.crypto.getRandomValues(new Uint8Array(12));
      const metaIv = window.crypto.getRandomValues(new Uint8Array(12));
      try {
        const [fileCiphertext, metadataCiphertext] = await Promise.all([
          window.crypto.subtle.encrypt({ name: "AES-GCM", iv: fileIv, additionalData: encoder.encode(`securify-file-v1:${id}:file`) }, state.vaultKey, fileBytes),
          window.crypto.subtle.encrypt({ name: "AES-GCM", iv: metaIv, additionalData: encoder.encode(`securify-file-v1:${id}:metadata`) }, state.vaultKey, metadataBytes)
        ]);
        await putRecord("files", {
          id,
          fileIv: bytesToBase64(fileIv),
          fileCiphertext,
          metaIv: bytesToBase64(metaIv),
          metadataCiphertext
        });
        state.files.unshift({ id, ...metadata });
        added += 1;
      } finally {
        fileBytes.fill(0);
        metadataBytes.fill(0);
      }
    }
  } catch (error) {
    showToast(error && error.name === "QuotaExceededError" ? "Browser storage is full. Remove or download an item before trying again." : "Securify could not finish adding these files. Check device storage and try again.", "error");
  }
  state.busy = false;
  state.progress = "";
  renderApp();
  if (added > 0) showToast(`${added} ${added === 1 ? "file was" : "files were"} encrypted and added to your vault.`);
  if (skipped > 0) showToast(`${skipped} item${skipped === 1 ? " was" : "s were"} skipped. Each file must be 25 MB or smaller and fit in available app storage.`, "error");
}

async function handleDownload(id) {
  if (!state.vaultKey || state.busy) return;
  const file = state.files.find((item) => item.id === id);
  if (!file || file.error) return;
  state.busy = true;
  state.progress = `Decrypting ${file.name}…`;
  renderApp();
  try {
    const record = await getRecord("files", id);
    if (!record) throw new Error("The encrypted file could not be found.");
    const plaintextBuffer = await window.crypto.subtle.decrypt(
      { name: "AES-GCM", iv: base64ToBytes(record.fileIv), additionalData: encoder.encode(`securify-file-v1:${record.id}:file`) },
      state.vaultKey,
      record.fileCiphertext
    );
    const plaintext = new Uint8Array(plaintextBuffer);
    try {
      if (isNativeAndroidApp()) {
        window.SecurifyAndroid.saveBase64(sanitizeDownloadName(file.name), safeMimeType(file.type), bytesToBase64(plaintext));
        showToast(`Choose where to save the decrypted copy of ${file.name}. The encrypted vault item was not changed.`);
      } else {
        const blob = new Blob([plaintext], { type: safeMimeType(file.type) });
        const objectUrl = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = objectUrl;
        link.download = sanitizeDownloadName(file.name);
        link.rel = "noopener";
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.setTimeout(() => URL.revokeObjectURL(objectUrl), 60_000);
        showToast(`Decrypted copy downloaded: ${file.name}. The encrypted vault item was not changed.`);
      }
    } finally {
      plaintext.fill(0);
    }
  } catch {
    showToast("This item could not be decrypted. The vault item was not changed.", "error");
  } finally {
    state.busy = false;
    state.progress = "";
    renderApp();
  }
}

async function handleDeleteFile(id) {
  if (!state.vaultKey || state.busy) return;
  const file = state.files.find((item) => item.id === id);
  if (!file) return;
  const name = file.error ? "this unreadable protected item" : `“${file.name}”`;
  if (!window.confirm(`Delete ${name} from the Securify vault? This removes only the encrypted vault copy; the original file is unchanged.`)) return;
  try {
    await deleteRecord("files", id);
    state.files = state.files.filter((item) => item.id !== id);
    renderApp();
    showToast("Encrypted copy removed from the vault. The original file is unchanged.");
  } catch {
    showToast("Securify could not remove this item from local storage.", "error");
  }
}

async function handleInstall() {
  if (state.installPrompt) {
    const promptEvent = state.installPrompt;
    state.installPrompt = null;
    renderHeader();
    try {
      await promptEvent.prompt();
      const result = await promptEvent.userChoice;
      if (result && result.outcome === "accepted") showToast("Securify is being installed on this device.");
      else showToast("Installation was cancelled. You can install later from Chrome's menu.");
    } catch {
      showToast("Open Chrome's ⋮ menu and choose Install app or Add to Home screen.");
    }
    return;
  }
  if (isInstalled()) {
    showToast("Securify is already running as an installed app.");
    return;
  }
  showToast("On Android, open this HTTPS page in Chrome, tap ⋮, then choose Install app or Add to Home screen.");
}

function bindEvents() {
  document.addEventListener("click", (event) => {
    const navigation = event.target.closest("[data-nav]");
    if (navigation) {
      const nextPage = navigation.dataset.nav;
      if (["overview", "vault", "checkup", "settings"].includes(nextPage)) {
        state.page = nextPage;
        renderApp();
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
      return;
    }

    const actionButton = event.target.closest("[data-action]");
    if (!actionButton) return;
    const action = actionButton.dataset.action;
    if (action === "lock") {
      if (!state.busy) lockVault(true);
    } else if (action === "choose-files") {
      const picker = document.getElementById("file-picker");
      if (picker && !state.busy) picker.click();
    } else if (action === "download-file") {
      void handleDownload(actionButton.dataset.id);
    } else if (action === "delete-file") {
      void handleDeleteFile(actionButton.dataset.id);
    } else if (action === "toggle-password") {
      const input = document.getElementById(actionButton.dataset.target);
      if (input) {
        const showing = input.type === "password";
        input.type = showing ? "text" : "password";
        actionButton.innerHTML = icon(showing ? "eyeOff" : "eye");
        actionButton.setAttribute("aria-label", showing ? "Hide passphrase" : "Show passphrase");
      }
    } else if (action === "install") {
      void handleInstall();
    } else if (action === "open-find-device") {
      if (isNativeAndroidApp()) window.SecurifyAndroid.openFindMyDevice();
    } else if (action === "reload") {
      window.location.reload();
    }
  });

  document.addEventListener("submit", (event) => {
    if (event.target.id === "vault-setup-form") {
      event.preventDefault();
      void handleVaultSetup(event.target);
    } else if (event.target.id === "vault-unlock-form") {
      event.preventDefault();
      void handleVaultUnlock(event.target);
    }
  });

  document.addEventListener("change", (event) => {
    if (event.target.id === "file-picker") {
      const selected = Array.from(event.target.files || []);
      event.target.value = "";
      void handleAddFiles(selected);
    } else if (event.target.name === "check-item") {
      state.checks[event.target.value] = event.target.checked;
      saveChecklist();
      renderApp();
    }
  });

  document.addEventListener("pointerdown", resetIdleLock, { passive: true });
  document.addEventListener("keydown", resetIdleLock);
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) resetIdleLock();
  });

  window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    state.installPrompt = event;
    renderHeader();
    if (state.page === "settings") renderApp();
  });
  window.addEventListener("appinstalled", () => {
    state.installPrompt = null;
    renderHeader();
    if (state.page === "settings") renderApp();
    showToast("Securify was installed successfully.");
  });
}

async function init() {
  bindEvents();
  loadChecklist();
  try {
    state.db = await openDatabase();
    state.vaultMeta = await getRecord("meta", "vault") || null;
  } catch (error) {
    state.dbError = error && error.message ? error.message : "Local browser storage could not be opened.";
  }
  renderApp();
  if (!isNativeAndroidApp() && "serviceWorker" in navigator && window.isSecureContext) {
    navigator.serviceWorker.register("./sw.js", { scope: "./" }).catch(() => {
      // The app can still run online if offline installation is unavailable.
    });
  }
}

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", () => { void init(); }, { once: true });
else void init();

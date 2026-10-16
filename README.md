# Securify

Securify is a local Android file vault and security guide. The app name and developer name are **Securify**. It includes a native Android WebView app and a browser-installable PWA.

## Install the testing APK

The **Build Securify Android APK** workflow produces a debug APK at `artifacts/Securify-debug.apk` and uploads it as the `Securify-debug-apk` workflow artifact. Download it to an Android phone, open it, and approve Android's install confirmation. Android may ask you to allow installs from that file manager/browser.

This debug-signed build is for personal testing and sideloading; it is **not** a Play Store release. Debug builds use temporary CI signing keys and are not suitable for update continuity. Uninstalling an installed build may erase its local vault.

## Build locally

Requirements: JDK 17, Android SDK Platform 36, and internet access for Gradle/Android dependencies.

```sh
cd android
./gradlew assembleDebug
```

The debug APK is written to `app/build/outputs/apk/debug/app-debug.apk`; the debug package ID is `com.securify.app.debug`. The Play package ID is `com.securify.app`. The Android project copies shared web assets during its build; no server is needed on the phone.

## Prepare a Play Store release

The release build targets API 36 and builds a signed Android App Bundle (AAB) when the developer upload key is configured. See [`PLAY_STORE_RELEASE.md`](PLAY_STORE_RELEASE.md) for listing copy, privacy/Data Safety preparation and the exact release steps. The **Build Securify Play Store bundle** workflow expects the developer's upload keystore and passwords to be configured as GitHub Actions secrets; never commit or send those secrets in chat. No Play Console submission has been made.

## Optional PWA install

The PWA can be installed from an HTTPS static host. Open it in Android Chrome, tap **⋮ → Install app** or **Add to Home screen**, then confirm. Its static shell works offline after loading once. A plain HTTP address on a phone's local network does not enable secure cryptography or PWA installation.

## What Securify does

- Creates a local vault with a user-chosen passphrase. PBKDF2-HMAC-SHA-256 (600,000 iterations) derives an AES-256-GCM key. Each file and its identifying metadata are encrypted before the encrypted copy is written to local app storage. The item count and approximate file sizes can still be inferred from storage.
- Keeps the passphrase and derived key out of persistent storage. The derived key exists in memory only while the vault is unlocked; it locks after five minutes without activity or when locked manually.
- Uses Android's document picker for individual files. Adding a file creates an encrypted copy and does **not** remove the original. Downloading creates a decrypted copy; deleting a vault item does not delete the original.
- Provides a self-guided Android security checklist and an external link to Google's lost-device service.
- Has no account, analytics, third-party scripts or file-upload service. The PWA service worker caches only static app assets; vault data is stored locally.

## Important limits

Securify is **not full-device Android security software**. It cannot scan all phone storage, detect or block malware/worms across Android, protect other apps or network traffic, enforce a device screen lock, or remotely locate/lock/wipe a stolen phone. Use Android's own security features, Google Play Protect, OS updates, backups, and Google's lost-device service.

Only manually selected files are included; each is limited to 25 MB. Clearing app data or uninstalling may erase the encrypted vault. There is no password reset; forgetting the passphrase makes vault files unrecoverable. Keep separate backups of important originals. This local WebView/browser vault is not Android hardware-backed Keystore storage and cannot protect against a compromised device, browser, or operating system.

## Project files

- `index.html`, `styles.css`, `app.js`, `privacy.html` — app UI, vault and in-app privacy policy
- `android/` — native Android host, API 36 Gradle build, manifest and launcher icons
- `manifest.webmanifest`, `sw.js` — PWA installation and offline shell
- `.github/workflows/android-apk.yml` — testing APK build
- `.github/workflows/play-store-release.yml` — signed AAB build from protected Actions secrets
- `PLAY_STORE_RELEASE.md` — Play listing draft and remaining release gates
- `play-store-assets/` — 1024 × 500 feature graphic

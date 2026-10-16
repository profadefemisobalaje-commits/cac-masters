# Securify

Securify is a small Android app for encrypting files the user chooses and following a practical Android security checklist. The app name and developer name are **Securify**. The Android APK wraps the same local-first app UI in a native Android WebView shell; a browser-installable PWA is also included.

## Install the Android APK

A debug APK is produced by the **Build Securify Android APK** GitHub Actions workflow and uploaded as the `Securify-debug-apk` workflow artifact. Download `Securify-debug.apk` from a successful workflow run, transfer it to the phone, open it, and approve Android's install confirmation. Android may ask you to allow that file manager/browser to install apps from this source.

This is a debug-signed APK for personal testing and sideloading, not a Play Store release. A Play Store or public production release must be built and signed with the developer's own release key. Never commit that private key or its passwords.

## Build the APK locally

Requirements: JDK 17, Android SDK Platform 35, and internet access for Gradle/Android dependencies.

```sh
cd android
./gradlew assembleDebug
```

The APK is written to `android/app/build/outputs/apk/debug/app-debug.apk`. The debug package ID is `com.securify.app.debug`. The Android project copies the shared web app assets during the build; no web server is needed on the phone.

## Optional: install the PWA

The same app can be installed from an HTTPS static host without an APK. Open the HTTPS address in Android Chrome, tap **⋮ → Install app** or **Add to Home screen**, and confirm. The PWA's static app shell works offline after it has loaded once. A plain HTTP address on a phone's local network does not enable secure cryptography or PWA installation.

## What it does

- Creates a local vault with a user-chosen passphrase. A key is derived with PBKDF2-HMAC-SHA-256 (600,000 iterations), and AES-256-GCM encrypts each selected file and its name/type metadata before the encrypted data is written to local app storage. Browser storage can still reveal the item count and approximate file sizes.
- Keeps the passphrase and derived key out of persistent storage. The derived key exists only in memory while the vault is unlocked; the vault locks after five minutes of inactivity or when locked manually.
- Lets the user download a decrypted copy through Android's document picker, or delete the encrypted vault copy. Adding a file **does not** remove the original.
- Uses Android's file picker so the user selects individual files; Securify does not request broad storage access, location access, device-admin access, or accessibility access.
- Provides an explicitly self-guided Android security checklist and opens Google's lost-device service outside the app.
- Does not include an account, file-upload endpoint, analytics, third-party scripts, or remote fonts. The PWA service worker caches only the static app shell; vault data is kept in local app storage, not the service-worker cache.

## Important limits

Securify is a local file vault and security guide, **not full-device Android security software**. It cannot scan all phone storage, detect or block malware and worms across Android, protect other apps or network traffic, enforce a device screen lock, or remotely locate/lock/wipe a stolen phone. Use Android's own security features, Google Play Protect, OS updates, backups, and Google's lost-device service.

Only files the user manually selects are included. Each file is limited to 25 MB in this version. The encrypted vault remains in the app's local storage: clearing app data or uninstalling may erase it. There is no password reset; a forgotten passphrase makes the encrypted vault unrecoverable. Keep separate backups of important originals. When downloading, Securify creates a decrypted copy; protect that copy appropriately.

The vault requires an up-to-date Android WebView/browser, IndexedDB, and Web Crypto. A local browser vault is not equivalent to Android hardware-backed Keystore storage, and this app cannot guarantee protection against a compromised device, browser, or operating system.

## Project files

- `index.html`, `styles.css`, `app.js` — responsive app UI and encrypted local vault
- `android/` — Android WebView host, Gradle build, app manifest, and launcher icon
- `manifest.webmanifest`, `sw.js` — PWA install and offline shell
- `.github/workflows/android-apk.yml` — build and publish the installable debug APK artifact

# Securify — Google Play release preparation

## Status

- Android package ID: `com.securify.app` (confirm it is available in Play Console before the first submission; package IDs cannot be changed after publishing).
- Release variant targets Android 16 / API 36 and builds an Android App Bundle (AAB).
- A signed AAB workflow is ready, but **no Play Console submission has been made**. This repository has no Play Console connection, developer account, or upload keystore.
- The current `Securify-debug.apk` is for sideload testing only. It is not a Play Store upload.

## Draft listing

**App name:** Securify
**Category:** Tools
**Ads:** No
**Short description:** Encrypt selected files locally and follow Android security best practices.

**Full description:**

> Keep selected files private with a passphrase-protected vault that runs on your device.
>
> Securify lets you choose individual files using Android's document picker, encrypts each selected copy locally, and keeps the encrypted copy in this app's private storage. Unlock it with your passphrase when you need to download a decrypted copy or remove the encrypted item. Adding a file does not delete the original.
>
> A practical checklist helps you review Android's screen lock, Google Play Protect, updates, backups and Google's lost-device service.
>
> **Important:** Securify is not an antivirus, malware scanner, firewall or remote anti-theft service. It does not scan all phone storage, protect files outside its vault, or locate/lock/erase a stolen phone. Use Android's built-in protections and Google Play Protect.
>
> No account, ads, analytics or file-upload feature. The passphrase is not saved. Forgotten passphrases cannot be reset, and clearing app data or uninstalling may erase the encrypted vault. Keep separate backups of important originals.

**Support URL:** `https://github.com/profadefemisobalaje-commits/cac-masters/issues`
**Privacy policy:** publish `privacy.html` at a permanent public HTTPS URL before submission.
**App icon:** `icons/securify-512.png` (512 × 512).
**Feature graphic:** `play-store-assets/feature-graphic-1024x500.png` (1024 × 500).
**Phone screenshots:** still required for the store listing; capture real screenshots from the final Android build after testing.

## Data Safety declaration — draft only

Based on the current code path, Securify does not send vault files, filenames, passphrases, checklist answers, account identifiers or location to a Securify server. These items stay in local app storage. There is no account, analytics or advertising SDK. The lost-device action opens Google's service outside the app, where Google's own privacy practices apply.

A likely Data Safety response is **no data collected or shared by Securify**, but the Play Console form must be completed and attested by the developer after auditing the final APK and its dependencies. The app includes Android's `INTERNET` permission to load its local WebView asset origin; it blocks embedded remote resources and has no Securify backend. Do not submit a Data Safety answer without checking the actual release build.

## Signed AAB workflow

1. Create or select the developer's **upload keystore** locally. Enroll in Play App Signing in Play Console. Do not commit the keystore or send its password in chat.
2. In this repository's GitHub **Settings → Secrets and variables → Actions**, add:
   - `SECU_UPLOAD_KEYSTORE_BASE64` — base64-encoded upload keystore file
   - `SECU_UPLOAD_STORE_PASSWORD`
   - `SECU_UPLOAD_KEY_ALIAS`
   - `SECU_UPLOAD_KEY_PASSWORD`
3. Run **Build Securify Play Store bundle** on `arena/01c4b409-cac-masters`, entering the version code and version name. Every Play update must use a version code higher than the last uploaded one.
4. The workflow signs `bundleRelease`, verifies it, and publishes `artifacts/Securify-release.aab` and its SHA-256 checksum to the session branch and workflow artifact. Upload that AAB to Play Console.
5. Complete the Play Console store listing, privacy policy URL, Data Safety form, content rating, target audience and app-access declarations. Start internal/closed testing, then submit for review.

The workflow refuses to produce a release bundle if any signing secret is missing. The private keystore is decoded only into the ephemeral GitHub Actions runner's temporary directory and is not committed or uploaded.

## Remaining release gates

- A verified Google Play developer account and app registration are required; the Play Console cannot be accessed from this workspace.
- Publish the privacy page at a permanent public HTTPS URL and enter that URL in Play Console.
- Capture at least two current phone screenshots and complete the Play Console graphics/listing fields.
- Confirm `com.securify.app` is available; if not, change it before the first Play submission.
- Review the app, privacy policy and Data Safety form against the release AAB. Securify must not be described as scanning or protecting all phone files.
- If the developer account is a personal account created after 13 November 2023, Google currently requires a closed test with at least 12 opted-in testers for 14 continuous days before applying for production access.

## Policy references

- [Google Play target API level requirements](https://support.google.com/googleplay/android-developer/answer/11926878?hl=en) — new apps and updates must target API 36 from 31 August 2026.
- [Testing requirements for new personal developer accounts](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en).
- [Data Safety section requirements](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en).
- [Google Play user data and privacy policy requirements](https://support.google.com/googleplay/android-developer/answer/10144311?hl=en).

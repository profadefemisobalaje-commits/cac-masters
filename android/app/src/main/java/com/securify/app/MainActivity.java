package com.securify.app;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.util.Base64;
import android.view.View;
import android.view.Window;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import androidx.webkit.WebViewAssetLoader;

import java.io.ByteArrayInputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;
import java.util.regex.Pattern;

public final class MainActivity extends Activity {
    private static final int REQUEST_OPEN_FILES = 3101;
    private static final int REQUEST_SAVE_FILE = 3102;
    private static final int MAX_BASE64_CHARS = 36 * 1024 * 1024;
    private static final String ASSET_HOST = "appassets.androidplatform.net";
    private static final String FIND_DEVICE_URL = "https://www.google.com/android/find/";
    private static final String SUPPORT_URL = "https://github.com/profadefemisobalaje-commits/cac-masters/issues";
    private static final Pattern MIME_PATTERN = Pattern.compile("^[a-zA-Z0-9!#$&^_.+-]+/[a-zA-Z0-9!#$&^_.+-]+$");

    private WebView webView;
    private WebViewAssetLoader assetLoader;
    private ValueCallback<Uri[]> pendingFileSelection;
    private String pendingSaveName;
    private String pendingSaveMime;
    private String pendingSaveBase64;

    @SuppressLint({"SetJavaScriptEnabled", "JavascriptInterface"})
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Window window = getWindow();
        WindowCompat.setDecorFitsSystemWindows(window, false);
        window.setStatusBarColor(Color.TRANSPARENT);
        window.setNavigationBarColor(Color.TRANSPARENT);
        WindowInsetsControllerCompat insetsController = WindowCompat.getInsetsController(window, window.getDecorView());
        if (insetsController != null) {
            insetsController.setAppearanceLightStatusBars(true);
            insetsController.setAppearanceLightNavigationBars(true);
        }

        assetLoader = new WebViewAssetLoader.Builder()
                .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
                .build();

        webView = new WebView(this);
        webView.setBackgroundColor(Color.rgb(244, 247, 245));
        webView.setOverScrollMode(View.OVER_SCROLL_NEVER);
        webView.setScrollBarStyle(View.SCROLLBARS_INSIDE_OVERLAY);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(true);
        settings.setAllowFileAccessFromFileURLs(false);
        settings.setAllowUniversalAccessFromFileURLs(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setSupportMultipleWindows(false);
        settings.setJavaScriptCanOpenWindowsAutomatically(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);

        ViewCompat.setOnApplyWindowInsetsListener(webView, (view, windowInsets) -> {
            Insets safeInsets = windowInsets.getInsets(
                    WindowInsetsCompat.Type.systemBars() | WindowInsetsCompat.Type.displayCutout()
            );
            view.setPadding(safeInsets.left, safeInsets.top, safeInsets.right, safeInsets.bottom);
            return windowInsets;
        });

        webView.addJavascriptInterface(new SecurifyBridge(), "SecurifyAndroid");
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public android.webkit.WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                if (!"https".equalsIgnoreCase(uri.getScheme()) || !ASSET_HOST.equalsIgnoreCase(uri.getHost())) {
                    return blockedResponse();
                }
                android.webkit.WebResourceResponse asset = assetLoader.shouldInterceptRequest(uri);
                return asset == null ? blockedResponse() : asset;
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return handleNavigation(request.getUrl());
            }

            @SuppressWarnings("deprecation")
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return handleNavigation(Uri.parse(url));
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) {
                if (pendingFileSelection != null) pendingFileSelection.onReceiveValue(null);
                pendingFileSelection = filePathCallback;

                Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("*/*");
                intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
                try {
                    startActivityForResult(intent, REQUEST_OPEN_FILES);
                    return true;
                } catch (ActivityNotFoundException exception) {
                    pendingFileSelection = null;
                    filePathCallback.onReceiveValue(null);
                    Toast.makeText(MainActivity.this, "No compatible file picker is available.", Toast.LENGTH_LONG).show();
                    return true;
                }
            }
        });

        setContentView(webView);
        ViewCompat.requestApplyInsets(webView);
        webView.loadUrl("https://" + ASSET_HOST + "/assets/index.html");
    }

    private boolean handleNavigation(Uri uri) {
        if (uri == null) return true;
        String scheme = uri.getScheme() == null ? "" : uri.getScheme().toLowerCase(Locale.ROOT);
        String host = uri.getHost() == null ? "" : uri.getHost().toLowerCase(Locale.ROOT);
        if ("https".equals(scheme) && ASSET_HOST.equals(host)) return false;

        if ("https".equals(scheme)
                && "www.google.com".equals(host)
                && uri.getPath() != null
                && uri.getPath().startsWith("/android/find")) {
            openFindMyDevice();
            return true;
        }
        if ("https".equals(scheme)
                && "github.com".equals(host)
                && uri.getPath() != null
                && uri.getPath().startsWith("/profadefemisobalaje-commits/cac-masters/issues")) {
            try {
                startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(SUPPORT_URL)));
            } catch (ActivityNotFoundException exception) {
                Toast.makeText(this, "No browser is available to open the support page.", Toast.LENGTH_LONG).show();
            }
        }
        // The WebView remains a local app surface; other sites are never loaded in it.
        return true;
    }

    private static android.webkit.WebResourceResponse blockedResponse() {
        return new android.webkit.WebResourceResponse(
                "text/plain",
                "UTF-8",
                403,
                "Blocked by Securify",
                Collections.emptyMap(),
                new ByteArrayInputStream(new byte[0])
        );
    }

    private void openFindMyDevice() {
        try {
            startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(FIND_DEVICE_URL)));
        } catch (ActivityNotFoundException exception) {
            Toast.makeText(this, "No browser is available to open Google's lost-device service.", Toast.LENGTH_LONG).show();
        }
    }

    private static String safeFileName(String value) {
        if (value == null) return "securify-file";
        String safe = value.replaceAll("[\\\\/:*?\"<>|\\p{Cntrl}]", "_").trim();
        if (safe.isEmpty()) safe = "securify-file";
        return safe.length() > 180 ? safe.substring(0, 180) : safe;
    }

    private static String safeMimeType(String value) {
        if (value == null || !MIME_PATTERN.matcher(value).matches()) return "application/octet-stream";
        return value;
    }

    private void requestSaveFile(String name, String mime, String base64) {
        if (base64 == null || base64.length() > MAX_BASE64_CHARS) {
            Toast.makeText(this, "This file is too large to save through the app.", Toast.LENGTH_LONG).show();
            return;
        }
        if (pendingSaveBase64 != null) {
            Toast.makeText(this, "Finish the current save first.", Toast.LENGTH_SHORT).show();
            return;
        }

        pendingSaveName = safeFileName(name);
        pendingSaveMime = safeMimeType(mime);
        pendingSaveBase64 = base64;
        Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType(pendingSaveMime);
        intent.putExtra(Intent.EXTRA_TITLE, pendingSaveName);
        try {
            startActivityForResult(intent, REQUEST_SAVE_FILE);
        } catch (ActivityNotFoundException exception) {
            clearPendingSave();
            Toast.makeText(this, "No compatible file picker is available.", Toast.LENGTH_LONG).show();
        }
    }

    private void clearPendingSave() {
        pendingSaveName = null;
        pendingSaveMime = null;
        pendingSaveBase64 = null;
    }

    private void writeSavedFile(Uri destination, String fileName, String base64) {
        new Thread(() -> {
            byte[] bytes = null;
            boolean success = false;
            try {
                bytes = Base64.decode(base64, Base64.DEFAULT);
                try (OutputStream output = getContentResolver().openOutputStream(destination, "w")) {
                    if (output == null) throw new IllegalStateException("Could not open the chosen destination.");
                    output.write(bytes);
                    output.flush();
                }
                success = true;
            } catch (Exception exception) {
                // Keep the error user-friendly; file contents and passphrases are never logged.
            } finally {
                if (bytes != null) Arrays.fill(bytes, (byte) 0);
                final boolean saved = success;
                runOnUiThread(() -> Toast.makeText(
                        MainActivity.this,
                        saved ? "Saved " + fileName : "Could not save the decrypted file.",
                        Toast.LENGTH_LONG
                ).show());
            }
        }, "securify-save-file").start();
    }

    @SuppressWarnings("deprecation")
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == REQUEST_OPEN_FILES) {
            Uri[] selectedUris = null;
            if (resultCode == RESULT_OK && data != null) {
                if (data.getClipData() != null) {
                    int count = data.getClipData().getItemCount();
                    List<Uri> uris = new ArrayList<>(count);
                    for (int index = 0; index < count; index++) {
                        Uri uri = data.getClipData().getItemAt(index).getUri();
                        if (uri != null) uris.add(uri);
                    }
                    selectedUris = uris.toArray(new Uri[0]);
                } else if (data.getData() != null) {
                    selectedUris = new Uri[]{data.getData()};
                }
            }
            if (pendingFileSelection != null) {
                pendingFileSelection.onReceiveValue(selectedUris);
                pendingFileSelection = null;
            }
            return;
        }

        if (requestCode == REQUEST_SAVE_FILE) {
            String encoded = pendingSaveBase64;
            String name = pendingSaveName == null ? "securify-file" : pendingSaveName;
            clearPendingSave();
            if (resultCode == RESULT_OK && data != null && data.getData() != null && encoded != null) {
                writeSavedFile(data.getData(), name, encoded);
            } else if (resultCode != RESULT_OK) {
                Toast.makeText(this, "Save cancelled. The encrypted vault item is unchanged.", Toast.LENGTH_SHORT).show();
            }
        }
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onDestroy() {
        if (pendingFileSelection != null) {
            pendingFileSelection.onReceiveValue(null);
            pendingFileSelection = null;
        }
        clearPendingSave();
        if (webView != null) {
            webView.removeJavascriptInterface("SecurifyAndroid");
            webView.stopLoading();
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }

    private final class SecurifyBridge {
        @JavascriptInterface
        public void saveBase64(String fileName, String mimeType, String base64) {
            runOnUiThread(() -> requestSaveFile(fileName, mimeType, base64));
        }

        @JavascriptInterface
        public void openFindMyDevice() {
            runOnUiThread(MainActivity.this::openFindMyDevice);
        }
    }
}

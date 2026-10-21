package com.noorulislam.app;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.ConsoleMessage;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.util.Log;

public class MainActivity extends Activity {

    private WebView view;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        view = new WebView(this);

        WebSettings settings = view.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setJavaScriptCanOpenWindowsAutomatically(true);

        view.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedError(
                    WebView webView,
                    WebResourceRequest request,
                    WebResourceError error) {
                super.onReceivedError(webView, request, error);
                Log.e("NoorIslam", "WebView error: " + error.getDescription());
            }
        });

        view.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onConsoleMessage(ConsoleMessage message) {
                Log.e("NoorIslam", message.message()
                        + " | line: " + message.lineNumber());
                return true;
            }
        });

        view.setBackgroundColor(0xFFF4F7F2);
        setContentView(view);
        view.loadUrl("file:///android_asset/index.html");
    }

    @Override
    public void onBackPressed() {
        if (view != null && view.canGoBack()) {
            view.goBack();
        } else {
            super.onBackPressed();
        }
    }
}

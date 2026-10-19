package com.noorulislam.app;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebSettings;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        WebView view = new WebView(this);
        view.setWebViewClient(new WebViewClient());
        WebSettings settings = view.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        view.setBackgroundColor(0xFFF4F7F2);
        setContentView(view);
        view.loadUrl("file:///android_asset/index.html");
    }

    @Override
    public void onBackPressed() {
        WebView view = (WebView) findViewById(android.R.id.content).getRootView();
        super.onBackPressed();
    }
}

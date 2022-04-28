package com.example.thesispoc

import android.Manifest
import android.annotation.SuppressLint
import android.app.DownloadManager
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.util.Log
import android.webkit.WebSettings.LOAD_DEFAULT
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity


class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Declare buttons
        val startButton: Button = findViewById(R.id.startButton)
        val captureButton: Button = findViewById(R.id.captureButton)
        val downloadButton: Button = findViewById(R.id.downloadButton)

        // Set webView settings
        @SuppressLint("SetJavaScriptEnabled")
        val url = "http://192.168.1.4:5000/"
        val captureUrl = "http://192.168.1.4:5000/capture"
        val downloadUrl = "http://192.168.1.4:5000/downloads"
        val webView = findViewById<WebView>(R.id.webView)

        webView.webViewClient = WebViewClient()
        webView.settings.javaScriptCanOpenWindowsAutomatically = true
        webView.settings.javaScriptEnabled = true
        webView.settings.mediaPlaybackRequiresUserGesture = false
        webView.settings.domStorageEnabled = true
        webView.settings.cacheMode = LOAD_DEFAULT
        webView.settings.loadWithOverviewMode = true
        webView.settings.useWideViewPort = true

        //Runtime External storage permission for saving download files
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE)
                == PackageManager.PERMISSION_DENIED
            ) {
                Log.d("permission", "permission denied to WRITE_EXTERNAL_STORAGE - requesting it")
                val permissions = arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE)
                requestPermissions(permissions, 1)
            }
        }


        // Define click listeners
        startButton.setOnClickListener {
            Toast.makeText(this, "Starting ESP32-CAM...", Toast.LENGTH_LONG).show()
            webView.loadUrl(url)
        }


        captureButton.setOnClickListener {
            Toast.makeText(this, "Capturing frame...", Toast.LENGTH_LONG).show()
            webView.loadUrl(captureUrl)
        }

        downloadButton.setOnClickListener {
            webView.loadUrl(downloadUrl)
            // Downloader
            webView.setDownloadListener { url, _, _, _, _ ->
                val request = DownloadManager.Request(
                    Uri.parse(url)
                )
                request.allowScanningByMediaScanner()
                request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
                request.setDestinationInExternalPublicDir(
                    Environment.DIRECTORY_DOWNLOADS,
                    "frames.zip"
                )
                val dm = getSystemService(DOWNLOAD_SERVICE) as DownloadManager
                dm.enqueue(request)
                Toast.makeText(this, "Downloading file...", Toast.LENGTH_LONG).show()
            }
        }
    }
}
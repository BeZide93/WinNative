package com.winlator.cmod

import android.app.Application
import android.util.Log
import com.winlator.cmod.steam.events.EventDispatcher
import dagger.hilt.android.HiltAndroidApp

import com.winlator.cmod.steam.utils.PrefManager
import com.winlator.cmod.service.DownloadService

@HiltAndroidApp
class PluviaApp : Application() {
    override fun onCreate() {
        super.onCreate()
        instance = this
        
        // Init our datastore preferences.
        PrefManager.init(this)

        DownloadService.populateDownloadService(this)

        // Initialize process-wide reactive network state
        com.winlator.cmod.utils.NetworkMonitor.init(this)
        
        // Initialize database
        com.winlator.cmod.db.PluviaDatabase.init(this)

        // Start SteamService
        try {
            val intent = android.content.Intent(this, com.winlator.cmod.steam.service.SteamService::class.java)
            startForegroundService(intent)
        } catch (e: Exception) {
            Log.e("PluviaApp", "Failed to start SteamService", e)
        }

        Thread.setDefaultUncaughtExceptionHandler { thread, throwable ->
            Log.e("PluviaApp", "CRASH in thread ${thread.name}", throwable)
        }
    }

    companion object {
        lateinit var instance: PluviaApp
            private set
            
        @JvmField
        val events = EventDispatcher()
    }
}

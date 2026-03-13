package com.winlator.cmod

import android.app.Application
import android.util.Log
import com.winlator.cmod.steam.events.EventDispatcher
import dagger.hilt.android.HiltAndroidApp

import com.winlator.cmod.gog.service.GOGAuthManager
import com.winlator.cmod.gog.service.GOGConstants
import com.winlator.cmod.gog.service.GOGService
import com.winlator.cmod.steam.service.SteamService
import com.winlator.cmod.steam.utils.PrefManager
import com.winlator.cmod.service.DownloadService
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

@HiltAndroidApp
class PluviaApp : Application() {
    override fun onCreate() {
        super.onCreate()
        instance = this
        
        // Init our datastore preferences.
        PrefManager.init(this)
        GOGConstants.init(this)
        GOGAuthManager.updateLoginStatus(this)

        if (PrefManager.enableSteamLogs) {
            timber.log.Timber.plant(timber.log.Timber.DebugTree())
        }

        DownloadService.populateDownloadService(this)

        // Initialize process-wide reactive network state
        com.winlator.cmod.utils.NetworkMonitor.init(this)
        
        // Initialize database
        com.winlator.cmod.db.PluviaDatabase.init(this)

        CoroutineScope(Dispatchers.IO).launch {
            SteamService.repairInstalledMetadataFromDisk()
        }

        // Start SteamService only if setup is complete to avoid premature permission popups
        try {
            if (SetupWizardActivity.isSetupComplete(this)) {
                val intent = android.content.Intent(this, com.winlator.cmod.steam.service.SteamService::class.java)
                startForegroundService(intent)
                if (GOGAuthManager.isLoggedIn(this)) {
                    val gogIntent = android.content.Intent(this, GOGService::class.java)
                    startForegroundService(gogIntent)
                }
            }
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

package com.winlator.cmod;

import android.content.Context;

import com.winlator.cmod.steam.SteamClientManager;
import com.winlator.cmod.steam.service.SteamService;

/**
 * Java bridge to call Kotlin Steam classes without triggering KSP 
 * NullPointerException when scanning Java source files.
 */
public class SteamBridge {

    public static String getAppDirPath(int appId) {
        return SteamService.Companion.getAppDirPath(appId);
    }

    public static boolean extractSteam(Context context) {
        return SteamClientManager.extractSteam(context);
    }

    public static boolean isSteamDownloaded(Context context) {
        return SteamClientManager.isSteamDownloaded(context);
    }

    public static boolean isSteamInstalled(Context context) {
        return SteamClientManager.isSteamInstalled(context);
    }
}

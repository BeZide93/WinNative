package com.winlator.cmod.steam.utils

import android.annotation.SuppressLint
import android.content.Context
import android.provider.Settings
import com.winlator.cmod.steam.utils.PrefManager
import com.winlator.cmod.steam.data.DepotInfo
import com.winlator.cmod.steam.data.SteamApp
import com.winlator.cmod.steam.enums.Marker
import com.winlator.cmod.steam.enums.SpecialGameSaveMapping
import com.winlator.cmod.steam.service.SteamService
import `in`.dragonbra.javasteam.enums.EOSType
import `in`.dragonbra.javasteam.enums.EPersonaState
import `in`.dragonbra.javasteam.steam.handlers.steamapps.PICSRequest
import `in`.dragonbra.javasteam.types.SteamID
import java.io.File
import java.util.Locale
import okhttp3.OkHttpClient
import java.util.concurrent.TimeUnit
import timber.log.Timber

import com.winlator.cmod.container.Container

object SteamUtils {
    /**
     * Writes the ColdClientLoader.ini file for the Goldberg emulator.
     */
    @JvmStatic
    fun writeColdClientIni(steamAppId: Int, container: Container) {
        val gameName = SteamService.getAppDirName(SteamService.getAppInfoOf(steamAppId))
        val executablePath = container.executablePath.replace("/", "\\")
        val exePath = "steamapps\\common\\$gameName\\$executablePath"
        val exeCommandLine = container.execArgs
        val iniFile = File(container.getRootDir(), ".wine/drive_c/Program Files (x86)/Steam/ColdClientLoader.ini")
        iniFile.parentFile?.mkdirs()

        val injectionSection = """
                [Injection]
                IgnoreLoaderArchDifference=1
            """

        iniFile.writeText(
            """
                [SteamClient]

                Exe=$exePath
                ExeRunDir=
                ExeCommandLine=$exeCommandLine
                AppId=$steamAppId

                # path to the steamclient dlls, both must be set, absolute paths or relative to the loader directory
                SteamClientDll=steamclient.dll
                SteamClient64Dll=steamclient64.dll

                $injectionSection
            """.trimIndent(),
        )
    }

    val http: OkHttpClient by lazy {
        OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(60, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .callTimeout(5, TimeUnit.MINUTES)
            .pingInterval(30, TimeUnit.SECONDS)
            .retryOnConnectionFailure(true)
            .build()
    }

    /**
     * Gets the machine name to use for the user file sync.
     */
    @SuppressLint("HardwareIds")
    fun getMachineName(context: Context): String {
        val deviceName = Settings.Global.getString(context.contentResolver, Settings.Global.DEVICE_NAME)
        val androidId = Settings.Secure.getString(context.contentResolver, Settings.Secure.ANDROID_ID)

        return (deviceName ?: "Android Device") + " ($androidId)"
    }

    fun getPersonaState(state: Int): EPersonaState {
        return EPersonaState.from(state) ?: EPersonaState.Offline
    }

    fun getOSType(): EOSType {
        return EOSType.WinUnknown
    }

    fun getSteamId64(): Long = PrefManager.steamUserSteamId64

    fun getSteam3AccountId(): Int = PrefManager.steamUserAccountId

    /**
     * Maps a Steam language string to a GN Language enum.
     */
    fun getLanguage(steamLanguage: String): String {
        return steamLanguage.lowercase()
    }

    fun removeSpecialChars(s: String): String = s.filter { it.isLetterOrDigit() }

    fun getUniqueDeviceId(context: Context): Int {
        return Settings.Secure.getString(context.contentResolver, Settings.Secure.ANDROID_ID).hashCode()
    }
}

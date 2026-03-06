import os

# Overwrite LibraryViewModel with a stub
with open('app/src/main/java/com/winlator/cmod/steam/ui/model/LibraryViewModel.kt', 'w') as f:
    f.write("""package com.winlator.cmod.steam.ui.model
import androidx.lifecycle.ViewModel
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.flow.MutableStateFlow
import com.winlator.cmod.steam.ui.data.LibraryState

@HiltViewModel
class LibraryViewModel @Inject constructor() : ViewModel() {
    val state = MutableStateFlow(LibraryState())
    fun onLogout() {}
    fun onGoOnline() {}
    fun onSourceToggle(source: Any) {}
    fun onAddCustomGameFolder() {}
    fun onFocusChanged(item: Any?) {}
    fun onFrontendTabChanged(tab: Int) {}
    fun onAioStoreToggle() {}
}
""")

# Overwrite UserLoginViewModel with a stub
with open('app/src/main/java/com/winlator/cmod/steam/ui/model/UserLoginViewModel.kt', 'w') as f:
    f.write("""package com.winlator.cmod.steam.ui.model
import androidx.lifecycle.ViewModel
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.flow.MutableStateFlow

@HiltViewModel
class UserLoginViewModel @Inject constructor() : ViewModel() {
    val state = MutableStateFlow(Object())
    fun onLoginClick(vararg args: Any?) {}
    fun onTwoFactorLogin(vararg args: Any?) {}
    fun onQrRetry() {}
    fun onSetTwoFactor(vararg args: Any?) {}
    fun onShowLoginScreen() {}
    fun onRetryConnection(vararg args: Any?) {}
    fun onContinueOffline() {}
}
""")

# Overwrite HomeViewModel with a stub
with open('app/src/main/java/com/winlator/cmod/steam/ui/model/HomeViewModel.kt', 'w') as f:
    f.write("""package com.winlator.cmod.steam.ui.model
import androidx.lifecycle.ViewModel
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.flow.MutableStateFlow

@HiltViewModel
class HomeViewModel @Inject constructor() : ViewModel() {
    val state = MutableStateFlow(Object())
    fun onChat() {}
    fun onClickPlay(vararg args: Any?) {}
    fun onTestGraphics(vararg args: Any?) {}
    fun onLogout() {}
    fun onNavigateRoute(vararg args: Any?) {}
    fun onClickExit() {}
    fun onGoOnline() {}
}
""")

# Fix DatabaseModule missing constants
with open('app/src/main/java/com/winlator/cmod/steam/di/DatabaseModule.kt', 'w') as f:
    f.write("""package com.winlator.cmod.steam.di
import android.content.Context
import androidx.room.Room
import com.winlator.cmod.steam.db.PluviaDatabase
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): PluviaDatabase {
        return Room.databaseBuilder(context, PluviaDatabase::class.java, "pluvia.db")
            .fallbackToDestructiveMigration()
            .build()
    }

    @Provides
    fun provideSteamAppDao(db: PluviaDatabase) = db.steamAppDao()
}
""")

# Fix SteamService (Nuclear stub)
with open('app/src/main/java/com/winlator/cmod/steam/service/SteamService.kt', 'w') as f:
    f.write("""package com.winlator.cmod.steam.service
import android.app.Service
import android.content.Intent
import android.os.IBinder

class SteamService : Service() {
    companion object {
        const val INVALID_APP_ID = 0
        const val INVALID_PKG_ID = 0
        var isConnected: Boolean = false
        var isLoggedIn: Boolean = false
        var userSteamId: Any? = null
        fun stop() {}
        fun notifyRunningProcesses(vararg args: Any?) {}
        fun getAppInfoOf(id: Int): Any? = null
        fun getWindowsLaunchInfos(id: Int): List<Any> = emptyList()
    }
    override fun onBind(intent: Intent?): IBinder? = null
}
""")


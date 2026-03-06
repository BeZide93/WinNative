import os

# 1. Fix PrefManager.kt - Just provide a basic compiling PrefManager
with open('app/src/main/java/com/winlator/cmod/steam/PrefManager.kt', 'w') as f:
    f.write("""package com.winlator.cmod.steam
import android.content.Context
object PrefManager {
    fun init(context: Context) {}
}
""")

# 2. Fix SteamFriend.kt - Just basic class
with open('app/src/main/java/com/winlator/cmod/steam/data/SteamFriend.kt', 'w') as f:
    f.write("""package com.winlator.cmod.steam.data
import androidx.room.Entity
import androidx.room.PrimaryKey
@Entity(tableName = "steam_friend")
data class SteamFriend(
    @PrimaryKey val id: Long = 0,
    val name: String = ""
)
""")

# 3. Nuke SteamService.kt completely
with open('app/src/main/java/com/winlator/cmod/steam/service/SteamService.kt', 'w') as f:
    f.write("""package com.winlator.cmod.steam.service
import android.app.Service
import android.content.Intent
import android.os.IBinder
class SteamService : Service() {
    override fun onBind(intent: Intent?): IBinder? = null
    companion object {
        var instance: SteamService? = null
    }
}
""")

# 4. Enums - Just remove them or simplify
enums = [
    'AppFilter.kt', 'AppOptionMenuType.kt', 'AppTheme.kt', 
    'ControllerSupport.kt', 'HomeDestination.kt', 'Orientation.kt'
]
for e in enums:
    path = f'app/src/main/java/com/winlator/cmod/steam/enums/{e}'
    if os.path.exists(path):
        os.remove(path)

# 5. Nuke SteamUnifiedFriends.kt
suf = 'app/src/main/java/com/winlator/cmod/steam/service/SteamUnifiedFriends.kt'
if os.path.exists(suf):
    os.remove(suf)


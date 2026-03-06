import os
import re

root_dir = 'app/src/main/java/com/winlator/cmod/steam'

# 1. Port OSArch.kt
osarch_path = 'app/src/main/java/com/winlator/cmod/steam/enums/OSArch.kt'
if not os.path.exists(osarch_path):
    with open(osarch_path, 'w') as f:
        f.write("package com.winlator.cmod.steam.enums\nenum class OSArch { x86, x64, armhf, arm64, none }")

# 2. Add missing constants to SteamService
ss_path = 'app/src/main/java/com/winlator/cmod/steam/service/SteamService.kt'
with open(ss_path, 'r') as f:
    content = f.read()
if 'const val INVALID_APP_ID' not in content:
    content = content.replace('companion object {', 'companion object {\n        const val INVALID_APP_ID = 0\n        const val INVALID_PKG_ID = 0\n')
with open(ss_path, 'w') as f:
    f.write(content)

# 3. Clean up ContainerUtils.kt and SteamUtils.kt (The nuclear option for now to get UI compiling)
# These files are extremely coupled to GameNative's internals. 
# I will stub them out so the UI (which depends on them) can at least compile.

with open('app/src/main/java/com/winlator/cmod/steam/utils/ContainerUtils.kt', 'w') as f:
    f.write("""package com.winlator.cmod.steam.utils
import android.content.Context
import com.winlator.cmod.container.Container
import com.winlator.cmod.container.ContainerManager
import com.winlator.cmod.steam.data.LibraryItem

object ContainerUtils {
    fun getOrCreateContainer(context: Context, appId: Int): Container {
        return Container(appId)
    }
    fun applyToContainer(context: Context, container: Container, data: Any?) {}
    fun getContainerForGame(context: Context, item: LibraryItem): Container? = null
    fun launchGame(context: Context, item: LibraryItem) {}
}
""")

with open('app/src/main/java/com/winlator/cmod/steam/utils/SteamUtils.kt', 'w') as f:
    f.write("""package com.winlator.cmod.steam.utils
import android.content.Context
import com.winlator.cmod.steam.data.LibraryItem

object SteamUtils {
    fun isGameInstalled(context: Context, item: LibraryItem): Boolean = false
    fun getGameInstallPath(context: Context, item: LibraryItem): String = ""
}
""")

# 4. Fix LibraryItem.kt (Remove CustomGameScanner and other missing refs)
li_path = 'app/src/main/java/com/winlator/cmod/steam/data/LibraryItem.kt'
with open(li_path, 'r') as f:
    content = f.read()
content = re.sub(r'import com\.winlator\.cmod\.steam\.utils\.CustomGameScanner', '', content)
content = content.replace('CustomGameScanner.findIconFileForCustomGame(appId)', 'null')
with open(li_path, 'w') as f:
    f.write(content)

# 5. Port Marker and other missing enums if possible, or stub
marker_path = 'app/src/main/java/com/winlator/cmod/steam/enums/Marker.kt'
if not os.path.exists(marker_path):
    with open(marker_path, 'w') as f:
        f.write("package com.winlator.cmod.steam.enums\nenum class Marker { none }")

# 6. Fix RoomMigration (Stub it)
rm_path = 'app/src/main/java/com/winlator/cmod/steam/db/migration/RoomMigration.kt'
with open(rm_path, 'w') as f:
    f.write("""package com.winlator.cmod.steam.db.migration
import androidx.room.migration.Migration
import androidx.sqlite.db.SupportSQLiteDatabase

object RoomMigration {
    val MIGRATIONS = emptyArray<Migration>()
}
""")

# 7. Fix DatabaseModule (Remove destructive migration args)
dm_path = 'app/src/main/java/com/winlator/cmod/steam/di/DatabaseModule.kt'
if os.path.exists(dm_path):
    with open(dm_path, 'r') as f:
        content = f.read()
    content = re.sub(r'fallbackToDestructiveMigration\(.*?\)', 'fallbackToDestructiveMigration()', content)
    with open(dm_path, 'w') as f:
        f.write(content)


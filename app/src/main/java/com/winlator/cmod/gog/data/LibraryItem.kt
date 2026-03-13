package com.winlator.cmod.gog.data

import com.winlator.cmod.steam.enums.GameSource

data class LibraryItem(
    val appId: String,
    val name: String,
    val gameSource: GameSource,
) {
    val gameId: Int
        get() = appId.substringAfterLast("_", appId).toIntOrNull()
            ?: appId.toIntOrNull()
            ?: appId.hashCode()
}

import re

# Update Container.java
with open('app/src/main/java/com/winlator/cmod/container/Container.java', 'r') as f:
    content = f.read()

if 'private String executablePath = "";' not in content:
    content = content.replace('private String emulator;', 'private String emulator;\n    private String executablePath = "";\n    private String execArgs = "";')
    
    # Add getters and setters
    methods = """
    public String getExecutablePath() {
        return executablePath;
    }

    public void setExecutablePath(String executablePath) {
        this.executablePath = executablePath != null ? executablePath : "";
    }

    public String getExecArgs() {
        return execArgs;
    }

    public void setExecArgs(String execArgs) {
        this.execArgs = execArgs != null ? execArgs : "";
    }
    """
    content = content.replace('public ContainerManager getManager()', methods + '\n    public ContainerManager getManager()')

    # Update saveData
    content = content.replace('data.put("emulator", emulator);', 'data.put("emulator", emulator);\n            data.put("executablePath", executablePath);\n            data.put("execArgs", execArgs);')

    # Update loadData
    load_cases = """
                case "executablePath":
                    setExecutablePath(data.getString(key));
                    break;
                case "execArgs":
                    setExecArgs(data.getString(key));
                    break;"""
    content = content.replace('case "emulator":', load_cases + '\n                case "emulator":')

with open('app/src/main/java/com/winlator/cmod/container/Container.java', 'w') as f:
    f.write(content)

# Update ContainerData.kt
with open('app/src/main/java/com/winlator/cmod/container/ContainerData.kt', 'r') as f:
    content = f.read()

if 'val executablePath: String = "",' not in content:
    content = content.replace('val desktopTheme: String = WineThemeManager.DEFAULT_DESKTOP_THEME,', 'val desktopTheme: String = WineThemeManager.DEFAULT_DESKTOP_THEME,\n    val executablePath: String = "",\n    val execArgs: String = "",')
    
    content = content.replace('desktopTheme = json.optString("desktopTheme", WineThemeManager.DEFAULT_DESKTOP_THEME),', 'desktopTheme = json.optString("desktopTheme", WineThemeManager.DEFAULT_DESKTOP_THEME),\n                    executablePath = json.optString("executablePath", ""),\n                    execArgs = json.optString("execArgs", ""),')
    
    content = content.replace('desktopTheme = savedMap["desktopTheme"] as String,', 'desktopTheme = savedMap["desktopTheme"] as String,\n                    executablePath = savedMap["executablePath"] as String,\n                    execArgs = savedMap["execArgs"] as String,')

with open('app/src/main/java/com/winlator/cmod/container/ContainerData.kt', 'w') as f:
    f.write(content)

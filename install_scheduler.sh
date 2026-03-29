#!/bin/bash
# Installiert den macOS LaunchAgent fuer naechtliche Recherche (22:00 Start)

PLIST_NAME="com.klincov.recherche"
PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$(which python3)"

echo "=== Recherche_Tool Scheduler Setup ==="
echo "  Script: $SCRIPT_DIR/recherche.py"
echo "  Python: $PYTHON"
echo "  Plist:  $PLIST_PATH"
echo ""

cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_NAME}</string>
    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON}</string>
        <string>${SCRIPT_DIR}/recherche.py</string>
        <string>--now</string>
    </array>
    <key>WorkingDirectory</key>
    <string>${SCRIPT_DIR}</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>6</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>${SCRIPT_DIR}/recherche_launchd.log</string>
    <key>StandardErrorPath</key>
    <string>${SCRIPT_DIR}/recherche_launchd.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
EOF

# Load the agent
launchctl unload "$PLIST_PATH" 2>/dev/null
launchctl load "$PLIST_PATH"

echo "LaunchAgent installiert und geladen."
echo "Recherche laeuft jeden Tag um 06:00 automatisch."
echo ""
echo "Befehle:"
echo "  launchctl list | grep recherche    # Status pruefen"
echo "  launchctl unload $PLIST_PATH       # Deaktivieren"
echo "  launchctl load $PLIST_PATH         # Aktivieren"

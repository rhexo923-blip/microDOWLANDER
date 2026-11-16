import json

KNOWN_ICONS = {
    # Browsers & Comm
    "chrome": ("fa-brands fa-chrome", "#4285F4"),
    "firefox": ("fa-brands fa-firefox-browser", "#FF7139"),
    "brave": ("fa-solid fa-lion", "#FB542B"),
    "edge": ("fa-brands fa-edge", "#0078D7"),
    "opera": ("fa-brands fa-opera", "#FF1B2D"),
    "discord": ("fa-brands fa-discord", "#5865F2"),
    "telegram": ("fa-brands fa-telegram", "#26A5E4"),
    "whatsapp": ("fa-brands fa-whatsapp", "#25D366"),
    "spotify": ("fa-brands fa-spotify", "#1ED760"),
    "slack": ("fa-brands fa-slack", "#4A154B"),
    "zoom": ("fa-solid fa-video", "#2D8CFF"),
    "skype": ("fa-brands fa-skype", "#00AFF0"),
    "signal": ("fa-solid fa-comment-dots", "#3A76F0"),
    "thunderbird": ("fa-solid fa-envelope", "#0A84FF"),

    # Dev & Code
    "visualstudio": ("fa-brands fa-microsoft", "#007ACC"),
    "vscode": ("fa-solid fa-code", "#007ACC"),
    "git": ("fa-brands fa-git-alt", "#F05032"),
    "github": ("fa-brands fa-github", "#FFFFFF"),
    "python": ("fa-brands fa-python", "#3776AB"),
    "node": ("fa-brands fa-node-js", "#5FA04E"),
    "docker": ("fa-brands fa-docker", "#2496ED"),
    "postman": ("fa-solid fa-paper-plane", "#FF6C37"),
    "java": ("fa-brands fa-java", "#F89820"),
    "rust": ("fa-brands fa-rust", "#DEA584"),
    "golang": ("fa-brands fa-golang", "#00ADD8"),
    "php": ("fa-brands fa-php", "#777BB4"),
    "sublime": ("fa-solid fa-code", "#FF9800"),
    "intellij": ("fa-solid fa-laptop-code", "#FE315D"),
    "pycharm": ("fa-solid fa-laptop-code", "#21D789"),
    "database": ("fa-solid fa-database", "#336791"),
    "dbeaver": ("fa-solid fa-database", "#382923"),
    "terminal": ("fa-solid fa-terminal", "#4EAA25"),
    "powershell": ("fa-solid fa-terminal", "#5391FE"),

    # Games
    "steam": ("fa-brands fa-steam", "#171A21"),
    "epic": ("fa-solid fa-gamepad", "#313131"),
    "itch": ("fa-brands fa-itch-io", "#FA5C5C"),
    "minecraft": ("fa-solid fa-cube", "#5B8731"),
    "gog": ("fa-solid fa-gamepad", "#86328A"),
    "battle.net": ("fa-solid fa-dragon", "#00AEFF"),
    "ea": ("fa-solid fa-gamepad", "#FF4747"),
    "roblox": ("fa-solid fa-cube", "#E32636"),
    "unity": ("fa-brands fa-unity", "#FFFFFF"),
    "unreal": ("fa-solid fa-gamepad", "#0E1128"),
    "game": ("fa-solid fa-gamepad", "#A855F7"),

    # Media & Design
    "vlc": ("fa-solid fa-cone-traffic", "#FF8800"),
    "obs": ("fa-solid fa-record-vinyl", "#999999"),
    "blender": ("fa-solid fa-cubes", "#EA7600"),
    "gimp": ("fa-solid fa-palette", "#5C5543"),
    "krita": ("fa-solid fa-paintbrush", "#3498DB"),
    "inkscape": ("fa-solid fa-bezier-curve", "#FFFFFF"),
    "audacity": ("fa-solid fa-headphones", "#0000CC"),
    "handbrake": ("fa-solid fa-compact-disc", "#E67E22"),
    "mpv": ("fa-solid fa-play", "#7B1FA2"),
    "photo": ("fa-solid fa-image", "#EC4899"),
    "music": ("fa-solid fa-music", "#10B981"),
    "video": ("fa-solid fa-film", "#F43F5E"),

    # Tools & Hardware
    "7zip": ("fa-solid fa-file-zipper", "#0098FF"),
    "winrar": ("fa-solid fa-file-zipper", "#27AE60"),
    "powertoys": ("fa-brands fa-windows", "#0078D4"),
    "cpu": ("fa-solid fa-microchip", "#8B5CF6"),
    "gpu": ("fa-solid fa-memory", "#10B981"),
    "hardware": ("fa-solid fa-server", "#F59E0B"),
    "disk": ("fa-solid fa-hard-drive", "#3B82F6"),
    "clean": ("fa-solid fa-broom", "#14B8A6"),
    "notepad": ("fa-solid fa-note-sticky", "#90E59A"),
    "process": ("fa-solid fa-chart-line", "#EF4444"),

    # Security & Net
    "bitwarden": ("fa-solid fa-shield-halved", "#175DDC"),
    "keepass": ("fa-solid fa-key", "#43A047"),
    "1password": ("fa-solid fa-lock", "#0A85EA"),
    "vpn": ("fa-solid fa-network-wired", "#06B6D4"),
    "wireguard": ("fa-solid fa-shield", "#88171A"),
    "tor": ("fa-solid fa-eye-slash", "#7D4698"),
    "firewall": ("fa-solid fa-fire", "#E53935"),

    # Office
    "libreoffice": ("fa-solid fa-file-lines", "#18A303"),
    "pdf": ("fa-solid fa-file-pdf", "#F40F02"),
    "word": ("fa-solid fa-file-word", "#2B579A"),
    "excel": ("fa-solid fa-file-excel", "#217346"),
    "office": ("fa-solid fa-briefcase", "#D83B01"),
    "obsidian": ("fa-solid fa-gem", "#7C3AED"),
    "notion": ("fa-solid fa-book", "#FFFFFF")
}

def assign_app_icon(name, app_id, category):
    text = (name + " " + app_id).lower()
    for key, (icon, color) in KNOWN_ICONS.items():
        if key in text:
            return icon, color

    if "Tarayıcı" in category:
        return "fa-solid fa-globe", "#3B82F6"
    elif "Geliştirici" in category:
        return "fa-solid fa-code", "#10B981"
    elif "Sistem" in category:
        return "fa-solid fa-screwdriver-wrench", "#F59E0B"
    elif "Oyun" in category:
        return "fa-solid fa-gamepad", "#8B5CF6"
    elif "Medya" in category:
        return "fa-solid fa-play", "#EC4899"
    elif "Ofis" in category:
        return "fa-solid fa-file-lines", "#06B6D4"
    elif "Güvenlik" in category:
        return "fa-solid fa-shield-halved", "#EF4444"
    return "fa-solid fa-box", "#64748B"

def update_apps():
    with open('apps.json', 'r', encoding='utf-8') as f:
        categories = json.load(f)

    for cat in categories:
        for app in cat['apps']:
            icon_cls, color = assign_app_icon(app['name'], app['id'], cat['category'])
            app['iconClass'] = icon_cls
            app['iconColor'] = color

    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)
    print("apps.json successfully updated with instant local vector icons!")

if __name__ == '__main__':
    update_apps()

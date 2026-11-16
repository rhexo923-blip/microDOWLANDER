import subprocess
import re
import json
import requests

def build_huge_app_catalog():
    apps_by_category = {
        "🌐 Web Tarayıcıları & İletişim": [],
        "💻 Geliştirici, Kodlama & IDE": [],
        "🛠️ Sistem Araçları, Bakım & Donanım": [],
        "🎮 Oyun, İstemciler & Emülatörler": [],
        "🎨 Medya, Tasarım, Ses & Video": [],
        "📂 Ofis, Notlar & PDF Araçları": [],
        "🔒 Güvenlik, Gizlilik, Şifre & Ağ": [],
        "📦 Genel Yazılımlar & Kütüphaneler": []
    }

    # 1. CTT apps
    print("Fetching CTT applications.json...")
    try:
        r = requests.get('https://raw.githubusercontent.com/ChrisTitusTech/winutil/main/config/applications.json', timeout=10)
        ctt_data = r.json()
        print(f"Loaded {len(ctt_data)} apps from CTT.")
        for k, item in ctt_data.items():
            app_id = item.get('winget')
            name = item.get('content') or k
            desc = item.get('description', '')
            cat = item.get('category', 'Utilities')
            
            target_cat = "🛠️ Sistem Araçları, Bakım & Donanım"
            if "Browser" in cat or "Communication" in cat:
                target_cat = "🌐 Web Tarayıcıları & İletişim"
            elif "Development" in cat:
                target_cat = "💻 Geliştirici, Kodlama & IDE"
            elif "Game" in cat:
                target_cat = "🎮 Oyun, İstemciler & Emülatörler"
            elif "Media" in cat or "Audio" in cat:
                target_cat = "🎨 Medya, Tasarım, Ses & Video"
            elif "Document" in cat or "Office" in cat:
                target_cat = "📂 Ofis, Notlar & PDF Araçları"
            elif "Security" in cat:
                target_cat = "🔒 Güvenlik, Gizlilik, Şifre & Ağ"

            if app_id:
                apps_by_category[target_cat].append({
                    "id": app_id,
                    "name": name,
                    "desc": desc,
                    "icon": f"https://cdn.simpleicons.org/{name.lower().replace(' ', '').replace('.', '')}/3B82F6"
                })
    except Exception as e:
        print(f"CTT fetch error: {e}")

    # 2. Query winget
    print("Collecting 1000+ apps from winget repository...")
    seen_ids = set()
    for cat_list in apps_by_category.values():
        for a in cat_list:
            seen_ids.add(a["id"])

    queries = ['tool', 'editor', 'player', 'client', 'browser', 'game', 'dev', 'server', 'studio', 'view', 'manager', 'driver', 'code', 'audio', 'video', 'pdf', 'terminal', 'sync', 'calc', 'font', 'clean']
    
    for q in queries:
        if len(seen_ids) >= 1100:
            break
        try:
            res = subprocess.run(f'winget search "{q}" -n 70', shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
            lines = res.stdout.split('\n')
            for line in lines[3:]:
                parts = re.split(r'\s{2,}', line.strip())
                if len(parts) >= 2:
                    name = parts[0].strip()
                    app_id = parts[1].strip()
                    if '.' in app_id and app_id not in seen_ids and not app_id.startswith('9') and len(app_id) < 50:
                        seen_ids.add(app_id)
                        
                        target_cat = "📦 Genel Yazılımlar & Kütüphaneler"
                        low_name = (name + " " + app_id).lower()
                        if any(w in low_name for w in ['browser', 'chat', 'mail', 'telegram', 'discord', 'social']):
                            target_cat = "🌐 Web Tarayıcıları & İletişim"
                        elif any(w in low_name for w in ['code', 'dev', 'studio', 'python', 'git', 'node', 'sdk', 'sql', 'compiler']):
                            target_cat = "💻 Geliştirici, Kodlama & IDE"
                        elif any(w in low_name for w in ['tweak', 'clean', 'system', 'hardware', 'monitor', 'cpu', 'driver', 'disk']):
                            target_cat = "🛠️ Sistem Araçları, Bakım & Donanım"
                        elif any(w in low_name for w in ['game', 'steam', 'epic', 'emulator', 'play', 'craft', 'xbox']):
                            target_cat = "🎮 Oyun, İstemciler & Emülatörler"
                        elif any(w in low_name for w in ['media', 'audio', 'video', 'vlc', 'player', 'music', 'sound', 'photo', 'draw']):
                            target_cat = "🎨 Medya, Tasarım, Ses & Video"
                        elif any(w in low_name for w in ['office', 'pdf', 'word', 'note', 'sheet', 'doc']):
                            target_cat = "📂 Ofis, Notlar & PDF Araçları"
                        elif any(w in low_name for w in ['vpn', 'security', 'antivirus', 'pass', 'crypto', 'firewall']):
                            target_cat = "🔒 Güvenlik, Gizlilik, Şifre & Ağ"

                        apps_by_category[target_cat].append({
                            "id": app_id,
                            "name": name,
                            "desc": f"Winget resmi deposundan: {app_id}",
                            "icon": f"https://cdn.simpleicons.org/{name.lower().replace(' ', '')}/3B82F6"
                        })
        except Exception as e:
            print(f"Error querying {q}: {e}")

    result = []
    total_count = 0
    for cat, apps in apps_by_category.items():
        if apps:
            result.append({"category": cat, "apps": apps})
            total_count += len(apps)

    print(f"TOTAL APPS GENERATED: {total_count}")
    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("apps.json successfully updated!")

if __name__ == '__main__':
    build_huge_app_catalog()

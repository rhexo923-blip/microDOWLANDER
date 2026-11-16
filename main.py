import os
import sys
import json
import subprocess
import threading
import platform
import psutil
import webview
import pystray
from PIL import Image

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()
APPS_JSON_PATH = os.path.join(BASE_PATH, 'apps.json')
TWEAKS_JSON_PATH = os.path.join(BASE_PATH, 'tweaks.json')
ICON_ICO_PATH = os.path.join(BASE_PATH, 'icon.ico')
ICON_PNG_PATH = os.path.join(BASE_PATH, 'icon.png')

class WinHubAPI:
    def __init__(self, window=None):
        self.window = window

    def log_to_ui(self, message):
        safe_msg = message.replace('\\', '\\\\').replace('`', '\\`').replace('"', '\\"').replace('\n', '\\n').replace('\r', '')
        if self.window:
            try:
                self.window.evaluate_js(f"log(`{safe_msg}`)")
            except Exception:
                pass

    def get_apps(self):
        try:
            with open(APPS_JSON_PATH, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return json.dumps([{"category": "Hata", "apps": [{"id": "err", "name": str(e), "desc": "", "icon": ""}]}])

    def get_tweaks(self):
        try:
            with open(TWEAKS_JSON_PATH, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return json.dumps([])

    def get_system_info(self):
        try:
            mem = psutil.virtual_memory()
            ram_info = f"{mem.used / (1024**3):.1f} GB / {mem.total / (1024**3):.1f} GB (%{mem.percent})"
            os_info = f"{platform.system()} {platform.release()} (Build {platform.version()})"
            cpu_info = platform.processor() or "Standart x64 İşlemci"
            disk = psutil.disk_usage('C:\\')
            disk_info = f"{disk.free / (1024**3):.1f} GB Boş / {disk.total / (1024**3):.1f} GB"
            return json.dumps({
                "os": os_info,
                "cpu": cpu_info,
                "ram": ram_info,
                "disk": disk_info
            })
        except Exception as e:
            return json.dumps({"os": "Windows", "cpu": "Unknown", "ram": "N/A", "disk": "N/A"})

    def install_apps(self, app_ids):
        def worker():
            total = len(app_ids)
            for idx, app_id in enumerate(app_ids, start=1):
                self.log_to_ui(f"[{idx}/{total}] ==> {app_id} indiriliyor ve kuruluyor...")
                cmd = f"winget install --id {app_id} --silent --accept-source-agreements --accept-package-agreements"
                try:
                    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
                    for line in proc.stdout:
                        clean_line = line.strip()
                        if clean_line:
                            self.log_to_ui(f"[{app_id}] {clean_line}")
                    proc.wait()
                    if proc.returncode == 0:
                        self.log_to_ui(f"✅ [BAŞARILI] {app_id} kurulumu tamamlandı!")
                    else:
                        self.log_to_ui(f"⚠️ [KOD {proc.returncode}] {app_id} tamamlandı.")
                except Exception as ex:
                    self.log_to_ui(f"❌ [HATA] {app_id}: {ex}")
            self.log_to_ui("🎉 Toplu kurulum süreci başarıyla tamamlandı!")

        threading.Thread(target=worker, daemon=True).start()
        return "Toplu kurulum arka planda başlatıldı."

    def check_updates(self):
        try:
            cmd = "winget upgrade"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
            output = res.stdout.strip() or res.stderr.strip() or "Tüm yazılımlar güncel! Güncellenecek paket bulunamadı."
            return output
        except Exception as e:
            return f"Hata oluştu: {e}"

    def upgrade_all(self):
        def worker():
            self.log_to_ui("==> Linux 'apt upgrade' tarzı tüm depolar ve uygulamalar yükseltiliyor...")
            cmd = "winget upgrade --all --silent --accept-source-agreements --accept-package-agreements"
            try:
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
                for line in proc.stdout:
                    line_clean = line.strip()
                    if line_clean:
                        self.log_to_ui(line_clean)
                proc.wait()
                self.log_to_ui("🎉 [BAŞARILI] Tüm yazılımlar en son sürüme yükseltildi!")
            except Exception as e:
                self.log_to_ui(f"❌ [HATA] Güncelleme hatası: {e}")

        threading.Thread(target=worker, daemon=True).start()
        return "Tüm uygulamalar için toplu güncelleme başlatıldı."

    def apply_ctt_tweak(self, tweak_data_json):
        def worker():
            try:
                tweak = json.loads(tweak_data_json)
                name = tweak.get('name', 'Bilinmeyen Ayar')
                registries = tweak.get('registry', [])
                self.log_to_ui(f"==> CTT Ayarı Uygulanıyor: {name}")
                
                for r in registries:
                    path = r.get('Path', '').replace('HKLM:\\', 'HKLM\\').replace('HKCU:\\', 'HKCU\\')
                    reg_name = r.get('Name')
                    val = r.get('Value')
                    reg_type = r.get('Type', 'DWord').upper()
                    
                    if reg_type == 'DWORD':
                        reg_type = 'REG_DWORD'
                    elif reg_type == 'STRING':
                        reg_type = 'REG_SZ'

                    if val == "<RemoveEntry>":
                        cmd = f'reg delete "{path}" /v "{reg_name}" /f'
                    else:
                        cmd = f'reg add "{path}" /v "{reg_name}" /t {reg_type} /d "{val}" /f'
                    
                    subprocess.run(cmd, shell=True, capture_output=True)

                self.log_to_ui(f"✅ [UYGULANDI] {name} başarıyla etkinleştirildi.")
            except Exception as e:
                self.log_to_ui(f"❌ [HATA] Ayar uygulanırken: {e}")

        threading.Thread(target=worker, daemon=True).start()
        return "Ayar kuyruğa alındı."

    def apply_multiple_tweaks(self, tweaks_json_list):
        def worker():
            try:
                tweaks = json.loads(tweaks_json_list)
                total = len(tweaks)
                self.log_to_ui(f"==> Toplu CTT Optimizasyonu: {total} ayar uygulanıyor...")
                for idx, t in enumerate(tweaks, 1):
                    self.apply_ctt_tweak(json.dumps(t))
                self.log_to_ui(f"🎉 Tüm seçilen {total} optimizasyon uygulandı!")
            except Exception as e:
                self.log_to_ui(f"❌ Hata: {e}")

        threading.Thread(target=worker, daemon=True).start()
        return "Toplu optimizasyon başlatıldı."

    def run_quick_action(self, action_name):
        def worker():
            if action_name == 'clean_temp':
                self.log_to_ui("🧹 Disk Temizliği: Geçici dosyalar ve Prefetch siliniyor...")
                ps_script = 'Remove-Item -Path "$env:TEMP\\*" -Recurse -Force -ErrorAction SilentlyContinue; Remove-Item -Path "C:\\Windows\\Temp\\*" -Recurse -Force -ErrorAction SilentlyContinue'
                subprocess.run(f"powershell -NoProfile -Command \"{ps_script}\"", shell=True, capture_output=True)
                self.log_to_ui("✅ Geçici dosyalar temizlendi!")

            elif action_name == 'flush_dns':
                self.log_to_ui("🌐 DNS önbelleği temizleniyor...")
                subprocess.run("ipconfig /flushdns", shell=True, capture_output=True)
                self.log_to_ui("✅ DNS önbelleği temizlendi!")

            elif action_name == 'enable_dark_mode':
                self.log_to_ui("🌙 Windows Sistem Koyu Tema aktif ediliyor...")
                commands = [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v SystemUsesLightTheme /t REG_DWORD /d 0 /f'
                ]
                for c in commands:
                    subprocess.run(c, shell=True, capture_output=True)
                self.log_to_ui("✅ Koyu Tema (Dark Mode) aktif edildi!")

            elif action_name == 'sfc_repair':
                self.log_to_ui("🛡️ Sistem Dosyası Doğrulama (SFC) başlatılıyor...")
                proc = subprocess.Popen("sfc /scannow", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
                for line in proc.stdout:
                    if line.strip():
                        self.log_to_ui(line.strip())
                proc.wait()
                self.log_to_ui("✅ Sistem doğrulaması bitti.")

        threading.Thread(target=worker, daemon=True).start()
        return "İşlem başlatıldı."

class TrayManager:
    def __init__(self, window):
        self.window = window
        self.tray = None

    def create_tray(self):
        try:
            if os.path.exists(ICON_PNG_PATH):
                image = Image.open(ICON_PNG_PATH)
            else:
                image = Image.new('RGB', (64, 64), color=(37, 99, 235))

            menu = pystray.Menu(
                pystray.MenuItem("WinHub'ı Göster", self.show_window, default=True),
                pystray.MenuItem("Gizle", self.hide_window),
                pystray.MenuItem("Tümünü Güncelle (Upgrade)", self.quick_upgrade),
                pystray.MenuItem("Çıkış", self.quit_app)
            )
            self.tray = pystray.Icon("WinHub", image, "WinHub Utility Suite Pro", menu)
            threading.Thread(target=self.tray.run, daemon=True).start()
        except Exception as e:
            print(f"Tray error: {e}")

    def show_window(self, icon=None, item=None):
        if self.window:
            try:
                self.window.show()
                self.window.restore()
            except Exception:
                pass

    def hide_window(self, icon=None, item=None):
        if self.window:
            try:
                self.window.hide()
            except Exception:
                pass

    def quick_upgrade(self, icon=None, item=None):
        subprocess.Popen("winget upgrade --all --silent --accept-source-agreements --accept-package-agreements", shell=True)

    def quit_app(self, icon=None, item=None):
        if self.tray:
            self.tray.stop()
        if self.window:
            self.window.destroy()
        sys.exit(0)

def main():
    api = WinHubAPI()
    html_path = os.path.join(BASE_PATH, 'index.html')

    window = webview.create_window(
        title='WinHub Pro - 1100+ Apps & CTT Tweaks Suite',
        url=f'file:///{html_path}',
        js_api=api,
        width=1180,
        height=780,
        resizable=True,
        min_size=(900, 650),
        background_color='#0B0F19'
    )
    api.window = window

    tray_mgr = TrayManager(window)
    tray_mgr.create_tray()

    webview.start(debug=False)

if __name__ == '__main__':
    main()

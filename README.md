# Azer AI (Desktop Voice Assistant)

<p>
  <img src="./images/azer_ai.png" alt="Logo" align="left" width="140" style="margin-right:15px; border-radius:8px;">
Azer AI, Windows ve Linux üzerinde çalışan, Türkçe ve Azərbaycan dili destekli modern bir masaüstü sesli asistanıdır. Açık kaynak olarak yayımlanmıştır; eklenti sistemi ile kolayca genişletilebilir. Pro ve Free lisans katmanları, yönetim paneli (admin panel), kullanıcı ayarları (user settings), sürekli dinleme ve tek seferlik dinleme modları, sistem komutları ve özel komutlar desteği sunar.
</p>

<br clear="left"/>

---

# 🖼️ Ekran Görüntüleri

<table>
  <tr>
    <td align="center">
      <img src="images/Azer%20AI%20main.png" alt="Ana Ekran" width="380" style="border-radius:12px;">
      <br>🏠 <b>Ana Ekran</b>
    </td>
    <td align="center">
      <img src="images/Azer%20AI%20write.png" alt="Yazı Alanı" width="380" style="border-radius:12px;">
      <br>✍️ <b>Yazı Alanı</b>
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="images/Azer%20AI%20update.png" alt="Güncelleme Kontrolü" width="380" style="border-radius:12px;">
      <br>⚙️ <b>Güncelleme Kontrolü</b>
    </td>
    <td align="center">
      <img src="images/Azer%20AI%20login.png" alt="Giriş" width="380" style="border-radius:12px;">
      <br>🔐 <b>Giriş</b>
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="images/Azer%20AI%20sign%20up.png" alt="Kayıt" width="380" style="border-radius:12px;">
      <br>🧾 <b>Kayıt</b>
    </td>
    <td align="center">
      <img src="images/Azer%20AI%20loading.png" alt="Yükleniyor" width="380" style="border-radius:12px;">
      <br>⏳ <b>Yükleniyor</b>
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="images/Azer%20AI%20settings.png" alt="Kullanıcı Ayarları" width="380" style="border-radius:12px;">
      <br>👤 <b>Kullanıcı Ayarları</b>
    </td>
    <td align="center">
      <img src="images/Azer%20AI%20commands%20list.png" alt="Komut Listesi" width="380" style="border-radius:12px;">
      <br>💬 <b>Komut Listesi</b>
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="images/Azer%20AI%20admin%20panel.png" alt="Admin Panel" width="380" style="border-radius:12px;">
      <br>🛠️ <b>Admin Panel</b>
    </td>
    <td align="center">
      <img src="images/Azer%20AI%20exit.png" alt="Çıkış Diyaloğu" width="380" style="border-radius:12px;">
      <br>🚪 <b>Çıkış Diyaloğu</b>
    </td>
  </tr>
</table>

## Özellikler

- Sesli komutlar (az-AZ ve tr-TR)
- Sürekli dinleme ve tek dinleme modları
- Sistem komutları: ses/parlaklık, ekran görüntüsü, saat/tarih, hava durumu, arama, YouTube, Wikipedia, sistem bilgisi, yazma vb.
- Pro ve Free lisans katmanları
  - Free: çekirdek özellikler
  - Pro: özel komutlar, bazı ek yetenekler (uygulama içinde lisans doğrulama)
- Özel komutlar (sadece Pro): GUI üzerinden tetikleyiciler ve aksiyonlar tanımlayın
- Admin Panel: kullanıcı ve lisans yönetimi
- Kullanıcı Ayarları: TTS motoru (Edge TTS / gTTS), dil, ses cinsi, wake word ayarları, özel komutlar ve eklenti yönetimi
- Eklenti sistemi (yalnız .py): manifest.json üzerinden tetikleyici ve meta tanımı
- Güncelleme denetimi, modern arayüz ve görsel-işitsel geri bildirimler

## Ekranlar ve Modlar

- **Sürekli Dinleme**: Asistan arka planda sürekli dinler; wake word tespitinde aktive olur
- **Tek Dinleme**: Wake word sonrası tek komutu dinleyip işler
- **Cevap Dinleme**: Asistan sorularına sesli cevap beklediği durumlar (zamanaşımı ile)

## Proje Yapısı (Kısaltılmış)

```
Azer ai/
  command/                 # Sistem komutları
  plugins/                 # Eklentiler ve yöneticisi
  resim/, wav/             # Görseller ve ses efektleri
  user_settings.py         # Kullanıcı ayarları (GUI)
  admin_panel.py           # Admin paneli (GUI)
  plugins/plugin_manager.py# Eklenti yöneticisi
  main.py                  # Ana uygulama (tam)
  mini-azer-ai.py          # Hafif sürüm (mini)
  db_manager.py            # Veritabanı erişim katmanı (konfig)
  requirements.txt         # Bağımlılıklar
```

## Kurulum

### 1) Sistem Gereksinimleri
- Python 3.10+
- Windows 10/11 veya modern bir Linux dağıtımı
- Mikrofon erişimi

### 2) Depoyu İndir
```bash
git clone https://github.com/QadirAbbasov/azer-ai.git
cd azer-ai
```

### 3) Sanal Ortam (önerilir)
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

### 4) Bağımlılıkların Kurulumu
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Notlar (platforma göre):
- Linux medya kontrolü için `playerctl` (önerilir): `sudo apt install playerctl`
- Linux yazma otomasyonu için `xdotool`: `sudo apt install xdotool`
- Linux ses seviyesi için `pactl` (PipeWire/PulseAudio) ya da `amixer` (ALSA) hazır olmalı
- Parlaklık için `screen_brightness_control`; gerekirse `brightnessctl` veya `xbacklight`

### 5) Veritabanı Kurulumu (Lokal)

`db_manager.py` konfig dosyasıdır; bağlantı ve tablo yapıları buradan yönetilir. Başlangıç şeması için kökteki `Azer AI.sql` dosyasını kullanabilirsiniz.

MySQL kullanımı önerilir (güncelleme kontrolleri vb. için merkezi yapı):

1) MySQL kurun ve bir veritabanı oluşturun (ör. `azer_ai`).
2) Gerekli tabloları `Azer AI.sql` içeriğiyle oluşturun.
3) Python bağlayıcıyı kurun:
```bash
pip install mysql-connector-python
```
4) `db_manager.py` içinde bağlantı bilgilerinizi ayarlayın (örnek):
```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'azer_user',
    'password': 'azer_password',
    'database': 'azer_ai',
    'charset': 'utf8mb4'
}
```
5) Tüm CRUD fonksiyonları bu bağlantıyı kullanacak şekilde yapılandırılmalıdır (dosya zaten merkezi bir arayüzdür).

Not: İsterseniz SQLite ile de çalışabilirsiniz; ancak MySQL ile çok-kullanıcılı ve sunucu tabanlı senaryolarda daha stabil sonuçlar elde edilir.

### 6) Uygulamayı Çalıştırma

Tam sürüm:
```bash
python main.py
```

Mini sürüm:
```bash
python mini-azer-ai.py
```

## Yapılandırma (db_manager.py)
- Veritabanı dosya yolu veya bağlantı bilgileri burada tutulur
- Ses ayarları, kullanıcı bilgileri, özel komutlar ve lisans kayıtları için CRUD fonksiyonları içerir
- Lokal geliştirme için ek bir .env gerekmez; istenirse eklenebilir

### MySQL yapılandırması hızlı özet
- Bağlantı: `mysql-connector-python`
- Ayarlar: `MYSQL_CONFIG`
- Şema: `Azer AI.sql` dosyası (user, licenses, voice_settings, custom_commands, versions vb.)
- Üretimde yetkili, sınırlı izinli bir kullanıcı tanımlayın (yalnız gerekli haklar)

## Lisans Sistemi
- Free: temel özellikler
- Pro: özel komutlar vb. gelişmiş fonksiyonlar
- Lisans durumu kullanıcı bazlıdır (`current_user.license_status`) ve veri tabanında saklanır
- Uygulama içi yükseltme akışı `subscription_manager.py` ile yönetilir

## Sistem Komutları (Örnekler)
Aşağıdaki komutlar Windows ve Linux’ta çalışacak şekilde uyarlanmıştır:

- **Ses** (`command/volume_manager.py`)
  - Windows: `pycaw` (yedek: `nircmd.exe` varsa)
  - Linux: `pactl` veya `amixer`
- **Parlaklık** (`command/brightness_manager.py`)
  - `screen_brightness_control` ortak kütüphane
  - Linux yedek: `brightnessctl` veya `xbacklight`
- **Medya** (`command/music_manager.py`)
  - Windows: sistem medya tuşları
  - Linux: `playerctl`
- **Yazma** (`command/typing_manager.py`)
  - Varsayılan: `keyboard` kütüphanesi
  - Linux yedek: `xdotool`
- **Hava Durumu** (`command/weather_manager.py`)
  - `wttr.in` API’si ile şehir bazlı sorgu
- **YouTube** (`command/youtube_manager.py`)
  - `youtube_search` ile arama, varsayılan tarayıcı ile açma
- **Wikipedia** (`command/wikipedia_manager.py`)
  - `wikipedia` paketi ile özet okuma ve sayfa açma
- **Arama** (`command/search_manager.py`)
  - Yandex sonuçlarından ilkini açma
- **Ekran Görüntüsü** (`command/screenshot.py`)
  - `pyautogui` ile kaydetme ve gösterme
- **Sistem Bilgisi** (`command/system.py`)
  - CPU/RAM kullanım yüzdeleri ve durum değerlendirmesi
- **Saat/Tarih** (`command/time_manager.py`, `command/date.py`)
  - Dil uyumlu doğal dilde duyuru
- **Not Alma** (`command/notes.py`)
  - `notes/notes.txt` dosyasına ekleme

## Wake Word ve Dinleme Modları
- Wake word listesi kullanıcı ayarlarından (User Settings) düzenlenebilir; birden çok varyant desteklenir
- Sürekli Dinleme: Wake word’ü yakalayınca asistan aktive olur
- Tek Dinleme: Wake word sonrasında tek bir komut alır ve durur
- Cevap Dinleme: Asistan bir soru sorar ve belirli süre kullanıcı cevabını bekler

## Kullanıcı Ayarları (user_settings.py)
- TTS Motoru: Edge TTS veya gTTS seçimi
- Dil: az-AZ veya tr-TR
- Ses Cinsi: erkek/kadın
- Wake Word: birden çok tetikleyici belirleyin
- Özel Komutlar (Pro): tetikleyiciler ve aksiyonlar (Program Aç/Kapat, Web Aç, Script, Web Arama, Klavye Kısayolu)
- Eklentiler: yükle, listele, kaldır

## Admin Paneli (admin_panel.py)
- Kullanıcıları listeleme, lisans durumlarını güncelleme
- Yönetici işlemleri

## Eklenti Sistemi
Yalnız Python (.py) eklentileri desteklenir. Her eklenti bir klasör olarak paketlenir ve .zip halinde yüklenir. Manifest ve ana .py dosyası zorunludur.

### Manifest (manifest.json)
```json
{
  "name": "MyPlugin",
  "version": "1.0.0",
  "main_file": "my_plugin.py",
  "description": "Kısa açıklama",
  "author": "Adınız",
  "license_type": "free",
  "logo": "logo.png",
  "triggers": {
    "az-AZ": ["tetikleyici 1", "tetikleyici 2"],
    "tr-TR": ["tetikleyici 1", "tetikleyici 2"]
  }
}
```

### Python Sınıfı
```python
class MyPlugin:
    @property
    def name(self) -> str: return "MyPlugin"
    @property
    def version(self) -> str: return "1.0.0"
    @property
    def description(self) -> str: return "Kısa açıklama"
    @property
    def author(self) -> str: return "Adınız"
    @property
    def license_type(self) -> str: return "free"
    @property
    def logo(self) -> str: return "logo.png"  # opsiyonel ama önerilir

    def execute(self, Azer_AI, command: str) -> None:
        lang = Azer_AI.voice_settings['language']
        if lang == 'az-AZ':
            Azer_AI.speak("Salam! Plugin çalıştı.")
        else:
            Azer_AI.speak("Merhaba! Eklenti çalıştı.")
```

### Yükleme
- Uygulama içinde Kullanıcı Ayarları > Plugin’ler > “Plugin Yükle” düğmesi ile .zip dosyanızı seçin
- Yüklenen eklentiler `plugins/installed_plugins.json` içinde minimal bilgilerle listelenir (sadece `name`, `version`)
- Eklenti tetikleyicileri yalnız `manifest.json` üzerinden alınır

### Eşleşme
- `plugins/plugin_manager.py` içinde tetikleyici eşleşmesi dil duyarlı yapılır (tam eşleşme, başında eşleşme ve basit sözcük benzerliği)

### Örnek: Hız Testi Eklentisi
- `plugins/SpeedTestPlugin/` klasöründe `manifest.json` ve `speed_test_plugin.py`
- `speedtest` Python modülü yoksa CLI fallback: `speedtest -f json` veya `speedtest-cli --json`

## Özel Komutlar (Pro)
- Kullanıcı Ayarları > “Xüsusi Əmrlər” bölümünden tetikleyiciler ve aksiyonlar ekleyin
- Aksiyonlar: Program Aç/Kapat, Web Aç, Script, Web Arama, Klavye Kısayolu
- Tetikleyiciler dil bazlıdır (az-AZ/tr-TR)

## Güncelleme Kontrolü (update_checker.py)

Uygulama açılışında sürüm kontrolü yapılır. Bu işlem `update_checker.py` tarafından yürütülür ve veritabanındaki sürüm tablosundan (MySQL önerilir) en son sürüm bilgisi okunur.

- `db_manager.py` aracılığıyla veritabanına bağlanır
- `version.txt` veya yerel `version.py` değerini sunucudaki son sürüm ile karşılaştırır
- Yeni sürüm varsa kullanıcıya bildirim gösterir ve güncelleme akışını başlatır (uygulama içinde yönlendirme)

Kurulum için ek bir yapılandırma gerekmez; yalnızca `db_manager.py` içinde MySQL bağlantı bilgilerinin doğru olması yeterlidir.

## Sık Sorulanlar
- “Ses gelmiyor”: Edge TTS için internet bağlantısı gerekli; gTTS de dosya üretir ve çalar. Ses kartı/devreleri erişilebilir olmalı
- “Komutlar çalışmıyor”: Mikrofon izni, doğru dil seçimi ve wake word doğrulaması yapın
- “Linux’ta medya/ses/parlaklık çalışmıyor”: `playerctl`, `pactl/amixer`, `brightnessctl/xbacklight` kurulu olmalı

## Katkı
- Pull Request’ler kabul edilir
- Yeni komutlar, eklentiler, hata düzeltmeleri memnuniyetle

## Lisans
Bu proje açık kaynak olarak yayımlanmıştır. Kullanım koşulları için repodaki lisans dosyasına bakınız.






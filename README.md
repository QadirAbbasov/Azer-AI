# Azer AI (Masaüstü Səsli Köməkçi)

<p>
  <img src="./images/azer_ai.png" alt="Logo" align="left" width="140" style="margin-right:15px; border-radius:8px;">
Azer AI — Windows və Linux üzərində işləyən, Türk və Azərbaycan dillərini dəstəkləyən müasir bir masaüstü səsli köməkçidir. Açıq mənbə (open-source) layihədir; plagin sistemi vasitəsilə asanlıqla genişləndirilə bilər. Pro və Pulsuz (Free) lisenziya qatları, idarə paneli (admin panel), istifadəçi parametrləri (user settings), davamlı və tək dinləmə modları, sistem əmrləri və xüsusi əmrlər dəstəyi təqdim edir.
</p>

<br clear="left"/>

---

# 🖼️ Ekran Görüntüləri

<table>
  <tr>
    <td align="center">
      <img src="images/Azer%20AI%20main.png" alt="Əsas Ekran" width="380" style="border-radius:12px;">
      <br>🏠 <b>Əsas Ekran</b>
    </td>
    <td align="center">
      <img src="images/Azer%20AI%20write.png" alt="Yazı Sahəsi" width="380" style="border-radius:12px;">
      <br>✍️ <b>Yazı Sahəsi</b>
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="images/Azer%20AI%20update.png" alt="Yeniləmə Yoxlaması" width="380" style="border-radius:12px;">
      <br>⚙️ <b>Yeniləmə Yoxlaması</b>
    </td>
    <td align="center">
      <img src="images/Azer%20AI%20login.png" alt="Giriş" width="380" style="border-radius:12px;">
      <br>🔐 <b>Giriş</b>
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="images/Azer%20AI%20sign%20up.png" alt="Qeydiyyat" width="380" style="border-radius:12px;">
      <br>🧾 <b>Qeydiyyat</b>
    </td>
    <td align="center">
      <img src="images/Azer%20AI%20loading.png" alt="Yüklənir" width="380" style="border-radius:12px;">
      <br>⏳ <b>Yüklənir</b>
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="images/Azer%20AI%20settings.png" alt="İstifadəçi Parametrləri" width="380" style="border-radius:12px;">
      <br>👤 <b>İstifadəçi Parametrləri</b>
    </td>
    <td align="center">
      <img src="images/Azer%20AI%20commands%20list.png" alt="Əmr Siyahısı" width="380" style="border-radius:12px;">
      <br>💬 <b>Əmr Siyahısı</b>
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="images/Azer%20AI%20admin%20panel.png" alt="Admin Panel" width="380" style="border-radius:12px;">
      <br>🛠️ <b>Admin Panel</b>
    </td>
    <td align="center">
      <img src="images/Azer%20AI%20exit.png" alt="Çıxış Dialoqu" width="380" style="border-radius:12px;">
      <br>🚪 <b>Çıxış Dialoqu</b>
    </td>
  </tr>
</table>

## Xüsusiyyətlər

* Səsli əmrlər (az-AZ və tr-TR)
* Davamlı və tək dinləmə rejimləri
* Sistem əmrləri: səs/parlaqlıq, ekran görüntüsü, saat/tarix, hava, axtarış, YouTube, Wikipedia, sistem məlumatı, yazı və s.
* Pro və Free lisenziya səviyyələri

  * Free: əsas funksiyalar
  * Pro: xüsusi əmrlər, əlavə imkanlar (tətbiqdaxili lisenziya yoxlaması)
* Xüsusi əmrlər (yalnız Pro): GUI üzərindən trigger və əməliyyatlar təyin edin
* Admin Panel: istifadəçi və lisenziya idarəetməsi
* İstifadəçi Parametrləri: TTS mühərriki (Edge TTS / gTTS), dil, səs növü, wake word tənzimləməsi, xüsusi əmrlər və plagin idarəetməsi
* Plagin sistemi (.py faylları): manifest.json ilə trigger və meta məlumatları
* Yeniləmə yoxlaması, müasir interfeys, vizual və səsli bildirişlər

## Ekranlar və Rejimlər

* **Davamlı Dinləmə**: Asistent arxa planda daima dinləyir, wake word eşidildikdə aktivləşir
* **Tək Dinləmə**: Wake word deyildikdən sonra yalnız bir əmr qəbul edir
* **Cavab Dinləmə**: Asistent sual verdikdə müəyyən müddət cavab gözləyir

## Layihə Quruluşu (Qısaldılmış)

```
Azer ai/
  command/                 # Sistem əmrləri
  plugins/                 # Plaginlər və idarəetmə
  resim/, wav/             # Şəkillər və səs effektləri
  user_settings.py         # İstifadəçi parametrləri (GUI)
  admin_panel.py           # Admin panel (GUI)
  plugins/plugin_manager.py# Plagin idarəçisi
  main.py                  # Tam tətbiq
  mini-azer-ai.py          # Yüngül versiya (mini)
  db_manager.py            # Məlumat bazası interfeysi
  requirements.txt         # Asılılıqlar
```

## Quraşdırma

### 1) Sistem Tələbləri

* Python 3.10+
* Windows 10/11 və ya müasir Linux distributivi
* Mikrofon girişi

### 2) Deponu endirin

```bash
git clone https://github.com/QadirAbbasov/azer-ai.git
cd azer-ai
```

### 3) Virtual mühit (məsləhət görülür)

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

### 4) Asılılıqların quraşdırılması

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Qeydlər (platformaya görə):**

* Linux üçün `playerctl` (media idarəetməsi): `sudo apt install playerctl`
* Avtomatik yazı üçün `xdotool`: `sudo apt install xdotool`
* Səs səviyyəsi üçün `pactl` (PipeWire/PulseAudio) və ya `amixer` (ALSA)
* Parlaqlıq üçün `screen_brightness_control`, alternativ: `brightnessctl` və ya `xbacklight`

### 5) Məlumat Bazası Qurulumu (Yerəl)

`db_manager.py` konfiqurasiya faylıdır; əlaqə və cədvəl strukturları burada idarə olunur. Başlanğıc sxemi üçün kökdəki `Azer AI.sql` faylını istifadə edin.

MySQL tövsiyə olunur (yeniləmə və çoxistifadəçi dəstəyi üçün):

1. MySQL quraşdırın və `azer_ai` adlı baza yaradın.
2. `Azer AI.sql` faylındakı cədvəlləri yaradın.
3. Python bağlayıcını quraşdırın:

   ```bash
   pip install mysql-connector-python
   ```
4. `db_manager.py` daxilində bağlantı məlumatlarını yazın:

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

SQLite də istifadə oluna bilər, amma çoxistifadəçi və server əsaslı senarilərdə MySQL daha sabitdir.

### 6) Proqramın İşə Salınması

Tam versiya:

```bash
python main.py
```

Yüngül versiya:

```bash
python mini-azer-ai.py
```

## Lisenziya Sistemi

* Free: əsas xüsusiyyətlər
* Pro: xüsusi əmrlər və əlavə funksiyalar
* Lisenziya vəziyyəti (`current_user.license_status`) məlumat bazasında saxlanılır
* Yenilənmə prosesi `subscription_manager.py` vasitəsilə idarə olunur

## Tez-tez Verilən Suallar

* "Səs gəlmir": Edge TTS internet tələb edir; gTTS səs faylı yaradır.
* "Əmrlər işləmir": Mikrofon icazəsini, dil seçimini və wake word-u yoxlayın.
* "Linux-da səs/media/parlaqlıq işləmir": `playerctl`, `pactl/amixer`, `brightnessctl/xbacklight` quraşdırılmalıdır.

## Layihəyə Dəstək

* Pull Request-lər qəbul olunur
* Yeni əmrlər, plaginlər və səhv düzəlişləri məmnuniyyətlə

## Lisenziya

Bu layihə açıq mənbədir. İstifadə şərtləri üçün repodakı LICENSE faylına baxın.
